#import jsonl
from kakaotrans import Translator
import sqlite3

from google.cloud import translate_v2 as translate
import datetime

print(datetime.datetime.now())

client = translate.Client()

translator = translate.Client()

#origin_data = jsonl.load_jsonl("data/train_mini.jsonl")
table_list=[]

#print(len(origin_data))
# train: 7002 / 1936
# dev: 1001 / 277
# test: 2002 /569

con = sqlite3.connect("outputs/refining/train/train_minimini.db")
cursor = con.cursor()

"""cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# print(cursor.fetchall())  # [('TEST_TABLE_1',), ('TEST_TABLE_2',), ('TEST_TABLE_3',)]
cnt = 0
for row in cursor:
    print(cnt)
    print(row[0])
    cnt=cnt+1"""

with open('outputs/table_lists_train.txt', 'r', encoding='utf-8') as rf:
    table_list= rf.readlines()
#print(table_list)

start = 0
end = 249
#start = 0

cnt = start



for t_id in table_list[start:end+1]:
#for t_id in table_list[start:]:
    print(t_id)
    print(cnt)
    cnt=cnt+1

    t_name = "table_"+t_id[:-1].replace('-', '_')
    """drop_query = "DROP TABLE \'"+t_name+ "\'"
    cursor.execute(drop_query)"""
    sel_query = "SELECT * FROM \'" + t_name + "\'"
    print(sel_query)
    cursor.execute(sel_query)
    table_data = cursor.fetchall()

    print(len(cursor.description))
    cols = "("
    cols = cols + ("?, " * len(cursor.description))
    cols = cols[:-2] + ")"
    #print(cols)
    translated_whole = []
    for d in table_data:
        print(d)
        translated_line = []
        for item in d:
            #print(item)
            if (type(item) is not str):
                res = item
            else:
                res = translator.translate(item, target_language='ko')['translatedText']
            translated_line.append(res)
        print(translated_line)
        translated_whole.append(translated_line)
    translated_whole=tuple(translated_whole)
    #print(translated_whole)

    #print(t_name)

    del_query = "DELETE FROM \'" + t_name + "\'"
    print(del_query)
    cursor.execute(del_query)

    in_query = "INSERT INTO \'" + t_name + "\' VALUES " + cols
    print(in_query)
    cursor.executemany(in_query, translated_whole)
    con.commit()

cursor.close()
con.close()