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
<img src="https://img.shields.io/badge/jupyter-F37626?style=flat&logo=jupyter&logoColor=white">
<img src="https://img.shields.io/badge/Anaconda-44A833?style=flat&logo=anaconda&logoColor=white">
<img src="https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white">
<img src="https://img.shields.io/badge/numpy-013243?style=flat&logo=numpy&logoColor=white">
<img src="https://img.shields.io/badge/scikitlearn-F7931E?style=flat&logo=scikitlearn&logoColor=white">
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

추출된 결과를 보면 앞서 설명한 바와 같이 라벨의 불균형이 심함을 알 수 있다. 라벨이 불균형할 경우 추후 학습하는 모델은 개수가 많은 데이터 위주로 학습하여 미지의 데이터가 입력되었을 때 하나의 라벨로 평가하는 오차가 생길 가능성이 높다. 따라서 수가 많은 라벨이 0인 데이터에 대해서만 중복성 제거를 시행하기로 하였다.

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

위 코드를 통해 기존 데이터셋의 Payload를 ASCII 빈도 벡터로 변환한 다음, 이 벡터 사이의 유사도를 기반으로 샘플링 이후 클러스터링을 시행하였다.

### 데이터 샘플링
전처리된 데이터의 품질에 보이는 바와 같이, 각 데이터셋에는 100만개 단위의 데이터가 포함되어 있어 비교적 간단한 클러스터링 과정을 통하더라도 수많은 시간이 소요되어 보다 이를 효율적으로 처리하는 방안이 중요하다. 이를 해결하기 위해 싱글 프로세스로 구동되던 기존의 Python 환경에서 여러개의 프로세스로 구동하는 Multiprocessing 과정을 도입하여 보다 효율적으로 이를 처리하고자 하였다.

Multiprocessing을 위해서는 우선, 각 데이터를 N개의 데이터로 구성된 Sample Dataset으로 분리해야 한다. 이후 각 Sample Dataset에 대해 클러스터링을 시행한 이후 이를 통합하여 반영하는 방법으로 모델을 구현하였다. 샘플링 코드는 아래와 같다.
```python
def df_sampling(df, n1, sampledir):
    k = 1
    while (len(df.index) >= n1):
        sample = df.sample(n1)
        df = df.drop(sample.index)
        sample.to_parquet(sampledir + str(k) + ".parquet")
        k += 1
    df.to_parquet(sampledir + str(k) + ".parquet")
    return k
```

샘플링을 하였기 때문에 당연히 해당 Sample 내에서 클러스터링이 시행되지만, 전체 데이터에 대해 클러스터링 알고리즘을 대입하면 시간 소모가 너무 길고, 중간에 메모리 초과 문제로 인해 코드가 정상적으로 실행되지 않으므로 해당 방법을 채택하였다.

클러스터링 과정에서는 최대 Process의 개수를 제한하여 각 Process마다 Sample을 할당하여 클러스터링을 수행하는 알고리즘을 적용하였다.

본 모델의 성능을 측정할 때는 10,000개의 데이터를 1개의 샘플로 변환하여 작업하였으며 각 데이터셋 별로 생성된 샘플의 수는 아래 표와 같다.

|이름|샘플링 데이터 수|샘플의 수|
|:---:|:---:|:---:|
|A.csv|869,555|87|
|B.csv|1,841,116|185|

각 샘플에는 최대 10,000개의 데이터가 포함되어 있으며 각 마지막 샘플에는 10,000개 이하의 데이터가 포함되어 있다. 이후 설명할 클러스터링 알고리즘은 해당 샘플에 적용하였다.

### 클러스터링
클러스터링이란, 유사한 벡터를 하나의 클러스터(군집)으로 변환하는 작업을 의미한다. 해당 모델에서는 앞서 추출한 벡터를 **코사인 유사도**를 기반으로 클러스터링한다. **코사인 유사도**는 두 벡터의 방향을 이용해 유사도를 비교하는 방법으로 비교적 간단한 연산을 통해 계산할 수 있다는 특징이 있다. 클러스터링 과정은 라벨의 불균형을 해소하기 위해 **라벨의 수가 많은 0인 데이터에 대해서만** 적용하였다.

