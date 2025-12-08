from tkinter import *
from tkinter import messagebox
import os
from db import baglanti_kur

root = Tk()
root.title("Bal Kaynak Sistemi | Giris Ekrani")

pencere_genislik = 400
pencere_yukseklik = 350
ekran_genislik = root.winfo_screenwidth()
ekran_yukseklik = root.winfo_screenheight()
x = (ekran_genislik - pencere_genislik) // 2
y = (ekran_yukseklik - pencere_yukseklik) // 2
root.geometry(f"{pencere_genislik}x{pencere_yukseklik}+{x}+{y}")

root.resizable(False, False)
icon = PhotoImage(file='minecraft-bee.png')
root.iconphoto(True, icon)
root.config(background="#ffd69c")

def kayit_ac():
    root.destroy()
    os.system('py kayit.py')

def giris_tikla():
    kullanici = kullaniciEntry.get()
    sifre = sifreEntry.get()
    giris_tipi = giris_var.get()
    
    if kullanici == "" or sifre == "":
        messagebox.showwarning("Uyari", "Tum alanlari doldurun!")
        return
    
    conn = baglanti_kur()
    if conn is None:
        messagebox.showerror("Hata", "Veritabani baglantisi kurulamadi!")
        return
    
    cursor = conn.cursor()
    
    if giris_tipi == "admin":
        sorgu = "SELECT * FROM admin WHERE kullanici_adi = %s AND sifre = %s"
        cursor.execute(sorgu, (kullanici, sifre))
        sonuc = cursor.fetchone()
        
        if sonuc:
            messagebox.showinfo("Basarili", f"Hosgeldiniz Admin {sonuc[3]}!")
            cursor.close()
            conn.close()
            
            with open("session.txt", "w") as f:
                f.write(f"admin,{sonuc[0]},{sonuc[3]}")
            
            root.destroy()
            os.system('py admin_panel.py')
        else:
            messagebox.showerror("Hata", "Admin kullanici adi veya sifre hatali!")
    else:
        sorgu = "SELECT * FROM musteriler WHERE kullanici_adi = %s AND sifre = %s"
        cursor.execute(sorgu, (kullanici, sifre))
        sonuc = cursor.fetchone()
        
        if sonuc:
            messagebox.showinfo("Basarili", f"Hosgeldiniz, {sonuc[2]}!")
            cursor.close()
            conn.close()
            
            with open("session.txt", "w") as f:
                f.write(f"musteri,{sonuc[0]},{sonuc[2]}")
            
            root.destroy()
            os.system('py panel.py')
        else:
            messagebox.showerror("Hata", "Kullanici adi veya sifre hatali!")
    
    cursor.close()
    conn.close()

# Arayuz
baslikLabel = Label(root, text="Hosgeldiniz! Giris Yapiniz", font=("Arial", 16), bg="#ffd69c")

giris_var = StringVar(value="musteri")
girisFrame = Frame(root, bg="#ffd69c")
musteriRadio = Radiobutton(girisFrame, text="Musteri Girisi", variable=giris_var, value="musteri", bg="#ffd69c")
adminRadio = Radiobutton(girisFrame, text="Admin Girisi", variable=giris_var, value="admin", bg="#ffd69c")

kullaniciLabel = Label(root, text="Kullanici Adi:", bg="#ffd69c")
kullaniciEntry = Entry(root, width=25)
sifreLabel = Label(root, text="Sifre:", bg="#ffd69c")
sifreEntry = Entry(root, show='*', width=25)
girisButton = Button(root, text="Giris Yap", command=giris_tikla,
                     bg='white', fg='orange',
                     activebackground='orange', activeforeground='white',
                     width=15)
hesapYokLabel = Label(root, text="Hesabim yok, kayit olustur.",
                      fg='blue', bg="#ffd69c",
                      font=('Arial', 9, 'underline'),
                      cursor='hand2')

baslikLabel.grid(row=0, column=0, columnspan=2, pady=20)
girisFrame.grid(row=1, column=0, columnspan=2, pady=10)
musteriRadio.pack(side="left", padx=20)
adminRadio.pack(side="left", padx=20)
kullaniciLabel.grid(row=2, column=0, padx=10, pady=10, sticky="e")
kullaniciEntry.grid(row=2, column=1, padx=10, pady=10)
sifreLabel.grid(row=3, column=0, padx=10, pady=10, sticky="e")
sifreEntry.grid(row=3, column=1, padx=10, pady=10)
girisButton.grid(row=4, column=0, columnspan=2, pady=20)
hesapYokLabel.grid(row=5, column=0, columnspan=2)

hesapYokLabel.bind("<Button-1>", lambda e: kayit_ac())

root.mainloop()
