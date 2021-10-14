# Korean Text-to-SQL

# **목표**

## WikiSQL dataset 을 이용한 한글 Text-to-SQL 데이터셋 구축

- 근래 높은 성능을 보이고 있는 기계 번역 알고리즘을 사용하여 영어로 구성된 테이블 및 쿼리 데이터들을 한글로 번역 (Google translator API)
- 번역된 데이터 중 잘못 번역되거나 한글 어순 등이 자연스럽지 않은 데이터 정제

## Korean-to-SQL 모델 구성

- 연구되어 오던 Text-to-SQL 논문들을 바탕으로 Korean-to-SQL 모델 학습
  - 네이버 Clova에서 발표한 [SQLova](https://github.com/naver/sqlova)를 바탕으로 한글 데이터셋에 대한 학습 진행 

- 한글 특화 Text-to-SQL 알고리즘 구상
  - 기존 SQLova에서는 BERT를 이용 → 구글 BERT base multilingual cased의 한국어 성능 한계
  - SKTBrain에서 발표한 [KoBERT](https://github.com/SKTBrain/KoBERT)로 대체하여 한글 특화 모델 구현 

# 내용

## 한글 Dataset

(진행중)

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