클러스터링 알고리즘을 간략하게 서술하면 아래의 단계를 거친다.
```python
clusters = []
while (클러스터링 되지 않은 데이터):
    pivot = 최상단 row
    cluster = [pivot, ]
    for data in (클러스터링 되지 않은 데이터):
        if cosSim(pivot, data) >= r: # r : 기준 코사인 유사도
            cluster.append(data)
        else:
            continue
    (클러스터링 되지 않은 데이터).drop(for data.index in clusters)
    cluster.append(clusters)
```

위의 의사 코드 중 `r`은 기준이 되는 코사인 유사도로 기준 Payload과 비교 Payload의 벡터 간 유사도가 해당 값 이상이어야 하나의 클러스터로 평가하는 지표이다. 본 모델을 실험할 때 이 값은 `0.95`로 설정하였다. `r`의 값은 0과 1 사이어야 하며, 1에 가까울 수록 유사성이 짙다고 평가한다. `r`의 값을 지나치게 높이면 데이터의 클러스터가 정상적으로 형성되지 않아 중복제거의 성능이 감소하며, 반대로 지나치게 낮추면 각 클러스터들에 유사하지 않은 데이터가 포함되어 이후 진행할 모델의 성능이 감소하게 된다.

위 클러스터링 알고리즘을 쉽게 풀이하면 아래의 과정을 거친다.

1. 우선 클러스터링 되지 않은 데이터 중 무작위로 1개의 데이터를 기준으로 설정한다.
2. 이후 클러스터링 되지 않은 데이터와 기준 데이터 사이의 벡터간 코사인 유사도 값을 비교한다.
3. 2번 결과, 유사도가 `r` 이상이면 두 개의 데이터를 하나의 클러스터로 포함하고 5번으로 이동한다.
4. 2번 결과, 유사도가 `r` 미만이면 두 개의 데이터는 클러스터로 포함하지 않고 5번으로 이동한다.
5. 이후 다른 클러스터링 되지 않은 데이터와 비교 작업을 반복한다.
6. 전체 비교가 끝나면 다시 클러스터링 되지 않은 데이터를 조회하고 이 데이터의 수가 없을 때 까지 1번 과정으로 반복한다.

해당 클러스터링 과정을 거치면 하나의 기준 벡터를 중심으로 일정한 거리에 분포한 데이터가 하나의 클러스터로 형성된다. 이후 각 클러스터 별 대표값 추출 작업을 통해 해당 클러스터 내부의 랜덤한 데이터를 추출하여 최종적으로 중복제거한 데이터셋을 출력한다.

코사인 유사도를 Python 코드로 풀이하면 아래와 같다.
```python
def cosSim(x : list, y : list) -> float:
    return dot(x, y)/(norm(x)*norm(y))
```

위에서 설명한 바와 같이 해당 모델에서는 메모리 한계와 시간적 한계로 인해 멀티프로세싱 방식을 채택하였기 때문에, 최대 프로세스의 개수를 제한하고 각 프로세스에 동일한 개수의 Sample을 할당하여 보다 빠르게 수행하도록 설계하였다. 또한 작업의 진행도를 파악하기 위해 `tqdm` 모듈을 활용하였다.

### 대표값 추출
클러스터링 작업 이후, 각 샘플별로 클러스터가 생성된다. 각 클러스터에는 기준 데이터와, 유사도가 높은 데이터들이 포함되어 있으며, 각 클러스터의 크기는 최소 1개 이상이다. 최종적으로 경량화된 데이터셋을 만들기 위해서는 각 클러스터 별로 대표값을 추출하여야 한다. 정해진 알고리즘을 통해 각 클러스터의 대표값을 추출하고 이를 합쳐 결과물을 산출한다.

클러스터에서 대표값을 많이 추출하면, 추후 서술할 모델의 평가 지표는 상대적으로 상승하지만, 데이터의 경량화 정도는 낮아진다는 단점이 있다. 본 실험에서는 다양한 경우에 따른 평가 지표를 모두 도출하였고, 그에 대한 결과를 후에 첨부한다.

대표값은 우선 **단일 클러스터**에 대한 처리를 먼저 수행한 이후 추출한다. **단일 클러스터**란, 기준 데이터 1개만을 가지는 클러스터를 의미한다. 이는 다른 기준 데이터와의 유사도가 강하지 않은 데이터를 의미한다. 이를 전부 제거하기보단, 각 샘플별로 절반 개수의 **단일 클러스터**를 경량화 데이터셋에 적용하는 알고리즘을 도입하였다.

