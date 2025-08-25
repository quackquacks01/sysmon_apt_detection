import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import requests

# 샘플 데이터 불러오기 (실제 분석 결과와 연결 시 수정)
data = {
    "CommandLine": [
        "powershell -EncodedCommand ZQBjAG8AIABIAH...",
        "curl http://malicious.site",
        "schtasks /create /tn Evil /tr bad.exe /sc daily /st 12:00"
    ],
    "Image": ["powershell.exe", "curl.exe", "schtasks.exe"],
    "Anomaly_Score": [0.1599, 0.1316, 0.0969],
    "Detected_At": [
        "2025-06-23 12:27:33",
        "2025-06-23 12:26:50",
        "2025-06-23 12:26:10"
    ]
}
df = pd.DataFrame(data)

st.title("🚨 APT 탐지 시스템 대시보드")
st.subheader("MITRE 기반 로그 탐지 결과")

# 필터: 점수 기준 필터링
score_threshold = st.slider("이상 점수 필터 (이상만 보기)", 0.0, 1.0, 0.05, 0.01)
df_filtered = df[df['Anomaly_Score'] >= score_threshold]

# 테이블 표시
st.dataframe(df_filtered)

# 그래프
st.bar_chart(df_filtered.set_index("Image")["Anomaly_Score"])

# PDF 리포트 저장 함수
def generate_pdf_report(dataframe, filename="APT_Report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(30, 750, "APT 탐지 리포트")
    c.setFont("Helvetica", 10)
    y = 720
    for i, row in dataframe.iterrows():
        line = f"[{row['Detected_At']}] {row['Image']} | Score: {row['Anomaly_Score']}"
        c.drawString(30, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    return filename

# 리포트 생성 버튼
if st.button("📄 PDF 리포트 생성"):
    filename = generate_pdf_report(df_filtered)
    st.success(f"PDF 리포트 저장됨: {filename}")

# Slack 알림 전송 함수 (Webhook URL 필요)
def send_to_slack(text, webhook_url):
    try:
        payload = {"text": text}
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    except:
        return False

# 슬랙 전송
slack_url = st.text_input("Slack Webhook URL 입력", type="password")
if st.button("📤 Slack으로 알림 보내기"):
    for _, row in df_filtered.iterrows():
        msg = f"🚨 탐지됨: {row['Image']}\nScore: {row['Anomaly_Score']}\nAt: {row['Detected_At']}"
        success = send_to_slack(msg, slack_url)
    st.success("Slack 알림 전송 완료")
