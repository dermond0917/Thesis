from google.cloud import translate_v2 as translate

import jsonl
from google.cloud import translate_v2 as translate
import datetime

print(datetime.datetime.now())

client = translate.Client()

translator = translate.Client()

origin_data = jsonl.load_jsonl("outputs/train/train_mini_tables_jebal.jsonl")

translated_data = []
print(len(origin_data))

output_path = "outputs/train/train_translated_mini.tables.jsonl"

start = 67
end = 67
cnt = start
word_cnt = 0

for d in origin_data[start: end+1]:
    print(cnt, "----------------", d['id'],"-----------------")
    print("header: ")
    tmp_h=[]
    for h in d['header']:
        if not (h):
            #print()
            tmp_h.append(None)

        else:
            if(type(h) is not str):
                    #print(h)
                    tmp_h.append(h)
                    #f.write(str(d['sql']['conds'][0][2]))
            else:
                res = translator.translate(h, target_language='ko')['translatedText']
                #res = "==>" + h
                #print(res)
                word_cnt = word_cnt + len(h)
                tmp_h.append(res)

    print(len(d['header']))
    d['header'] = tmp_h
    print(len(d['header']))


    tmp_rows = []
    print("rows: ")
    print(len(d['rows']))
    rcnt = 0

    for r in d['rows']:
        print("row",rcnt)
        tmp_r = []
        for c in r:
            if not (c):
                #print()
                tmp_r.append(None)

            else:
                if (type(c) is not str):
                    #print(c)
                    tmp_r.append(c)


                else:
                    res = translator.translate(c, target_language='ko')['translatedText']
                    #res = "==>"+c
                    #print(res)
                    word_cnt=word_cnt+len(c)
                    tmp_r.append(res)
        tmp_rows.append(tmp_r)
        print(tmp_rows)
        print(word_cnt)
        rcnt=rcnt+1

    d['rows']=tmp_rows
    print(len(d['rows']))

    print(d)
    translated_data.append(d)
    #jsonl.dump_jsonl(d, output_path, append=True)

    cnt = cnt+1

jsonl.dump_jsonl(translated_data, output_path, append=True)
