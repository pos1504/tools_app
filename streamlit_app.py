import streamlit as st
import pandas as pd
import os
from datetime import datetime
# ==========================================
# 1. Streamlit 기본 UI 숨기기 CSS 코드 추가
# ==========================================
hide_streamlit_style = """
<style>
/* 우측 상단 깃허브 링크 및 각종 툴바 숨기기 */
[data-testid="stToolbar"] {visibility: hidden !important;}

/* 우측 상단 햄버거 메뉴(점 3개) 숨기기 */
#MainMenu {visibility: hidden !important;}

/* 하단 'Made with Streamlit' 워터마크 숨기기 */
footer {visibility: hidden !important;}

/* 상단 헤더 영역 전체 숨기기 (필요시 사용) */
header {visibility: hidden !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# ==========================================
# ==========================================
# ⚙️ 설정 부분
# ==========================================
FILE_NAME = "purchase_log_v2.xlsx"
ADMIN_PASSWORD = "admin"  # ⚠️ 필요시 변경하여 사용하세요

st.set_page_config(page_title="공구/자재 구매 요청 시스템", page_icon="🛠️", layout="wide")

st.title("🛠️ 공구/자재 구매 요청")

# 탭을 나누어 폼 입력 방식을 다르게 설정
tab1, tab2 = st.tabs(["📦 기존 자재 신청 (자재번호 있음)", "🆕 신규 공구/자재 신청 (자재번호 없음)"])

# ------------------------------------------
# 탭 1: 자재번호 있을 때 (상세사양, 옵션-래퍼런스 제거 버전)
# ------------------------------------------
with tab1:
    st.subheader("📦 기존 자재번호 입력 구매 요청")
    st.markdown("자재번호가 있는 품목을 여러 개 입력할 수 있습니다. 아래 표에서 **'+' 버튼**을 눌러 항목을 추가하세요.")
    
    if 'df_exist' not in st.session_state:
        st.session_state.df_exist = pd.DataFrame([
            {"자재번호": "", "구매수량": 1, "담당자 성함": "", "옵션-업무연락": "업무연락 000팀 00-0000"}
        ])

    edited_df_exist = st.data_editor(
        st.session_state.df_exist,
        num_rows="dynamic",
        width="stretch",
        key="editor_exist",
        column_config={
            "자재번호": st.column_config.TextColumn("자재번호 (필수)", required=True),
            "구매수량": st.column_config.NumberColumn("구매수량", min_value=1, step=1, required=True),
            "담당자 성함": st.column_config.TextColumn("담당자 성함", required=True),
            "옵션-업무연락": st.column_config.TextColumn("옵션-업무연락 (예: 업무연락 000팀 00-0000)")
        }
    )

    if st.button("기존 자재 구매 요청 제출", type="primary", key="btn_exist"):
        valid_data = edited_df_exist[edited_df_exist["자재번호"].str.strip() != ""].copy()

        if valid_data.empty:
            st.warning("⚠️ 입력된 자재번호가 없습니다.")
        else:
            # 엑셀 데이터 표준화 (화면에 없는 상세사양, 래퍼런스는 '-'로 백그라운드 자동 채움)
            valid_data.insert(0, "요청일시", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            valid_data.insert(2, "자재명", "-")
            valid_data.insert(3, "상세사양", "-") 
            valid_data.insert(6, "옵션-래퍼런스", "-") 
            
            # 컬럼 순서 정렬: 통합 엑셀 파일 스키마에 맞춤
            valid_data = valid_data[["요청일시", "자재번호", "자재명", "상세사양", "구매수량", "담당자 성함", "옵션-래퍼런스", "옵션-업무연락"]]

            try:
                if os.path.exists(FILE_NAME):
                    existing_df = pd.read_excel(FILE_NAME)
                    updated_df = pd.concat([existing_df, valid_data], ignore_index=True)
                else:
                    updated_df = valid_data

                updated_df.to_excel(FILE_NAME, index=False, engine='openpyxl')
                st.success(f"✅ 성공적으로 {len(valid_data)}건의 기존 자재 요청이 엑셀에 기록되었습니다!")
                
                st.session_state.df_exist = pd.DataFrame([
                    {"자재번호": "", "구매수량": 1, "담당자 성함": "", "옵션-업무연락": "업무연락 000팀 00-0000"}
                ])
                st.rerun()
            except Exception as e:
                st.error(f"엑셀 저장 오류: {e}")

# ------------------------------------------
# 탭 2: 자재번호 없고 신규일 때
# ------------------------------------------
with tab2:
    st.subheader("🆕 신규 공구/자재 입력 구매 요청")
    st.markdown("자재번호가 없는 신규 품목입니다. 자재명과 사양을 입력해주세요.")
    
    if 'df_new' not in st.session_state:
        st.session_state.df_new = pd.DataFrame([
            {"자재명": "", "상세사양": "사양을 입력해주세요 예: 임팩 드라이버 RPM : 2,000~3,000 RPM, 6.35mm(1/4인치) 육각 샹크 원터치 방식", 
             "구매수량": 1, "담당자 성함": "", "옵션-래퍼런스": "임팩렌치 (DCF900P2T)", "옵션-업무연락": "업무연락 000팀 00-0000"}
        ])

    edited_df_new = st.data_editor(
        st.session_state.df_new,
        num_rows="dynamic",
       width="stretch",
        key="editor_new",
        column_config={
            "자재명": st.column_config.TextColumn("자재명 (필수)", required=True),
            "상세사양": st.column_config.TextColumn("사양 (필수)", required=True),
            "구매수량": st.column_config.NumberColumn("구매수량", min_value=1, step=1, required=True),
            "담당자 성함": st.column_config.TextColumn("담당자 성함", required=True),
            "옵션-래퍼런스": st.column_config.TextColumn("옵션-래퍼런스 (예: 임팩렌치 (DCT321PT))"),
            "옵션-업무연락": st.column_config.TextColumn("옵션-업무연락 (예: 업무연락 000팀 00-0000)")
        }
    )

    if st.button("신규 자재 구매 요청 제출", type="primary", key="btn_new"):
        valid_data = edited_df_new[edited_df_new["자재명"].str.strip() != ""].copy()

        if valid_data.empty:
            st.warning("⚠️ 입력된 자재명이 없습니다.")
        else:
            valid_data.insert(0, "요청일시", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            valid_data.insert(1, "자재번호", "신규")
            
            valid_data = valid_data[["요청일시", "자재번호", "자재명", "상세사양", "구매수량", "담당자 성함", "옵션-래퍼런스", "옵션-업무연락"]]

            try:
                if os.path.exists(FILE_NAME):
                    existing_df = pd.read_excel(FILE_NAME)
                    updated_df = pd.concat([existing_df, valid_data], ignore_index=True)
                else:
                    updated_df = valid_data

                updated_df.to_excel(FILE_NAME, index=False, engine='openpyxl')
                st.success(f"✅ 성공적으로 {len(valid_data)}건의 신규 자재 요청이 엑셀에 기록되었습니다!")
                
                st.session_state.df_new = pd.DataFrame([
                    {"자재명": "", "상세사양": "사양을 입력해주세요 예: 임팩 드라이버 RPM : 2,000~3,000 RPM, 6.35mm(1/4인치) 육각 샹크 원터치 방식", 
                     "구매수량": 1, "담당자 성함": "", "옵션-래퍼런스": "임팩렌치 (DCF900P2T)", "옵션-업무연락": "업무연락 000팀 00-0000"}
                ])
                st.rerun()
            except Exception as e:
                st.error(f"엑셀 저장 오류: {e}")

# ==========================================
# 🔒 관리자 전용 메뉴 (엑셀 다운로드 영역)
# ==========================================
st.divider()
st.subheader("관리자")

pwd_input = st.text_input("관리자 비밀번호를 입력하세요", type="password", key="admin_pwd")

if pwd_input == ADMIN_PASSWORD:
    st.success("인증되었습니다. 데이터를 다운로드하거나 확인할 수 있습니다.")
    
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "rb") as f:
            excel_data = f.read()
            
        st.download_button(
            label="📥 전체 구매로그 엑셀 다운로드",
            data=excel_data,
            file_name=f"구매로그_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
        
        with st.expander("👀 현재 엑셀 로그 데이터 전체 미리보기"):
            current_df = pd.read_excel(FILE_NAME)
            st.dataframe(current_df, width="stretch")
            
    else:
        st.info("아직 저장된 엑셀 파일(구매 기록)이 없습니다.")

elif pwd_input != "":
    st.error("비밀번호가 일치하지 않습니다.")
