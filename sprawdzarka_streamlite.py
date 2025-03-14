import pandas as pd
import streamlit as st

st.title("✅ Sprawdzanie spójności plików CSV/Excel")

# Lista kolumn, które mają być zawsze pominięte (zaktualizowana)
excluded_columns = [
    "Indeks", "Jm", "Stawka VAT", "Główny kod EAN", "Główny numer katalogowy", 
    "Waga netto", "Waga brutto", "Jednostka wagi", "Szerokość", "Wysokość", 
    "Głębokość", "Jednostka wymiarów", "Cena hurtowa bazowa n. PLN", 
    "Kat 4 - Nazwa", "Rozmiar - Nazwa", "Rozmiar producenta - Nazwa", 
    "Kanał sprzedaży - Nazwa", "Ilość paczek", "Typ kartoteki", 
    "Kategoria sprzedaży", "Dropshipping - Nazwa",
    "Wewnętrzny numer katalogowy - Nazwa", "Producent", "Główny dostawca - Nazwa skrócona",
    "INTRASTAT", "Kraj pochodzenia", "Kod CN", "Katalogowa PLN b. PLN",
    "Promocyjna PLN b. PLN", "Kat 1 - Nazwa", "Kat 2 - Nazwa", "Kat 3 - Nazwa",
    "Sezon rok - Nazwa", "Typ sezonu - Nazwa", "Rok - Nazwa", "Sezon zamówienia - Nazwa",
    "Kolor - Nazwa", "Płeć - Nazwa", "Wiek - Nazwa", "Rodzaj produktu - Nazwa",
    "Rodzaj zasilania - Nazwa", "Szablon - Nazwa", "Dane producenta"
]

uploaded_file = st.file_uploader("Wgraj plik CSV lub Excel", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Wczytanie pliku
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, dtype=str)
        else:
            df = pd.read_excel(uploaded_file, dtype=str)

        # Usunięcie ewentualnych spacji z nazw kolumn i zamiana na małe litery
        df.columns = df.columns.str.strip().str.lower()
        excluded_columns_lower = [col.lower().strip() for col in excluded_columns]

        # Pokaż rzeczywiste nazwy kolumn w aplikacji
        st.write("📌 Rzeczywiste nazwy kolumn w pliku:", df.columns.tolist())

        # Sprawdzenie, czy jest kolumna Modelokolor
        if "modelokolor" not in df.columns:
            st.error("❌ Brak wymaganej kolumny 'Modelokolor' w pliku!")
        else:
            # Odfiltrowanie kolumn do sprawdzania (pomijamy wykluczone)
            columns_to_check = [col for col in df.columns if col not in excluded_columns_lower]

            # Sprawdzanie spójności danych dla każdej kolumny (poza wykluczonymi)
            inconsistent_data = {}
            grouped = df.groupby("modelokolor")

            for col in columns_to_check:
                unique_values = grouped[col].nunique()
                inconsistent_rows = unique_values[unique_values > 1]

                if not inconsistent_rows.empty:
                    inconsistent_data[col] = df.groupby("modelokolor")[col].apply(lambda x: x.unique())

            # Wyświetlanie tylko kolumn, które mają błędy
            if not inconsistent_data:
                st.success("✅ Wszystkie sprawdzane kolumny są spójne dla Modelokoloru!")
            else:
                st.warning("⚠️ Wykryto różne wartości w następujących kolumnach:")
                for col, data in inconsistent_data.items():
                    st.write(f"🔸 **Kolumna:** `{col}`")
                    st.write(data)

    except Exception as e:
        st.error(f"❌ Wystąpił błąd: {e}")
