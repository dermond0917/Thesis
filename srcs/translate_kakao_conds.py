import jsonl
from kakaotrans import Translator

translator = Translator()

restAPI_key = "KakaoAK f1ae08a4109abfb514bb5ed5c406f39c"

origin_data = jsonl.load_jsonl("data/dev.jsonl")
print(len(origin_data))

with open("outputs/dev/translated_kakao_conds.txt", "a", encoding='utf-8') as f:
    start = 735
    for d in origin_data[start:]:
        if not (d['sql']['conds']):
            print()
            f.write("\n")

        elif(type(d['sql']['conds'][0][2]) is not str):
            print(d['sql']['conds'][0][2])
            f.write(str(d['sql']['conds'][0][2]))
            f.write("\n")
        else:
            res = translator.translate(d['sql']['conds'][0][2], src='en', tgt='kr')
            print(res)
            f.write(res)
            f.write("\n")
