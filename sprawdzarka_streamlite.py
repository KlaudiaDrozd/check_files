import pandas as pd
import streamlit as st
from io import BytesIO

st.title("✅ Sprawdzanie spójności plików CSV/Excel")

# 🔹 **Lista kolumn, które mają być ZAWSZE pominięte**
excluded_columns = [
    "indeks", "jm", "stawka vat", "główny kod ean", "główny numer katalogowy", 
    "waga netto", "waga brutto", "jednostka wagi", "szerokość", "wysokość", 
    "głębokość", "jednostka wymiarów", "cena hurtowa bazowa n. pln", 
    "kat 4 - nazwa", "kanał sprzedaży - nazwa", "ilość paczek", "typ kartoteki", 
    "kategoria sprzedaży", "dropshipping - nazwa", "rozmiar - nazwa", "rozmiar producenta - nazwa",
    "główny dostawca - nazwa skrócona",
    "rodzaj zasilania - nazwa", "szablon - nazwa", "dane producenta"
]

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Błędy')
    processed_data = output.getvalue()
    return processed_data

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
            inconsistent_modelokolors = set()
            grouped = df.groupby("modelokolor")

            for col in columns_to_check:
                unique_values = grouped[col].nunique()
                inconsistent_keys = unique_values[unique_values > 1].index.tolist()
                inconsistent_modelokolors.update(inconsistent_keys)

            # 🔹 **Filtrowanie tylko błędnych rekordów**
            if not inconsistent_modelokolors:
                st.success("✅ Wszystkie sprawdzane kolumny są spójne dla Modelokoloru!")
            else:
                result_df = df[df['modelokolor'].isin(inconsistent_modelokolors)]
                st.warning(f"⚠️ Wykryto niespójności dla {len(inconsistent_modelokolors)} Modelokolorów:")
                st.dataframe(result_df)

                excel_data = convert_df_to_excel(result_df)
                st.download_button(
                    label="📥 Pobierz błędne dane jako Excel",
                    data=excel_data,
                    file_name="bledy_modelokoloru.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"❌ Wystąpił błąd: {e}")
