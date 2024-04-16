<div name=header align=center>
<h1>Data Deduplication Model</h1>
<p>
머신러닝 성능 향상을 위한 데이터 중복성 제거 모델
</p>
</div>

<div name=author align=right>
2024 ~ <br>
Kookmin Univ.
</div>

<div align=center> <h3><b>🛠️Tools🛠️</b></h3> </div>
<div align=center>
<img src="https://img.shields.io/badge/python-3776AB?style=flat&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Anaconda-44A833?style=flat&logo=anaconda&logoColor=white">
<img src="https://img.shields.io/badge/scikitlearn-F7931E?style=flat&logo=scikitlearn&logoColor=white">
<img src="https://img.shields.io/badge/pytorch-EE4C2C?style=flat&logo=pytorch&logoColor=white">
<img src="https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white">
<img src="https://img.shields.io/badge/numpy-013243?style=flat&logo=numpy&logoColor=white">
</div>

### 목적
패킷 데이터의 악성 유무를 분석하는 정오탐 분석기는 다량의 네트워크 패킷 데이터를 통해 학습한다. 하지만, 이 과정에서 데이터의 수가 방대하여 학습하는 데 소요되는 시간이 높아지고 다량의 데이터의 편향이 동반되는 문제점이 생긴다. 이를 해결하기 위해 효율적으로 각 패킷 데이터의 유사도를 기반으로 중복성 제거를 제안한다.

### 데이터 분석
각 데이터는 비공개 데이터셋을 이용하여 시행한다. 따라서 본 저장소에서는 해당 데이터셋을 공개하진 않지만, 데이터셋의 구조는 아래와 같이 구성되어 있다.
|번호|이름|설명|예시|
|:---:|:---:|:---:|:---:|
|1|Payload|16진수로 이루어진 각 패킷 페이로드|474555ABF11...
|2|Label|정오탐 분류 결과|0-오탐, 1-정탐

해당 데이터셋에서는 위의 2개의 속성값만 사용하였다. 각 패킷의 Payload에는 해당 패킷에서 사용된 페이로드가 16진수로 기록되어 있다. 이를 바탕으로 중복성이 높은 패킷은 제거하여 효율적으로 전체 데이터의 규모를 감소시키는 것이 해당 모델의 목적이다.

Payload의 경우 16진수로 기록되어 있어 일부 패킷의 경우 알파벳으로 이루어져 있지만, 특정 패킷의 경우 읽을 수 없는 이진 데이터로 이루어져 있음을 알 수 있다.
Label의 경우 0과 1로 이루어져 있으며 0은 오탐으로 정상 패킷을 의미하고 1은 정탐으로 악성 패킷을 의미한다. 해당 모델의 분석에 사용된 데이터셋은 총 2개 (A.csv, B.csv)를 사용하였는데, 각 데이터셋의 Label 구분은 아래와 같다.
|이름|총 개수|0|1|
|:---:|:---:|:---:|:---:|
|A.csv|1118257|1086944|31313|
|B.csv|2336672|2301395|35277|

