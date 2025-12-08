from tkinter import *
from tkinter import messagebox
import os
from db import baglanti_kur

root = Tk()
root.title("Bal Kaynak Sistemi | Kayit Ekrani")

pencere_genislik = 400
pencere_yukseklik = 400
ekran_genislik = root.winfo_screenwidth()
ekran_yukseklik = root.winfo_screenheight()
x = (ekran_genislik - pencere_genislik) // 2
y = (ekran_yukseklik - pencere_yukseklik) // 2
root.geometry(f"{pencere_genislik}x{pencere_yukseklik}+{x}+{y}")

root.resizable(False, False)
icon = PhotoImage(file='minecraft-bee.png')
root.iconphoto(True, icon)
root.config(background="#ffd69c")

def giris_ac():
    root.destroy()
    os.system('py giris.py')

def kayit_tikla():
    isim = isimEntry.get()
    soyisim = soyisimEntry.get()
    kullanici = kullaniciEntry.get()
    eposta = epostaEntry.get()
    sifre = sifreEntry.get()
    cinsiyet_sec = cinsiyet.get()
    
    # Bos alan kontrolu
    if isim == "" or soyisim == "" or kullanici == "" or eposta == "" or sifre == "":
        messagebox.showwarning("Uyari", "Tum alanlari doldurun!")
        return
    
    # Cinsiyet kontrolu
    if cinsiyet_sec == 0:
        messagebox.showwarning("Uyari", "Cinsiyet secin!")
        return
    
    # Sifre uzunluk kontrolu
    if len(sifre) < 8:
        messagebox.showwarning("Uyari", "Sifre en az 8 karakter olmali!")
        return
    
    # Cinsiyet degerini belirle
    if cinsiyet_sec == 1:
        cinsiyet_str = "Erkek"
    elif cinsiyet_sec == 2:
        cinsiyet_str = "Kadin"
    else:
        cinsiyet_str = "Belirtmek Istemiyorum"
    
    conn = baglanti_kur()
    if conn is None:
        messagebox.showerror("Hata", "Veritabani baglantisi kurulamadi!")
        return
    
    cursor = conn.cursor()
    
    # Kullanici adi kontrolu
    cursor.execute("SELECT * FROM musteriler WHERE kullanici_adi = %s", (kullanici,))
    if cursor.fetchone():
        messagebox.showerror("Hata", "Bu kullanici adi zaten kullaniliyor!")
        cursor.close()
        conn.close()
        return
    
    # Eposta kontrolu
    cursor.execute("SELECT * FROM musteriler WHERE eposta = %s", (eposta,))
    if cursor.fetchone():
        messagebox.showerror("Hata", "Bu e-posta zaten kullaniliyor!")
        cursor.close()
        conn.close()
        return
    
    # Kayit islemi
    sorgu = """INSERT INTO musteriler (kullanici_adi, isim, soyisim, cinsiyet, eposta, sifre) 
               VALUES (%s, %s, %s, %s, %s, %s)"""
    
    try:
        cursor.execute(sorgu, (kullanici, isim, soyisim, cinsiyet_str, eposta, sifre))
        conn.commit()
        messagebox.showinfo("Basarili", "Kayit basarili! Giris yapabilirsiniz.")
        cursor.close()
        conn.close()
        giris_ac()
    except Exception as e:
        messagebox.showerror("Hata", f"Kayit sirasinda hata olustu: {e}")
        cursor.close()
        conn.close()

# Arayuz elemanlari
baslikLabel = Label(root, text="Kayit Ol!", font=("Arial", 16), bg="#ffd69c")
isimLabel = Label(root, text="Isim:", bg="#ffd69c")
isimEntry = Entry(root)
soyisimLabel = Label(root, text="Soyisim:", bg="#ffd69c")
soyisimEntry = Entry(root)

cinsiyet = IntVar()
cinsiyetLabel = Label(root, text="Cinsiyet:", bg="#ffd69c")
erkek = Radiobutton(root, text="Erkek", variable=cinsiyet, value=1, bg="#ffd69c")
kadin = Radiobutton(root, text="Kadin", variable=cinsiyet, value=2, bg="#ffd69c")

kullaniciLabel = Label(root, text="Kullanici Adi:", bg="#ffd69c")
kullaniciEntry = Entry(root)
epostaLabel = Label(root, text="E-posta:", bg="#ffd69c")
epostaEntry = Entry(root)
sifreLabel = Label(root, text="Sifre:", bg="#ffd69c")
sifreEntry = Entry(root, show='*')

kayitButton = Button(root, text="Kayit Ol", command=kayit_tikla,
                     bg='white', fg='orange',
                     activebackground='orange', activeforeground='white',
                     width=15)
hesapVarLabel = Label(root, text="Zaten bir hesabim var, giris yap.",
                      fg='blue', bg="#ffd69c",
                      font=('Arial', 9, 'underline'),
                      cursor='hand2')

# Yerlestirme
baslikLabel.grid(row=0, column=0, columnspan=2, pady=15)
isimLabel.grid(row=1, column=0, padx=10, pady=5, sticky="e")
isimEntry.grid(row=1, column=1, padx=10, pady=5)
soyisimLabel.grid(row=2, column=0, padx=10, pady=5, sticky="e")
soyisimEntry.grid(row=2, column=1, padx=10, pady=5)
cinsiyetLabel.grid(row=3, column=0, padx=10, pady=5, sticky="e")
erkek.grid(row=3, column=1, sticky="w")
kadin.grid(row=4, column=1, sticky="w")
kullaniciLabel.grid(row=5, column=0, padx=10, pady=5, sticky="e")
kullaniciEntry.grid(row=5, column=1, padx=10, pady=5)
epostaLabel.grid(row=6, column=0, padx=10, pady=5, sticky="e")
epostaEntry.grid(row=6, column=1, padx=10, pady=5)
sifreLabel.grid(row=7, column=0, padx=10, pady=5, sticky="e")
sifreEntry.grid(row=7, column=1, padx=10, pady=5)
kayitButton.grid(row=8, column=0, columnspan=2, pady=15)
hesapVarLabel.grid(row=9, column=0, columnspan=2)

hesapVarLabel.bind("<Button-1>", lambda e: giris_ac())

root.mainloop()
