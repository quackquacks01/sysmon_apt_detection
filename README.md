# Sysmon-based APT Detection & Response 🔍🛡️

**Windows Sysmon 로그 기반 APT 공격 실시간 탐지 및 대응 자동화 시스템 (PoC)**  
MITRE ATT&CK 기반 공격 시나리오를 재현하고, Sysmon 로그를 활용해 이상 행위를 탐지 및 시각화하는 프로젝트입니다.

---

## 📑 프로젝트 개요
- **배경**  
  기존 NDR(Network Detection & Response)은 네트워크 패킷 위주 분석이라, Windows 내부 행위 기반 APT 공격은 탐지에 한계가 있습니다.  
  본 프로젝트는 Sysmon 로그를 활용해 명령어 수준의 행위 기반 탐지와 자동 보고 체계를 제안합니다.

- **목표**  
  1. MITRE ATT&CK 시나리오(T1059.001, T1105, T1053 등) 기반 APT 공격 재현  
  2. Sysmon 로그(Event ID 1, 3, 11 등) 수집 및 전처리  
  3. 조건 기반 탐지 + PyCaret 기반 이상 탐지 (Isolation Forest)  
  4. Streamlit 대시보드, PDF 자동 보고서, Slack 경고 기능  

---

## 📂 Repository Structure
```markdown
sysmon/
├── sysmon.py # Sysmon 로그 전처리 및 탐지 엔진
├── sysmon_dashboard.py # Streamlit 대시보드 시각화
└── sysmon-Logs.csv # 샘플 Sysmon 로그 데이터
```

---

## ⚙️ 주요 기능
- **로그 전처리**: Sysmon 로그(.csv) 파싱 → pandas DataFrame 변환
- **탐지 엔진**
  - 조건 기반: PowerShell EncodedCommand, curl, schtasks, Invoke-WebRequest 등
  - 비지도 학습: PyCaret Isolation Forest 모델
- **시각화 & 자동화**
  - Streamlit 대시보드 (위험 명령어 타임라인, 이상치 분포 차트)
  - ReportLab 기반 PDF 자동 보고서 생성
  - Slack API 연동 실시간 알림

---

## 🏆 성과
- 473건 Sysmon 로그 분석 → 조건 기반 + ML 혼합 탐지
- 전체 로그 중 약 5%를 이상치로 탐지, MITRE TTP와 매핑 검증
- PDF 자동 리포트 + Slack 알림으로 보안 대응 속도 향상

---

## 🔧 기술 스택
- **로그 수집**: Sysmon, Windows Event Log
- **언어/라이브러리**: Python, pandas, PyCaret, scikit-learn
- **시각화/리포트**: Streamlit, ReportLab
- **알림 연동**: Slack API

---

## 🚀 실행 방법
```bash
# 1. 의존성 설치
pip install pandas pycaret scikit-learn streamlit reportlab slack_sdk

# 2. 탐지 엔진 실행
python sysmon.py

# 3. Streamlit 대시보드 실행
streamlit run sysmon_dashboard.py
```

## 📜 LICENSE (MIT)
```text
MIT License

Copyright (c) 2025 quackquacks01

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
