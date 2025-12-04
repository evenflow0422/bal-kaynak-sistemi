Log in ekranı ile başlayacak
Altında kayıt ol butonu olsun ve Kayıt Ol ekranına gitsin

Veritabanında admin bilgileri kaydedilecek
Admin bilgileri uygulama içinden kayıt olamaz, veritabandaki tabloya yazılır
Kayıt olan kullanıcılar otomatikman müşteriler tablosuna gelsin

#Bal Tablosunda
bal_id
bal isim (kavanoz ismi)
bal cinsi=çiçek balı, salgı balı (sadece 2 tane)
bal türü=çiçek balları tablosu ve salgı balı tablosundan çekilecek.
bal rengi=renk skalası (25/35 mm Light amber gibi)
arıcı_id

#Arıcı Tablosu
arıcı_id
İsim
Soyisim
Telefon numarası
AKS kod
Şehir, Köy
Arıcılık Türü = Gezgin veya Sabit
Üretim Türü = 1.Konvansiyel 2.Organik 3.Coğrafi İşaret tescil belgeli arıcı
Kovan Sayısı = Küçük ve büyüklüğü önemli (hobi ya da profesyonel arıcı olduğunu belirler.)

#Müşteriler Tablosu
kullanıcı adı
isim
soyisim
cinsiyet
eposta
şifre

#admin tablosu
admin kullanıcı adı
şifre
isim
soyisim

#Çiçek Balları Tablosu
Yayla Balı
Ayçiçek Balı
Pamuk Balı
Kestane Balı
Ihlamur Balı
Lavanta Balı
Akasya Balı
Çörek Otu Balı

#Salgı Balı Tablosu
Çam Balı
Sedir Balı

#Değerlendirme
id
bal_id (hangi bal)
musteri_id (hangi müşteri)
yildiz (1-5 arası)
yorum (metin)
tarih

Kullanıcı Panelinde:
Balların hepsini gösterme
Balları filtreleme ()
Değerlendirme ekleme
