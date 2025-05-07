import streamlit as st
import pandas as pd
import os

# Ustawienie ścieżki do lokalnego pliku CSV
CSV_PATH = r"C:\Users\KlaudiaDrozd\Desktop\KIEDY PRODUKT_CC\purchase_orders_data.csv"

# Funkcja ładująca dane
@st.cache_data(ttl=600)
def load_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH, sep=';')
    else:
        st.error(f"Nie znaleziono pliku CSV w lokalizacji:\n{CSV_PATH}")
        return pd.DataFrame()  # pusty DataFrame

# Ustawienia aplikacji
st.set_page_config(page_title="Kiedy przyjdzie produkt?", layout="centered")
st.title("📦 Kiedy przyjdzie produkt?")
st.caption("Dane z lokalnego pliku CSV (z Verto / SharePoint)")

# Przycisk odświeżenia danych
if st.button("🔄 Odśwież dane"):
    st.cache_data.clear()

# Wczytanie danych
df = load_data()

# Pole wyszukiwania
query = st.text_input("🔍 Wpisz EAN lub fragment modelu (modelcolor):", "")

# Filtrowanie i wyświetlanie wyników
if not df.empty:
    if query:
        filtered = df[
            df['ean'].astype(str).str.contains(query, case=False, na=False) |
            df['modelcolor'].astype(str).str.contains(query, case=False, na=False)
        ]
        if filtered.empty:
            st.warning("Brak wyników dla podanego zapytania.")
        else:
            st.write("### Wyniki wyszukiwania:")
            st.dataframe(filtered[[
                'index', 'ean', 'modelcolor', 'document_date', 'product_short_name'
            ]])
    else:
        st.info("Wpisz EAN lub fragment modelcolor, aby rozpocząć wyszukiwanie.")
