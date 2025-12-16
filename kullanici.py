from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import sys
from baglanti import veritabani_baglanti, baglanti_kapat
kullanici_adi = sys.argv[1] if len(sys.argv) > 1 else "Kullanıcı"
musteri_id = None
def get_musteri_id():
    global musteri_id
    if musteri_id is None:
        baglanti = veritabani_baglanti()
        cursor = baglanti.cursor(dictionary=True)
        cursor.execute("SELECT musteri_id FROM musteriler WHERE kullanici_adi=%s", (kullanici_adi,))
        result = cursor.fetchone()
        if result:
            musteri_id = result['musteri_id']
        baglanti_kapat(baglanti)
    return musteri_id
def cikis():
    cevap = messagebox.askyesno("Çıkış", "Emin misiniz?")
    if cevap:
        root.destroy()
def aricilar():
    ariciPencere = Toplevel()
    ariciPencere.title("Arıcılar")
    ariciPencere.geometry("1100x500")
    ariciPencere.resizable(False, False)
    ariciPencere.config(bg="#8e4200")
    icon = PhotoImage(file='minecraft-bee.png')
    ariciPencere.iconphoto(True, icon)
    
    Label(ariciPencere, text="Arıcı Listesi", font=("Times New Roman", 20), 
          bg="#8e4200", fg="white").grid(row=0, column=0, pady=10, sticky=EW)
    
    frameArici = Frame(ariciPencere, bg="#8e4200")
    frameArici.grid(row=1, column=0, sticky=NSEW, padx=10, pady=10)
    
    ariciTree = ttk.Treeview(frameArici)
    ariciTree['columns'] = ("ID", "Ad Soyad", "Telefon", "AKS Kod", "Şehir", "Köy", 
                            "Arıcılık Türü", "Üretim Türü", "Kovan Sayısı")
    ariciTree.column("#0", width=0, stretch=NO)
    ariciTree.column("ID", width=50, anchor=CENTER)
    ariciTree.column("Ad Soyad", width=150, anchor=W)
    ariciTree.column("Telefon", width=110, anchor=CENTER)
    ariciTree.column("AKS Kod", width=120, anchor=CENTER)
    ariciTree.column("Şehir", width=100, anchor=CENTER)
    ariciTree.column("Köy", width=100, anchor=CENTER)
    ariciTree.column("Arıcılık Türü", width=120, anchor=CENTER)
    ariciTree.column("Üretim Türü", width=150, anchor=CENTER)
    ariciTree.column("Kovan Sayısı", width=100, anchor=CENTER)
    ariciTree.heading("ID", text="ID")
    ariciTree.heading("Ad Soyad", text="Ad Soyad")
    ariciTree.heading("Telefon", text="Telefon")
    ariciTree.heading("AKS Kod", text="AKS Kod")
    ariciTree.heading("Şehir", text="Şehir")
    ariciTree.heading("Köy", text="Köy")
    ariciTree.heading("Arıcılık Türü", text="Arıcılık Türü")
    ariciTree.heading("Üretim Türü", text="Üretim Türü")
    ariciTree.heading("Kovan Sayısı", text="Kovan Sayısı")
    
    scrollbar = ttk.Scrollbar(frameArici, orient=VERTICAL, command=ariciTree.yview)
    ariciTree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky=NS)
    ariciTree.grid(row=0, column=0, sticky=NSEW)
    
    baglanti = veritabani_baglanti()
    cursor = baglanti.cursor(dictionary=True)
    cursor.execute("""
        SELECT arici_id, isim, soyisim, telefon, aks_kod, sehir, koy, 
               aricilik_turu, uretim_turu, kovan_sayisi 
        FROM aricilar WHERE aktif=1 ORDER BY arici_id
    """)
    aricilar_list = cursor.fetchall()
    baglanti_kapat(baglanti)
    for arici in aricilar_list:
        ariciTree.insert("", END, values=(
            arici['arici_id'],
            f"{arici['isim']} {arici['soyisim']}",
            arici['telefon'],
            arici['aks_kod'],
            arici['sehir'],
            arici['koy'] or "-",
            arici['aricilik_turu'],
            arici['uretim_turu'],
            arici['kovan_sayisi']
        ))
