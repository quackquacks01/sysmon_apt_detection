import pandas as pd
from pycaret.anomaly import *

# 1. CSV 불러오기
df = pd.read_csv("sysmon-Logs.csv", encoding='utf-16')  # 한글 윈도우면 utf-16

# 2. 작업 범주 필드 파싱
def parse_event_details(event_text):
    lines = str(event_text).splitlines()
    parsed = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            parsed[key.strip()] = value.strip()
    return parsed

parsed_logs = [parse_event_details(row) for row in df["작업 범주"]]
parsed_df = pd.DataFrame(parsed_logs)

# 3. 분석용 필드 추가
parsed_df["CommandLine"] = parsed_df.get("CommandLine", "")
parsed_df["ImageName"] = parsed_df["Image"].fillna("").apply(lambda x: x.split('\\')[-1].lower())
parsed_df["CommandLineLength"] = parsed_df["CommandLine"].fillna("").apply(len)
parsed_df["ProcessId"] = pd.to_numeric(parsed_df["ProcessId"], errors='coerce')
parsed_df["Image_encoded"] = parsed_df["ImageName"].astype("category").cat.codes

# 4. PyCaret 환경 설정
features = parsed_df[["CommandLineLength", "ProcessId", "Image_encoded"]].dropna()
setup(data=features, session_id=42, silent=True, verbose=False)

# 5. Isolation Forest 모델 학습
model = create_model('iforest')
results = predict_model(model, data=features)

# 6. 이상 로그 추출
anomalies = features.copy()
anomalies["Anomaly_Score"] = results["Anomaly"]
anomalies["Anomaly_Label"] = results["Label"]

# 7. 이상 탐지된 항목만 필터링
suspicious = anomalies[anomalies["Anomaly_Label"] == 1]
print(suspicious.head(10))
