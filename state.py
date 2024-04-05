from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
import streamlit as st

import colors_names_db

class State(ABC):
    def __init__(self, ctx: SessionContext) -> None:
        self._ctx = ctx

    def transition(self, state: State) -> None:
        temp_state = self._ctx.state
        state.initialize()
        self._ctx.state = state
        temp_state.finalize()

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def finalize(self) -> None:
        pass

    @abstractmethod
    def process(self) -> None:
        st.markdown(
            f"""
            <style>
            .stButton>button {{
                background-color: {colors_names_db.color_names_db[self._ctx.color_name_index]};
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

class SessionContext:
    def _set(self, key: str, value: Any) -> None:
        st.session_state[key] = value
                
    def _get(self, key: str) -> Any:
        if key in st.session_state:
            return st.session_state[key]
        else:
            return None
        
    def _get_default_zero(self, key: str) -> int:
        if key in st.session_state:
            return st.session_state[key]
        else:
            return 0
        
    @property
    def state(self) -> State:
        return self._get('state')
        
    @state.setter
    def state(self, state: State) -> None:
        self._set('state', state)
        st.rerun()
        
    @property
    def color_name_index(self) -> int:
        return self._get_default_zero('color_name_index')
    
    @color_name_index.setter
    def color_name_index(self, color_name_index: int) -> None:
        self._set('color_name_index', color_name_index)

    @property
    def publication_name(self) -> str:
        return self._get('publication_name')
    
    @publication_name.setter
    def publication_name(self, publication_name: str) -> None:
        self._set('publication_name', publication_name)