from datetime import datetime

class Islem:
    def __init__(self, miktar, kategori, uye):
        self.__miktar = miktar  # Kapsülleme (Encapsulation)
        self.kategori = kategori
        self.uye = uye  # Koca, Karı, Çocuk
        self.tarih = datetime.now().strftime("%d-%m-%Y %H:%M")

    def get_miktar(self): # Getter Metodu
        return self.__miktar

class Gelir(Islem):
    def __init__(self, miktar, kategori, uye):
        super().__init__(miktar, kategori, uye)
        self.tip = "Gelir"

class Gider(Islem):
    def __init__(self, miktar, kategori, uye):
        super().__init__(miktar, kategori, uye)
        self.tip = "Gider"