def degerlendirmelerim():
    degerPencere = Toplevel()
    degerPencere.title("Değerlendirmelerim")
    degerPencere.geometry("900x450")
    degerPencere.resizable(False, False)
    degerPencere.config(bg="#8e4200")
    icon = PhotoImage(file='minecraft-bee.png')
    degerPencere.iconphoto(True, icon)
    
    Label(degerPencere, text="Değerlendirmelerim", font=("Times New Roman", 20), 
          bg="#8e4200", fg="white").grid(row=0, column=0, pady=10, sticky=EW)
    
    frameDeger = Frame(degerPencere, bg="#8e4200")
    frameDeger.grid(row=1, column=0, sticky=NSEW, padx=10, pady=10)
    
    degerTree = ttk.Treeview(frameDeger)
    degerTree['columns'] = ("ID", "Bal Adı", "Yıldız", "Yorum", "Tarih", "Onay")
    degerTree.column("#0", width=0, stretch=NO)
    degerTree.column("ID", width=50, anchor=CENTER)
    degerTree.column("Bal Adı", width=200, anchor=W)
    degerTree.column("Yıldız", width=80, anchor=CENTER)
    degerTree.column("Yorum", width=300, anchor=W)
    degerTree.column("Tarih", width=150, anchor=CENTER)
    degerTree.column("Onay", width=100, anchor=CENTER)
    degerTree.heading("ID", text="ID")
    degerTree.heading("Bal Adı", text="Bal Adı")
    degerTree.heading("Yıldız", text="Yıldız")
    degerTree.heading("Yorum", text="Yorum")
    degerTree.heading("Tarih", text="Tarih")
    degerTree.heading("Onay", text="Durum")
    
    scrollbar = ttk.Scrollbar(frameDeger, orient=VERTICAL, command=degerTree.yview)
    degerTree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky=NS)
    degerTree.grid(row=0, column=0, sticky=NSEW)
    
    def degerlendirmeleri_yukle():
        for item in degerTree.get_children():
            degerTree.delete(item)
        baglanti = veritabani_baglanti()
        cursor = baglanti.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.degerlendirme_id, b.bal_isim, d.yildiz, d.yorum, d.tarih, d.onaylandi
            FROM degerlendirmeler d
            JOIN ballar b ON d.bal_id = b.bal_id
            WHERE d.musteri_id = %s
            ORDER BY d.tarih DESC
        """, (get_musteri_id(),))
        degerlendirmeler = cursor.fetchall()
        baglanti_kapat(baglanti)
        for deg in degerlendirmeler:
            durum = "Onaylandı" if deg['onaylandi'] else "Bekliyor"
            tarih = deg['tarih'].strftime("%Y-%m-%d %H:%M") if deg['tarih'] else ""
            degerTree.insert("", END, values=(
                deg['degerlendirme_id'],
                deg['bal_isim'],
                "*" * deg['yildiz'],
                deg['yorum'] or "-",
                tarih,
                durum
            ))
    def degerlendirme_sil():
        secili = degerTree.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen silinecek değerlendirmeyi seçin.")
            return
        cevap = messagebox.askyesno("Silme Onayı", "Bu değerlendirmeyi silmek istediğinize emin misiniz?")
        if not cevap:
            return
        degerlendirme_id = degerTree.item(secili[0])['values'][0]
        baglanti = veritabani_baglanti()
        cursor = baglanti.cursor()
        cursor.execute("DELETE FROM degerlendirmeler WHERE degerlendirme_id=%s", (degerlendirme_id,))
        baglanti.commit()
        baglanti_kapat(baglanti)
        messagebox.showinfo("Başarılı", "Değerlendirme silindi.")
        degerlendirmeleri_yukle()
    frameButon = Frame(degerPencere, bg="#8e4200")
    frameButon.grid(row=2, column=0, pady=10)
    Button(frameButon, text="Sil", command=degerlendirme_sil, bg="#773903", 
           fg='orange', font=("Georgia", 11)).grid(row=0, column=0, padx=5)
    degerlendirmeleri_yukle()
def ballari_yukle():
    for item in balTree.get_children():
        balTree.delete(item)
    sehir_filtre = sehirCombo.get()
    bal_cinsi_filtre = balCinsiCombo.get()
    uretim_filtre = uretimCombo.get()
    baglanti = veritabani_baglanti()
    cursor = baglanti.cursor(dictionary=True)
    sql = """
        SELECT b.bal_id, b.bal_isim, b.bal_cinsi, 
               CASE 
                   WHEN b.bal_cinsi = 'Cicek Bali' THEN cb.bal_adi
                   ELSE sb.bal_adi
               END AS bal_turu,
               CONCAT(rs.renk_adi, ' (', rs.mm_aralik, ')') AS renk,
               CASE WHEN b.stok_miktari > 0 THEN 'Stokta' ELSE 'Tükendi' END AS stok,
               a.sehir, a.aricilik_turu, a.aks_kod, b.fiyat, a.uretim_turu
        FROM ballar b
        LEFT JOIN cicek_ballari cb ON b.cicek_bal_id = cb.cicek_bal_id
        LEFT JOIN salgi_ballari sb ON b.salgi_bal_id = sb.salgi_bal_id
        LEFT JOIN renk_skalasi rs ON b.renk_id = rs.renk_id
        LEFT JOIN aricilar a ON b.arici_id = a.arici_id
        WHERE b.aktif = 1
    """
    params = []
    if sehir_filtre and sehir_filtre!= "Tümü":
        sql += " AND a.sehir = %s"
        params.append(sehir_filtre)
    if bal_cinsi_filtre and bal_cinsi_filtre!= "Tümü":
        sql += " AND b.bal_cinsi = %s"
        params.append(bal_cinsi_filtre)
    if uretim_filtre and uretim_filtre!= "Tümü":
        sql += " AND a.uretim_turu = %s"
        params.append(uretim_filtre)
    sql += " ORDER BY b.bal_id"
    cursor.execute(sql, params)
    ballar = cursor.fetchall()
    baglanti_kapat(baglanti)
    for bal in ballar:
        balTree.insert("", END, values=(
            bal['bal_id'],
            bal['bal_turu'],
            bal['bal_cinsi'],
            bal['renk'],
            bal['stok'],
            bal['sehir'],
            bal['aricilik_turu'],
            bal['aks_kod'],
            f"{bal['fiyat']:.2f} ₺"
        ))

def bal_sec(event):
    secili = balTree.selection()
    if not secili:
        return
    bal_id = balTree.item(secili[0])['values'][0]
    bal_adi = balTree.item(secili[0])['values'][1]
    degerPencere = Toplevel()
    degerPencere.title(f"Değerlendirme - {bal_adi}")
    degerPencere.geometry("550x500")
    degerPencere.resizable(False, False)
    degerPencere.config(bg="#8e4200")
    icon = PhotoImage(file='minecraft-bee.png')
    degerPencere.iconphoto(True, icon)
    frame = Frame(degerPencere, bg="#8e4200", padx=20, pady=20)
    frame.grid(row=0, column=0)
    
    Label(frame, text=f"Bal: {bal_adi}", font=("Times New Roman", 16), 
          bg="#8e4200", fg="white").grid(row=0, column=0, columnspan=2, pady=10)
    baglanti = veritabani_baglanti()
    cursor = baglanti.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM degerlendirmeler 
        WHERE bal_id=%s AND musteri_id=%s
    """, (bal_id, get_musteri_id()))
    mevcut_deger = cursor.fetchone()
    baglanti_kapat(baglanti)
    if mevcut_deger:
        Label(frame, text="Bu balı zaten değerlendirdiniz!", font=("Georgia", 12), 
              bg="#8e4200", fg="#ffb825").grid(row=1, column=0, columnspan=2, pady=10)
        Label(frame, text=f"Yıldız: {'*' * mevcut_deger['yildiz']}", font=("Georgia", 12), 
              bg="#8e4200", fg="white").grid(row=2, column=0, columnspan=2, pady=5)
        Label(frame, text=f"Yorum: {mevcut_deger['yorum'] or 'Yorum yok'}", font=("Georgia", 10), 
              bg="#8e4200", fg="white", wraplength=400).grid(row=3, column=0, columnspan=2, pady=5)
        durum = "Onaylandı" if mevcut_deger['onaylandi'] else "Onay Bekliyor"
        Label(frame, text=f"Durum: {durum}", font=("Georgia", 10), 
              bg="#8e4200", fg="#ffb825").grid(row=4, column=0, columnspan=2, pady=5)
        return
    Label(frame, text="Yıldız Puanı:", font=("Georgia", 12), 
          bg="#8e4200", fg="#ffd69c").grid(row=1, column=0, sticky=W, pady=10)
    yildizVar = IntVar(value=5)
    frameYildiz = Frame(frame, bg="#8e4200")
    frameYildiz.grid(row=1, column=1, pady=10, sticky=W)
    for i in range(1, 6):
        Radiobutton(frameYildiz, text=f"{'*' * i}", variable=yildizVar, value=i, 
                   bg="#8e4200", fg="white", font=("Georgia", 10), 
                   selectcolor="#8e4200", activebackground="#8e4200").grid(row=i-1, column=0, sticky=W)
    Label(frame, text="Yorumunuz:", font=("Georgia", 12), 
          bg="#8e4200", fg="#ffd69c").grid(row=2, column=0, sticky=NW, pady=10)
    yorumText = Text(frame, width=35, height=8, font=("Georgia", 10))
    yorumText.grid(row=2, column=1, pady=10)
    def degerlendirme_kaydet():
        yildiz = yildizVar.get()
        yorum = yorumText.get("1.0", END).strip()
        baglanti = veritabani_baglanti()
        cursor = baglanti.cursor()
        cursor.execute("""
            INSERT INTO degerlendirmeler (bal_id, musteri_id, yildiz, yorum) 
            VALUES (%s, %s, %s, %s)
        """, (bal_id, get_musteri_id(), yildiz, yorum if yorum else None))
        baglanti.commit()
        baglanti_kapat(baglanti)
        messagebox.showinfo("Başarılı", "Değerlendirmeniz kaydedildi!")
        degerPencere.destroy()
    Button(frame, text="Kaydet", command=degerlendirme_kaydet, bg="#773903", 
           fg='orange', font=("Georgia", 12), activebackground='orange',
           activeforeground='white').grid(row=3, column=0, columnspan=2, pady=20)
    
