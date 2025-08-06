# 🌎 FTTH Multitools

**FTTH Multitools** adalah aplikasi desktop berbasis Python yang dirancang untuk membantu analisis dan konversi data jaringan FTTH. Aplikasi ini mendukung file **CSV dan KML**, serta menyajikan tampilan data secara langsung dan interaktif.

<img width="821" height="651" alt="Screenshot 2025-08-05 170123" src="https://github.com/user-attachments/assets/54c8e0ca-95a7-48f8-9ced-6a091682db67" />


---

## ✨ Fitur Utama

- ✅ **Konversi CSV ke KML** secara otomatis
- 🗺️ **Preview Peta** langsung di browser
- 📊 **Hitung jumlah Placemark** dari file KML

---

## 📊 Metode Penghitungan Placemark

Ambil data placemark dengan metode copy folder yang berisi placemark dari Google Earth. 

---

## Virus Total
https://www.virustotal.com/gui/file/be8652648053445e12a5bc18b160efd33e1d2ff5c7503fe4f55ec02e193572ba/

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

