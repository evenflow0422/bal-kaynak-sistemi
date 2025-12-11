from tkinter import *
import os 
from tkinter import messagebox
import bcrypt
import json
from baglanti import veritabani_baglanti, baglanti_kapat

root = Tk()
root.title("Bal Kaynak Sistemi | Giriş Ekranı")

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

def kayit_ac():
    root.destroy()
    os.system('py kayit.py')

def giris_tikla():
    kullaniciAdi = kullaniciEntry.get().strip()
    sifre = sifreEntry.get().strip()
    if not kullaniciAdi or not sifre:
        messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
        return
    baglanti = veritabani_baglanti()

    if baglanti is None:
        messagebox.showerror("Hata","Veritabanına bağlanılamadı")
        return
    try:
        cursor=baglanti.cursor(dictionary=True)
        girisSql="SELECT * FROM musteriler WHERE kullanici_adi=%s"
        cursor.execute(girisSql,(kullaniciAdi,))
        kullanici=cursor.fetchone()
        
        giris_basarili=False

        if kullanici is not None:
            db_sifre=kullanici['sifre']
        #şifre hashli mi değil mi
            try:
                if bcrypt.checkpw(sifre.encode('utf-8'),db_sifre.encode('utf-8')):
                    giris_basarili=True
            except:
                if sifre==db_sifre:
                    giris_basarili=True
        if giris_basarili:
            messagebox.showinfo("Başarılı","Giriş başarılı!")
            baglanti_kapat(baglanti)
            root.destroy()
            os.system('py kullanici.py')
        else:
            messagebox.showerror("Hata","Kullanıcı adı veya şifre yanlış.")
            #kullanıcının girdiği alanları siler
            kullaniciEntry.delete(0,END)
            sifreEntry.delete(0,END)
            kullaniciEntry.focus()
    except Exception as e:
        messagebox.showerror("Hata",f"Giriş sırasında bir hata oluştu: {str(e)}")
        kullaniciEntry.delete(0,END)
        sifreEntry.delete(0,END)
        kullaniciEntry.focus()
    finally:
        if baglanti and baglanti.is_connected():
            baglanti_kapat(baglanti)
              
#design olarak border ve padding ekle sonra
#font seç

#arayüzde gözüken değerler
baslikLabel=Label(root,text="Hoşgeldiniz! Giriş Yapınız",font=("Arial",16))
kullaniciLabel=Label(root,text="Kullanıcı Adı:")
kullaniciEntry=Entry(root)
sifreLabel=Label(root,text="Şifre:")
sifreEntry=Entry(root,show='*')
girisButton=Button(root,text="Giriş Yap",command=giris_tikla,
                   bg='white', fg='orange',
                   activebackground='orange',activeforeground='white')
hesapYokLabel=Label(root,text="Hesabım yok, kayıt oluştur.",
                    fg='blue',
                    font=('Arial',9,'underline'),
                    cursor='hand2')

 #yerleştirme
baslikLabel.grid(row=0,column=0)
kullaniciLabel.grid(row=1,column=0)
kullaniciEntry.grid(row=1,column=1)
sifreLabel.grid(row=2,column=0)
sifreEntry.grid(row=2,column=1)
girisButton.grid(row=3,column=0)
hesapYokLabel.grid(row=4,column=0)

hesapYokLabel.bind("<Button-1>",lambda e: kayit_ac())

root.mainloop()