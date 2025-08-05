# FTTH Multitools

**FTTH Multitools** adalah aplikasi desktop berbasis Python yang dirancang untuk membantu analisis dan konversi data jaringan FTTH. Aplikasi ini mendukung file **CSV dan KML**, serta menyajikan tampilan data secara langsung dan interaktif.

<img width="849" height="662" alt="Screenshot 2025-08-05 164805" src="https://github.com/user-attachments/assets/aba012ac-80d6-4e59-9db1-9607b2490d5e" />

---

## ✨ Fitur Utama

- ✅ **Konversi CSV ke KML** secara otomatis
- 🗺️ **Preview Peta** langsung di browser
- 📊 **Hitung jumlah Placemark** dari file KML

---

## 📊 Metode Penghitungan Placemark

Ambil data placemark dengan metode copy folder yang berisi placemark dari Google Earth. 

---

## 📁 Format CSV yang Didukung

File CSV harus memiliki minimal kolom:
- `latitude` (atau `Latitude`)
- `longitude` (atau `Longitude`)

Kolom tambahan seperti `name`, `description` akan otomatis digunakan jika tersedia.

```csv
name,latitude,longitude,description
Kantor A,-7.12345,110.12345,Deskripsi lokasi A
Kantor B,-7.54321,110.54321,Deskripsi lokasi B


