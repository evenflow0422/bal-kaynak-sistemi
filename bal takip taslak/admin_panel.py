from tkinter import *
from tkinter import ttk, messagebox
import os
from db import baglanti_kur

# Session bilgisini oku
admin_id = 1
admin_isim = "Admin"
try:
    with open("session.txt", "r") as f:
        session = f.read().split(",")
        if session[0] == "admin":
            admin_id = int(session[1])
            admin_isim = session[2]
except:
    pass

root = Tk()
root.title(f"Bal Kaynak Sistemi | Admin Paneli - {admin_isim}")

pencere_genislik = 1000
pencere_yukseklik = 600
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

def cicek_turleri():
    conn = baglanti_kur()
    cursor = conn.cursor()
    cursor.execute("SELECT cicek_bal_id, bal_adi FROM cicek_ballari")
    sonuc = cursor.fetchall()
    cursor.close()
    conn.close()
    return sonuc

def salgi_turleri():
    conn = baglanti_kur()
    cursor = conn.cursor()
    cursor.execute("SELECT salgi_bal_id, bal_adi FROM salgi_ballari")
    sonuc = cursor.fetchall()
    cursor.close()
    conn.close()
    return sonuc

def renk_listesi():
    conn = baglanti_kur()
    cursor = conn.cursor()
    cursor.execute("SELECT renk_id, CONCAT(mm_aralik, ' - ', renk_adi) FROM renk_skalasi")
    sonuc = cursor.fetchall()
    cursor.close()
    conn.close()
    return sonuc

def arici_listesi():
    conn = baglanti_kur()
    cursor = conn.cursor()
    cursor.execute("SELECT arici_id, CONCAT(isim, ' ', soyisim) FROM aricilar")
    sonuc = cursor.fetchall()
    cursor.close()
    conn.close()
    return sonuc

# ========== ARAYUZ ==========
ustFrame = Frame(root, bg="#ffd69c")
ustFrame.pack(fill="x", padx=10, pady=10)

Label(ustFrame, text="Admin Paneli", font=("Arial", 18, "bold"), bg="#ffd69c").pack(side="left")
Button(ustFrame, text="Cikis Yap", command=cikis_yap, bg="white", fg="red").pack(side="right")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# ===== BAL SEKMESI =====
bal_frame = Frame(notebook, bg="#ffd69c")
notebook.add(bal_frame, text="  Ballar  ")

bal_buton_frame = Frame(bal_frame, bg="#ffd69c")
bal_buton_frame.pack(fill="x", pady=10)

bal_tablo_frame = Frame(bal_frame)
bal_tablo_frame.pack(fill="both", expand=True)

bal_kolonlar = ("ID", "Bal Ismi", "Cinsi", "Turu", "Rengi", "Fiyat", "Stok", "Arici", "Durum")
bal_tablo = ttk.Treeview(bal_tablo_frame, columns=bal_kolonlar, show="headings", height=15)

for kolon in bal_kolonlar:
    bal_tablo.heading(kolon, text=kolon)
    bal_tablo.column(kolon, width=100)

bal_tablo.column("Bal Ismi", width=150)

bal_scroll = ttk.Scrollbar(bal_tablo_frame, orient="vertical", command=bal_tablo.yview)
bal_tablo.configure(yscrollcommand=bal_scroll.set)
bal_tablo.pack(side="left", fill="both", expand=True)
bal_scroll.pack(side="right", fill="y")

# ===== ARICI SEKMESI =====
arici_frame = Frame(notebook, bg="#ffd69c")
notebook.add(arici_frame, text="  Aricilar  ")

arici_buton_frame = Frame(arici_frame, bg="#ffd69c")
arici_buton_frame.pack(fill="x", pady=10)

arici_tablo_frame = Frame(arici_frame)
arici_tablo_frame.pack(fill="both", expand=True)

arici_kolonlar = ("ID", "Isim", "Soyisim", "Telefon", "AKS Kod", "Sehir", "Aricilik", "Uretim", "Kovan", "Tipi")
arici_tablo = ttk.Treeview(arici_tablo_frame, columns=arici_kolonlar, show="headings", height=15)

for kolon in arici_kolonlar:
    arici_tablo.heading(kolon, text=kolon)
    arici_tablo.column(kolon, width=90)

