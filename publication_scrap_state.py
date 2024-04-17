import datetime
import calendar

import book
import paper
import publication
import state

import pandas as pd
import streamlit as st

class PublicationScrapState(state.State):        
    def scrap_publications(self, pubs_file_path: str, pub_name: str, year: str, month: str, day: str) -> pd.DataFrame:
        search_api = {
            'book': book.search_books,
            'paper': paper.search_papers
        }
        pubs = search_api[pub_name](pubs_file_path, year, month, day)
        return pubs

    def initialize(self):
        super().initialize()
        self._ctx.publication_name = 'book'
        
    def finalize(self):
        super().finalize()

    def process(self):
        super().process()
        
        st.title('다긁어')
        
        selected_publication_name = st.selectbox(' ', options=['book', 'paper'], index=1)        
        
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        
        pubs_file_path = selected_publication_name + '.csv'
        pubs = publication.read_publications_from_csv_file(pubs_file_path)
        if len(pubs) > 0:
            year, month, day = publication.get_latest_publication_release(pubs).split('.')
            pubs_df = st.data_editor(publication.create_publications_df(pubs), hide_index=True, column_config={'select': st.column_config.CheckboxColumn(required=True), 'url': st.column_config.LinkColumn()})
            st.write(f"{year}년 {month}월 {day}일 까지 긁었어")
            
            if st.button(f"고른거 다삭제"):
                pubs_to_be_removed_df = pubs_df[pubs_df['select']]
                removed_pubs = publication.remove_publications(pubs, pubs_to_be_removed_df['title'].to_list())
                publication.write_publications_to_csv_file(removed_pubs, pubs_file_path)
                st.experimental_rerun()
        else:
            selected_year = st.selectbox(' ', range(2023, year+1), index=year-2023)
            selected_month = st.selectbox(' ', range(1, month+1 if selected_year == year else 13), index=month-1)
            selected_day = st.selectbox(' ', range(1, day+1 if selected_month == month else calendar.monthrange(year, month)[1]+1), index=day-1)
            year = str(selected_year)
            month = str(selected_month).zfill(2)
            day = str(selected_day).zfill(2)

        if st.button(f"{year}년 {month}월 {day}일 이후에 나온거 다긁어"):
            scraped_pubs = self.scrap_publications(pubs_file_path, selected_publication_name, year, month, day)
            # merged_pubs = publication.merge_publications(pubs, scraped_pubs)
            # publication.write_publications_to_csv_file(merged_pubs, pubs_file_path)
            st.experimental_rerun()