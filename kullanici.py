from tkinter import *
from tkinter import messagebox
import os

def cikis():
    cevap = messagebox.askyesno("Çıkış", "Emin misiniz?")
    if cevap:
        root.destroy()
#menubar olacak (ballar,çıkış)
#çıkış butonu =basıldığında emin misin diye sor
#ballara tıklanıldığında yeni pencere açılsın ve bal bilgileri gözüksün
#değerlendirmelerimde tıklanıldığında yeni pencere açılsın ve kullanıcının yaptığı değerlendirmeler gözüksün

#bal ekranında değerlendirme yap butonuna tıklanıldığında yeni pencere açılsın ve değerlendirme formu gözüksün
root = Tk()
root.title("Bal Kaynak Sistemi | Kullanıcı Ekranı")

pencere_genislik = 1000
pencere_yukseklik = 600
ekran_genislik = root.winfo_screenwidth()
ekran_yukseklik = root.winfo_screenheight()
x = (ekran_genislik - pencere_genislik) // 2
y = (ekran_yukseklik - pencere_yukseklik) // 2
root.geometry(f"{pencere_genislik}x{pencere_yukseklik}+{x}+{y}")

root.resizable(False, False)
icon = PhotoImage(file='minecraft-bee.png')
root.iconphoto(True,icon)
root.config(background="#ffd69c")

menubar = Menu(root)

ballar_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Ballar", menu=ballar_menu)
menubar.add_command(label="Değerlendirmelerim")
menubar.add_command(label="Çıkış", command=cikis)

#veritabanından isim çekilecek
hosgeldinLabel=Label(root,text=f"Hoşgeldiniz, Kullanıcı!",font=("Arial",16),bg="#ffd69c")
hosgeldinLabel.grid(row=0,column=0)
root.config(menu=menubar)
root.mainloop()