import streamlit as st
import pandas as pd
import os
import finder
import datetime
import mybook

def main():
    st.set_page_config(layout="wide")
    st.title('다 찾아주마')
    
    if 'page' not in st.session_state:
        st.session_state.page = 0

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    
    year = st.selectbox('', range(2023, current_year+1), index=current_year-2023)
    month = st.selectbox('', range(1, 13), index=current_month-1)
    year = str(year)
    month = str(month).zfill(2)
    st.write(f"{year}년 {month}월 이후에 나온 책들을 다 찾아주마")
    
    books_file_path = 'books.csv'
    if st.button("다 찾아주마"):
        if os.path.exists(books_file_path):
            books = mybook.read_books_from_csv_file(books_file_path)
        else:
            books = finder.find_books(year + month)
            mybook.write_books_to_csv_file(books, books_file_path)
        st.session_state.books = books
        st.session_state.page = 0

    if 'books' in st.session_state:
        books_df = pd.DataFrame([{
            'select': False,
            'number': str(i + 1),
            'title': book.contents['title'],
            'release': book.contents['release'],
            'publishers': ', '.join(book.contents['publishers']),
            'url': book.url,
            'authors': ', '.join(book.contents['authors']),
        } for i, book in enumerate(st.session_state.books)])
        st.data_editor(books_df, hide_index=True, column_config={'select': st.column_config.CheckboxColumn(required=True), 'url': st.column_config.LinkColumn()})
        if st.button("다 바꿔주마"):
            pass
            
if __name__ == "__main__":
    main()
