"""
Title : functions.py
- Data_deduplication_model을 위한 함수를 저장한 Python 파일
"""

import pandas as pd
import os
from numpy import dot
from numpy.linalg import norm

# 폴더 생성 Function
def createFolder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
        else:
            return None
    except OSError:
        print("파일을 생성하는 과정에서 오류 발생")

# Payload를 256차원 ASCII 벡터 변환 Function        
def char256(payload):
    vector = [0 for _ in range(256)]
    for i in range(0, len(payload), 2):
        vector[int(payload[i:i+2], 16)] += 1
    return vector

# Dataframe Sampling Function
def df_sampling(df, n1, sampledir):
    k = 1
    while (len(df.index) >= n1):
        sample = df.sample(n1)
        df = df.drop(sample.index)
        sample.to_parquet(sampledir + str(k) + ".parquet")
        k += 1
    df.to_parquet(sampledir + str(k) + ".parquet")
    return k

# 코사인 유사도 Function
def cosSim(x, y) -> float:
    x = [int(x) for x in x]; y = [int(y) for y in y]
    return dot(x, y)/(norm(x)*norm(y))

# Clustering Function
def prototype_clustering(params):
    filename = params[0]
    sampledir = params[1]
    clusterdir = params[2]
    data = pd.read_parquet(sampledir + filename)
    data["sim"] = [0.0 for _ in range(len(data.index))]
    data["cluster"] = [-1 for _ in range(len(data.index))]
    remain = pd.DataFrame(data).copy()
    clusteridx = 1
    while True:
        remain = data[data["cluster"] == -1].copy()
        if (len(remain.index) == 0): break
        if (data["cluster"].max() == -1):
            pivot = remain.iloc[0]
        else:
            pivot = remain.loc[remain["sim"].idxmin()]
        pivot_index = remain.index[(remain["payload"] == pivot.payload)]
        data.loc[pivot_index, "cluster"] = remain.loc[pivot_index, "cluster"] = clusteridx
        for idx, row in remain.iterrows():
            remain.loc[idx, "sim"] = cosSim((char256(pivot.payload)), (char256(row.payload)))
            data.loc[idx, "sim"] = cosSim((char256(pivot.payload)), (char256(row.payload)))
            if (float(remain.loc[idx, "sim"]) >= 0.95):
                remain.loc[idx, "cluster"] = clusteridx
                data.loc[idx, "cluster"] = clusteridx
        clusteridx += 1
        data.to_parquet(clusterdir + filename)
    return 0

# Cluster 대표값 추출 Function
def sample_clustering(params):
    filename = params[0]; clusterdir = params[1]; resultdir = params[2]
    data_original = pd.read_parquet(clusterdir + filename)
    value_counts = data_original["cluster"].value_counts()
    single_cluster_index = value_counts[value_counts == 1].index
    single_cluster_cnt = len(single_cluster_index)
    single_cluster_cnt = single_cluster_cnt
    # 단일 클러스터는 랜덤으로 절반만 추출
    outliner = data_original[data_original["cluster"].isin(single_cluster_index)].sample(single_cluster_cnt//2)
    result_original = pd.DataFrame(columns=data_original.columns)
    result_original = pd.concat([result_original, outliner])
    data_original = data_original[~data_original["cluster"].isin(single_cluster_index)]
    total_cnt = len(data_original.index)
    for k in [1, 2, 4, 8, 10, 20, 30, 40, 50]:
        data = data_original.copy(); result = result_original.copy()
        k_dir = resultdir + str(k) + "/"
        os.makedirs(k_dir, exist_ok=True)
        
        # 클러스터 비율에 따라 K개 추출
        k = single_cluster_cnt * k
        n = k / total_cnt; p = 0
        while (p < k):
            if (len(data.index) == 0): break
            max_cluster = data[data["cluster"] == data.mode().loc[0, "cluster"]]
            t = int(n * len(max_cluster.index))
            if (p + t > k): t = k - p
            if (t > len(max_cluster.index)): t = len(max_cluster.index)
            result = pd.concat([result, max_cluster[max_cluster["sim"] == max_cluster.max()["sim"]]])
            if (t >= 1): result = pd.concat([result, max_cluster.sample(t-1)])
            data = data.drop(max_cluster.index)
        
        result.to_csv(k_dir + f"{filename}_result.csv")