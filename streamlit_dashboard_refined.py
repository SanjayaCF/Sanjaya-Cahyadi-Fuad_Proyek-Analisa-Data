import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv('Dataset/day.csv')
    return df

data = load_data()

weather_mapping = {
    1: 'Cerah/Berawan Sedikit',
    2: 'Berawan/Berkabut',
    3: 'Hujan/Hujan Salju Ringan',
    4: 'Hujan Lebat/Hujan Es'
}

data['kondisi_cuaca'] = data['weathersit'].map(weather_mapping)

st.markdown('''            
**Nama:** Sanjaya Cahyadi Fuad<br>\n
**Email:** m239b4ky4066@bangkit.academy<br>\n
**ID Dicoding:** sanjayacf<br>
''')

st.title('Dashboard Interaktif Data Penyewaan Sepeda')

st.markdown('''            
## Pengenalan
Dashboard ini memberikan analisa data penyewaan sepeda berdasarkan rentang waktu. Anda dapat mencoba bereksperimen dengan tanggal 
guna memahami bagaimana berbagai faktor seperti kondisi cuaca, musim, dan hari kerja memengaruhi pola penyewaan sepeda. 
''')

st.subheader('Gambaran Umum Dataset')
st.write(data.head())

st.sidebar.header('Filter Tanggal')

if 'dteday' in data.columns:
    data['dteday'] = pd.to_datetime(data['dteday']) 
    date_range = st.sidebar.date_input('Pilih Rentang Tanggal', 
                                       [data['dteday'].min(), data['dteday'].max()])
    data = data[(data['dteday'] >= pd.to_datetime(date_range[0])) & 
                (data['dteday'] <= pd.to_datetime(date_range[1]))]

st.write(f"Data yang Difilter (menampilkan {len(data)} baris):")
st.write(data)

st.subheader('Visualisasi')

st.markdown('### Distribusi Penyewaan Berdasarkan Musim')
plt.figure(figsize=(8, 6))
sns.countplot(x='season', data=data, palette='coolwarm')
plt.title('Distribusi Penyewaan Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(plt)

st.markdown('### Penyewaan Berdasarkan Hari Kerja dan Akhir Pekan')
plt.figure(figsize=(8, 6))
sns.countplot(x='workingday', data=data, palette='Blues')
plt.title('Penyewaan Berdasarkan Hari Kerja dan Akhir Pekan')
plt.xlabel('Hari Kerja (1 = Ya, 0 = Tidak)')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(plt)

st.markdown('### Pengaruh Cuaca Terhadap Penyewaan')
plt.figure(figsize=(8, 6))
sns.scatterplot(x='kondisi_cuaca', y='cnt', data=data)
plt.title('Pengaruh Cuaca Terhadap Penyewaan')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Jumlah Penyewaan')
st.pyplot(plt)

st.markdown('### Penyewaan Sepeda Berdasarkan Suhu dan Kelembaban')
plt.figure(figsize=(8, 6))
sns.heatmap(data[['temp', 'hum', 'cnt']].corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Korelasi Penyewaan dengan Suhu dan Kelembaban')
st.pyplot(plt)

st.subheader('Kesimpulan')
if len(data) > 0:
    total_rentals = data['cnt'].sum()
    avg_temp = data['temp'].mean()
    avg_humidity = data['hum'].mean()
    
    st.write(f'''
    - **Total Penyewaan dari {date_range[0]} hingga {date_range[1]}**: {total_rentals} total sepeda
    - **Rata-rata Suhu**: {avg_temp:.2f}
    - **Rata-rata Kelembaban**: {avg_humidity:.2f}
    
    Berdasarkan analisis di atas, Anda dapat menarik kesimpulan bahwa:
    - **Musim**: Musim tertentu memiliki pengaruh yang signifikan terhadap jumlah penyewaan.
    - **Hari Kerja**: Hari kerja cenderung memiliki lebih banyak penyewaan dibandingkan akhir pekan.
    - **Cuaca**: Terdapat pengaruh antara kondisi cuaca dan jumlah penyewaan, yang menunjukkan pola perilaku penyewaan sepeda.
    - **Korelasi Suhu dan Kelembaban**: Ada hubungan antara suhu dan kelembaban dengan jumlah penyewaan, yang dapat membantu dalam analisis lebih lanjut.
    ''')
else:
    st.write("Tidak ada data yang memenuhi rentang waktu yang dipilih.")
