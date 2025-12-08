from tkinter import *
from tkinter import ttk, messagebox
import os
from db import baglanti_kur

# Session bilgisini oku
musteri_id = 1
musteri_isim = "Misafir"
try:
    with open("session.txt", "r") as f:
        session = f.read().split(",")
        if session[0] == "musteri":
            musteri_id = int(session[1])
            musteri_isim = session[2]
except:
    pass

root = Tk()
root.title(f"Bal Kaynak Sistemi | {musteri_isim}")

pencere_genislik = 900
pencere_yukseklik = 500
ekran_genislik = root.winfo_screenwidth()
ekran_yukseklik = root.winfo_screenheight()
x = (ekran_genislik - pencere_genislik) // 2
y = (ekran_yukseklik - pencere_yukseklik) // 2
root.geometry(f"{pencere_genislik}x{pencere_yukseklik}+{x}+{y}")

root.config(background="#ffd69c")
icon = PhotoImage(file='minecraft-bee.png')
root.iconphoto(True, icon)

def cikis_yap():
    try:
        os.remove("session.txt")
    except:
        pass
    root.destroy()
    os.system('py giris.py')

def ballari_yukle(filtre_cinsi=None, filtre_turu=None):
    for row in tablo.get_children():
        tablo.delete(row)
    
    conn = baglanti_kur()
    if conn is None:
        messagebox.showerror("Hata", "Veritabani baglantisi kurulamadi!")
        return
    
    cursor = conn.cursor()
    
    sorgu = "SELECT * FROM v_bal_detay WHERE aktif = 1"
    params = []
    
    if filtre_cinsi and filtre_cinsi != "Tumu":
        sorgu += " AND bal_cinsi = %s"
        params.append(filtre_cinsi)
    
    if filtre_turu and filtre_turu != "Tumu":
        sorgu += " AND bal_turu = %s"
        params.append(filtre_turu)
    
    cursor.execute(sorgu, params)
    ballar = cursor.fetchall()
    
    for bal in ballar:
        tablo.insert("", "end", values=(
            bal[0],
            bal[1],
            bal[2],
            bal[3],
            bal[4],
            f"{bal[5]} TL",
            bal[8],
            bal[9],
            bal[15] if bal[15] else "0"
        ))
    
    cursor.close()
    conn.close()

def turleri_yukle():
    conn = baglanti_kur()
    if conn is None:
        return ["Tumu"]
    
    cursor = conn.cursor()
    turler = ["Tumu"]
    
    cursor.execute("SELECT bal_adi FROM cicek_ballari")
    for row in cursor.fetchall():
        turler.append(row[0])
    
    cursor.execute("SELECT bal_adi FROM salgi_ballari")
    for row in cursor.fetchall():
        turler.append(row[0])
    
    cursor.close()
    conn.close()
    return turler

def filtrele():
    cinsi = cinsiCombo.get()
    turu = turuCombo.get()
    ballari_yukle(cinsi, turu)

