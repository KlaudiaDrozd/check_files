import streamlit as st
import pandas as pd

# Funkcja do wczytywania pliku
def load_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            return pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            st.error("Wspierane formaty: CSV i XLSX")
            return None
    else:
        return None

# Funkcja do porównania danych na modelokolorze
def compare_modelokolor(df):
    if df is not None:
        if 'modelokolor' in df.columns:
            # Sprawdzanie niezgodności
            missing_data = df[df.isnull().any(axis=1)]
            if not missing_data.empty:
                st.write("Niezgodności w danych (brakujące wartości):")
                st.write(missing_data)
            else:
                st.success("Brak niezgodności. Wszystkie dane są spójne.")
        else:
            st.error("Brak kolumny 'modelokolor' w pliku.")
    else:
        st.error("Brak danych do analizy")

# Interfejs Streamlit
st.title('Porównanie danych na modelokolorze')
st.write("Wczytaj plik CSV lub XLSX i sprawdź, czy wszystkie dane na modelokolorze są spójne.")

uploaded_file = st.file_uploader("Wybierz plik", type=["csv", "xlsx"])

df = load_file(uploaded_file)
compare_modelokolor(df)
