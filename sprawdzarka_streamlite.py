import pandas as pd
import streamlit as st

st.title("✅ Sprawdzanie spójności plików CSV/Excel")

uploaded_file = st.file_uploader("Wgraj plik CSV lub Excel", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Wczytanie pliku
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, dtype=str)
        else:
            df = pd.read_excel(uploaded_file, dtype=str)

        # Sprawdzenie, czy jest kolumna Modelokolor
        if "Modelokolor" not in df.columns:
            st.error("❌ Brak wymaganej kolumny 'Modelokolor' w pliku!")
        else:
            # Sprawdzanie spójności danych dla każdej kolumny
            inconsistent_data = {}
            grouped = df.groupby("Modelokolor")

            for col in df.columns:
                if col != "Modelokolor":
                    unique_values = grouped[col].nunique()
                    inconsistent_rows = unique_values[unique_values > 1]

                    if not inconsistent_rows.empty:
                        inconsistent_data[col] = df.groupby("Modelokolor")[col].apply(lambda x: x.unique())

            # Wyświetlanie wyników
            if not inconsistent_data:
                st.success("✅ Wszystkie kolumny są spójne dla Modelokoloru!")
            else:
                st.warning("⚠️ Wykryto różne wartości w następujących kolumnach:")
                for col, data in inconsistent_data.items():
                    st.write(f"🔸 **Kolumna:** `{col}`")
                    st.write(data)

    except Exception as e:
        st.error(f"❌ Wystąpił błąd: {e}")
