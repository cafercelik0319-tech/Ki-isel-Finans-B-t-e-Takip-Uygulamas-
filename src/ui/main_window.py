import tkinter as tk
from tkinter import ttk, messagebox
from models.transaction import Gelir, Gider
from services.db_manager import DBManager

class AnaEkran:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Kişisel Finans ve Bütçe Takip Uygulaması")
        self.pencere.geometry("600x850")
        self.db = DBManager()
        self.arayuz_hazirla()

    def arayuz_hazirla(self):
        # --- ÜST BAŞLIK ---
        tk.Label(self.pencere, text="👨‍👩‍👧‍👦 Kişisel Finans ve Bütçe Takip Uygulaması", font=("Helvetica", 18, "bold"), fg="#2c3e50", pady=15).pack()
        
        # Giriş Alanları
        tk.Label(self.pencere, text="Miktar:", font=("Arial", 9, "bold")).pack()
        self.ent_miktar = tk.Entry(self.pencere, justify="center", font=("Arial", 11))
        self.ent_miktar.pack(pady=3, ipady=3)
        
        tk.Label(self.pencere, text="Kategori (Örn: Market, Fatura):", font=("Arial", 9, "bold")).pack()
        self.ent_kategori = tk.Entry(self.pencere, justify="center", font=("Arial", 11))
        self.ent_kategori.pack(pady=3, ipady=3)
        
        tk.Label(self.pencere, text="İşlemi Yapan Üye:", font=("Arial", 9, "bold")).pack()
        self.combo_uye = ttk.Combobox(self.pencere, values=["ERKEK EŞ", "KADIN EŞ", "ÇOCUK"], state="readonly", font=("Arial", 10))
        self.combo_uye.set("SEÇİNİZ"); self.combo_uye.pack(pady=3)

        tk.Label(self.pencere, text="İşlem Tipi:", font=("Arial", 9, "bold")).pack()
        self.combo_tip = ttk.Combobox(self.pencere, values=["Gelir", "Gider"], state="readonly", font=("Arial", 10))
        self.combo_tip.set("Gider"); self.combo_tip.pack(pady=3)

        # Butonlar
        tk.Button(self.pencere, text="➕ İŞLEMİ KAYDET", command=self.kaydet_click, bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=25).pack(pady=10)
        tk.Button(self.pencere, text="🗑️ SEÇİLİ SATIRI SİL", command=self.sil_click, bg="#e67e22", fg="white", font=("Arial", 10, "bold"), width=25).pack(pady=5)

        # --- FİLTRELEME ALANI ---
        tk.Frame(self.pencere, height=2, bg="#bdc3c7").pack(fill="x", padx=30, pady=10)
        filter_frame = tk.Frame(self.pencere)
        filter_frame.pack(pady=5)
        
        tk.Label(filter_frame, text="🔍 Üyeye Göre Filtrele: ", font=("Arial", 10, "bold")).pack(side="left")
        self.combo_filtre = ttk.Combobox(filter_frame, values=["Hepsi", "ERKEK EŞ", "KADIN EŞ", "ÇOCUK"], state="readonly", width=12)
        self.combo_filtre.set("Hepsi")
        self.combo_filtre.pack(side="left", padx=5)
        self.combo_filtre.bind("<<ComboboxSelected>>", lambda e: self.tabloyu_guncelle())

        # Tablo
        self.tree = ttk.Treeview(self.pencere, columns=("Tarih", "Üye", "Tip", "Kategori", "Miktar"), show='headings')
        for col in ("Tarih", "Üye", "Tip", "Kategori", "Miktar"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")
        self.tree.pack(pady=10, fill="both", expand=True)

        # Kar/Zarar Paneli
        self.lbl_ozet = tk.Label(self.pencere, text="", font=("Arial", 11, "bold"), pady=10, bg="#f8f9fa")
        self.lbl_ozet.pack(fill="x", pady=5)

        # --- GELİŞTİRİCİ İSİMLERİ ---
        yazar_metni = "Hazırlayanlar: Beyzanur SARI & Cafer ÇELİK"
        tk.Label(self.pencere, text=yazar_metni, font=("Arial", 9, "italic"), fg="#7f8c8d", pady=5).pack(side="bottom")

        self.tabloyu_guncelle()

    def kaydet_click(self):
        try:
            m, k, uye, t = self.ent_miktar.get(), self.ent_kategori.get(), self.combo_uye.get(), self.combo_tip.get()
            if not m or not k: raise ValueError("Lütfen tüm alanları doldurun!")
            
            islem = Gelir(float(m), k, uye) if t == "Gelir" else Gider(float(m), k, uye)
            self.db.islem_ekle(islem)
            
            self.tabloyu_guncelle()
            self.ent_miktar.delete(0, tk.END)
            self.ent_kategori.delete(0, tk.END)
            messagebox.showinfo("Başarılı", "İşlem başarıyla eklendi!")
        except Exception as e: 
            messagebox.showerror("Hata", str(e))

    def sil_click(self):
        secili = self.tree.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Silinecek satırı seçin!")
            return
        if messagebox.askyesno("Onay", "Seçili kaydı silmek istiyor musunuz?"):
            for s in secili:
                self.db.islem_sil(self.tree.item(s)['tags'][0])
            self.tabloyu_guncelle()

    def tabloyu_guncelle(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        
        secili_filtre = self.combo_filtre.get()
        for islem in self.db.tum_islemleri_getir(secili_filtre):
            self.tree.insert('', 'end', values=(islem[4], islem[5], islem[1], islem[2], f"{islem[3]} TL"), tags=(islem[0],))
        
        gel, gid, net = self.db.toplam_durum_hesapla(secili_filtre)
        renk = "#2ecc71" if net >= 0 else "#e74c3c"
        
        gosterim_ismi = "Aile Geneli" if secili_filtre == "Hepsi" else f"{secili_filtre} Üyesi"
        self.lbl_ozet.config(text=f"📊 {gosterim_ismi} Özet -> Gelir: {gel} TL | Gider: {gid} TL | Net: {net} TL", fg=renk)
