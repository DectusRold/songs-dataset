import streamlit as st
import pandas as pd

st.title("Song list")


# Import tracks:
df = pd.read_csv("data/tracks.csv", sep="|")

# convert all object columns to pandas string type:
object_columns = df.select_dtypes(include=['object']).columns
df[object_columns] = df[object_columns].astype('string')

#st.subheader("Data preview")
#st.write(df.head())

# Add year to dataframe:
df['year'] = df['album_release_date'].str[:4].apply(lambda x: int(x) if pd.notnull(x) and x.isdigit() else None)
#df['album_release_date'] = pd.to_datetime(df['album_release_date'], errors='coerce')
year_range = (df['year'].min(), df['year'].max())

# Add artist_album to dataframe:
#df['artist_album'] = df['album_name'] + ' (' + ['Diverse' if album_type == 'compilation' else 'Album' for album_type in df['album_type']] + ')'
#['Compilation' if album_type == 'compilation' else df['track_artists'] for album_type in df['album_type']]
#df['artist_album'] = df['album_name'] + ' (' + df['track_artists'] + ')'


#st.subheader("Column Types")
#st.write(df.dtypes)

#st.subheader("Data summary")
#st.write(df.describe())

st.subheader("Distinct genres")
all_genres = df['artist_genres'].str.split(',').explode().str.strip().unique()
#all_genres_as_str = all_genres.astype(str)
#all_genres_sorted = sorted(all_genres_as_str)
st.write(all_genres)

# Filter songs:
st.subheader("Filter release year")
filter_years = st.slider("Years", 1970, 1980, year_range)

# Show a multiselect widget with the genres using `st.multiselect`.
top_genres=["Rock", "Pop", "Metal", "Hard Rock", "Techno", "Dance", "Electro", "Indie", "Grunge", "Hip-Hip"]
filter_genres = st.multiselect(
    "Genres",
    top_genres,
    ["Rock", "Pop"],
)

#st.subheader("Filter data")
#columns = df.columns.tolist()
#selected_column = st.selectbox("Select column to filter by", columns)
#unique_values = sorted(df[selected_column].unique())
#
#selected_value = st.selectbox("Select value", unique_values)
#
#filtered_df = df[df[selected_column] == selected_value]

filtered_df = df[df["year"].between(filter_years[0], filter_years[1])]

#filtered_df = filtered_df.style.format({
#    'year': '{:.0f}'
#})

display_columns = ['track_name', 'track_artists', 'year', 'album_name', 'artist_genres', 'track_duration_ms']
display_df = filtered_df[display_columns].style.format({
    'year': '{:.0f}'
})

st.subheader("Filtered Tracks")
st.write(display_df)
#st.dataframe(
#    filtered_df,
#    use_container_width=True,
#)

