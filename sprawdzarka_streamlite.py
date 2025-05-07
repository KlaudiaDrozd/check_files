import pandas as pd
import streamlit as st
from io import BytesIO

st.title("✅ Sprawdzanie spójności plików CSV/Excel")

# 🔹 Lista kolumn, które mają być ZAWSZE pominięte
excluded_columns = [
    "indeks", "jm", "stawka vat", "główny kod ean", "główny numer katalogowy", 
    "waga netto", "waga brutto", "jednostka wagi", "szerokość", "wysokość", 
    "głębokość", "jednostka wymiarów", "cena hurtowa bazowa n. pln", 
    "kat 4 - nazwa", "kanał sprzedaży - nazwa", "ilość paczek", "typ kartoteki", 
    "kategoria sprzedaży", "dropshipping - nazwa", "rozmiar - nazwa", "rozmiar producenta - nazwa",
    "główny dostawca - nazwa skrócona",
    "rodzaj zasilania - nazwa", "dane producenta",
    "id_good", "index"
]

# 🔧 Funkcja do konwersji DataFrame do Excela
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Błędy')
    return output.getvalue()

# 📁 Wczytywanie pliku
uploaded_file = st.file_uploader("Wgraj plik CSV lub Excel", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # 📥 Wczytanie danych
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, dtype=str, sep=';')  # Ustawiamy separator na średnik
        else:
            df = pd.read_excel(uploaded_file, dtype=str)

        # 🧼 Normalizacja nagłówków
        df.columns = df.columns.str.strip().str.lower()
        excluded_columns_lower = [col.lower().strip() for col in excluded_columns]

        # 🔍 Podgląd kolumn po kliknięciu przycisku
        if st.button("🔎 Pokaż rzeczywiste nazwy kolumn w pliku"):
            st.write("📌 **Rzeczywiste nazwy kolumn w pliku:**", df.columns.tolist())

        # 🧠 Elastyczne dopasowanie kolumny 'modelokolor' dla różnych wariantów
        modelokolor_column = None
        for col in df.columns:
            # Sprawdzamy, czy w nazwie kolumny dokładnie znajduje się 'modelokolor' w różnych wariantach
            if 'modelokolor' in col:
                modelokolor_column = col
                break

        # Debugowanie, wyświetlanie kolumny, którą aplikacja zidentyfikowała
        if modelokolor_column is None:
            st.error("❌ Brak wymaganej kolumny 'Modelokolor' w pliku!")
        else:
            st.write(f"✅ Kolumna 'modelokolor' została znaleziona jako: {modelokolor_column}")

            # Wybór kolumn do sprawdzenia (pomijamy te z wykluczonych)
            columns_to_check = [col for col in df.columns if col not in excluded_columns_lower and col != modelokolor_column]
            st.write("🔎 **Kolumny, które aplikacja sprawdza:**", columns_to_check)

            # 🔍 Sprawdzanie spójności danych dla każdej kolumny (poza wykluczonymi)
            inconsistent_data = []
            grouped = df.groupby(modelokolor_column)

            for col in columns_to_check:
                unique_values = grouped[col].nunique()
                inconsistent_keys = unique_values[unique_values > 1].index.tolist()

                if inconsistent_keys:
                    st.warning(f"⚠️ Kolumna: `{col}` zawiera niespójności")
                    col_issues = df[df[modelokolor_column].isin(inconsistent_keys)][[modelokolor_column, col]].drop_duplicates()
                    st.dataframe(col_issues)  # Zachowujemy ukryty przycisk CSV
                    col_issues['kolumna'] = col
                    inconsistent_data.append(col_issues)

            if not inconsistent_data:
                st.success("✅ Wszystkie sprawdzane kolumny są spójne dla Modelokoloru!")
            else:
                full_error_df = pd.concat(inconsistent_data, ignore_index=True)
                excel_data = convert_df_to_excel(full_error_df)
                st.download_button(
                    label="📥 Pobierz wszystkie błędy jako Excel",
                    data=excel_data,
                    file_name="bledy_modelokoloru.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"❌ Wystąpił błąd: {e}")
