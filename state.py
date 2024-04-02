from __future__ import annotations
from abc import ABC, abstractmethod
import streamlit as st

import colors_names_db

class State(ABC):
    def __init__(self, ctx: SessionContext) -> None:
        self._ctx = ctx

    def transition(self, state: State) -> None:
        self._ctx.state.finalize()
        state.initialize()
        self._ctx.state = state

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def finalize(self):
        pass

    @abstractmethod
    def process(self):
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
    def _set(self, key, value):
        st.session_state[key] = value
                
    def _get(self, key):
        if key in st.session_state:
            return st.session_state[key]
        else:
            return None
        
    def _get_default_zero(self, key):
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