def degerlendirme_ac():
    secili = tablo.selection()
    if not secili:
        messagebox.showwarning("Uyari", "Lutfen bir bal secin!")
        return
    
    bal_id = tablo.item(secili[0])['values'][0]
    bal_isim = tablo.item(secili[0])['values'][1]
    
    # Onceki degerlendirmeyi kontrol et
    conn = baglanti_kur()
    cursor = conn.cursor()
    cursor.execute("SELECT yildiz, yorum FROM degerlendirmeler WHERE bal_id = %s AND musteri_id = %s", 
                   (bal_id, musteri_id))
    onceki = cursor.fetchone()
    cursor.close()
    conn.close()
    
    deg_pencere = Toplevel(root)
    deg_pencere.title("Degerlendirme Yap")
    deg_pencere.geometry("350x250")
    deg_pencere.config(background="#ffd69c")
    
    Label(deg_pencere, text=f"Bal: {bal_isim}", bg="#ffd69c", font=("Arial", 11, "bold")).pack(pady=10)
    
    if onceki:
        Label(deg_pencere, text="(Onceki degerlendirmenizi guncelleyebilirsiniz)", 
              bg="#ffd69c", fg="gray", font=("Arial", 8)).pack()
    
    Label(deg_pencere, text="Yildiz (1-5):", bg="#ffd69c").pack(pady=5)
    yildiz_var = IntVar(value=onceki[0] if onceki else 5)
    yildiz_spin = Spinbox(deg_pencere, from_=1, to=5, textvariable=yildiz_var, width=5)
    yildiz_spin.pack()
    
    Label(deg_pencere, text="Yorum:", bg="#ffd69c").pack(pady=5)
    yorum_text = Text(deg_pencere, height=4, width=35)
    yorum_text.pack(pady=5)
    if onceki and onceki[1]:
        yorum_text.insert("1.0", onceki[1])
    
    def kaydet():
        yildiz = yildiz_var.get()
        yorum = yorum_text.get("1.0", END).strip()
        
        conn = baglanti_kur()
        if conn is None:
            messagebox.showerror("Hata", "Veritabani hatasi!")
            return
        
        cursor = conn.cursor()
        
        try:
            if onceki:
                # Guncelle
                sorgu = """UPDATE degerlendirmeler SET yildiz = %s, yorum = %s, tarih = NOW() 
                           WHERE bal_id = %s AND musteri_id = %s"""
                cursor.execute(sorgu, (yildiz, yorum, bal_id, musteri_id))
                mesaj = "Degerlendirmeniz guncellendi!"
            else:
                # Yeni ekle
                sorgu = """INSERT INTO degerlendirmeler (bal_id, musteri_id, yildiz, yorum) 
                           VALUES (%s, %s, %s, %s)"""
                cursor.execute(sorgu, (bal_id, musteri_id, yildiz, yorum))
                mesaj = "Degerlendirmeniz kaydedildi!"
            
            conn.commit()
            messagebox.showinfo("Basarili", mesaj)
            deg_pencere.destroy()
            ballari_yukle()
        except Exception as e:
            messagebox.showerror("Hata", f"Hata: {e}")
        
        cursor.close()
        conn.close()
    
    Button(deg_pencere, text="Kaydet", command=kaydet, bg="white", fg="orange", width=15).pack(pady=15)

# Ust Frame
ustFrame = Frame(root, bg="#ffd69c")
ustFrame.pack(fill="x", padx=10, pady=10)

Label(ustFrame, text="Bal Listesi", font=("Arial", 18), bg="#ffd69c").pack(side="left")
Label(ustFrame, text=f"Hosgeldin, {musteri_isim}!", font=("Arial", 10), bg="#ffd69c").pack(side="left", padx=30)
Button(ustFrame, text="Cikis Yap", command=cikis_yap, bg="white", fg="red").pack(side="right")

# Filtre Frame
filtreFrame = Frame(root, bg="#ffd69c")
filtreFrame.pack(fill="x", padx=10)

Label(filtreFrame, text="Bal Cinsi:", bg="#ffd69c").pack(side="left", padx=5)
cinsiCombo = ttk.Combobox(filtreFrame, values=["Tumu", "Cicek Bali", "Salgi Bali"], state="readonly", width=15)
cinsiCombo.set("Tumu")
cinsiCombo.pack(side="left", padx=5)

Label(filtreFrame, text="Bal Turu:", bg="#ffd69c").pack(side="left", padx=5)
turuCombo = ttk.Combobox(filtreFrame, values=turleri_yukle(), state="readonly", width=15)
turuCombo.set("Tumu")
turuCombo.pack(side="left", padx=5)

Button(filtreFrame, text="Filtrele", command=filtrele, bg="white", fg="orange").pack(side="left", padx=10)
Button(filtreFrame, text="Degerlendirme Yap", command=degerlendirme_ac, bg="white", fg="orange").pack(side="right", padx=10)

# Tablo
tabloFrame = Frame(root)
tabloFrame.pack(fill="both", expand=True, padx=10, pady=10)

kolonlar = ("ID", "Bal Ismi", "Cinsi", "Turu", "Rengi", "Fiyat", "Arici", "Sehir", "Puan")
tablo = ttk.Treeview(tabloFrame, columns=kolonlar, show="headings", height=15)

for kolon in kolonlar:
    tablo.heading(kolon, text=kolon)
    tablo.column(kolon, width=80)

tablo.column("Bal Ismi", width=180)
tablo.column("Rengi", width=130)

scrollbar = ttk.Scrollbar(tabloFrame, orient="vertical", command=tablo.yview)
tablo.configure(yscrollcommand=scrollbar.set)

tablo.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

ballari_yukle()

root.mainloop()
