#!/usr/bin/env python

# Use existing model to predict sql from tables and questions.
#
# For example, you can get a pretrained model from https://github.com/naver/sqlova/releases:
#    https://github.com/naver/sqlova/releases/download/SQLova-parameters/model_bert_best.pt
#    https://github.com/naver/sqlova/releases/download/SQLova-parameters/model_best.pt
#
# Make sure you also have the following support files (see README for where to get them):
#    - bert_config_uncased_*.json
#    - vocab_uncased_*.txt
#
# Finally, you need some data - some files called:
#    - <split>.db
#    - <split>.jsonl
#    - <split>.tables.jsonl
#    - <split>_tok.jsonl         # derived using annotate_ws.py
# You can play with the existing train/dev/test splits, or make your own with
# the add_csv.py and add_question.py utilities.
#
# Once you have all that, you are ready to predict, using:
#   python predict.py \
#     --bert_type_abb uL \       # need to match the architecture of the model you are using
#     --model_file <path to models>/model_best.pt            \
#     --bert_model_file <path to models>/model_bert_best.pt  \
#     --bert_path <path to bert_config/vocab>  \
#     --result_path <where to place results>                 \
#     --data_path <path to db/jsonl/tables.jsonl>            \
#     --split <split>
#
# Results will be in a file called results_<split>.jsonl in the result_path.

import os, sys
import torch.nn as nn
import torch
import random as python_random

from sqlnet.dbengine import DBEngine
from sqlova.utils.utils_wikisql_ale import *
from train_ale import get_models

