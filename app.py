import streamlit as st
import state
import book_scrap_state

class App:
    def __init__(self) -> None:
        self._ctx = state.SessionContext()
        if self._ctx.state is None:
            self.initialize(book_scrap_state.BookScrapState(self._ctx))

    def initialize(self, state: state) -> None:
        state.initialize()
        self._ctx.state = state

    def process(self) -> None:
        self._ctx.state.process()

def main():
    st.set_page_config(layout="wide")
    app = App()
    app.process()

if __name__ == "__main__":
    main()