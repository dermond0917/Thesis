# Korean Text-to-SQL (진행중)

# **목표**

## WikiSQL dataset 을 이용한 한글 Text-to-SQL 데이터셋 구축

- 근래 높은 성능을 보이고 있는 기계 번역 알고리즘을 사용하여 영어로 구성된 테이블 및 쿼리 데이터들을 한글로 번역 (Google translator API)
- 번역된 데이터 중 잘못 번역되거나 한글 어순 등이 자연스럽지 않은 데이터 정제
- minimini data: data_minimini.zip (train 1004 / dev 144 / test 290)

# **진행**

## Korean-to-SQL 모델 구성

- 기존 SoTA 모델에 대한 한글 데이터셋 학습

  - 네이버 Clova에서 발표한 [SQLova](https://github.com/naver/sqlova)를 바탕으로 구축한 한글 데이터셋에 대한 학습 진행

- 한글 특화 Text-to-SQL

  - 기존 SQLova에서는 BERT를 이용 → 구글 BERT base multilingual cased의 한국어 성능 한계
  - SKTBrain에서 발표한 [KoBERT](https://github.com/SKTBrain/KoBERT)로 대체하여 한글 특화 모색
  - 교착어인 한글에 공백 기준 토크나이저를 사용하는 것의 한계
  - konlpy의 okt 모듈로 대체

- 영어 데이터 dev 셋의 기존 모델 accuracy
  - 수정한 모델의 정확도를 평가할 기준을 마련하기 위해 구성한 한글 데이터 셋 크기만큼의 영어 데이터를 사용하여 학습 및 evaluation을 진행
    - ex acc: 쿼리 실행을 통해 측정 (execution accuracy)  
    - lf acc: SQL의 모든 요소 (6가지 모듈에 대해)가 정확히 일치하는지 확인(logical form accuracy)

  ![image](https://user-images.githubusercontent.com/38035718/138372161-b12be74f-ff45-4bc2-8b75-f094a3e5ccd0.png)

- 수정한 모델의 한글 데이터 셋에 대한 성능 향상 확인
  - 기존 공백 기준의 CoreNLP tokenizer를 형태소 기준의 okt tokenizer로 변경시 큰 정확도 향상을 보임
    - 어간과 어미가 결합되어 단어를 이루는 한국어의 특성상 공백을 통한 토큰화가 모델의 성능 저하를 발생시킴을 확인함
    - 형태소 단위의 토큰화를 진행하면 이후에 단어를 재구성하는데에 있어 불필요한 어미가 딸려오는 상황을 방지할 수 있어 WHERE VALUE의 정확도를 높일 수 있음
  - 인코더로 사용된 언어모델 BERT를 한글에 대해 더 나은 성능을 보이는 SKTBrains의 KoBERT로 변경시 오히려 정확도가 떨어짐
    - 번역 데이터를 사용하였기 때문에 평소 한글과의 차이점 존재, 번역 시 다른 의미가 있을 수 있는 데이터들 다수 존재함
    - KoBERT를 이용하기 위해서는 번역 데이터가 아닌 원문이 한글인 데이터를 이용 해야 할 것으로 보임

  ![image](https://user-images.githubusercontent.com/38035718/138371902-56054776-450a-45e9-aa37-93e7c03546e0.png)
  

- 한글 데이터셋에 대해 학습한 모델의 경우 다음 [링크](https://drive.google.com/file/d/10dPKIWtezuAh14zKB6-L5VgEbIVG2C8_/view?usp=sharing)를 통해 다운로드 가능

## 사용자의 데이터로 기 학습된 모델 사용 가능한 web
-  사용자가 csv 형식의 테이블 데이터를 업로드하고 자연어 질문을 입력하면 기 학습된 모델을 통해 해당하는 SQL Query를 예측하는 자연어-SQL 번역 웹 사이트를 구성하였다.

*index page*![image](https://user-images.githubusercontent.com/38035718/138371781-0797dbff-9de3-4067-918f-931b6f731058.png)

*query page*![image](https://user-images.githubusercontent.com/38035718/138371797-78214560-81cb-4e8b-8525-fbb461a4702a.png)

## 한글 Dataset

#### minimini dataset 
<img src="https://user-images.githubusercontent.com/38035718/137361761-0746c138-a176-4113-82b2-1cf87bb55ee6.png" alt="외부 이미지" height="200px" />

## **Requirements**

- `python 3.6` 이상
- `PyTorch 1.7.0` 이상

- SQLova
    - `CUDA 9.0`
    - `sqlalchemy == 1.3`  (반드시 1.3으로 설정)
    - `records == 0.5.2` (반드시 0.5.2로 설정)
    - Python libraries: `babel, matplotlib, defusedxml, tqdm, ujson, stanza`
- KoBERT
    - `MXNet >= 1.4.0`
    - `gluonnlp >= 0.6.0`
    - `sentencepiece >= 0.1.6`
    - `onnxruntime >= 0.3.0`
    - `transformers >= 3.5.0`
