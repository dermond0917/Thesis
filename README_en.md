# Korean Text-to-SQL

# Goal

## Korean Text-to-SQL Dataset from WikiSQL dataset

- Translate English table data and query data into Korean using machine translation algorithms that are showing high performance in recent years (Google Translator API)
- Refine data that is translated incorrectly or sounds awkward in Korean.

## Modify SoTA model

- Replace SoTA model(SQLova) to suit the characteristics of the Korean data set

# Content

## Korean Dataset

![image](https://user-images.githubusercontent.com/38035718/161673972-7e6cefec-b3be-4210-99cd-95092b4c9cb2.png)

![image](https://user-images.githubusercontent.com/38035718/161673980-babad175-e8fe-45be-9aaf-16561c002f9b.png)

## Korean-to-SQL Model

- Trained Korean-to-SQL model based on the Text-to-SQL papers.
    - Trained Korean dataset based on [SQLova](https://github.com/naver/sqlova) from Naver Clova
    

- Concept of Korean-specific Text-to-SQL algorithms
    - Google BERT base multilingual case's performance limitation on Korean
        - Replaced BERT with [KoBERT](https://github.com/SKTBrain/KoBERT) from SKTBrain
        
    - Limitations of using a space-based tokenizer in Korean which is agglutinative
        - Replaced CoreNLP tokenizer with the okt module from konlpy

- Measured accuracy of the SoTA model on the English data(dev split)
    - Trained and evaluated using English data equivalent to the size of a Korean data set to establish criteria for evaluating the accuracy of the modified model.
        - ex acc: measured through query execution (execution accuracy)
        - lf acc: ensure that all elements of SQL -for 6 modules- are exactly the same(logical form accuracy)
        
        ![image](https://user-images.githubusercontent.com/38035718/161674567-f4d71b5e-f664-44f0-adef-1ad5e0a7e968.png)
        

- Checked the performance improvement of modified model on Korean data sets
    - Replacing CoreNLP tokenizer with morpheme-based okt tokenizer greatly improved the accuracy.
        - Confirmed that tokenization based on spacing causes a degradation in the performance since a stem and a suffix are combined to form a Korean word.
        - Tokenization based on morpheme units can prevent unnecessary endings in subsequent word reconstruction and increase the accuracy of WHERE VALUE.
    - Replacing BERT (encoder) with SKTBrain’s KoBERT rather degraded the accuracy.
        - Since dataset was created through translation, there are differences from ordinary Korean, and there are many data that meanings have changed through translation.
        - In order to use KoBERT, it seems necessary to use data whose original text is Korean, not translated from other language.
    
    ![https://user-images.githubusercontent.com/38035718/138371902-56054776-450a-45e9-aa37-93e7c03546e0.png](https://user-images.githubusercontent.com/38035718/138371902-56054776-450a-45e9-aa37-93e7c03546e0.png)
    
- Please refer to [mariequery_korean_minimini.ipynb](https://github.com/dermond0917/Thesis/blob/master/srcs/mariequery_korean_minimini.ipynb) for the progress of the study.
- In the case of a model that has learned about the Korean dataset, it can be downloaded through this [link](https://drive.google.com/file/d/10dPKIWtezuAh14zKB6-L5VgEbIVG2C8_/view?usp=sharing)

## ****Web available to use pre-learned models with user data****

Pre-learned models with user data are available.

- Implemented a natural language-SQL translation website which predicts the corresponding SQL Query through a pre-learned model.
- Users can upload table data in csv format and enters a natural language question.
- For source code, refer to [flask_app.py](https://github.com/dermond0917/Thesis/blob/master/pyflask/flask_app.py)

*index page*

![https://user-images.githubusercontent.com/38035718/138371781-0797dbff-9de3-4067-918f-931b6f731058.png](https://user-images.githubusercontent.com/38035718/138371781-0797dbff-9de3-4067-918f-931b6f731058.png)

*query page*

![https://user-images.githubusercontent.com/38035718/138371797-78214560-81cb-4e8b-8525-fbb461a4702a.png](https://user-images.githubusercontent.com/38035718/138371797-78214560-81cb-4e8b-8525-fbb461a4702a.png)

*demo*

![https://user-images.githubusercontent.com/38035718/140654392-182321b3-d525-409b-9d2f-d406ab8e8664.GIF](https://user-images.githubusercontent.com/38035718/140654392-182321b3-d525-409b-9d2f-d406ab8e8664.GIF)

### **Requirements**

- `python >= 3.6`
- `PyTorch >= 1.7.0`

- SQLova
    - `CUDA 9.0`
    - `sqlalchemy == 1.3` 
    - `records == 0.5.2` 
    - Python libraries: `babel, matplotlib, defusedxml, tqdm, ujson, stanza`
    
- KoBERT
    - `MXNet >= 1.4.0`
    - `gluonnlp >= 0.6.0`
    - `sentencepiece >= 0.1.6`
    - `onnxruntime >= 0.3.0`
    - `transformers >= 3.5.0`
