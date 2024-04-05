import os
import datetime

import book
import publication
import state

import pandas as pd
import streamlit as st

class PublicationScrapState(state.State):        
    def scrap_publications(self, pub_name, year, month) -> pd.DataFrame:
        search_api = {
            'book': book.search_books,
        }
        pubs = search_api[pub_name](year + month)
        return pubs

    def initialize(self):
        super().initialize()
        self._ctx.publication_name = 'book'
        
    def finalize(self):
        super().finalize()

    def process(self):
        super().process()
        
        st.title('다긁어')
        
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        
        pubs_file_path = self._ctx.publication_name + '.csv'
        pubs = publication.read_publications_from_csv_file(pubs_file_path)
        if len(pubs) > 0:
            year, month = publication.get_latest_publication_release(pubs).split('.')
            pubs_df = st.data_editor(publication.create_publications_df(pubs), hide_index=True, column_config={'select': st.column_config.CheckboxColumn(required=True), 'url': st.column_config.LinkColumn()})
            st.write(f"{year}년 {month}월 까지 긁었어")
            
            if st.button(f"선택한 책들은 다삭제"):
                pubs_to_be_removed_df = pubs_df[pubs_df['select']]
                removed_pubs = publication.remove_publications(pubs, pubs_to_be_removed_df['title'].to_list())
                publication.write_publications_to_csv_file(removed_pubs, pubs_file_path)
                st.experimental_rerun()
        else:
            year = st.selectbox('', range(2023, year+1), index=year-2023)
            month = st.selectbox('', range(1, month+1 if year == year else 13), index=month-1)
            year = str(year)
            month = str(month).zfill(2)

        if st.button(f"{year}년 {month}월 이후에 나온 책들을 다긁어"):
            scraped_pubs = self.scrap_publications(self._ctx.publication_name, year, month)
            merged_pubs = publication.merge_publications(pubs, scraped_pubs)
            publication.write_publications_to_csv_file(merged_pubs, pubs_file_path)
            st.experimental_rerun()