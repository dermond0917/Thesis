import jsonl
from kakaotrans import Translator

translator = Translator()

#restAPI_key = "KakaoAK f1ae08a4109abfb514bb5ed5c406f39c"
restAPI_key = "KakaoAK bd5597437d9dcee62a8b5ed97a19d8e1"

print(restAPI_key)

origin_data = jsonl.load_jsonl("data/train.tables.jsonl")

translated_data = []
print(len(origin_data))

output_path = "outputs/train/train_translated_mini.tables.jsonl"

start = 10
cnt = start

for d in origin_data[start:start+10]:
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
                res = translator.translate(h, src='en', tgt='kr')
                #res = "==>" + h
                #print(res)
                tmp_h.append(res)

    print(len(d['header']))
    d['header'] = tmp_h
    print(len(d['header']))


    tmp_rows = []
    print("rows: ")
    for r in d['rows']:
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
                    res = translator.translate(c, src='en', tgt='kr')
                    #res = "==>"+c
                    #print(res)
                    tmp_r.append(res)
        tmp_rows.append(tmp_r)

    print(len(d['rows']))
    d['rows']=tmp_rows
    print(len(d['rows']))

    print(d)
    translated_data.append(d)

    cnt = cnt+1

jsonl.dump_jsonl(translated_data, output_path, append=True)
