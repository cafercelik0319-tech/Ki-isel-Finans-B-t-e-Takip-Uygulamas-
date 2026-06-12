# 👨‍👩‍👧‍👦 Aile Bütçe Takip Sistemi v2.0

Bu proje, bir ailenin (Anne, Baba, Çocuk) gelir ve giderlerini dinamik bir ortamda kayıt altına alabilmesi, harcamalarını kategorize edebilmesi, üye bazlı anlık filtreleme yapabilmesi ve bütçe durumunu grafiksel olarak analiz edebilmesi amacıyla geliştirilmiş bir **Yazılım Geliştirme Teknolojileri** dersi bütünleme projesidir.

## 🛠️ Kullanılan Teknolojiler & Mimari
- **Dil:** Python 3
- **Arayüz:** Tkinter (GUI - Grafiksel Kullanıcı Arayüzü)
- **Veritabanı:** SQLite3 (İlişkisel Veritabanı)
- **Tasarım Deseni:** Modüler Tasarım ve Katmanlı Mimari (Models, Services, UI, Core)

## 🎯 Projede Uygulanan Akademik Kriterler
1. **Nesne Yönelimli Programlama (OOP):**
   - `Islem` adında bir kalıtım (inheritance) ana sınıfı oluşturulmuştur.
   - `Gelir` ve `Gider` sınıfları bu ana sınıftan türetilmiştir (`super()`).
   - Miktar değişkeni `__miktar` şeklinde gizlenerek **Kapsülleme (Encapsulation)** uygulanmış ve `get_miktar()` metodu ile güvenli bir şekilde kapsülden okunmuştur.
2. **Hata Yönetimi (Try-Except Mekanizması):**
   - Kullanıcının miktar alanını boş bırakması veya sayı girilmesi gereken yere geçersiz metin girmesi gibi durumlarda programın çökmesi `try-except` blokları ile engellenmiştir. Hatalar yakalanarak kullanıcıya `messagebox` ile bilgilendirici mesajlar gösterilir.
3. **Grafiksel Görselleştirme (Hocanın İstediği Özellik):**
   - Uygulamaya harici hiçbir kütüphane bağımlılığı (`matplotlib`, `pandas` vb.) eklenmeden, tamamen Python'ın çekirdek arayüz mimarisi (`Tkinter Canvas`) kullanılarak **Dinamik Sütun Grafiği** entegre edilmiştir. "Grafiği Göster" butonuna tıklandığında toplam gelir ve gider yüzdeleri hesaplanarak görsel analiz sunulur.
4. **Dinamik SQL Filtreleme:**
   - Veritabanı sorgularında `WHERE uye=?` parametrik yapısı kullanılarak SQL Injection açıkları engellenmiş ve üyeye göre anlık filtreleme mekanizması kurulmuştur.

## 📁 Klasör Yapısı
- `src/models/`: Veri modelleri ve OOP sınıfları (`transaction.py`)
- `src/services/`: Veritabanı yönetim katmanı (`db_manager.py`)
- `src/ui/`: Grafiksel arayüz bileşenleri ve grafik çizim motoru (`main_window.py`)
- `src/core/`: Uygulamanın ana giriş noktası (`app.py`)
- `data/`: SQLite veritabanı dosyası (`butce.db`)
- `docs/`: Gereksinim analizi, UML ve Sınıf (Class) diyagramları PDF dokümanları

## 🚀 Çalıştırma Talimatı

🚨 **ÇOK ÖNEMLİ NOT:** Programın veritabanı yollarını ve klasör hiyerarşisini doğru okuyabilmesi için komut satırının (CMD) doğrudan proje klasörünün içinde açılması gerekmektedir! `Windows + R` ile rastgele bir dizinde açılan CMD yapısı hataya sebep olur.

**Doğru Çalıştırma Adımları:**
1. Bilgisayarınızda ana **`ButceTakipProjesi`** klasörünün içine girin.
2. Klasörün en üstünde yer alan, klasör yolunun yazdığı **adres çubuğuna** (boş bir yere) sol tıklayın.
3. Oradaki mevcut yazıları tamamen silip doğrudan **`cmd`** yazın ve `Enter` tuşuna basın.
4. Doğrudan proje dizininde açılan siyah komut satırı ekranına şu komutu yapıştırıp `Enter` diyerek programı başlatın:
```bash
python src/core/app.py