root = Tk()
root.title("Bal Kaynak Sistemi | Kullanıcı Ekranı")
pencere_genislik = 1200
pencere_yukseklik = 700
ekran_genislik = root.winfo_screenwidth()
ekran_yukseklik = root.winfo_screenheight()
x = (ekran_genislik - pencere_genislik) // 2
y = (ekran_yukseklik - pencere_yukseklik) // 2
root.geometry(f"{pencere_genislik}x{pencere_yukseklik}+{x}+{y}")
root.resizable(False, False)
icon = PhotoImage(file='minecraft-bee.png')
root.iconphoto(True, icon)
root.config(background="#8e4200")

menubar = Menu(root)
menubar.add_command(label="Arıcılar", command=aricilar)
menubar.add_command(label="Değerlendirmelerim", command=degerlendirmelerim)
menubar.add_command(label="Hakkında", command=lambda: messagebox.showinfo("Hakkında", 
                    "Bal Kaynak Sistemi v1.0\nGeliştirici: Serena Üzümcü & Ali Eren Onyıl"))
menubar.add_command(label="Çıkış", command=cikis)

baglanti = veritabani_baglanti()
isim = "Kullanıcı"
cursor = baglanti.cursor(dictionary=True)
kullaniciSql = "SELECT isim FROM musteriler WHERE kullanici_adi=%s"
cursor.execute(kullaniciSql, (kullanici_adi,))
kullanici = cursor.fetchone()
if kullanici:
    isim = kullanici['isim']
