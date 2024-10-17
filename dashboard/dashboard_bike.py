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

# Pertanyaan 1: Pengaruh suhu dan kelembapan terhadap jumlah pengguna sepeda
st.subheader(f"Pengaruh Suhu dan Kelembapan terhadap Pengguna Sepeda pada Bulan {selected_month} dan Jam {selected_hour}")
if not filtered_df.empty:
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='suhu', y='total_pengguna', hue='kelembaban', data=filtered_df, ax=ax1, palette='coolwarm')
    ax1.set_title('Pengaruh Suhu dan Kelembaban terhadap Jumlah Pengguna Sepeda')
    ax1.set_xlabel('Suhu')
    ax1.set_ylabel('Total Pengguna Sepeda')
    st.pyplot(fig1)
else:
    st.write(f"Tidak ada data untuk Bulan {selected_month} dan Jam {selected_hour}.")

# Pertanyaan 2: Perbedaan jumlah pengguna sepeda pada hari kerja dan hari libur/akhir pekan
st.subheader("Perbandingan Jumlah Pengguna Sepeda: Hari Kerja vs Hari Libur/Akhir Pekan")
if not hour_df.empty:
    working_day_df = hour_df.groupby('hari_bekerja')['total_pengguna'].mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='hari_bekerja', y='total_pengguna', data=working_day_df, ax=ax2, palette='viridis')
    ax2.set_title('Perbandingan Jumlah Pengguna Sepeda antara Hari Kerja dan Hari Libur/Akhir Pekan')
    ax2.set_xlabel('Hari Bekerja (1 = Hari Kerja, 0 = Libur/Akhir Pekan)')
    ax2.set_ylabel('Rata-rata Total Pengguna Sepeda')
    st.pyplot(fig2)
else:
    st.write("Tidak ada data yang tersedia untuk hari kerja vs hari libur/akhir pekan.")