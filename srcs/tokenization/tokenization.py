"""Copyright 2019-present NAVER Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.ㄴ
"""

import copy
from srcs import jsonl
import ujson as json
from konlpy.tag import Okt
from tqdm import tqdm

okt=Okt()

def annotate(sentence):
    words, gloss = [], []
    tokenized = okt.morphs(sentence)
    for t in tokenized:
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
    for ind in (i for i, e in enumerate(l) if e == sl[0]):
        if l[ind:ind + sll] == sl:
            results.append((ind, ind + sll - 1))

    return results

def check_wv_tok_in_nlu_tok(wv_tok1, nlu_t1):
    """
    Jan.2019: Wonseok
    Generate SQuAD style start and end index of wv in nlu. Index is for of after WordPiece tokenization.

    Assumption: where_str always presents in the nlu.

    return:
    st_idx of where-value string token in nlu under CoreNLP tokenization scheme.
    """

    g_wvi1_corenlp = []

    for i_wn, wv_tok11 in enumerate(wv_tok1):
        results = find_sub_list(wv_tok11, nlu_t1)
        st_idx, ed_idx = results[0]

        g_wvi1_corenlp.append( [st_idx, ed_idx] )

    return g_wvi1_corenlp


def annotate_example_ale(example, table):
    """
    Jan. 2019: Wonseok
    Annotate only the information that will be used in our model.
    Sep. 2021: ale
    Modified for Okt
    """
    ann = {'table_id': example['table_id'],'phase': example['phase']}
    _nlu_ann = annotate(example['question'])
    ann['question'] = example['question']
    ann['question_tok'] = _nlu_ann['gloss']
    # ann['table'] = {
    #     'header': [annotate(h) for h in table['header']],
    # }
    ann['sql'] = example['sql']
    ann['query'] = sql = copy.deepcopy(example['sql'])

    conds1 = ann['sql']['conds']
    wv_ann1 = []
    for conds11 in conds1:
        _wv_ann1 = annotate(str(conds11[2]))
        wv_ann11 = _wv_ann1['gloss']
        wv_ann1.append( wv_ann11 )

        # Check whether wv_ann exsits inside question_tok

    try:
        wvi1_corenlp = check_wv_tok_in_nlu_tok(wv_ann1, ann['question_tok'])
        ann['wvi_corenlp'] = wvi1_corenlp
    except:
        ann['wvi_corenlp'] = None
        ann['tok_error'] = 'SQuAD style st, ed are not found under CoreNLP.'

    return ann

if __name__ == '__main__':

    answer_toy = True
    toy_size = 10

    fsplit = 'outputs/dev/dev_translated_mini_cp_cut.jsonl'
    ftable = 'data/dev.tables.jsonl'
    fout = 'outputs/dev/dev_translated_mini_cp_cut_tok.jsonl'

    print('annotating {}'.format(fsplit))
    with open(fsplit, encoding='utf-8') as fs, open(ftable, encoding='utf-8') as ft:
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
            a = annotate_example_ale(d, tables[d['table_id']])
            done.append(a)
            n_written += 1

            if answer_toy:
                if cnt > toy_size:
                    break
        jsonl.dump_jsonl(done, fout, append=True)
        print('wrote {} examples'.format(n_written))
