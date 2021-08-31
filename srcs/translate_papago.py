import os
import sys
import time
import urllib.request
import jsonl
import parse_translated

#client_id = "-------" # 개발자센터에서 발급받은 Client ID 값
#client_secret = "-------" # 개발자센터에서 발급받은 Client Secret 값
origin_data = jsonl.load_jsonl("data/data/dev.jsonl")
print(len(origin_data))
#print(int(len(data)/4))

#quarter = data[:int(len(data)/4)]
#print(quarter[0])
### get translated Text from response ###
### jonna slow jonna slow jonna slow...###

with open("translated_1611translate.py_.txt", "w", encoding='utf-8') as f:
    #for sub in range(1540, len(data), 70):
    for sub in range(1610, int(len(origin_data)/4), 70):
        questions = ""
        print(sub)

        if (sub+70>len(origin_data)):
            for d in origin_data[sub:]:
                questions = questions+d['question']+"\n"

        else:
            for d in origin_data[sub:sub+70]:
                print(type(d))
                questions = questions+d['question']+"\n"
        print(questions)


        """if (sub + 70 > len(quarter)):
            for d in quarter[sub:]:
                questions = questions + d['question'] + "\n"


        else:
            for d in quarter[sub:sub + 70]:
                questions = questions + d['question'] + "\n"
                """

        #print(questions)
        #f.write(questions)

        encText = urllib.parse.quote(questions)
        print(encText)
        data = "source=en&target=ko&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        print(request)
        """response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()

        if (rescode == 200):
            response_body = response.read()
            body = response_body.decode('utf-8')
            print(body)
            flag_s = body.find("translatedText") + len("translatedText\":\"")
            flag_e = body.find("engineType") - 3
            #print(body[flag_s:flag_e])
            f.write(body[flag_s:flag_e] + '\n')

        elif (rescode == 429):
            time.sleep(int(response.headers["Retry-After"]))
        else:
            print("Error Code:" + rescode)"""

"""translated_files = ["translated.txt"]
for file_name in translated_files:
    with open(file_name, 'r', encoding='utf-8') as f:
        parse_translated(f, data)"""

#jsonl.dump_jsonl(data, "out.txt")