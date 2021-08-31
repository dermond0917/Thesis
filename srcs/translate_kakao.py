import jsonl
from kakaotrans import Translator

translator = Translator()

restAPI_key = "KakaoAK ---------"

origin_data = jsonl.load_jsonl("data/data/dev.jsonl")
print(len(origin_data))

with open("translated_kakao_4.txt", "a", encoding='utf-8') as f:
    start = 2195
    result_list = []
    for d in origin_data[start:]:
        res = translator.translate(d['question'], src='en', tgt='kr')
        print(res)
        result_list.append(res)
        f.write(res)
        f.write("\n")
