# Bike Sharing Analysis

Analisis data penggunaan layanan berbagi sepeda menggunakan Python dan Streamlit.

## 📌 Demo

Lihat aplikasi secara langsung di: [Bike Sharing Dashboard](https://echaan-bike-dashboard.streamlit.app/)

## 📂 Struktur Proyek

```
submission
├───dashboard
│   ├───main_data.csv
│   └───dashboard.py
├───data
│   ├───data_1.csv
│   └───data_2.csv
├───.gitignore
├───README.md
├───notebook.ipynb
├───requirements.txt
└───url.txt
```

## 🚀 Cara Menjalankan Aplikasi

### 1. Clone Repository
```bash
git clone https://github.com/echaan/bike-sharing-analysis.git
cd bike-sharing-analysis
```

### 2. Buat Virtual Environment (Opsional)
```bash
python -m venv venv
source venv/bin/activate  # Untuk macOS/Linux
venv\Scripts\activate     # Untuk Windows
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi Streamlit
```bash
streamlit run dashboard/dashboard.py
```

Aplikasi akan berjalan di `http://localhost:8501/`.

