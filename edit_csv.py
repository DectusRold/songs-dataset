import streamlit as st
import pandas as pd

# Funktion zum Hochladen der CSV-Datei
def load_csv():
    uploaded_file = st.file_uploader("CSV-Datei hochladen", type="csv")
    if uploaded_file:
        return pd.read_csv(uploaded_file, sep=";")
    return None

# Funktion zum Filtern des DataFrames
def filter_dataframe(df):
    st.sidebar.header("Filteroptionen")
    filtered_df = df.copy()
    
    # Filtereinstellungen für jede Spalte
    for column in df.columns:
        if df[column].dtype == 'object' or df[column].dtype == 'category':
            options = st.sidebar.multiselect(f"Werte für {column} auswählen", df[column].unique(), default=df[column].unique())
            filtered_df = filtered_df[filtered_df[column].isin(options)]
        elif pd.api.types.is_numeric_dtype(df[column]):
            min_val, max_val = st.sidebar.slider(f"Bereich für {column} auswählen", float(df[column].min()), float(df[column].max()), (float(df[column].min()), float(df[column].max())))
            filtered_df = filtered_df[(filtered_df[column] >= min_val) & (filtered_df[column] <= max_val)]
    return filtered_df

# Funktion zum Bearbeiten eines DataFrames
def edit_dataframe(df):
    st.header("Daten editieren")
    edited_df = st.data_editor(df, num_rows="dynamic")
    return edited_df

# Funktion zum Herunterladen des DataFrames als CSV
def download_csv(df):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="CSV-Datei herunterladen",
        data=csv,
        file_name="bearbeiteter_dataframe.csv",
        mime="text/csv",
    )

# Hauptprogramm
def main():
    st.title("CSV-Datei anzeigen, filtern und bearbeiten")

    # 1. CSV-Datei hochladen
    df = load_csv()
    if df is not None:
        st.subheader("Originaler DataFrame")
        st.dataframe(df)

        # 2. DataFrame filtern
        filtered_df = filter_dataframe(df)
        st.subheader("Gefilterter DataFrame")
        st.dataframe(filtered_df)

        # 3. DataFrame editieren
        edited_df = edit_dataframe(filtered_df)

        # 4. Aktualisierten DataFrame herunterladen
        st.subheader("Aktualisierter DataFrame herunterladen")
        download_csv(edited_df)
    else:
        st.info("Bitte eine CSV-Datei hochladen, um zu starten.")

if __name__ == "__main__":
    main()