arici_scroll = ttk.Scrollbar(arici_tablo_frame, orient="vertical", command=arici_tablo.yview)
arici_tablo.configure(yscrollcommand=arici_scroll.set)
arici_tablo.pack(side="left", fill="both", expand=True)
arici_scroll.pack(side="right", fill="y")

# ========== FONKSIYONLAR ==========
def ballari_yukle():
    for row in bal_tablo.get_children():
        bal_tablo.delete(row)
    
    conn = baglanti_kur()
    if conn is None:
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM v_bal_detay")
    ballar = cursor.fetchall()
    
    for bal in ballar:
        durum = "Aktif" if bal[14] == 1 else "Pasif"
        bal_tablo.insert("", "end", values=(
            bal[0], bal[1], bal[2], bal[3], bal[4], 
            f"{bal[5]} TL", bal[6], bal[8], durum
        ))
    
    cursor.close()
    conn.close()

def aricilari_yukle():
    for row in arici_tablo.get_children():
        arici_tablo.delete(row)
    
    conn = baglanti_kur()
    if conn is None:
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM aricilar")
    aricilar = cursor.fetchall()
    
    for arici in aricilar:
        tipi = "Profesyonel" if arici[9] >= 50 else "Hobi"
        arici_tablo.insert("", "end", values=(
            arici[0], arici[1], arici[2], arici[3], 
            arici[4], arici[5], arici[7], arici[8], arici[9], tipi
        ))
    
    cursor.close()
    conn.close()

