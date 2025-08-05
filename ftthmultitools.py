import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd
import simplekml
import folium
import tempfile
import webbrowser
import sys
import os
import re

# ---------- Fungsi umum ----------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Folder script aktif

    return os.path.join(base_path, relative_path)

# ---------- Popup Author Sebelum GUI ----------
def show_author_popup():
    info = (
        "📌 Aplikasi: FTTH Multitools\n"
        "🧾 Versi: 2.0\n"
        "👨‍💻 Author: Galih Prima Aditya Firdaus\n"
        "✉️ Email: galprim48@gmail.com\n"
    )
    root = tk.Tk()
    root.withdraw()  # Sembunyikan sementara
    messagebox.showinfo("Tentang Aplikasi", info)
    root.destroy()

# ---------- Aplikasi Utama ----------
class FTTHMultitoolsApp:
    def center_window(self, width=750, height=550):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}") 

    def __init__(self, root):
        self.root = root
        self.root.title("FTTH Multitools")
        self.root.iconbitmap(resource_path("icon.ico"))
        self.root.geometry("800x600")
        self.root.configure(bg="#2E2E2E")
        self.center_window(800, 600)
        icon_path = resource_path("icon.ico")

        # Tab controlpy
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1: CSV to KML
        self.tab_csv = tk.Frame(self.notebook, bg="#2E2E2E")
        self.notebook.add(self.tab_csv, text="CSV to KML")
        self.setup_csv_tab()

        # Tab 2: Placemark Counter
        self.tab_kml = tk.Frame(self.notebook, bg="#2E2E2E")
        self.notebook.add(self.tab_kml, text="Hitung Placemark")
        self.setup_kml_tab()

        # Footer
        self.footer_label = tk.Label(
            root,
            text="FTTH Multitools v2.0 | Author: Galih Prima Aditya Firdaus",
            anchor="w",
            fg="#AAAAAA",
            bg="#2E2E2E",
            font=("Arial", 8)
        )
        self.footer_label.pack(side=tk.BOTTOM, pady=5)

    # ---------------- Tab CSV to KML ----------------
    def setup_csv_tab(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#3A3A3A", foreground="white", fieldbackground="#3A3A3A")
        style.configure("Treeview.Heading", background="#555555", foreground="white")

        self.drop_label = tk.Label(self.tab_csv, text="📂 Drag & Drop file CSV", width=80, height=4,
                                   bg="#3E3E3E", fg="white")
        self.drop_label.pack(pady=12)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop)
        self.drop_label.bind("<Button-1>", self.browse_file)

        self.tree = ttk.Treeview(self.tab_csv)
        self.tree.pack(padx=10, pady=(0, 10), expand=True, fill=tk.BOTH)

        self.count_label = tk.Label(self.tab_csv, text="Jumlah data: 0", fg="white", bg="#2E2E2E", font=("Arial", 10, "bold"))
        self.count_label.pack(pady=(0, 5))

        btn_style = {"bg": "#4B4B4B", "fg": "white", "activebackground": "#5E5E5E", "activeforeground": "white"}
        self.save_button = tk.Button(self.tab_csv, text="💾 Convert & Save KML", command=self.convert_and_save, state=tk.DISABLED, **btn_style)
        self.save_button.pack(pady=(0, 6), ipadx=10, ipady=2)

        self.preview_button = tk.Button(self.tab_csv, text="🗺️ Preview Peta", command=self.preview_map, state=tk.DISABLED, **btn_style)
        self.preview_button.pack(pady=(0, 6), ipadx=10, ipady=2)

        self.clear_button = tk.Button(self.tab_csv, text="🧹 Clear Data", command=self.clear_data, **btn_style)
        self.clear_button.pack(pady=(0, 15), ipadx=10, ipady=2)

        self.csv_file_path = None
        self.df = None
      
    def browse_file(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.load_csv(file_path)

    def on_drop(self, event):
        file_path = event.data.strip('{}')
        if file_path.lower().endswith(".csv"):
            self.load_csv(file_path)
        else:
            messagebox.showerror("Error", "File yang didrop bukan CSV.")

    def load_csv(self, file_path):
        try:
            df = pd.read_csv(file_path, sep=None, engine='python')
            self.csv_file_path = file_path
            self.df = df

            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(df.columns)
            self.tree["show"] = "headings"

            for col in df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor="w")

            for _, row in df.iterrows():
                self.tree.insert("", tk.END, values=list(row))
            self.save_button.config(state=tk.NORMAL)
            self.preview_button.config(state=tk.NORMAL)

            self.count_label.config(text=f"Jumlah data: {len(df)}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca CSV: {e}")

    def convert_and_save(self):
        try:
            if self.df is None:
                raise ValueError("Data tidak tersedia.")

            col_lower = [c.lower() for c in self.df.columns]
            if "latitude" not in col_lower or "longitude" not in col_lower:
                raise ValueError("CSV harus memiliki kolom 'latitude' dan 'longitude'.")

            lat_col = self.df.columns[col_lower.index("latitude")]
            lon_col = self.df.columns[col_lower.index("longitude")]

            kml = simplekml.Kml()
            for _, row in self.df.iterrows():
                try:
                    lat = float(row[lat_col])
                    lon = float(row[lon_col])
                    name = str(row.get("name", ""))
                    kml.newpoint(name=name, coords=[(lon, lat)])
                except:
                    continue

            save_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
            if save_path:
                kml.save(save_path)
                messagebox.showinfo("Berhasil", f"File KML disimpan di:\n{save_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Konversi gagal: {e}")

    def preview_map(self):
        try:
            if self.df is None:
                raise ValueError("Data tidak tersedia.")

            col_lower = [c.lower() for c in self.df.columns]
            if "latitude" not in col_lower or "longitude" not in col_lower:
                raise ValueError("CSV harus memiliki kolom 'latitude' dan 'longitude'.")

            lat_col = self.df.columns[col_lower.index("latitude")]
            lon_col = self.df.columns[col_lower.index("longitude")]

            center_lat = self.df[lat_col].astype(float).mean()
            center_lon = self.df[lon_col].astype(float).mean()

            m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

            for _, row in self.df.iterrows():
                try:
                    lat = float(row[lat_col])
                    lon = float(row[lon_col])
                    name = str(row.get("name", ""))
                    folium.Marker(location=[lat, lon], popup=name).add_to(m)
                except:
                    continue

            temp_map_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
            m.save(temp_map_file.name)
            webbrowser.open(f"file://{temp_map_file.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat peta: {e}")

    def clear_data(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()
        self.df = None
        self.csv_file_path = None
        self.count_label.config(text="Jumlah data: 0")
        self.save_button.config(state=tk.DISABLED)
        self.preview_button.config(state=tk.DISABLED)

    # ---------------- Tab Hitung Placemark ----------------
    def setup_kml_tab(self):
        instruksi = tk.Label(
            self.tab_kml,
            text="Paste isi file KML di sini:",
            font=("Arial", 12, "bold"),
            bg="#2E2E2E",
            fg="white"
        )
        instruksi.pack(pady=10)

        frame_text = tk.Frame(self.tab_kml, bg="#2E2E2E")
        frame_text.pack(padx=10, pady=5, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_text)
        scrollbar.pack(side="right", fill="y")

        self.textbox = tk.Text(
            frame_text,
            wrap="word",
            yscrollcommand=scrollbar.set,
            height=20,
            bg="#2E2E2E",
            fg="white",
            insertbackground="white"
        )
        self.textbox.pack(side="left", fill="both", expand=True)
        self.textbox.bind("<KeyRelease>", self.hitung_coordinates)

        scrollbar.config(command=self.textbox.yview)

        self.label_kml_hasil = tk.Label(
            self.tab_kml, text="Jumlah Placemark : -",
            font=("Arial", 11, "bold"), bg="#2E2E2E", fg="white"
        )
        self.label_kml_hasil.pack(pady=5)

        self.clear_kml_btn = tk.Button(
            self.tab_kml, text="🧹 Clear Data", command=self.clear_kml_text,
            bg="#4B4B4B", fg="white", activebackground="#5E5E5E", activeforeground="white"
        )
        self.clear_kml_btn.pack(pady=10, ipadx=10, ipady=2)

    def hitung_coordinates(self, event=None):
        text = self.textbox.get("1.0", tk.END)
        if not text.strip():
            self.label_kml_hasil.config(text="Jumlah Placemark : -")
            return

        try:
            coordinates = re.findall(r"<coordinates>.*?</coordinates>", text, re.DOTALL | re.IGNORECASE)
            jumlah = len(coordinates)
            self.label_kml_hasil.config(text=f"Jumlah Placemark : {jumlah}")
        except Exception as e:
            self.label_kml_hasil.config(text=f"Error parsing: {e}")

    def clear_kml_text(self):
        self.textbox.delete("1.0", tk.END)
        self.label_kml_hasil.config(text="Jumlah Placemark : -")

# ---------- Main ----------
if __name__ == "__main__":
    # Root sementara untuk popup
    popup_root = tk.Tk()
    popup_root.withdraw()  # Tidak menampilkan jendela kosong
    messagebox.showinfo(
        "Tentang Aplikasi",
        "📌 Aplikasi: FTTH Multitools\n"
        "🧾 Versi: 2.0\n"
        "👨‍💻 Author: Galih Prima Aditya Firdaus\n"
        "✉️ Email: galprim48@gmail.com\n",
        parent=popup_root
    )
    popup_root.destroy()  # Tutup root popup

    # Buat root utama setelah popup ditutup
    root = TkinterDnD.Tk()
    root.withdraw()
    app = FTTHMultitoolsApp(root)
    root.deiconify()
    root.mainloop()
