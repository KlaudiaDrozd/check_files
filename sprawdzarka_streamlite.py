import pandas as pd
import streamlit as st

st.title("✅ Sprawdzanie spójności plików CSV/Excel")

# 🔹 **Lista kolumn, które mają być ZAWSZE pominięte**
excluded_columns = [
    "indeks", "jm", "stawka vat", "główny kod ean", "główny numer katalogowy", 
    "waga netto", "waga brutto", "jednostka wagi", "szerokość", "wysokość", 
    "głębokość", "jednostka wymiarów", "cena hurtowa bazowa n. pln", 
    "kat 4 - nazwa", "kanał sprzedaży - nazwa", "ilość paczek", "typ kartoteki", 
    "kategoria sprzedaży", "dropshipping - nazwa",
    "główny dostawca - nazwa skrócona",
    "rodzaj zasilania - nazwa", "szablon - nazwa", "dane producenta"
]

# Wczytywanie pliku przez użytkownika
uploaded_file = st.file_uploader("Wgraj plik CSV lub Excel", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # 📌 **Wczytanie pliku CSV lub Excel**
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, dtype=str)
        else:
            df = pd.read_excel(uploaded_file, dtype=str)

        # 🔹 **Przetwarzanie nazw kolumn – usunięcie spacji i zamiana na małe litery**
        df.columns = df.columns.str.strip().str.lower()
        excluded_columns_lower = [col.lower().strip() for col in excluded_columns]

        # 📌 **Opcjonalne wyświetlenie nazw kolumn – ukryte domyślnie!**
        if st.button("🔎 Pokaż rzeczywiste nazwy kolumn w pliku"):
            st.write("📌 **Rzeczywiste nazwy kolumn w pliku:**", df.columns.tolist())

        # 🔍 **Sprawdzenie, czy plik zawiera 'Modelokolor'**
        if "modelokolor" not in df.columns:
            st.error("❌ Brak wymaganej kolumny 'Modelokolor' w pliku!")
        else:
            # 🔹 **Znalezienie kolumn, które będą sprawdzane (nie są w wykluczonych)**
            columns_to_check = [col for col in df.columns if col not in excluded_columns_lower and col != "modelokolor"]

            # 📌 **NOWOŚĆ: Wyświetlenie kolumn, które aplikacja sprawdza**
            st.write("🔎 **Kolumny, które aplikacja sprawdza:**", columns_to_check)

            # 🔍 **Sprawdzanie spójności danych dla każdej kolumny (poza wykluczonymi)**
            inconsistent_data = {}
            grouped = df.groupby("modelokolor")

            for col in columns_to_check:
                unique_values = grouped[col].nunique()
                inconsistent_rows = unique_values[unique_values > 1]

                if not inconsistent_rows.empty:
                    inconsistent_data[col] = df.groupby("modelokolor")[col].apply(lambda x: x.unique())

            # 🟢 **Wyświetlanie tylko kolumn, które mają błędy**
            if not inconsistent_data:
                st.success("✅ Wszystkie sprawdzane kolumny są spójne dla Modelokoloru!")
            else:
                st.warning("⚠️ Wykryto różne wartości w następujących kolumnach:")
                for col, data in inconsistent_data.items():
                    st.write(f"🔸 **Kolumna:** `{col}`")
                    st.write(data)

    except Exception as e:
        st.error(f"❌ Wystąpił błąd: {e}")
