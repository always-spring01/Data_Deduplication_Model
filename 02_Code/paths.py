"""
Title : paths.py
- Data_deduplication_model을 위한 경로를 저장한 Python 파일
"""

# Root Path
root = "..\\" # Data_Deduplicaton_Model
dataset = root + "01_Dataset\\"
code = root + "02_Code\\"
output = root + "03_Output\\"

# 01_Dataset
dataset_a = dataset + r"A-PAT_dedup.parquet"
dataset_b = dataset + r"B-PAT_dedup.parquet"

# 03_Output
output_a = output + "A\\"
output_b = output + "B\\"
study_a = output + "A\\study.parquet"
test_a = output + "A\\test.parquet"
study_b = output + "B\\study.parquet"
test_b = output + "B\\test.parquet"
samples_a = output_a + "samples\\"
samples_b = output_b + "samples\\"
clusters_a = output_a + "clusters\\"
clusters_b = output_b + "clusters\\"
results_a = output_a + "results\\"
results_b = output_b + "results\\"