from tkinter import *
import os
from tkinter import messagebox
import bcrypt
from baglanti import veritabani_baglanti, baglanti_kapat

root = Tk()
root.title("Bal Kaynak Sistemi | Kayıt Ekranı")

pencere_genislik = 400
pencere_yukseklik = 300
ekran_genislik = root.winfo_screenwidth()
ekran_yukseklik = root.winfo_screenheight()
x = (ekran_genislik - pencere_genislik) // 2
y = (ekran_yukseklik - pencere_yukseklik) // 2
root.geometry(f"{pencere_genislik}x{pencere_yukseklik}+{x}+{y}")

root.resizable(False, False)
icon = PhotoImage(file='minecraft-bee.png')
root.iconphoto(True,icon)
root.config(background="#ffd69c")

def giris_ac():
    root.destroy()
    os.system('py giris.py')

def kayit_tikla():
    isim=isimEntry.get().strip()
    soyisim=soyisimEntry.get().strip()
    cinsiyetDeger=cinsiyet.get()
    eposta=epostaEntry.get().strip()
    kullaniciAdi=kullaniciEntry.get().strip()
    sifre=sifreEntry.get().strip()
    
    if not isim or not soyisim or not cinsiyet or not eposta or not kullaniciAdi or not sifre:
        messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
        return
    if len(sifre)<8:
        messagebox.showwarning("Zayıf Şifre", "Şifreniz en az 8 karakter uzunluğunda olmalıdır.")
        return
    baglanti=veritabani_baglanti()
    if baglanti is None:
        messagebox.showerror("Hata","Veritabanına bağlanılamadı")
        return
    try:
        cursor=baglanti.cursor(dictionary=True)
        kullaniciKontrolSql="SELECT * FROM musteriler WHERE kullanici_adi=%s"
        cursor.execute(kullaniciKontrolSql,(kullaniciAdi,))
        if cursor.fetchone() is not None:
            messagebox.showwarning("Kullanıcı Adı Alınmış","Bu kullanıcı adı zaten kullanılıyor. Lütfen başka bir tane deneyin.")
            return
        epostaKontrolSql="SELECT * FROM musteriler WHERE eposta=%s"
        cursor.execute(epostaKontrolSql,(eposta,))
        if cursor.fetchone() is not None:
            messagebox.showwarning("E-posta Alınmış","Bu e-posta zaten kullanılıyor. Lütfen başka bir tane deneyin.")
            return
        hashedSifre=bcrypt.hashpw(sifre.encode('utf-8'),bcrypt.gensalt())
        kayitSql="INSERT INTO musteriler (isim, soyisim, cinsiyet, eposta, kullanici_adi, sifre) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(kayitSql,(isim,soyisim,cinsiyetDeger,eposta,kullaniciAdi,hashedSifre.decode('utf-8')))
        baglanti.commit()
        messagebox.showinfo("Başarılı","Kayıt başarılı! Giriş yapabilirsiniz.")
        baglanti_kapat(baglanti)
        root.destroy()
        os.system('py giris.py')
    except Exception as e:
        messagebox.showerror("Hata",f"Kayıt işlemi sırasında bir hata oluştu:{e}")
    finally:
        if baglanti and baglanti.is_connected():
            baglanti_kapat(baglanti)
        
#değer falan filan 
baslikLabel=Label(root,text="Kayıt Yap!",font=("Arial",16))
isimLabel=Label(root,text="İsim:")
isimEntry=Entry(root)
soyisimLabel=Label(root,text="Soyisim:")
soyisimEntry=Entry(root)
cinsiyet=StringVar()
erkek=Radiobutton(root,text="Erkek",variable=cinsiyet,value="Erkek")
kadin=Radiobutton(root,text="Kadın",variable=cinsiyet,value="Kadın")
epostaLabel=Label(root,text="E-posta:")
epostaEntry=Entry(root)
kullaniciLabel=Label(root,text="Kullanıcı Adı:")
kullaniciEntry=Entry(root)
sifreLabel=Label(root,text="Şifre:")
sifreEntry=Entry(root,show='*')
kayitButton=Button(root,text="Kayıt Ol",command=kayit_tikla,
                   bg='white', fg='orange',
                   activebackground='orange',activeforeground='white')
hesapVarLabel=Label(root,text="Zaten bir hesabım var, giriş yap.",
                    fg='blue',
                    font=('Arial',9,'underline'),
                    cursor='hand2')
#yerleştirme
baslikLabel.grid(row=0,column=0)
isimLabel.grid(row=1,column=0)
isimEntry.grid(row=1,column=1)
soyisimLabel.grid(row=2,column=0)
soyisimEntry.grid(row=2,column=1)
erkek.grid(row=3,column=0)
kadin.grid(row=3,column=1)
kullaniciLabel.grid(row=4,column=0)
kullaniciEntry.grid(row=4,column=1)
epostaLabel.grid(row=5,column=0)
epostaEntry.grid(row=5,column=1)
sifreLabel.grid(row=6,column=0)
sifreEntry.grid(row=6,column=1)
kayitButton.grid(row=7,column=0)
hesapVarLabel.grid(row=8,column=0)

hesapVarLabel.bind("<Button-1>", lambda e: giris_ac())


root.mainloop()