이후 다중 클러스터에 대해서는 변수 `k`에 따라 크기에 비례하여 추출하였다. 각 샘플별 생성된 단일 클러스터의 `k`배를 해당 샘플에서 추출할 데이터의 총량으로 설정하고, 생성된 다중 클러스터의 크기에 비례하여 랜덤으로 대표값을 추출하는 방법을 채택하였다. 이러한 방법을 채택한 이유는 크기가 큰 클러스터는 유사성이 강한 데이터가 많다는 것을 의미하므로, 이러한 데이터의 수를 많이 추출하여 반영해야 상대적으로 좋은 평가지표가 나올 것으로 판단했기 때문이다. 이를 수식으로 나타내면 아래와 같다.

>$C_i = (N \times K) \times \frac{c_i}{\Sigma{c_i}}$ <br>
>$C_i$ : 다중 클러스터의 크기, $N$ : 단일 클러스터의 수

`k`값의 경우 본 실험에서는 `[1, 2, 4, 8, 10, 20, 30, 40, 50]`으로 총 9가지의 경우의 수를 대입하여 각 실험 별 평가 지표를 추출하였다.

### 평가
대표값 추출 이후 생성된 경량화된 데이터셋과 원본 데이터셋을 비교하여 평가 지표를 비교하며 최종적으로 본 모델에 대한 연구를 마쳤다. 평가 지표로는 클러스터링 평가 지표로 주로 사용되는 `F1 score, Accuracy score, Precision score, Recall score`과 `Run time`으로 평가하였다. 이 중 `Run time`의 경우 머신러닝 모델이 학습하는데 소요한 시간으로 경량화된 데이터셋의 학습 시간의 감소율을 판단할 수 있다.

평가지표를 추출하기 위한 머신러닝 모델의 경우 `sklearn.ensemble.RandomForestClassifier`를 사용하여 측정하였다.

#### 1. A 데이터셋에 대한 평가

데이터 셋 A에 대한 기초 정보는 아래 표와 같다.

|이름|총 개수|0|1|
|:---:|:---:|:---:|:---:|
|A.csv|1,118,257|1,086,944|31,313|

원본, K의 값 별 실험 결과는 아래와 같다.

|K|학습 데이터 크기|F1 score|Accuracy score|Precision score|Recall score|Run time|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|원본|894,605|0.9811|0.9989|0.9749|0.9874|47s|
|1|234,568|0.9794|0.9988|0.9674|0.9917|11s|
|2|369,464|0.9810|0.9989|0.9702|0.9920|17s|
|4|643,533|0.9809|0.9989|0.9718|0.9901|28s|
|8|825,187|0.9813|0.9989|0.9742|0.9885|37s|
|10|825,187|0.9811|0.9989|0.9742|0.9882|36s|
|20|825,187|0.9811|0.9989|0.9739|0.9885|36s|
|30|825,187|0.9813|0.9989|0.9742|0.9885|37s|
|40|825,187|0.9810|0.9989|0.9718|0.9901|28s|
|50|825,187|0.9812|0.9989|0.9739|0.9887|37s|

#### 2. B 데이터셋에 대한 평가

데이터 셋 B에 대한 기초 정보는 아래 표와 같다.

|이름|총 개수|학습 데이터|평가 데이터|
|:---:|:---:|:---:|:---:|
|B.csv|2,336,672|1,869,338|467,334|

원본, K의 값 별 실험 결과는 아래와 같다.

|K|학습 데이터 크기|F1 score|Accuracy score|Precision score|Recall score|Run time|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|원본|1,869,338|0.8312|0.9954|0.9329|0.7494|120s|
|1|145,403|0.6890|0.9880|0.5627|0.9189|10s|
|2|178,902|0.7381|0.9902|0.6174|0.9175|12s|
|4|250,942|0.7686|0.9918|0.6679|0.9050|16s|
|8|403,794|0.7885|0.9928|0.7119|0.8835|24s|
|10|483,219|0.7966|0.9932|0.7262|0.8822|27s|
|20|893,840|0.8285|0.9949|0.8346|0.8225|54s|
|30|1,319,549|0.8355|0.9954|0.8973|0.7817|84s|
|40|1,734,498|0.8327|0.9954|0.9211|0.7597|116s|
|50|1,847,063|0.8331|0.9954|0.9263|07569|126s|

### 결론
