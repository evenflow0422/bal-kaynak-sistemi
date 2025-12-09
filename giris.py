from tkinter import *
import os 
from tkinter import messagebox
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
    #veritabanındaki veriler doğruysa musteri sistemine yollar.
    #doğru değilse kullanıcıya uyarı verir
    root.destroy()
    os.system('py kullanici.py')
    
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