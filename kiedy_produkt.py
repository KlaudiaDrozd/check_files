import streamlit as st
import pandas as pd
import os

# Automatyczne określenie ścieżki pliku względem lokalizacji aplikacji
APP_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(APP_DIR, "purchase_orders_data.csv")

# Funkcja ładująca dane
@st.cache_data(ttl=600)
def load_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH, sep=';')
    else:
        st.error(f"Nie znaleziono pliku purchase_orders_data.csv w folderze aplikacji:\n{APP_DIR}")
        return pd.DataFrame()

# Ustawienia aplikacji
st.set_page_config(page_title="Kiedy przyjdzie produkt?", layout="centered")
st.title("📦 Kiedy przyjdzie produkt?")
st.caption("Dane z lokalnego pliku CSV umieszczonego w folderze aplikacji.")

# Przycisk odświeżenia danych
if st.button("🔄 Odśwież dane"):
    st.cache_data.clear()

# Wczytanie danych
df = load_data()

# Pole wyszukiwania
query = st.text_input("🔍 Wpisz EAN, model, nazwę, producenta, numer katalogowy lub fragment:", "")

# Filtrowanie i wyświetlanie wyników
if not df.empty:
    if query:
        query = query.lower()
        filtered = df[df.apply(lambda row:
            row.astype(str).str.lower().str.contains(query).any(), axis=1)]

        if filtered.empty:
            st.warning("Brak wyników dla podanego zapytania.")
        else:
            st.write(f"### 🔍 Znaleziono {len(filtered)} wyników:")
            # Pokazuje dostępne kolumny – dopasuj do swojego pliku
            columns_to_show = ['index', 'ean', 'modelcolor', 'product_short_name',
                               'manufacturer', 'product_code', 'document_date']
            visible_cols = [col for col in columns_to_show if col in filtered.columns]
            st.dataframe(filtered[visible_cols])
    else:
        st.info("Wpisz dowolne słowo lub fragment, aby rozpocząć wyszukiwanie.")
