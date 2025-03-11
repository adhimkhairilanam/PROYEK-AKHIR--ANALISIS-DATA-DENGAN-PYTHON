import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df_day = pd.read_csv("Dashboard\df_day.csv")
df_hour = pd.read_csv("Dashboard\df_hour.csv")

# Mapping kategori musim
kategori_musim = {
    1: "Sangat Sedikit Pengguna",
    2: "Banyak Pengguna",
    3: "Sangat Banyak Pengguna",
    4: "Sedikit Pengguna"
}
df_day["Kategori Musim"] = df_day["season"].map(kategori_musim)

# Binning jumlah peminjam
bin_peminjam = [0, 2000, 4000, df_day["cnt"].max()]
kategori_peminjam = ["Rendah", "Menengah", "Tinggi"]
df_day["Kategori Peminjam"] = pd.cut(df_day["cnt"], bins=bin_peminjam, labels=kategori_peminjam)

# Binning suhu
temp_bins = [0, 0.3, 0.6, df_day["temp"].max()]
kategori_suhu = ["Dingin", "Sedang", "Panas"]
df_day["Kategori Suhu"] = pd.cut(df_day["temp"], bins=temp_bins, labels=kategori_suhu)

# Sidebar konfigurasi
with st.sidebar:
    st.image("Dashboard/logo.png", width=300)
    st.title("DBS Bike Sharing Dashboard")
    menu = st.selectbox("Pilih Data untuk Ditampilkan", [
        "Clustering", "Perbandingan Peminjam", "Pola Penggunaan Sepeda", 
        "Pengaruh Cuaca per Hari", "Hubungan Musim dan Cuaca"
    ])

# Tampilan berdasarkan menu
if menu == "Clustering":
    musim_terpilih = st.sidebar.selectbox("Pilih Kategori Musim", df_day["Kategori Musim"].unique())
    suhu_terpilih = st.sidebar.selectbox("Pilih Kategori Suhu", df_day["Kategori Suhu"].unique())
    
    df_filtered = df_day[(df_day["Kategori Musim"] == musim_terpilih) & (df_day["Kategori Suhu"] == suhu_terpilih)]
    
    st.subheader("Tren Peminjaman Sepeda Harian")
    st.line_chart(df_day.set_index("dteday")["cnt"])
    
    st.subheader("Data Peminjaman Sepeda")
    st.write(df_filtered[["dteday", "Kategori Musim", "Kategori Suhu", "Kategori Peminjam", "cnt"]])
    
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    sns.countplot(x=df_day["Kategori Peminjam"], ax=ax[0], palette="coolwarm")
    ax[0].set_title("Distribusi Kategori Peminjaman")
    sns.countplot(x=df_day["Kategori Suhu"], ax=ax[1], palette="coolwarm")
    ax[1].set_title("Distribusi Kategori Suhu")
    st.pyplot(fig)

elif menu == "Perbandingan Peminjam":
    st.subheader("Perbandingan Pengguna Terdaftar dan Kasual")
    total_pengguna = df_day[['casual', 'registered']].sum()
    rata_pengguna = df_day[['casual', 'registered']].mean()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.barplot(x=total_pengguna.index, y=total_pengguna, palette='viridis', ax=axes[0])
    axes[0].set_title('Total Pengguna')
    sns.barplot(x=rata_pengguna.index, y=rata_pengguna, palette='viridis', ax=axes[1])
    axes[1].set_title('Rata-rata Pengguna')
    st.pyplot(fig)

elif menu == "Pola Penggunaan Sepeda":
    st.subheader("Pola Penggunaan Sepeda Per Jam")
    pola_jam = df_hour.groupby("hr")["cnt"].mean()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=pola_jam.index, y=pola_jam.values, marker="o", linewidth=2.5, color="blue")
    plt.title("Jumlah Peminjam Berdasarkan Jam")
    st.pyplot(plt)

elif menu == "Pengaruh Cuaca per Hari":
    st.subheader("Pengaruh Cuaca terhadap Peminjaman Sepeda")
    df_cuaca = df_day.groupby("cuaca").agg({'cnt': 'mean'}).reset_index()
    plt.figure(figsize=(9, 9))
    plt.pie(df_cuaca['cnt'], labels=df_cuaca['cuaca'], autopct='%1.1f%%', colors=sns.color_palette("viridis", len(df_cuaca)))
    plt.title("Distribusi Pengguna Berdasarkan Cuaca")
    st.pyplot(plt)

elif menu == "Hubungan Musim dan Cuaca":
    st.subheader("Hubungan Musim dan Cuaca dengan Peminjaman Sepeda")
    df_musim = df_day.groupby("Kategori Musim").agg({'cnt': 'sum'}).reset_index()
    plt.figure(figsize=(9, 9))
    plt.pie(df_musim['cnt'], labels=df_musim['Kategori Musim'], autopct='%1.1f%%', colors=sns.color_palette("viridis", len(df_musim)))
    plt.title("Distribusi Peminjaman Berdasarkan Musim")
    st.pyplot(plt)

    df_korelasi = df_day.groupby(["Kategori Musim", "cuaca"]).agg({'cnt': 'sum'}).reset_index()
    pivot_korelasi = df_korelasi.pivot(index='Kategori Musim', columns='cuaca', values='cnt')
    plt.figure(figsize=(9, 9))
    sns.heatmap(pivot_korelasi, annot=True, cmap='coolwarm', fmt='.0f')
    plt.title("Hubungan Musim dan Cuaca terhadap Jumlah Pengguna")
    st.pyplot(plt)
    
st.caption("Adhim Khairil Anam")
