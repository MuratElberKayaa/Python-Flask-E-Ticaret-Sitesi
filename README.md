# Mekaya E-Ticaret Sitesi

Python Flask framework kullanılarak geliştirilmiş modern bir e-ticaret web uygulaması.

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Teknolojiler](#-teknolojiler)
- [Kurulum](#-kurulum)
- [Yapılandırma](#-yapılandırma)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)
- [İletişim](#-iletişim)

## ✨ Özellikler

### Kullanıcı Özellikleri
- 🔐 Kullanıcı kayıt ve giriş sistemi
- 👤 Kullanıcı profil yönetimi
- 🛍️ Ürün kategorileri (Tişört, Cüzdan, Kemer, Ayakkabı)
- 🔍 Ürün arama özelliği
- 👁️ Ürün detay görüntüleme
- 🛒 Sipariş verme sistemi
- 📦 Sipariş geçmişi görüntüleme
- 🎯 İçerik tabanlı ürün öneri sistemi

### Admin Özellikleri
- 🔑 Admin giriş paneli
- 📊 Dashboard (İstatistikler)
- ➕ Ürün ekleme ve düzenleme
- 📝 Sipariş yönetimi
- 👥 Kullanıcı yönetimi
- 🖼️ Ürün görsel yükleme

## 🛠️ Teknolojiler

### Backend
- **Python 3.x**
- **Flask 1.0.2** - Web framework
- **MySQL** - Veritabanı
- **Flask-MySQLdb** - MySQL entegrasyonu
- **WTForms** - Form validasyonu
- **Passlib** - Şifre hashleme
- **Flask-Uploads** - Dosya yükleme
- **Flask-Mail** - E-posta gönderimi

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript**
- **Bootstrap** - Responsive tasarım

## 📦 Kurulum

### Gereksinimler

- Python 3.6 veya üzeri
- MySQL Server 5.7 veya üzeri
- pip (Python paket yöneticisi)

### Adım 1: Projeyi İndirin

```bash
git clone https://github.com/kullaniciadi/Mekaya-E-ticaret.git
cd Mekaya-E-ticaret/mekaya
```

### Adım 2: Virtual Environment Oluşturun (Önerilir)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r Gereksinimler.txt
```

**Not:** Eğer `Gereksinimler.txt` dosyası yoksa, aşağıdaki komutu kullanabilirsiniz:

```bash
pip install Flask==1.0.2 Flask-MySQLdb==0.2.0 Flask-Mail==0.9.1 Flask-Uploads==0.2.1 WTForms==2.2.1 passlib==1.7.1 mysqlclient==1.4.2.post1
```

### Adım 4: MySQL Veritabanını Kurun

1. MySQL Server'ı başlatın
2. MySQL'e giriş yapın:

```bash
mysql -u root -p
```

3. Veritabanını oluşturun ve SQL dosyasını içe aktarın:

```sql
CREATE DATABASE mekaya CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci;
USE mekaya;
SOURCE database/mekaya.sql;
```

Veya MySQL Workbench veya phpMyAdmin gibi bir araç kullanarak `database/mekaya.sql` dosyasını içe aktarabilirsiniz.

## ⚙️ Yapılandırma

`app.py` dosyasını açın ve MySQL bağlantı bilgilerinizi güncelleyin:

```python
app.config['MYSQL_HOST'] = '127.0.0.1'      # MySQL host adresi
app.config['MYSQL_USER'] = 'root'            # MySQL kullanıcı adı
app.config['MYSQL_PASSWORD'] = '1234'        # MySQL şifresi
app.config['MYSQL_DB'] = 'mekaya'            # Veritabanı adı
```

**Güvenlik Notu:** Üretim ortamında şifreleri ve hassas bilgileri environment variable olarak saklayın!

### Varsayılan Admin Bilgileri

SQL dosyası içinde varsayılan bir admin hesabı bulunmaktadır:
- **E-posta:** elberfener@gmail.com
- **Şifre:** SQL dosyasındaki hashlenmiş şifre (giriş yapmak için yeni bir admin oluşturmanız veya şifreyi değiştirmeniz gerekebilir)

## 🚀 Kullanım

### Uygulamayı Başlatma

```bash
python app.py
```

Uygulama varsayılan olarak `http://127.0.0.1:5000` adresinde çalışacaktır.

### Erişim Adresleri

- **Ana Sayfa:** http://127.0.0.1:5000/
- **Kullanıcı Girişi:** http://127.0.0.1:5000/login
- **Kullanıcı Kayıt:** http://127.0.0.1:5000/register
- **Admin Paneli:** http://127.0.0.1:5000/admin_login

### Kullanım Akışı

1. **Kullanıcı Olarak:**
   - Kayıt olun veya giriş yapın
   - Ürünleri kategorilere göre gezebilirsiniz
   - Ürün detaylarını görüntüleyebilirsiniz
   - Sipariş verebilirsiniz
   - Profilinizden sipariş geçmişinizi görebilirsiniz

2. **Admin Olarak:**
   - Admin paneline giriş yapın
   - Dashboard'dan genel istatistikleri görüntüleyin
   - Ürün ekleyin, düzenleyin
   - Siparişleri yönetin
   - Kullanıcıları görüntüleyin

## 📁 Proje Yapısı

```
mekaya/
│
├── app.py                      # Ana uygulama dosyası
├── Gereksinimler.txt           # Python bağımlılıkları
├── benioku.md                  # Proje bilgileri
│
├── database/
│   └── mekaya.sql              # Veritabanı SQL dosyası
│
├── static/                     # Statik dosyalar
│   ├── css/
│   │   └── style.css           # Özel CSS stilleri
│   ├── js/
│   │   ├── custom.js           # Özel JavaScript
│   │   └── sb-admin-2.js       # Admin panel JS
│   └── image/                  # Görseller
│       ├── product/            # Ürün görselleri
│       │   ├── tshirt/
│       │   ├── wallet/
│       │   ├── belt/
│       │   └── shoes/
│       └── ...
│
└── templates/                  # HTML şablonları (projede mevcut)
    ├── home.html
    ├── login.html
    ├── register.html
    ├── profile.html
    ├── pages/                  # Admin panel şablonları
    │   ├── index.html
    │   ├── login.html
    │   ├── add_product.html
    │   └── ...
    └── ...
```

## 🎯 Özellikler Detayı

### Ürün Öneri Sistemi

Proje, içerik tabanlı filtreleme (content-based filtering) algoritması kullanarak benzer ürünleri önermektedir. Sistem, ürün kategorileri ve özelliklerine göre eşleşme puanı hesaplar.

### Güvenlik Özellikleri

- Şifreler SHA256 ile hashlenir
- Session yönetimi
- Kullanıcı ve admin yetkilendirme decorator'ları
- Form validasyonu

## 📸 Ekran Görüntüleri

> **Not:** Ekran görüntüleri eklenecek...

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen şu adımları izleyin:

1. Bu projeyi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Bir Pull Request oluşturun

## 📝 Lisans

Bu proje açık kaynaklıdır. Kendi projelerinizde kullanabilirsiniz.

## 👤 İletişim

**Geliştirici:** Murat Elber Kaya

- 🌐 Facebook: [Muratelber.kaya](https://www.facebook.com/Muratelber.kaya)
- 📺 YouTube: [Kanal](https://www.youtube.com/channel/UCEPrBlkej6CbTHmTyh7IuoQ?view_as=subscriber)

## ⚠️ Önemli Notlar

- Bu proje eğitim amaçlı geliştirilmiştir
- Üretim ortamında kullanmadan önce güvenlik önlemlerini gözden geçirin
- Veritabanı şifrelerini ve hassas bilgileri environment variable olarak saklayın
- Debug modunu üretim ortamında kapalı tutun

## 🔄 Güncellemeler

- **v1.0.0** - İlk sürüm
  - Kullanıcı kayıt/giriş sistemi
  - Ürün yönetimi
  - Sipariş sistemi
  - Admin paneli
  - İçerik tabanlı öneri sistemi

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

