#!/usr/bin/env python3
# docker run --name corenlp -d -p 9000:9000 vzhong/corenlp-server
# Wonseok Hwang. Jan 6 2019, Comment added
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import os
import records
import ujson as json
import jsonl
import re

from konlpy.tag import Okt
from tqdm import tqdm

okt=Okt()
"""#from stanza.nlp.corenlp import CoreNLPClient
from stanza.server import CoreNLPClient
from tqdm import tqdm"""
import copy
from wikisql.lib.common import count_lines, detokenize
from wikisql.lib.query import Query

def text_prep(sentence):
    words, gloss = [], []
    josa = ['을', '를', '이', '가', '은', '는']
    txt = re.sub('[^가-힣a-z]]', '', sentence)
    tokenized = okt.morphs(txt)

    for t in tokenized:
        if t not in josa:
            words.append(t)
            gloss.append(t)

    return {
        'gloss': gloss,
        'words': words,
        }

def find_sub_list(sl, l):
    # from stack overflow.
    results = []
    sll = len(sl)
    #print(sl, "<", l)
    sl = [s.lower() for s in sl]
    l = [ll.lower() for ll in l]
    #print(sl,"<",l)
    for i, e in enumerate(l):
        #print(type(e))
        #print(type(sl[0]))

        #if (e.lower() == str(sl[0]).lower() or str(e).lower().find(str(sl[0]).lower())==0):
        if (e == str(sl[0]) or str(e).find(str(sl[0])) == 0):
            #print("\n-> ",e.lower(), str(sl[0].lower()))
            if (l[i:i + sll] == sl or ''.join(l[i:i + sll]).find(''.join(sl))==0):
                results.append((i, i + sll - 1))
    st_idx, ed_idx = results[0]

    #print(sl,"||", l[st_idx:ed_idx+1])
    return results

def check_wv_tok_in_nlu_tok(wv_tok1, nlu_t1):
    """
    Jan.2019: Wonseok
    Generate SQuAD style start and end index of wv in nlu. Index is for of after WordPiece tokenization.
    Sep. 2021: ale
    Modified for Korean data with Okt. Index is for of after WordPiece tokenization from BERT / SentencePiece tokenization from KoBERT

    Assumption: where_str always presents in the nlu.

    return:
    st_idx of where-value string token in nlu under CoreNLP tokenization scheme.
    """

    #print(wv_tok1, nlu_t1)

    g_wvi1_okt = []

    for i_wn, wv_tok11 in enumerate(wv_tok1):
        results = find_sub_list(wv_tok11, nlu_t1)
        st_idx, ed_idx = results[0]

        g_wvi1_okt.append( [st_idx, ed_idx] )

    return g_wvi1_okt


def annotate_ale(example, table):
    """
    Jan. 2019: Wonseok
    Annotate only the information that will be used in our model.
    Sep. 2021: ale
    Modified for Korean data with Okt
    """
    ann = {'table_id': example['table_id'],'phase': example['phase']}
    _nlu_ann = text_prep(example['question'])
    ann['question'] = example['question']
    ann['question_tok'] = _nlu_ann['gloss']
    ann['sql'] = example['sql']
    ann['query'] = sql = copy.deepcopy(example['sql'])

    conds1 = ann['sql']['conds']
    wv_ann1 = []
    for conds11 in conds1:
        _wv_ann1 = text_prep(str(conds11[2]))
        wv_ann11 = _wv_ann1['gloss']
        wv_ann1.append( wv_ann11 )

    try:
        wvi1_okt = check_wv_tok_in_nlu_tok(wv_ann1, ann['question_tok'])
        #ann['wvi_okt'] = wvi1_okt
        ann['wvi_corenlp'] = wvi1_okt
    except:
        #ann['wvi_okt'] = None
        ann['wvi_corenlp'] = None
        ann['tok_error'] = 'SQuAD style st, ed are not found under CoreNLP.'

    return ann

if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--din', default='/Users/wonseok/data/WikiSQL-1.1/data', help='data directory')
    parser.add_argument('--dout', default='/Users/wonseok/data/wikisql_tok', help='output directory')
    parser.add_argument('--split', default='train,dev,test', help='comma=separated list of splits to process')
    args = parser.parse_args()

    answer_toy = not True
    toy_size = 12

    if not os.path.isdir(args.dout):
        os.makedirs(args.dout)

    # for split in ['train', 'dev', 'test']:
    for split in args.split.split(','):
        fsplit = os.path.join(args.din, split) + '.jsonl'
        ftable = os.path.join(args.din, split) + '.tables.jsonl'
        fout = os.path.join(args.dout, split) + '_tok.jsonl'

        print('annotating {}'.format(fsplit))
        with open(fsplit, encoding='utf-8') as fs, open(ftable, encoding='utf-8') as ft, open(fout, 'wt', encoding='utf-8') as fo:
            print('loading tables')

            ft_data = jsonl.load_jsonl(ftable)
            t_total = len(ft_data)

            # table dict with table_id as key
            tables = {}
            for line in tqdm(ft, total=t_total):
                d = json.loads(line)
                tables[d['id']] = d

            print('loading examples')

            n_written = 0
            cnt = -1

            done=[]
            for line in tqdm(fs, total=t_total):
                cnt += 1
                d = json.loads(line)
                a = annotate_ale(d, tables[d['table_id']])
                done.append(a)
                n_written += 1

            jsonl.dump_jsonl(done, fout, append=True)
            print('wrote {} data'.format(n_written))