class args_ale():
    def __init__(self):
        self.do_train=False
        self.do_infer=False
        self.infer_loop=False
        self.trained=False
        self.tepoch=False
        self.bS=32
        self.accumulate_gradients=1
        self.fine_tune=False
        self.model_type='Seq2SQL_v1'
        
        # BERT params
        self.vocab_file='vocab.txt'
        self.max_seq_length=222
        self.num_target_layers=2
        self.lr_bert=1e-5
        self.seed=42
        self.no_pretraining=False
        self.bert_type_abb='mcS'
        self.do_lower_case=True

        # Seq-to-SQL module params
        self.lS=2
        self.dr=0.3
        self.lr=1e-4
        self.hS=100

        # execution quited deconding beam-size
        self.EG=False
        self.beam_size=4

        self.toy_model=False

    def construct_hyper_param_ale(self,bert_type_abb):
        map_bert_type_abb = {'uS': 'uncased_L-12_H-768_A-12',
                         'uL': 'uncased_L-24_H-1024_A-16',
                         'cS': 'cased_L-12_H-768_A-12',
                         'cL': 'cased_L-24_H-1024_A-16',
                         'mcS': 'multi_cased_L-12_H-768_A-12'
                       }
    
        self.bert_type=map_bert_type_abb[bert_type_abb]

        if self.bert_type_abb == 'cS' or self.bert_type_abb == 'cL' or self.bert_type_abb == 'mcS':
            self.do_lower_case = False

        seed(self.seed)
        python_random.seed(self.seed)
        np.random.seed(self.seed)
        torch.manual_seed(self.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(self.seed)




# This is a stripped down version of the test() method in train.py - identical, except:
#   - does not attempt to measure accuracy and indeed does not expect the data to be labelled.
#   - saves plain text sql queries.
#
def predict(data_loader, data_table, model, model_bert, bert_config, tokenizer,
            max_seq_length,
            num_target_layers, detail=False, st_pos=0, cnt_tot=1, EG=False, beam_size=4,
            path_db=None, dset_name='test'):

    model.eval()
    model_bert.eval()

    engine = DBEngine(os.path.join(path_db, f"{dset_name}.db"))
    results = []
    for iB, t in enumerate(data_loader):
        nlu, nlu_t, sql_i, sql_q, sql_t, tb, hs_t, hds = get_fields(t, data_table, no_hs_t=True, no_sql_t=True)
        g_sc, g_sa, g_wn, g_wc, g_wo, g_wv = get_g(sql_i)
        g_wvi_corenlp = get_g_wvi_corenlp(t)
        wemb_n, wemb_h, l_n, l_hpu, l_hs, \
        nlu_tt, t_to_tt_idx, tt_to_t_idx \
            = get_wemb_bert(bert_config, model_bert, tokenizer, nlu_t, hds, max_seq_length,
                            num_out_layers_n=num_target_layers, num_out_layers_h=num_target_layers)
        if not EG:
            # No Execution guided decoding
            s_sc, s_sa, s_wn, s_wc, s_wo, s_wv = model(wemb_n, l_n, wemb_h, l_hpu, l_hs)
            pr_sc, pr_sa, pr_wn, pr_wc, pr_wo, pr_wvi = pred_sw_se(s_sc, s_sa, s_wn, s_wc, s_wo, s_wv, )
            pr_wv_str, pr_wv_str_wp = convert_pr_wvi_to_string(pr_wvi, nlu_t, nlu_tt, tt_to_t_idx, nlu)
            pr_sql_i = generate_sql_i(pr_sc, pr_sa, pr_wn, pr_wc, pr_wo, pr_wv_str, nlu)
        else:
            # Execution guided decoding
            prob_sca, prob_w, prob_wn_w, pr_sc, pr_sa, pr_wn, pr_sql_i = model.beam_forward(wemb_n, l_n, wemb_h, l_hpu,
                                                                                            l_hs, engine, tb,
                                                                                            nlu_t, nlu_tt,
                                                                                            tt_to_t_idx, nlu,
                                                                                            beam_size=beam_size)
            # sort and generate
            pr_wc, pr_wo, pr_wv, pr_sql_i = sort_and_generate_pr_w(pr_sql_i)
            # Following variables are just for consistency with no-EG case.
            pr_wvi = None # not used
            pr_wv_str=None
            pr_wv_str_wp=None

        pr_sql_q = generate_sql_q(pr_sql_i, tb)

        for b, (pr_sql_i1, pr_sql_q1) in enumerate(zip(pr_sql_i, pr_sql_q)):
            results1 = {}
            results1["query"] = pr_sql_i1
            results1["table_id"] = tb[b]["id"]
            results1["nlu"] = nlu[b]
            results1["sql"] = pr_sql_q1
            results.append(results1)

    return results

def run_predict(model_file, bert_model_file, bert_path, data_path, user_id, att, result_path):
    ## Set up hyper parameters and paths
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--model_file", required=True, help='model file to use (e.g. model_best.pt)', default = model_file)
    #parser.add_argument("--bert_model_file", required=True, help='bert model file to use (e.g. model_bert_best.pt)', default = bert_model_file)
    #parser.add_argument("--bert_path", required=True, help='path to bert files (bert_config*.json etc)', default = bert_path)
    #parser.add_argument("--data_path", required=True, help='path to *.jsonl and *.db files', default=data_path)
    #parser.add_argument("--split", required=True, help='prefix of jsonl and db files (e.g. dev)', default=user_id)
    #parser.add_argument("--result_path", required=True, help='directory in which to place results', default=result_path)
    args = args_ale()
    args.construct_hyper_param_ale('mcS')

    BERT_PT_PATH = bert_path
    path_save_for_evaluation = result_path

    # Load pre-trained models
    path_model_bert = bert_model_file
    path_model = model_file
    args.no_pretraining = True  # counterintuitive, but avoids loading unused models
    print(f"BERT-type: {args.bert_type}")
    model, model_bert, tokenizer, bert_config = get_models(args, BERT_PT_PATH, trained=True, path_model_bert=path_model_bert, path_model=path_model)

    args.toy_model=False
    #args.toy_model=True
    #args.toy_size=1001
    #args.toy_size=300
    #args.toy_size=70
    args.toy_size=4

    # Load data
    dev_data, dev_table = load_wikisql_data(data_path, att, mode=user_id, toy_model=args.toy_model, toy_size=args.toy_size, no_hs_tok=True)
    dev_loader = torch.utils.data.DataLoader(
        batch_size=args.bS,
        dataset=dev_data,
        shuffle=False,
        num_workers=1,
        collate_fn=lambda x: x  # now dictionary values are not merged!
    )

    # Run prediction
    with torch.no_grad():
        results = predict(dev_loader,
                          dev_table,
                          model,
                          model_bert,
                          bert_config,
                          tokenizer,
                          args.max_seq_length,
                          args.num_target_layers,
                          detail=False,
                          path_db=data_path,
                          st_pos=0,
                          dset_name=user_id, EG=args.EG)

    # Save results
    save_for_evaluation(path_save_for_evaluation, results, user_id+'_'+att)

def run_predict_tmp(model, model_bert, tokenizer, bert_config, data_path, user_id, att, result_path):
    ## Set up hyper parameters and paths
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--model_file", required=True, help='model file to use (e.g. model_best.pt)', default = model_file)
    #parser.add_argument("--bert_model_file", required=True, help='bert model file to use (e.g. model_bert_best.pt)', default = bert_model_file)
    #parser.add_argument("--bert_path", required=True, help='path to bert files (bert_config*.json etc)', default = bert_path)
    #parser.add_argument("--data_path", required=True, help='path to *.jsonl and *.db files', default=data_path)
    #parser.add_argument("--split", required=True, help='prefix of jsonl and db files (e.g. dev)', default=user_id)
    #parser.add_argument("--result_path", required=True, help='directory in which to place results', default=result_path)
    args = args_ale()
    args.construct_hyper_param_ale('mcS')

    #BERT_PT_PATH = bert_path
    path_save_for_evaluation = result_path

    # Load pre-trained models
    #path_model_bert = bert_model_file
    #path_model = model_file
    #args.no_pretraining = True  # counterintuitive, but avoids loading unused models
    #print(f"BERT-type: {args.bert_type}")
    #model, model_bert, tokenizer, bert_config = get_models(args, BERT_PT_PATH, trained=True, path_model_bert=path_model_bert, path_model=path_model)

    args.toy_model=False
    #args.toy_model=True
    #args.toy_size=1001
    #args.toy_size=300
    #args.toy_size=70
    args.toy_size=4

    # Load data
    dev_data, dev_table = load_wikisql_data(data_path, att, mode=user_id, toy_model=args.toy_model, toy_size=args.toy_size, no_hs_tok=True)
    dev_loader = torch.utils.data.DataLoader(
        batch_size=args.bS,
        dataset=dev_data,
        shuffle=False,
        num_workers=1,
        collate_fn=lambda x: x  # now dictionary values are not merged!
    )

    # Run prediction
    with torch.no_grad():
        results = predict(dev_loader,
                          dev_table,
                          model,
                          model_bert,
                          bert_config,
                          tokenizer,
                          args.max_seq_length,
                          args.num_target_layers,
                          detail=False,
                          path_db=data_path,
                          st_pos=0,
                          dset_name=user_id, EG=args.EG)

    # Save results
    save_for_evaluation(path_save_for_evaluation, results, user_id+'_'+att)

#run_predict('./data_and_model/model_best.pt', './data_and_model/model_bert_best.pt', './data_and_model', './data_and_model', 'tmp','./data_and_model/flask_test/')
