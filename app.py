import streamlit as st
import pandas as pd

# CSV 파일 로드
def load_data():
    return pd.read_csv("your_file.csv")

# 선택된 아이템을 CSV로 저장
def save_selected_items(selected_items):
    selected_items.to_csv("selected_items.csv", index=False)

# 메인 함수
def main():
    st.title("CSV 파일 데이터 뷰어 & 선택기")

    df = load_data()

    # 페이지네이션을 위한 세션 상태 설정
    if 'page' not in st.session_state:
        st.session_state.page = 0

    # 페이지당 표시할 아이템 수
    items_per_page = 50
    start = st.session_state.page * items_per_page
    end = (st.session_state.page + 1) * items_per_page
    displayed_data = df[start:end]

    # 체크박스로 선택된 아이템을 저장할 리스트
    selected_indices = []

    # 데이터와 체크박스 표시
    for index, row in displayed_data.iterrows():
        if st.checkbox(f"{row['your_column_name']}", key=index):
            selected_indices.append(index)

    # 선택된 아이템을 DataFrame으로 변환
    if selected_indices:
        selected_items = df.loc[selected_indices]

        # 선택된 아이템을 CSV로 저장하는 버튼
        if st.button("선택된 아이템을 CSV로 저장"):
            save_selected_items(selected_items)
            st.success("선택된 아이템이 CSV 파일로 저장되었습니다.")

    # 페이지네이션 버튼
    if st.button("이전"):
        if st.session_state.page > 0:
            st.session_state.page -= 1
    if st.button("다음"):
        if end < len(df):
            st.session_state.page += 1

if __name__ == "__main__":
    main()