baglanti_kapat(baglanti)

frame = Frame(root, bg="#8e4200")
frame.grid(row=0, column=0, pady=5, sticky=EW)
hosgeldinLabel = Label(frame, text=f"Hoşgeldiniz, {isim}!", font=("Times New Roman", 24), 
                       bg="#8e4200", fg="white")
hosgeldinLabel.grid(row=0, column=0, pady=10)

frameFiltre = Frame(root, bg="#8e4200", padx=20, pady=10)
frameFiltre.grid(row=1, column=0, pady=5, sticky=EW)
Label(frameFiltre, text="Filtrele:", font=("Georgia", 12, "bold"), 
      bg="#8e4200", fg="#ffd69c").grid(row=0, column=0, padx=5)
Label(frameFiltre, text="Şehir:", font=("Georgia", 10), 
      bg="#8e4200", fg="#ffd69c").grid(row=0, column=1, padx=5)

baglanti = veritabani_baglanti()
cursor = baglanti.cursor()
cursor.execute("SELECT DISTINCT sehir FROM aricilar ORDER BY sehir")
sehirler = ["Tümü"] + [row[0] for row in cursor.fetchall()]
baglanti_kapat(baglanti)
sehirCombo = ttk.Combobox(frameFiltre, values=sehirler, state="readonly", width=15)
sehirCombo.set("Tümü")
sehirCombo.grid(row=0, column=2, padx=5)
Label(frameFiltre, text="Bal Cinsi:", font=("Georgia", 10), 
      bg="#8e4200", fg="#ffd69c").grid(row=0, column=3, padx=5)
