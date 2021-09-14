read_files = ['translated_kakao.txt', 'translated_kakao_2.txt', 'translated_kakao_3.txt', 'translated_kakao_4.txt', 'translated_kakao_4-5.txt', 'translated_kakao_5.txt', 'translated_kakao_6.txt', 'translated_kakao_7.txt', 'translated_kakao_8.txt', 'translated_kakao_9.txt']

print(read_files)

with open("outputs/dev/translated_kakao_concat.txt", "wb") as outfile:
    for f in read_files:
        with open("outputs/dev/"+f, "rb") as infile:
            outfile.write(infile.read())