# Korean Text-to-SQL (진행중)

# **목표**

## WikiSQL dataset 을 이용한 한글 Text-to-SQL 데이터셋 구축

- 근래 높은 성능을 보이고 있는 기계 번역 알고리즘을 사용하여 영어로 구성된 테이블 및 쿼리 데이터들을 한글로 번역 (Google translator API)
- 번역된 데이터 중 잘못 번역되거나 한글 어순 등이 자연스럽지 않은 데이터 정제
- minimini data: data_minimini.zip (train 1004 / dev 144 / test 290)

## Korean-to-SQL 모델 구성

- 연구되어 오던 Text-to-SQL 논문들을 바탕으로 Korean-to-SQL 모델 학습
  - 네이버 Clova에서 발표한 [SQLova](https://github.com/naver/sqlova)를 바탕으로 한글 데이터셋에 대한 학습 진행 

- 한글 특화 Text-to-SQL 알고리즘 구상
  - 기존 SQLova에서는 BERT를 이용 → 구글 BERT base multilingual cased의 한국어 성능 한계
  - SKTBrain에서 발표한 [KoBERT](https://github.com/SKTBrain/KoBERT)로 대체하여 한글 특화 모델 구현 
  - 교착어인 한글에 공백 기준 토크나이저를 사용하는 것의 한계
  - konlpy의 okt 모듈로 대체

- 영어 데이터 dev 셋의 기존 모델 accuracy
<img width="495" alt="그림1" src="https://user-images.githubusercontent.com/38035718/138372161-b12be74f-ff45-4bc2-8b75-f094a3e5ccd0.png">

- okt 모듈을 이용한 토큰화를 통해 한글 데이터 셋에 대해 성능 향상 확인
![image](https://user-images.githubusercontent.com/38035718/138371902-56054776-450a-45e9-aa37-93e7c03546e0.png)


- 한글 데이터셋에 대해 학습한 모델의 경우 다음 링크를 통해 다운로드 가능
https://drive.google.com/file/d/10dPKIWtezuAh14zKB6-L5VgEbIVG2C8_/view?usp=sharing, https://drive.google.com/file/d/10fWLT6sLiPS1UOvi_n3EOUMwT2jaqV50/view?usp=sharing

## 사용자의 데이터로 기 학습된 모델 사용 가능한 web
![image](https://user-images.githubusercontent.com/38035718/138371781-0797dbff-9de3-4067-918f-931b6f731058.png)
![image](https://user-images.githubusercontent.com/38035718/138371797-78214560-81cb-4e8b-8525-fbb461a4702a.png)

# 내용

## 한글 Dataset

#### minimini
![image](https://user-images.githubusercontent.com/38035718/137361761-0746c138-a176-4113-82b2-1cf87bb55ee6.png)

### **Requirements**

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
