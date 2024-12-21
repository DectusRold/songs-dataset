import streamlit as st
import pandas as pd

st.title("Song list")

uploaded_file = st.file_uploader("Chose as CSV file", type="csv")


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep="|")

    st.subheader("Data preview")
    st.write(df.head())

#    st.subheader("Data summary")
#    st.write(df.describe())

    st.subheader("Distinct genres")
    all_genres = df['artist_genres'].str.split(',').explode().str.strip().unique()
    all_genres_as_str = all_genres.astype(str)
    all_genres_sorted = sorted(all_genres_as_str)
    st.write(all_genres_sorted)

    st.subheader("Filter data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = sorted(df[selected_column].unique())

    selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]

    st.write(filtered_df)

