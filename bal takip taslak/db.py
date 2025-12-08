import mysql.connector

def baglanti_kur():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="14531453",  # Kendi şifreni yaz
            database="bal_takip"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Veritabani hatasi: {err}")
        return None
