import os
import datetime

import book_search
import book
import state

import streamlit as st

class BookScrapState(state.State):
    def initialize(self):
        super().initialize()
        
    def finalize(self):
        super().finalize()
        
    def process(self):
        super().process()
        
        st.title('다긁어')
        
        old_books = []
        new_books = []
        books_file_path = 'books.csv'        
        if os.path.exists(books_file_path):
            old_books = book.read_books_from_csv_file(books_file_path)
            year, month = book.get_latest_book_release(old_books).split('.')

            st.write(f"{year}년 {month}월 까지 긁었어")
            edited_books_df = st.data_editor(book.create_books_df(old_books), hide_index=True, column_config={'select': st.column_config.CheckboxColumn(required=True), 'url': st.column_config.LinkColumn()})
        else:
            now_year = datetime.datetime.now().year
            now_month = datetime.datetime.now().month

            year = st.selectbox('', range(2023, now_year+1), index=now_year-2023)
            month = st.selectbox('', range(1, now_month+1 if year == now_year else 13), index=now_month-1)

            year = str(year)
            month = str(month).zfill(2)

        if st.button(f"{year}년 {month}월 이후에 나온 책들을 다긁어"):
            new_books = book_search.search_books(year + month)
            st.data_editor(book.create_books_df(new_books), hide_index=True, column_config={'select': st.column_config.CheckboxColumn(required=True), 'url': st.column_config.LinkColumn()})
            
            books = book.merge_books(old_books, new_books)
            book.write_books_to_csv_file(books, books_file_path)

        if st.button(f"선택한 책들은 다삭제"):
            books_to_be_removed_df = edited_books_df[edited_books_df['select']]
            books = book.remove_books(old_books, books_to_be_removed_df['title'].to_list())
            book.write_books_to_csv_file(books, books_file_path)
            st.experimental_rerun()
