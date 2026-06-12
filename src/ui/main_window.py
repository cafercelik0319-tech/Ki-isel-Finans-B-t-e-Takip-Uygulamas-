import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class AnaEkran:
    def __init__(self, root):
        self.root = root
        self.root.title("Aile Bütçe Takip Sistemi")
        self.root.geometry("700x550")
        self.root.configure(bg="#2c3e50")

        # Veritabanı bağlantısı
        self.conn = sqlite3.connect("data/butce.db")
        self.cursor = self.conn.cursor()
        self.db_olustur()

        # Arayüz Elemanları
        self.create_widgets()
        self.verileri_yukle()

    def db_olustur(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uye TEXT,
                type TEXT,
                category TEXT,
                amount REAL,
                date TEXT
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        # Başlık
        title = tk.Label(self.root, text="👨‍👩‍👧‍👦 AİLE BÜTÇE TAKİP SİSTEMİ", fg="#f1c40f", bg="#2c3e50", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Giriş Alanları Çerçevesi
        frame = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
        frame.pack(pady=10, fill="x", padx=20)

        # Üye Seçimi
        tk.Label(frame, text="Aile Üyesi:", fg="white", bg="#34495e", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.uye_box = ttk.Combobox(frame, values=["Anne", "Baba", "Çocuk"], state="readonly", width=12)
        self.uye_box.grid(row=0, column=1, padx=5, pady=5)
        self.uye_box.set("Anne")

        # İşlem Tipi
        tk.Label(frame, text="İşlem Tipi:", fg="white", bg="#34495e", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
        self.tip_box = ttk.Combobox(frame, values=["Gelir", "Gider"], state="readonly", width=12)
        self.tip_box.grid(row=0, column=3, padx=5, pady=5)
        self.tip_box.set("Gelir")

        # Kategori
        tk.Label(frame, text="Kategori:", fg="white", bg="#34495e", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.kategori_entry = tk.Entry(frame, width=15)
        self.kategori_entry.grid(row=1, column=1, padx=5, pady=5)

        # Miktar
        tk.Label(frame, text="Miktar (TL):", fg="white", bg="#34495e", font=("Arial", 10, "bold")).grid(row=1, column=2, padx=5, pady=5)
        self.miktar_entry = tk.Entry(frame, width=15)
        self.miktar_entry.grid(row=1, column=3, padx=5, pady=5)

        # Tarih
        tk.Label(frame, text="Tarih:", fg="white", bg="#34495e", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5, pady=5)
        self.tarih_entry = tk.Entry(frame, width=12)
        self.tarih_entry.grid(row=0, column=5, padx=5, pady=5)
        self.tarih_entry.insert(0, "12.06.2026")

        # Butonlar Çerçevesi
        btn_frame = tk.Frame(self.root, bg="#2c3e50")
        btn_frame.pack(pady=5)

        # Kaydet Butonu
        self.kaydet_btn = tk.Button(btn_frame, text="➕ İşlem Ekle", command=self.islem_ekle, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"))
        self.kaydet_btn.grid(row=0, column=0, padx=10)

        # Grafik Butonu
        self.grafik_btn = tk.Button(btn_frame, text="📊 Grafiği Göster", command=self.grafik_goster, bg="#f1c40f", fg="black", font=("Arial", 10, "bold"))
        self.grafik_btn.grid(row=0, column=1, padx=10)

        # Filtreleme Alanı
        filter_frame = tk.Frame(self.root, bg="#2c3e50")
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Üyeye Göre Filtrele:", fg="white", bg="#2c3e50", font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.filtre_box = ttk.Combobox(filter_frame, values=["Hepsi", "Anne", "Baba", "Çocuk"], state="readonly", width=12)
        self.filtre_box.grid(row=0, column=1, padx=5)
        self.filtre_box.set("Hepsi")
        self.filtre_box.bind("<<ComboboxSelected>>", lambda e: self.verileri_yukle())

        # Tablo (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("id", "uye", "tip", "kategori", "miktar", "tarih"), show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("uye", text="Aile Üyesi")
        self.tree.heading("tip", text="Tip")
        self.tree.heading("kategori", text="Kategori")
        self.tree.heading("miktar", text="Miktar (TL)")
        self.tree.heading("tarih", text="Tarih")
       
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("uye", width=100, anchor="center")
        self.tree.column("tip", width=80, anchor="center")
        self.tree.column("kategori", width=120, anchor="center")
        self.tree.column("miktar", width=100, anchor="center")
        self.tree.column("tarih", width=100, anchor="center")
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

    def islem_ekle(self):
        uye = self.uye_box.get()
        tip = self.tip_box.get()
        kategori = self.kategori_entry.get().strip()
        miktar_str = self.miktar_entry.get().strip()
        tarih = self.tarih_entry.get().strip()

        if not kategori or not miktar_str:
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun!")
            return

        try:
            miktar = float(miktar_str)
        except ValueError:
            messagebox.showerror("Hata", "Miktar alanına sadece sayı girmelisiniz!")
            return

        self.cursor.execute("INSERT INTO transactions (uye, type, category, amount, date) VALUES (?, ?, ?, ?, ?)",
                            (uye, tip, kategori, miktar, tarih))
        self.conn.commit()
       
        self.kategori_entry.delete(0, tk.END)
        self.miktar_entry.delete(0, tk.END)
       
        messagebox.showinfo("Başarılı", "İşlem başarıyla eklendi!")
        self.verileri_yukle()

    def verileri_yukle(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        secilen_filtre = self.filtre_box.get()
        if secilen_filtre == "Hepsi":
            self.cursor.execute("SELECT * FROM transactions")
        else:
            self.cursor.execute("SELECT * FROM transactions WHERE uye=?", (secilen_filtre,))

        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def grafik_goster(self):
        grafik_penceresi = tk.Toplevel(self.root)
        grafik_penceresi.title("Gelir / Gider Dağılım Grafiği")
        grafik_penceresi.geometry("400x420")
        grafik_penceresi.configure(bg="#2c3e50")

        self.cursor.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
        veriler = self.cursor.fetchall()

        gelir = 0
        gider = 0
        for tip, miktar in veriler:
            if tip == "Gelir":
                gelir = miktar
            elif tip == "Gider":
                gider = miktar

        toplam = gelir + gider
        if toplam == 0:
            tk.Label(grafik_penceresi, text="Grafik için henüz veri yok!\nLütfen önce işlem ekleyin.", fg="white", bg="#2c3e50", font=("Arial", 12)).pack(expand=True)
            return

        gelir_yuzde = (gelir / toplam) * 100
        gider_yuzde = (gider / toplam) * 100

        tk.Label(grafik_penceresi, text="📊 BÜTÇE GÖRSEL ANALİZİ", fg="#f1c40f", bg="#2c3e50", font=("Arial", 14, "bold")).pack(pady=15)

        canvas = tk.Canvas(grafik_penceresi, width=300, height=220, bg="#34495e", highlightthickness=0)
        canvas.pack(pady=10)

        gelir_boy = int((gelir_yuzde / 100) * 160)
        canvas.create_rectangle(50, 190 - gelir_boy, 110, 190, fill="#2ecc71", outline="white")
        canvas.create_text(80, 205, text=f"Gelir\n%{int(gelir_yuzde)}", fill="white", font=("Arial", 10, "bold"))

        gider_boy = int((gider_yuzde / 100) * 160)
        canvas.create_rectangle(190, 190 - gider_boy, 250, 190, fill="#e74c3c", outline="white")
        canvas.create_text(220, 205, text=f"Gider\n%{int(gider_yuzde)}", fill="white", font=("Arial", 10, "bold"))

        durum_text = f"Toplam Gelir: {gelir} TL\nToplam Gider: {gider} TL"
        tk.Label(grafik_penceresi, text=durum_text, fg="white", bg="#2c3e50", font=("Arial", 11)).pack(pady=10)