def bal_ekle_pencere():
    pencere = Toplevel(root)
    pencere.title("Yeni Bal Ekle")
    pencere.geometry("400x500")
    pencere.config(background="#ffd69c")
    
    Label(pencere, text="Yeni Bal Ekle", font=("Arial", 14, "bold"), bg="#ffd69c").pack(pady=10)
    
    frame = Frame(pencere, bg="#ffd69c")
    frame.pack(pady=10)
    
    Label(frame, text="Bal Ismi:", bg="#ffd69c").grid(row=0, column=0, pady=5, sticky="e")
    isim_entry = Entry(frame, width=25)
    isim_entry.grid(row=0, column=1, pady=5)
    
    Label(frame, text="Bal Cinsi:", bg="#ffd69c").grid(row=1, column=0, pady=5, sticky="e")
    cinsi_var = StringVar(value="Cicek Bali")
    cinsi_combo = ttk.Combobox(frame, textvariable=cinsi_var, values=["Cicek Bali", "Salgi Bali"], state="readonly", width=22)
    cinsi_combo.grid(row=1, column=1, pady=5)
    
    Label(frame, text="Bal Turu:", bg="#ffd69c").grid(row=2, column=0, pady=5, sticky="e")
    turu_combo = ttk.Combobox(frame, state="readonly", width=22)
    turu_combo.grid(row=2, column=1, pady=5)
    
    def cinsi_degisti(e):
        if cinsi_var.get() == "Cicek Bali":
            turler = [t[1] for t in cicek_turleri()]
        else:
            turler = [t[1] for t in salgi_turleri()]
        turu_combo['values'] = turler
        if turler:
            turu_combo.set(turler[0])
    
    cinsi_combo.bind("<<ComboboxSelected>>", cinsi_degisti)
    cinsi_degisti(None)
    
    Label(frame, text="Renk:", bg="#ffd69c").grid(row=3, column=0, pady=5, sticky="e")
    renkler = renk_listesi()
    renk_combo = ttk.Combobox(frame, values=[r[1] for r in renkler], state="readonly", width=22)
    renk_combo.grid(row=3, column=1, pady=5)
    if renkler:
        renk_combo.set(renkler[0][1])
    
    Label(frame, text="Arici:", bg="#ffd69c").grid(row=4, column=0, pady=5, sticky="e")
    aricilar = arici_listesi()
    arici_combo = ttk.Combobox(frame, values=[a[1] for a in aricilar], state="readonly", width=22)
    arici_combo.grid(row=4, column=1, pady=5)
    if aricilar:
        arici_combo.set(aricilar[0][1])
    
    Label(frame, text="Fiyat (TL):", bg="#ffd69c").grid(row=5, column=0, pady=5, sticky="e")
    fiyat_entry = Entry(frame, width=25)
    fiyat_entry.grid(row=5, column=1, pady=5)
    
    Label(frame, text="Stok:", bg="#ffd69c").grid(row=6, column=0, pady=5, sticky="e")
    stok_entry = Entry(frame, width=25)
    stok_entry.grid(row=6, column=1, pady=5)
    
    Label(frame, text="Agirlik (gram):", bg="#ffd69c").grid(row=7, column=0, pady=5, sticky="e")
    agirlik_entry = Entry(frame, width=25)
    agirlik_entry.grid(row=7, column=1, pady=5)
    
    def kaydet():
        isim = isim_entry.get()
        cinsi = cinsi_var.get()
        turu = turu_combo.get()
        renk = renk_combo.get()
        arici = arici_combo.get()
        fiyat = fiyat_entry.get()
        stok = stok_entry.get()
        agirlik = agirlik_entry.get()
        
        if not all([isim, turu, renk, arici, fiyat, stok]):
            messagebox.showwarning("Uyari", "Tum alanlari doldurun!")
            return
        
        conn = baglanti_kur()
        cursor = conn.cursor()
        
        renk_id = [r[0] for r in renkler if r[1] == renk][0]
        arici_id = [a[0] for a in aricilar if a[1] == arici][0]
        
        if cinsi == "Cicek Bali":
            cicek_id = [t[0] for t in cicek_turleri() if t[1] == turu][0]
            salgi_id = None
        else:
            cicek_id = None
            salgi_id = [t[0] for t in salgi_turleri() if t[1] == turu][0]
        
        try:
            sorgu = """INSERT INTO ballar (bal_isim, bal_cinsi, cicek_bal_id, salgi_bal_id, 
                       renk_id, arici_id, fiyat, stok_miktari, agirlik_gram) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sorgu, (isim, cinsi, cicek_id, salgi_id, renk_id, arici_id, 
                                   float(fiyat), int(stok), int(agirlik) if agirlik else None))
            conn.commit()
            messagebox.showinfo("Basarili", "Bal eklendi!")
            pencere.destroy()
            ballari_yukle()
        except Exception as e:
            messagebox.showerror("Hata", f"Hata: {e}")
        
        cursor.close()
        conn.close()
    
    Button(pencere, text="Kaydet", command=kaydet, bg="white", fg="orange", width=15).pack(pady=20)

def bal_sil():
    secili = bal_tablo.selection()
    if not secili:
        messagebox.showwarning("Uyari", "Lutfen bir bal secin!")
        return
    
    bal_id = bal_tablo.item(secili[0])['values'][0]
    bal_isim = bal_tablo.item(secili[0])['values'][1]
    
    cevap = messagebox.askyesno("Onay", f"'{bal_isim}' balini silmek istediginize emin misiniz?")
    if not cevap:
        return
    
    conn = baglanti_kur()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM ballar WHERE bal_id = %s", (bal_id,))
        conn.commit()
        messagebox.showinfo("Basarili", "Bal silindi!")
        ballari_yukle()
    except Exception as e:
        messagebox.showerror("Hata", f"Hata: {e}")
    
    cursor.close()
    conn.close()

def bal_durum_degistir():
    secili = bal_tablo.selection()
    if not secili:
        messagebox.showwarning("Uyari", "Lutfen bir bal secin!")
        return
    
    bal_id = bal_tablo.item(secili[0])['values'][0]
    
    conn = baglanti_kur()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE ballar SET aktif = NOT aktif WHERE bal_id = %s", (bal_id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    messagebox.showinfo("Basarili", "Durum degistirildi!")
    ballari_yukle()

def arici_ekle_pencere():
    pencere = Toplevel(root)
    pencere.title("Yeni Arici Ekle")
    pencere.geometry("400x450")
    pencere.config(background="#ffd69c")
    
    Label(pencere, text="Yeni Arici Ekle", font=("Arial", 14, "bold"), bg="#ffd69c").pack(pady=10)
    
    frame = Frame(pencere, bg="#ffd69c")
    frame.pack(pady=10)
    
    labels = ["Isim:", "Soyisim:", "Telefon:", "AKS Kod:", "Sehir:", "Koy:", "Kovan Sayisi:"]
    entries = []
    
    for i, label in enumerate(labels):
        Label(frame, text=label, bg="#ffd69c").grid(row=i, column=0, pady=5, sticky="e")
        entry = Entry(frame, width=25)
        entry.grid(row=i, column=1, pady=5)
        entries.append(entry)
    
    Label(frame, text="Aricilik Turu:", bg="#ffd69c").grid(row=7, column=0, pady=5, sticky="e")
    aricilik_combo = ttk.Combobox(frame, values=["Gezgin", "Sabit"], state="readonly", width=22)
    aricilik_combo.set("Sabit")
    aricilik_combo.grid(row=7, column=1, pady=5)
    
    Label(frame, text="Uretim Turu:", bg="#ffd69c").grid(row=8, column=0, pady=5, sticky="e")
    uretim_combo = ttk.Combobox(frame, values=["Konvansiyonel", "Organik", "Cografi Isaret Tescil Belgeli"], 
                                 state="readonly", width=22)
    uretim_combo.set("Konvansiyonel")
    uretim_combo.grid(row=8, column=1, pady=5)
    
    def kaydet():
        veriler = [e.get() for e in entries]
        
        if not all(veriler[:5]):
            messagebox.showwarning("Uyari", "Zorunlu alanlari doldurun!")
            return
        
        conn = baglanti_kur()
        cursor = conn.cursor()
        
        try:
            sorgu = """INSERT INTO aricilar (isim, soyisim, telefon, aks_kod, sehir, koy, 
                       aricilik_turu, uretim_turu, kovan_sayisi) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sorgu, (veriler[0], veriler[1], veriler[2], veriler[3], 
                                   veriler[4], veriler[5], aricilik_combo.get(), 
                                   uretim_combo.get(), int(veriler[6]) if veriler[6] else 0))
            conn.commit()
            messagebox.showinfo("Basarili", "Arici eklendi!")
            pencere.destroy()
            aricilari_yukle()
        except Exception as e:
            messagebox.showerror("Hata", f"Hata: {e}")
        
        cursor.close()
        conn.close()
    
    Button(pencere, text="Kaydet", command=kaydet, bg="white", fg="orange", width=15).pack(pady=20)

