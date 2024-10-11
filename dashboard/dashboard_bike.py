import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set style untuk seaborn
st.set_page_config(page_title="Analisis Data Penggunaan Sepeda", layout="wide", initial_sidebar_state="expanded")

# Membaca data dari CSV
hour_df = pd.read_csv("Bike-sharing-dataset/hour.csv")

# Menghapus kolom yang tidak diperlukan
drop_cols = ['instant', 'dteday', 'windspeed']
hour_df.drop(labels=drop_cols, axis=1, inplace=True)

# Mengubah nama judul kolom
hour_df.rename(columns={
    'season': 'musim',
    'yr': 'tahun',
    'mnth': 'bulan',
    'hr': 'jam',
    'holiday': 'hari_libur',
    'weekday': 'hari_kerja',
    'workingday': 'hari_bekerja',
    'weathersit': 'kondisi_cuaca',
    'temp': 'suhu',
    'atemp': 'suhu_terasa',
    'hum': 'kelembaban',
    'casual': 'pengguna_casual',
    'registered': 'pengguna_terdaftar',
    'cnt': 'total_pengguna'
}, inplace=True)

# Mengubah angka menjadi keterangan
hour_df['bulan'] = hour_df['bulan'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
hour_df['musim'] = hour_df['musim'].map({
    1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'
})
hour_df['hari_kerja'] = hour_df['hari_kerja'].map({
    0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
})
hour_df['kondisi_cuaca'] = hour_df['kondisi_cuaca'].map({
    1: 'Cerah/Agak Berawan',
    2: 'Berkabut/Berawan',
    3: 'Salju/Rintik Hujan',
    4: 'Cuaca Ekstrem'
})

# Komponen sidebar untuk filter
st.sidebar.header("Filter Data")
selected_month = st.sidebar.selectbox("Pilih Bulan", hour_df['bulan'].unique())
selected_hour = st.sidebar.slider("Pilih Jam", min_value=0, max_value=23, value=12)

# Filter data berdasarkan pilihan user
filtered_df = hour_df[(hour_df['bulan'] == selected_month) & (hour_df['jam'] == selected_hour)]

# Tampilan data yang difilter
st.write("Data yang difilter:")
st.dataframe(filtered_df)

# Membuat plot
st.subheader(f"Distribusi Pengguna Sepeda pada Bulan {selected_month} dan Jam {selected_hour}")
fig, ax = plt.subplots()
sns.histplot(filtered_df['total_pengguna'], bins=20, ax=ax)
ax.set_title('Distribusi Jumlah Pengguna Sepeda')
st.pyplot(fig)
