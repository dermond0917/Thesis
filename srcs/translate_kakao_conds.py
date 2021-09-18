import jsonl
from kakaotrans import Translator

translator = Translator()

restAPI_key = "KakaoAK ------"

origin_data = jsonl.load_jsonl("data/dev.jsonl")
translated_data = []
print(len(origin_data))

#with open("outputs/dev/translated_kakao_conds.txt", "a", encoding='utf-8') as f:
#output_path = "outputs/dev/dev_translated.jsonl"
output_path = "outputs/dev/dev_translated_tmp.jsonl"
with open("outputs/dev/translated_kakao_concat.txt", "r", encoding='utf-8') as rf:
    lines = rf.readlines()
    start = 4000
    cnt = start
    for d in origin_data[start:start+1000]:
        print(cnt)
        d['question'] = lines[cnt]

        if not (d['sql']['conds']):
            print()

        else:
            for c in d['sql']['conds']:
                if(type(c[2]) is not str):
                    print(c[2])
                    #f.write(str(d['sql']['conds'][0][2]))
                else:
                    res = translator.translate(c[2], src='en', tgt='kr')
                    print(res)
                    c[2] = res
        translated_data.append(d)
        cnt += 1

    jsonl.dump_jsonl(translated_data, output_path, append=True)