def arici_sil():
    secili = arici_tablo.selection()
    if not secili:
        messagebox.showwarning("Uyari", "Lutfen bir arici secin!")
        return
    
    arici_id = arici_tablo.item(secili[0])['values'][0]
    arici_isim = arici_tablo.item(secili[0])['values'][1]
    
    cevap = messagebox.askyesno("Onay", f"'{arici_isim}' aricisini silmek istediginize emin misiniz?\n(Bagli ballar da silinecek!)")
    if not cevap:
        return
    
    conn = baglanti_kur()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM aricilar WHERE arici_id = %s", (arici_id,))
        conn.commit()
        messagebox.showinfo("Basarili", "Arici silindi!")
        aricilari_yukle()
        ballari_yukle()
    except Exception as e:
        messagebox.showerror("Hata", f"Hata: {e}")
    
    cursor.close()
    conn.close()

# Butonlari ekle
Button(bal_buton_frame, text="Yeni Bal Ekle", command=bal_ekle_pencere, bg="green", fg="white").pack(side="left", padx=5)
Button(bal_buton_frame, text="Secili Bali Sil", command=bal_sil, bg="red", fg="white").pack(side="left", padx=5)
Button(bal_buton_frame, text="Durum Degistir", command=bal_durum_degistir, bg="orange", fg="white").pack(side="left", padx=5)
Button(bal_buton_frame, text="Yenile", command=ballari_yukle, bg="white", fg="black").pack(side="right", padx=5)

Button(arici_buton_frame, text="Yeni Arici Ekle", command=arici_ekle_pencere, bg="green", fg="white").pack(side="left", padx=5)
Button(arici_buton_frame, text="Secili Ariciyi Sil", command=arici_sil, bg="red", fg="white").pack(side="left", padx=5)
Button(arici_buton_frame, text="Yenile", command=aricilari_yukle, bg="white", fg="black").pack(side="right", padx=5)

# Tablolari yukle
ballari_yukle()
aricilari_yukle()

root.mainloop()
