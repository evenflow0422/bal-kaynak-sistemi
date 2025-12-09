import mysql.connector
from mysql.connector import Error
#xampp üzerinden mysql bağlantısı
def veritabani_baglanti():
    try:
        baglanti = mysql.connector.connect(
            host='localhost',          
            database='bal_takip',      
            user='root',               
            password='',               
            charset='utf8mb4'
        )
        
        if baglanti.is_connected():
            return baglanti
        
    except Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None

def baglanti_kapat(baglanti):
    if baglanti and baglanti.is_connected():
        baglanti.close()