# Ringkasan Evaluasi Machine Learning: Sistem Rekomendasi Musik berdasarkan Mood & Genre

Dokumen ini berisi catatan mengenai model *Machine Learning* yang digunakan, pemilihan model terbaik, parameter yang diterapkan, serta metrik evaluasi untuk tugas *Data Mining* atau *Machine Learning* pada project ini.

---

## 1. Daftar Model yang Digunakan
Sistem ini membandingkan 3 model klasifikasi standar untuk data tabular:
1. **Logistic Regression**
2. **Random Forest Classifier**
3. **Support Vector Classifier (SVC)**

Sistem mengadopsi pendekatan **Hybrid**, yaitu menggabungkan **Audio Features** (seperti *danceability, energy, valence*) dan **Text Features** (pemrosesan bahasa alami dari kolom *artist_genres*).

---

## 2. Model Terbaik: Logistic Regression
Berdasarkan hasil eksperimen (*training* dan *testing* pada dataset gabungan sebesar 427 lagu), **Logistic Regression** terpilih sebagai model yang terbaik untuk project ini.

**Justifikasi Pemilihan:**
- Menghasilkan tingkat akurasi tertinggi di antara ketiga model, yaitu mencapai **~91.8%**.
- Algoritmanya sederhana dan stabil. Karena dataset yang dimiliki ukurannya relatif kecil (ratusan baris), model linier seperti Logistic Regression jauh lebih aman dari risiko *overfitting* (menghafal data) dibandingkan model rumit seperti SVC.
- Kecepatan komputasi (waktu *training* dan *predict*) sangat efisien.

---

## 3. Parameter Pengaturan Terbaik
Berikut adalah pengaturan parameter (hyperparameters) yang diterapkan pada *Pipeline* untuk menghasilkan performa maksimal:

### Pada Preprocessor (Ekstraksi Fitur Hybrid)
* **`TfidfVectorizer(max_features=100)`**: Saat memproses teks dari nama genre artis (*artist_genres*), program dibatasi hanya mempelajari 100 kosakata genre yang paling penting dan paling sering muncul. Ini sangat menolong dalam merampingkan proses komputasi serta membuang nama genre yang "nyeleneh" (outlier).
* **`StandardScaler()`**: Digunakan untuk mengubah seluruh *Spotify Audio Features* (yang awalnya memiliki rentang skala berbeda-beda seperti *tempo* yang ratusan dan *valence* yang desimal) agar menjadi skala matematis yang seragam.

### Pada Model Terbaik (Logistic Regression)
* **`random_state=42`**: Mengunci sifat pengacakan algoritma agar hasil model konsisten setiap kali *notebook* dijalankan ulang.
* **`max_iter=1000`**: Meningkatkan batas batas iterasi pembelajaran algoritma menjadi 1000 siklus, guna memastikan algoritma mencapai konvergensi (titik paling akurat).
* **`penalty='l2'`** *(bawaan)*: Menerapkan penalti matematis pada bobot (*Ridge Regularization*) yang berguna mencegah model memihak pada satu fitur secara berlebihan.

---

## 4. Metrik Evaluasi yang Digunakan
Untuk membenarkan (menjustifikasi) kehebatan model, project ini menggunakan beberapa metrik evaluasi standar industri:

1. **Accuracy (Akurasi ~91.8%):** 
   Metrik dasar yang mengukur persentase tebakan Mood yang benar dari keseluruhan total lagu yang diuji.
2. **Classification Report (Precision, Recall, F1-Score):**
   Metrik ini membuktikan seberapa seimbang tebakan model untuk setiap Mood (Happy, Sad, Energetic, Chill). F1-Score yang tinggi membuktikan bahwa model tidak sekadar asal menebak satu Mood saja.
   *(Catatan: Terdapat nilai recall yang rendah atau 0 pada kategori "Chill" karena fenomena **Class Imbalance**, di mana dari 400+ total data hanya terdapat 18 lagu Chill).*
3. **Confusion Matrix (Heatmap):**
   Digunakan untuk melihat pola kesalahan model secara detail. Membuktikan secara visual (*heat map*) bahwa sebagian besar lagu berhasil ditebak dengan benar (terkumpul di sepanjang garis diagonal dari kiri atas ke kanan bawah matriks).
