import jsonl
from google.cloud import translate_v2 as translate
import datetime

print(datetime.datetime.now())

client = translate.Client()
translator = translate.Client()

origin_data = jsonl.load_jsonl("data/train_mini.jsonl")
#origin_data = jsonl.load_jsonl("data/dev_mini.jsonl")
#origin_data = jsonl.load_jsonl("data/test_mini.jsonl")

translated_data = []
print(len(origin_data))


with open("outputs/train/translated_google_train_mini_mini.txt", "a", encoding='utf-8') as wf:
#with open("outputs/dev/translated_google_dev_mini_mini.txt", "a", encoding='utf-8') as wf:
#with open("outputs/test/translated_google_test_mini_mini.txt", "a", encoding='utf-8') as wf:
    start = 0
    end = 1003
    cnt = start
    word_cnt = 0

    for d in origin_data[start:end + 1]:
        res = translator.translate(d['question'], target_language='ko')['translatedText']
        print(res)
        word_cnt = word_cnt + len(d['question'])
        wf.write(res)
        wf.write("\n")

print("---------conds----------")

output_path = "outputs/refining/train/train_translated_google_mini_mini.jsonl"
#output_path = "outputs/refining/dev/dev_translated_google_mini_mini.jsonl"
#output_path = "outputs/refining/test/test_translated_google_mini_mini.jsonl"
with open("outputs/train/translated_google_train_mini_mini.txt", "r", encoding='utf-8') as rf:
#with open("outputs/dev/translated_google_dev_mini_mini.txt", "r", encoding='utf-8') as rf:
#with open("outputs/test/translated_google_test_mini_mini.txt", "r", encoding='utf-8') as rf:

    lines = rf.readlines()
    start = 0
    end = 1003
    cnt = start
    word_cnt = 0

    for d in origin_data[start:end+1]:
        print(cnt)
        d['question'] = lines[cnt]

        if not (d['sql']['conds']):
            print()

        else:
            for c in d['sql']['conds']:
                if (type(c[2]) is not str):
                    print(c[2])
                    # f.write(str(d['sql']['conds'][0][2]))
                else:
                    if (c[2].isnumeric()):
                        print(c[2])
                    else:
                        res = translator.translate(c[2], target_language='ko')['translatedText']
                        print(res)
                        c[2] = res
        translated_data.append(d)
        cnt += 1

    jsonl.dump_jsonl(translated_data, output_path, append=True)