balCinsiCombo = ttk.Combobox(frameFiltre, values=["Tümü", "Cicek Bali", "Salgi Bali"], 
                             state="readonly", width=15)
balCinsiCombo.set("Tümü")
balCinsiCombo.grid(row=0, column=4, padx=5)
Label(frameFiltre, text="Üretim Türü:", font=("Georgia", 10), 
      bg="#8e4200", fg="#ffd69c").grid(row=0, column=5, padx=5)
uretimCombo = ttk.Combobox(frameFiltre, values=["Tümü", "Organik", "Konvansiyonel", 
                           "Cografi Isaret Tescil Belgeli"], state="readonly", width=20)
uretimCombo.set("Tümü")
uretimCombo.grid(row=0, column=6, padx=5)
Button(frameFiltre, text="Ara", command=ballari_yukle, bg="#773903", 
       fg='orange', font=("Georgia", 10)).grid(row=0, column=7, padx=10)

frameTree = Frame(root, bg="#8e4200")
frameTree.grid(row=2, column=0, sticky=NSEW, padx=20, pady=10)

balTree = ttk.Treeview(frameTree, height=20)
balTree['columns'] = ("ID", "Bal Türü", "Bal Cinsi", "Renk", "Stok Durumu", 
                      "Şehir", "Arıcılık Türü", "AKS Kod", "Fiyat")

balTree.column("#0", width=0, stretch=NO)
balTree.column("ID", width=50, anchor=CENTER)
balTree.column("Bal Türü", width=150, anchor=CENTER)
balTree.column("Bal Cinsi", width=120, anchor=CENTER)
balTree.column("Renk", width=200, anchor=CENTER)
balTree.column("Stok Durumu", width=100, anchor=CENTER)
balTree.column("Şehir", width=120, anchor=CENTER)
balTree.column("Arıcılık Türü", width=120, anchor=CENTER)
balTree.column("AKS Kod", width=130, anchor=CENTER)
balTree.column("Fiyat", width=100, anchor=E)
balTree.heading("ID", text="ID")
balTree.heading("Bal Türü", text="Bal Türü")
balTree.heading("Bal Cinsi", text="Bal Cinsi")
balTree.heading("Renk", text="Renk")
balTree.heading("Stok Durumu", text="Stok Durumu")
balTree.heading("Şehir", text="Şehir")
balTree.heading("Arıcılık Türü", text="Arıcılık Türü")
balTree.heading("AKS Kod", text="AKS Kod")
balTree.heading("Fiyat", text="Fiyat")

scrollbar = ttk.Scrollbar(frameTree, orient=VERTICAL, command=balTree.yview)
balTree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky=NS)
balTree.grid(row=0, column=0, sticky=NSEW)
balTree.bind("<Double-1>", bal_sec)

Label(root, text="İpucu: Bal üzerine çift tıklayarak değerlendirme yapabilirsiniz", 
      font=("Georgia", 9), bg="#8e4200", fg="#ffb825").grid(row=3, column=0, pady=5)

root.config(menu=menubar)
ballari_yukle()
root.mainloop()