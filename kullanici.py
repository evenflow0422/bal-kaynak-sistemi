from tkinter import *
from tkinter import messagebox
import os
import sys
from baglanti import veritabani_baglanti, baglanti_kapat

def cikis():
    cevap = messagebox.askyesno("Çıkış", "Emin misiniz?")
    if cevap:
        root.destroy()
def aricilar():
    #arıcıların bilgileri gözükecek
    ariciPencere=Toplevel()
    ariciPencere.title("Arıcılar")
    ariciPencere.geometry("400x300")
def degerlendirmelerim():
    #kullanıcının yaptığı değerlendirmeler gözükecek
    degerPencere=Toplevel()
    degerPencere.title("Değerlendirmelerim")
    degerPencere.geometry("400x300")
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
root.config(background="#8e4200")
#-------------------------------------------------------------------------------------
menubar = Menu(root)
menubar.add_command(label="Arıcılar",command=aricilar)
menubar.add_command(label="Değerlendirmelerim",command=degerlendirmelerim)
menubar.add_command(label="Hakkında",command=lambda: messagebox.showinfo("Hakkında","Bal Kaynak Sistemi v1.0\nGeliştirici: Serena Üzümcü & Ali Eren Onyıl"))
menubar.add_command(label="Çıkış", command=cikis)

kullanici_adi = sys.argv[1] if len(sys.argv) > 1 else "Kullanıcı"
baglanti=veritabani_baglanti()
isim="Kullanıcı"
if baglanti:
    try:
        cursor = baglanti.cursor(dictionary=True)
        kullaniciSql = "SELECT isim FROM musteriler WHERE kullanici_adi=%s"
        cursor.execute(kullaniciSql, (kullanici_adi,))
        kullanici = cursor.fetchone()
        
        if kullanici:
            isim = kullanici['isim']
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        baglanti_kapat(baglanti)

#veritabanından isim çekilecek
hosgeldinLabel=Label(root,text=f"Hoşgeldiniz, {isim}!",font=("Arial",16),bg="#ffd69c")
hosgeldinLabel.grid(row=0,column=0)
root.config(menu=menubar)
root.mainloop()