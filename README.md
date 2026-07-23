# 🛠️ 공구/자재 구매 요청 및 엑셀 자동화 시스템

## 📌 프로젝트 개요
[cite_start]수작업으로 진행하던 구매 요청과 사양 비교를 자동화하여 실무 업무 시간을 획기적으로 줄이기 위해 기획된 사내용 웹 애플리케이션입니다[cite: 3]. [cite_start]파이썬(Python) 기반의 Streamlit 프레임워크를 사용하여 복잡한 프론트엔드 개발 없이 엑셀 형태의 입력 폼을 웹에 구현했습니다[cite: 25].

## ✨ 주요 기능

* [cite_start]**상황별 맞춤형 탭 분리**: 기존 자재(자재번호 있음)와 신규 자재(자재번호 없음) 입력 방식을 탭으로 완전히 분리하여 사용자 편의성을 높였습니다[cite: 75, 76].
* [cite_start]**동적 다중 행 추가 UI**: `num_rows="dynamic"` 옵션을 적용하여 사용자가 행을 무한정 늘리며 여러 자재와 수량을 한 번에 입력할 수 있습니다[cite: 36].
* [cite_start]**엑셀 로그 자동 누적 (Append)**: 제출 버튼을 누르면 pandas 라이브러리가 기존 엑셀 파일(`purchase_log_v2.xlsx`)의 맨 아랫줄에 새로운 데이터를 차곡차곡 이어 붙여 저장합니다[cite: 28, 37].
* [cite_start]**관리자 전용 보안 다운로드**: 사전에 설정된 비밀번호를 입력해야만 누적된 엑셀 데이터를 웹에서 미리보기 하거나 파일로 다운로드할 수 있도록 보안 처리되었습니다[cite: 68, 70, 71].

## 🛠️ 기술 스택 (Tech Stack)

* [cite_start]**Web UI 및 프레임워크**: Python (Streamlit) [cite: 32]
* [cite_start]**데이터베이스 및 파일 처리**: Python (pandas, openpyxl) [cite: 32]

## 🚀 향후 개발 로드맵 (Roadmap)

* [cite_start]**AI Agent 기반 사양 검색**: 자재번호가 없을 때 크롤링 대신 AI Agent(OpenAI API + 웹 검색 도구)를 활용하여 시중의 유사 제품 사양을 똑똑하게 도출하는 기능 추가[cite: 30, 31].
* [cite_start]**구매 사양서(PPT) 자동화**: `python-pptx` 라이브러리를 통해 도출된 상세 사양을 회사 양식의 빈 PPT 템플릿에 끼워 넣어 자동으로 생성 및 다운로드하는 기능 연동[cite: 113].

## 💻 설치 및 실행 방법

1. 리포지토리를 클론(Clone)하거나 다운로드하여 폴더로 이동합니다.
2. 터미널에서 필요한 파이썬 라이브러리를 설치합니다.
   `pip install streamlit pandas openpyxl`
3. 아래 명령어를 통해 앱을 실행합니다.
   `streamlit run streamlit_app_v2.py`
4. [cite_start]브라우저 창이 열리며 엑셀을 입력하는 것과 동일한 편리한 폼 화면을 확인할 수 있습니다[cite: 41].

## ⚠️ 실무 적용 시 주의사항

* [cite_start]코드 상단의 `ADMIN_PASSWORD = "admin"` 부분에서 "admin" 텍스트를 반드시 강력한 비밀번호로 변경 후 사용하시기 바랍니다[cite: 73].
* [cite_start]외부 인터넷에서 접속하려면 Cloudflare Tunnel 또는 Tailscale을 활용한 보안 연결을 권장합니다[cite: 49, 50].
