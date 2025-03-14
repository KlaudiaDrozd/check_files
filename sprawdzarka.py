import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def sprawdz_plik():
    file_path = filedialog.askopenfilename(filetypes=[("Pliki CSV", "*.csv"), ("Pliki Excel", "*.xlsx")])
    
    if not file_path:
        return
    
    try:
        # Wczytanie pliku
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path, dtype=str)
        else:
            df = pd.read_excel(file_path, dtype=str)

        # Sprawdzenie, czy są wymagane kolumny
        required_columns = {"Modelokolor", "Indeks", "Nazwa krótka"}
        if not required_columns.issubset(df.columns):
            messagebox.showerror("Błąd", "Brak wymaganych kolumn w pliku!")
            return

        # Sprawdzenie unikalności indeksów
        duplicated_indexes = df[df.duplicated(subset=["Indeks"], keep=False)]
        # Sprawdzenie spójności nazw
        inconsistent_names = df.groupby("Modelokolor")["Nazwa krótka"].nunique()
        inconsistent_names = inconsistent_names[inconsistent_names > 1]

        # Przygotowanie raportu
        report = []
        if not duplicated_indexes.empty:
            report.append(f"⚠️ Powtarzające się indeksy:\n{duplicated_indexes.to_string(index=False)}")
        if not inconsistent_names.empty:
            report.append(f"⚠️ Różne nazwy dla tego samego Modelokoloru:\n{inconsistent_names.to_string()}")

        if not report:
            messagebox.showinfo("Wynik", "✅ Wszystko w porządku! Plik jest poprawny.")
        else:
            messagebox.showwarning("Wykryto błędy", "\n\n".join(report))
    
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

# Tworzenie okna GUI
root = tk.Tk()
root.title("Sprawdzanie plików CSV/Excel")
root.geometry("400x200")

label = tk.Label(root, text="Wybierz plik CSV lub Excel do sprawdzenia:")
label.pack(pady=10)

btn = tk.Button(root, text="Wybierz plik", command=sprawdz_plik)
btn.pack(pady=10)

root.mainloop()
