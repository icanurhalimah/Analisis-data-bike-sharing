import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets directly
@st.cache_data
def load_data():
    day_data = pd.read_csv('day.csv', parse_dates=['dteday'])
    hour_data = pd.read_csv('hour.csv', parse_dates=['dteday'])
    return day_data, hour_data

day_data, hour_data = load_data()

# Sidebar filtering options
st.sidebar.header("Filter Options")
filter_season = st.sidebar.multiselect(
    "Select Seasons:", options=[1, 2, 3, 4], default=[1, 2, 3, 4],
    format_func=lambda x: {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}[x]
)

filter_weather = st.sidebar.multiselect(
    "Select Weather Situations:", options=[1, 2, 3, 4], default=[1, 2, 3, 4],
    format_func=lambda x: {
        1: 'Clear/Partly Cloudy',
        2: 'Mist/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Snow'
    }[x]
)

filter_date_range = st.sidebar.date_input(
    "Select Date Range:", 
    [hour_data['dteday'].min(), hour_data['dteday'].max()],
    min_value=hour_data['dteday'].min(), 
    max_value=hour_data['dteday'].max()
)

# Apply filters
hour_filtered = hour_data[
    (hour_data['season'].isin(filter_season)) &
    (hour_data['weathersit'].isin(filter_weather)) &
    (hour_data['dteday'].between(pd.to_datetime(filter_date_range[0]), pd.to_datetime(filter_date_range[1])))
]

# Title and description
st.title('Analisis Data Penyewaan Sepeda')
st.write("\nDashboard ini menampilkan analisis data penyewaan sepeda berdasarkan dataset Bike Sharing.")

# Data overview
st.header("Data Overview")
st.write("### Data Preview")
st.dataframe(hour_filtered.head())
st.write("### Statistik Deskriptif")
st.write(hour_filtered.describe())

# Visualisasi 1: Penyewaan Sepeda per Bulan
st.header("Rata-rata Penyewaan Sepeda per Bulan")
data_agg = hour_filtered.groupby(['yr', 'mnth']).agg({'casual': 'mean', 'registered': 'mean', 'cnt': 'mean'}).reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=data_agg, x='mnth', y='cnt', hue='yr', marker='o', ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan (Rata-rata)')
ax.legend(title='Tahun', labels=['2011', '2012'])
st.pyplot(fig)

# Visualisasi 2: Top 20 Hari dengan Penyewaan Tertinggi
st.header("Top 20 Hari dengan Penyewaan Sepeda Tertinggi")
df_grouped = hour_filtered.groupby(['yr', 'dteday'])[['cnt', 'casual', 'registered']].sum().reset_index()
df_combined = pd.concat([
    df_grouped[df_grouped['yr'] == 0].sort_values(by='cnt', ascending=False).head(20),
    df_grouped[df_grouped['yr'] == 1].sort_values(by='cnt', ascending=False).head(20)
])
fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(data=df_combined, x='dteday', y='cnt', hue='yr', dodge=True, ax=ax)
ax.set_title('Top 20 Hari dengan Jumlah Penyewaan Sepeda Tertinggi di Setiap Tahun')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Jumlah Penyewaan (Total)')
ax.legend(title='Tahun', labels=['2011', '2012'])
st.pyplot(fig)

# Visualisasi 3: Penyewaan Sepeda per Jam
st.header("Rata-rata Penyewaan Sepeda per Jam")
data_hourly = hour_filtered.groupby(['yr', 'hr']).agg({'casual': 'mean', 'registered': 'mean', 'cnt': 'mean'}).reset_index()
fig, ax = plt.subplots(figsize=(14, 7))
sns.lineplot(data=data_hourly, x='hr', y='cnt', hue='yr', marker='o', ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda per Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan (Rata-rata)')
ax.legend(title='Tahun', labels=['2011', '2012'])
st.pyplot(fig)

# Visualisasi 4: Penyewaan Sepeda per Musim
st.header("Rata-rata Penyewaan Sepeda per Musim")
data_seasonal = hour_filtered.groupby(['yr', 'season']).agg({'casual': 'mean', 'registered': 'mean', 'cnt': 'mean'}).reset_index()
data_seasonal['season_label'] = data_seasonal['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=data_seasonal, x='season_label', y='cnt', hue='yr', dodge=True, ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda per Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Penyewaan (Rata-rata)')
ax.legend(title='Tahun', labels=['2011', '2012'])
st.pyplot(fig)

# Visualisasi 5: Korelasi Antar Variabel
st.header("Korelasi Antar Variabel")
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(hour_filtered.corr(numeric_only=True), annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Heatmap Korelasi Antar Variabel')
st.pyplot(fig)

# Kesimpulan
st.header("Kesimpulan")
st.write("""
**Faktor yang Mempengaruhi Penyewaan Sepeda:**
1. Keadaan lingkungan seperti badai dan acara besar.
2. Jam kerja (pagi, siang, sore).
3. Suhu udara (semakin tinggi, semakin banyak penyewaan).
4. Musim (penyewaan lebih sedikit pada musim semi).

**Strategi untuk Meningkatkan Penyewaan:**
- Mengadakan promo musiman.
- Mengoptimalkan ketersediaan sepeda selama jam sibuk.
- Menyediakan paket langganan untuk pengguna casual.
- Strategi penempatan sepeda di lokasi strategis.
""")
