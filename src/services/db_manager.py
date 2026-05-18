import os
import sqlite3

class DBManager:
    def __init__(self):
        proje_dizini = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.db_yolu = os.path.join(proje_dizini, "data", "butce.db")
        os.makedirs(os.path.join(proje_dizini, "data"), exist_ok=True)
        self.tablo_olustur()

    def tablo_olustur(self):
        with sqlite3.connect(self.db_yolu) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS islemler 
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                          tip TEXT, kategori TEXT, miktar REAL, tarih TEXT, uye TEXT)""")

    def islem_ekle(self, islem):
        with sqlite3.connect(self.db_yolu) as conn:
            conn.execute("INSERT INTO islemler (tip, kategori, miktar, tarih, uye) VALUES (?, ?, ?, ?, ?)", 
                         (islem.tip, islem.kategori, islem.get_miktar(), islem.tarih, islem.uye))

    def islem_sil(self, islem_id):
        with sqlite3.connect(self.db_yolu) as conn:
            conn.execute("DELETE FROM islemler WHERE id = ?", (islem_id,))

    def tum_islemleri_getir(self, filtre_uye="Hepsi"):
        with sqlite3.connect(self.db_yolu) as conn:
            cursor = conn.cursor()
            if filtre_uye == "Hepsi":
                cursor.execute("SELECT id, tip, kategori, miktar, tarih, uye FROM islemler ORDER BY id DESC")
            else:
                cursor.execute("SELECT id, tip, kategori, miktar, tarih, uye FROM islemler WHERE uye=? ORDER BY id DESC", (filtre_uye,))
            return cursor.fetchall()

    def toplam_durum_hesapla(self, filtre_uye="Hepsi"):
        with sqlite3.connect(self.db_yolu) as conn:
            cursor = conn.cursor()
            if filtre_uye == "Hepsi":
                gelir = cursor.execute("SELECT SUM(miktar) FROM islemler WHERE tip='Gelir'").fetchone()[0] or 0
                gider = cursor.execute("SELECT SUM(miktar) FROM islemler WHERE tip='Gider'").fetchone()[0] or 0
            else:
                gelir = cursor.execute("SELECT SUM(miktar) FROM islemler WHERE tip='Gelir' AND uye=?", (filtre_uye,)).fetchone()[0] or 0
                gider = cursor.execute("SELECT SUM(miktar) FROM islemler WHERE tip='Gider' AND uye=?", (filtre_uye,)).fetchone()[0] or 0
            return gelir, gider, (gelir - gider)
