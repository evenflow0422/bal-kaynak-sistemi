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

frame=Frame(root,background="#8e4200",padx=20,pady=20)

root.resizable(False, False)
icon = PhotoImage(file='minecraft-bee.png')
root.iconphoto(True,icon)
root.config(background="#8e4200")

def giris_ac():
    root.destroy()
    os.system('py giris.py')

def kayit_tikla():
    isim=isimEntry.get().strip()
    soyisim=soyisimEntry.get().strip()
    cinsiyetDeger=cinsiyet.get().strip()
    eposta=epostaEntry.get().strip()
    kullaniciAdi=kullaniciEntry.get().strip()
    sifre=sifreEntry.get().strip()
    
    if not isim or not soyisim or cinsiyetDeger not in ["Erkek","Kadin"] or not eposta or not kullaniciAdi or not sifre:
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
baslikLabel=Label(frame,text="Kayıt Yap!",font=("Times New Roman",20),fg="#ff9624",
                  bg="#8e4200")
isimLabel=Label(frame,text="İsim:",fg="#ffd69c",bg="#8e4200",
                     font=("Georgia",12))
isimEntry=Entry(frame)
soyisimLabel=Label(frame,text="Soyisim:",fg="#ffd69c",bg="#8e4200",
                     font=("Georgia",12))
soyisimEntry=Entry(frame)
cinsiyet=StringVar()
cinsiyet.set(0)
erkek=Radiobutton(frame,text="Erkek",variable=cinsiyet,value="Erkek",fg="#ffd69c",bg="#8e4200",
                     font=("Georgia",12),selectcolor="#8e4200",activebackground="#8e4200")
kadin=Radiobutton(frame,text="Kadın",variable=cinsiyet,value="Kadin",fg="#ffd69c",bg="#8e4200",
                     font=("Georgia",12),selectcolor="#8e4200",activebackground="#8e4200")
kullaniciLabel=Label(frame,text="Kullanıcı Adı:",fg="#ffd69c",bg="#8e4200",
                     font=("Georgia",12))
kullaniciEntry=Entry(frame)
epostaLabel=Label(frame,text="E-posta:",fg="#ffd69c",bg="#8e4200",
                     font=("Georgia",12))
epostaEntry=Entry(frame)
sifreLabel=Label(frame,text="Şifre:",fg="#ffd69c",bg="#8e4200",
                     font=("Georgia",12))
sifreEntry=Entry(frame,show='*')
kayitButton=Button(frame,text="Kayıt Ol",command=kayit_tikla,
                   bg="#773903", fg='orange', font=("Georgia",12),
                   activebackground='orange',activeforeground='white')
hesapVarLabel=Label(frame,text="Zaten bir hesabım var, giriş yap.",
                    fg='#ffb825',
                    font=('Arial',9,'underline'),
                    cursor='hand2',bg="#8e4200")
#yerleştirme
baslikLabel.grid(row=0,column=0,columnspan=2)
isimLabel.grid(row=1,column=0)
isimEntry.grid(row=1,column=1,pady=5)
soyisimLabel.grid(row=2,column=0)
soyisimEntry.grid(row=2,column=1,pady=5)
erkek.grid(row=3,column=0)
kadin.grid(row=3,column=1)
kullaniciLabel.grid(row=4,column=0)
kullaniciEntry.grid(row=4,column=1,pady=5)
epostaLabel.grid(row=5,column=0)
epostaEntry.grid(row=5,column=1,pady=5)
sifreLabel.grid(row=6,column=0)
sifreEntry.grid(row=6,column=1,pady=5)
kayitButton.grid(row=7,column=0,columnspan=2,pady=5)
hesapVarLabel.grid(row=8,column=0,sticky=E)

hesapVarLabel.bind("<Button-1>", lambda e: giris_ac())
root.bind("<Return>", lambda event: kayitButton.invoke())
frame.pack()

root.mainloop()