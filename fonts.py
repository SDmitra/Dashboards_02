import streamlit as st
import pandas as pd

# CSS стили для таблицы с шрифтом Comic Sans
table_style = """
    <style>
        table {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }
        th {
            background-color: #f2f2f2;
            text-align: left;
        }
        td, th {
            border: 1px solid #dddddd;
            padding: 8px;
        }
        tr:nth-child(even) {
            background-color: #dddddd;
        }
    </style>
"""

# Применение стилей к таблице
st.markdown(table_style, unsafe_allow_html=True)

# Пример таблицы
data = {
    'Имя': ['Анна', 'Петр', 'Мария'],
    'Возраст': [25, 30, 28],
    'Город': ['Москва', 'Санкт-Петербург', 'Казань']
}

df = pd.DataFrame(data)
st.write(df)