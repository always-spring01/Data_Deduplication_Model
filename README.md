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
Label의 경우 0과 1로 이루어져 있으며 0은 오탐으로 정상 패킷을 의미하고 1은 정탐으로 악성 패킷을 의미한다. 해당 모델의 분석에 사용된 데이터셋은 총 2개 (`A.csv`, `B.csv`)를 사용하였는데, 각 데이터셋의 Label 구분은 아래와 같다.
|이름|총 개수|0|1|
|:---:|:---:|:---:|:---:|
|A.csv|1,118,257|1,086,944|31,313|
|B.csv|2,336,672|2,301,395|35,277|

`A.csv` 파일의 경우, 상대적으로 데이터의 양이 적음을 알 수 있고, `B.csv`의 양이 많음을 알 수 있다. 또한 두개 데이터셋 모두 **라벨의 편향**이 강함을 알 수 있다. **라벨의 편향**이란, 전체 데이터 중에서 라벨이 0인 패킷과 라벨이 1인 패킷의 비율이 한쪽으로 치중되었음을 의미한다.

### 데이터 전처리
위에서 분석한 결과를 바탕으로 데이터를 전처리한다.<br>

먼저 학습, 평가 데이터를 분리한다. 학습 데이터란, 실질적으로 중복성 제거가 이뤄지는 데이터셋이며 해당 데이터를 기반으로 머신러닝 모델을 학습시킨다. 평가 데이터란, 학습 데이터로 학습된 머신러닝 모델의 성능을 판단하는 근거로 사용한다.<br>

학습, 평가 데이터는 전체 데이터셋을 비율로 축소하는 것이 현 모델의 성능 검증에서 가장 적합하다고 판단하였다. 그 이유는 아래와 같다.<br>
첫 번째, 라벨의 편향을 처리하는 과정이다. 원본 데이터셋 모두 라벨의 불균형이 명확하게 드러났으므로 중복성 제거의 성능을 효과적으로 보기 위해서는 이 불균형을 유지하는 것이 중요하다고 판단하였다.<br>
두 번째, 각 데이터셋의 크기가 다르기 때문이다. 성능 평가는 데이터셋에 따라 두 번 측정하였으므로 각 데이터셋의 크기에 맞춰 최적화되어야 하는데, 이는 비율로 축소하는 것이 가장 적합하다고 판단하였다.<br>

이러한 이유로 학습 데이터와 평가 데이터의 비율은 각각 80%, 20%로 설정하였으며, 각 데이터셋의 라벨의 비율을 유지하고 안의 패킷은 정해진 개수만큼 랜덤으로 추출하였다. 각 데이터셋 별 추출된 결과는 아래와 같다.
|이름|총 개수|학습 데이터|평가 데이터|
|:---:|:---:|:---:|:---:|
|A.csv|1,118,257|894,605|223,652|
|B.csv|2,336,672|1,869,338|467,334|

### 데이터 벡터화
중복성 제거를 하기 위해서는 16진수로 이루어진 Payload 부분을 벡터로 변환할 필요가 있다.

본 모델은 비교적 간단하고 적은 차원으로 구성할 수 있는 ASCII 벡터로 데이터를 변환하였다. 그 이유로는, 이후 진행할 유사도 비교에서 차원 수가 많을수록 구동 시간이 오래걸리는 문제가 있었기 때문이다. 반대로, 차원 수가 너무 적으면 다른 Payload가 하나의 쌍으로 묶이는 문제가 발생한다.

ASCII 벡터란, 256개의 ASCII 문자 (0~255)의 개수를 기록한 벡터를 의미하며, 16진수로 이루어진 Payload는 2개의 문자를 10진수로 변환하고, 이를 ASCII 문자로 변환할 수 있다. 코드는 아래와 같다.
```python
def payload_to_vector(payloads : list) -> list:
    ans = []
    for payload in payloads:
        result = [0 for _ in range(256)]
        for i in range(0, len(payload), 2):
            result[int(payload[i:i+2], 16)] += 1
        ans.append(result)
    return ans
```

위 코드를 통해 기존 데이터셋의 Payload를 ASCII 빈도 벡터로 변환한 다음, 이 벡터 사이의 유사도를 기반으로 클러스터링을 시행하였다.

### 클러스터링
클러스터링이란, 유사한 벡터를 하나의 클러스터(군집)으로 변환하는 작업을 의미한다. 해당 모델에서는 앞서 추출한 벡터를 **코사인 유사도**를 기반으로 클러스터링한다. **코사인 유사도**는 두 벡터의 방향을 이용해 유사도를 비교하는 방법으로 비교적 간단한 연산을 통해 계산할 수 있다는 특징이 있다.

클러스터링 알고리즘을 간략하게 서술하면 아래의 단계를 거친다.
```python
clusters = []
while (클러스터링 되지 않은 데이터):
    pivot = 최상단 row
    cluster = [pivot, ]
    for data in (클러스터링 되지 않은 데이터):
        if cosSim(pivot, data) >= r:
            cluster.append(data)
        else:
            continue
    (클러스터링 되지 않은 데이터).drop(for data.index in clusters)
    cluster.append(clusters)
```
코사인 유사도를 Python 코드로 풀이하면 아래와 같다.
```python
def cosSim(x : list, y : list) -> float:
    return dot(x, y)/(norm(x)*norm(y))
```
