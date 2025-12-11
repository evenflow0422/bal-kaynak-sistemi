-- =====================================================
-- BAL TAKİP SİSTEMİ VERİTABANI
-- MySQL 8.0+ uyumlu - Aktif/Pasif durumu kaldırılmış
-- =====================================================

DROP DATABASE IF EXISTS bal_takip;

CREATE DATABASE bal_takip 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_turkish_ci;

USE bal_takip;
-- =====================================================
-- MÜŞTERİLER TABLOSU
-- =====================================================
CREATE TABLE musteriler (
    musteri_id INT AUTO_INCREMENT PRIMARY KEY,
    kullanici_adi VARCHAR(50) NOT NULL UNIQUE,
    isim VARCHAR(100) NOT NULL,
    soyisim VARCHAR(100) NOT NULL,
    cinsiyet ENUM('Erkek', 'Kadin', 'Belirtmek Istemiyorum') NOT NULL,
    eposta VARCHAR(150) NOT NULL UNIQUE,
    sifre VARCHAR(255) NOT NULL,
    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    son_giris TIMESTAMP NULL
) ENGINE=InnoDB;

-- =====================================================
-- ARICI TABLOSU
-- =====================================================
CREATE TABLE aricilar (
    arici_id INT AUTO_INCREMENT PRIMARY KEY,
    isim VARCHAR(100) NOT NULL,
    soyisim VARCHAR(100) NOT NULL,
    telefon VARCHAR(20) NOT NULL,
    aks_kod VARCHAR(50) UNIQUE,
    sehir VARCHAR(100) NOT NULL,
    koy VARCHAR(100),
    aricilik_turu ENUM('Gezgin', 'Sabit') NOT NULL,
    uretim_turu ENUM('Konvansiyonel', 'Organik', 'Cografi Isaret Tescil Belgeli') NOT NULL,
    kovan_sayisi INT NOT NULL,
    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =====================================================
-- ÇİÇEK BALLARI TABLOSU
-- =====================================================
CREATE TABLE cicek_ballari (
    cicek_bal_id INT AUTO_INCREMENT PRIMARY KEY,
    bal_adi VARCHAR(100) NOT NULL UNIQUE,
    aciklama TEXT
) ENGINE=InnoDB;

INSERT INTO cicek_ballari (bal_adi) VALUES 
('Yayla Bali'),
('Aycicek Bali'),
('Pamuk Bali'),
('Kestane Bali'),
('Ihlamur Bali'),
('Lavanta Bali'),
('Akasya Bali'),
('Corek Otu Bali');

-- =====================================================
-- SALGI BALLARI TABLOSU
-- =====================================================
CREATE TABLE salgi_ballari (
    salgi_bal_id INT AUTO_INCREMENT PRIMARY KEY,
    bal_adi VARCHAR(100) NOT NULL UNIQUE,
    aciklama TEXT
) ENGINE=InnoDB;

INSERT INTO salgi_ballari (bal_adi) VALUES 
('Cam Bali'),
('Sedir Bali');

-- =====================================================
-- RENK SKALASI TABLOSU
-- =====================================================
CREATE TABLE renk_skalasi (
    renk_id INT AUTO_INCREMENT PRIMARY KEY,
    renk_kodu VARCHAR(50) NOT NULL,
    renk_adi VARCHAR(100) NOT NULL,
    mm_aralik VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

INSERT INTO renk_skalasi (renk_kodu, renk_adi, mm_aralik) VALUES 
('WW', 'Water White', '0-8 mm'),
('EW', 'Extra White', '9-17 mm'),
('W', 'White', '18-34 mm'),
('ELA', 'Extra Light Amber', '35-50 mm'),
('LA', 'Light Amber', '51-85 mm'),
('A', 'Amber', '86-114 mm'),
('DA', 'Dark Amber', '115+ mm');

-- =====================================================
-- BAL TABLOSU
-- =====================================================
CREATE TABLE ballar (
    bal_id INT AUTO_INCREMENT PRIMARY KEY,
    bal_isim VARCHAR(150) NOT NULL,
    bal_cinsi ENUM('Cicek Bali', 'Salgi Bali') NOT NULL,
    cicek_bal_id INT NULL,
    salgi_bal_id INT NULL,
    renk_id INT NOT NULL,
    arici_id INT NOT NULL,
    fiyat DECIMAL(10,2) DEFAULT 0.00,
    stok_miktari INT DEFAULT 0,
    agirlik_gram INT,
    uretim_tarihi DATE,
    aciklama TEXT,
    resim_url VARCHAR(500),
    eklenme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (cicek_bal_id) REFERENCES cicek_ballari(cicek_bal_id) ON DELETE RESTRICT,
    FOREIGN KEY (salgi_bal_id) REFERENCES salgi_ballari(salgi_bal_id) ON DELETE RESTRICT,
    FOREIGN KEY (renk_id) REFERENCES renk_skalasi(renk_id) ON DELETE RESTRICT,
    FOREIGN KEY (arici_id) REFERENCES aricilar(arici_id) ON DELETE CASCADE,
    
    CONSTRAINT chk_bal_turu CHECK (
        (bal_cinsi = 'Cicek Bali' AND cicek_bal_id IS NOT NULL AND salgi_bal_id IS NULL) OR
        (bal_cinsi = 'Salgi Bali' AND salgi_bal_id IS NOT NULL AND cicek_bal_id IS NULL)
    )
) ENGINE=InnoDB;

-- =====================================================
-- DEĞERLENDİRME TABLOSU
-- =====================================================
CREATE TABLE degerlendirmeler (
    degerlendirme_id INT AUTO_INCREMENT PRIMARY KEY,
    bal_id INT NOT NULL,
    musteri_id INT NOT NULL,
    yildiz TINYINT NOT NULL,
    yorum TEXT,
    tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    onaylandi TINYINT(1) DEFAULT 0,
    
    FOREIGN KEY (bal_id) REFERENCES ballar(bal_id) ON DELETE CASCADE,
    FOREIGN KEY (musteri_id) REFERENCES musteriler(musteri_id) ON DELETE CASCADE,
    
    CONSTRAINT chk_yildiz CHECK (yildiz >= 1 AND yildiz <= 5),
    UNIQUE KEY unique_musteri_bal (musteri_id, bal_id)
) ENGINE=InnoDB;

-- =====================================================
-- İNDEKSLER
-- =====================================================
CREATE INDEX idx_ballar_cinsi ON ballar(bal_cinsi);
CREATE INDEX idx_ballar_arici ON ballar(arici_id);
CREATE INDEX idx_degerlendirme_bal ON degerlendirmeler(bal_id);
CREATE INDEX idx_degerlendirme_musteri ON degerlendirmeler(musteri_id);
CREATE INDEX idx_aricilar_sehir ON aricilar(sehir);
CREATE INDEX idx_musteriler_eposta ON musteriler(eposta);

-- =====================================================
-- VIEW - Bal Detay
-- =====================================================
CREATE VIEW v_bal_detay AS
SELECT 
    b.bal_id,
    b.bal_isim,
    b.bal_cinsi,
    CASE 
        WHEN b.bal_