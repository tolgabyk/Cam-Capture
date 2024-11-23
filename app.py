import cv2
import time
import os
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread

# Varsayılan ayarlar
kamera_id = 1
dosya_yolu = os.getcwd()
dosya_ismi = '%Y-%m-%d--%H-%M-%S'
uzanti = '.jpg'
aralik = 5
kayit_durumu = False  

def foto_yakala():
    
    global kayit_durumu
    yakala = cv2.VideoCapture(kamera_id)
    while kayit_durumu:
        ret, frame = yakala.read()
        if ret and frame is not None:
            
            dosya_yolu_str = dosya_yolu.get()
            foto_ismi = datetime.datetime.today().strftime(dosya_ismi) + uzanti
            cv2.imwrite(os.path.join(dosya_yolu_str, foto_ismi), frame)
        time.sleep(aralik)
    yakala.release()

def baslat():

    global kayit_durumu, kamera_id, aralik
    try:
        kamera_id = int(kamera_id_giris.get())
        aralik = int(aralik_giris.get())
    except ValueError:
        messagebox.showerror("Hata", "Kamera ID veya Aralık değeri geçersiz!")
        return
    
    if not kayit_durumu:
        kayit_durumu = True
        Thread(target=foto_yakala).start()
        messagebox.showinfo("Başlatıldı", "Fotoğraf çekme işlemi başlatıldı.")
    else:
        messagebox.showwarning("Zaten Çalışıyor", "Fotoğraf çekme işlemi zaten çalışıyor.")

def durdur():

    global kayit_durumu
    if kayit_durumu:
        kayit_durumu = False
        messagebox.showinfo("Durduruldu", "Fotoğraf çekme işlemi durduruldu.")
    else:
        messagebox.showwarning("Zaten Durduruldu", "Fotoğraf çekme işlemi zaten durdurulmuş.")

def dosya_yolu_sectir():

    global dosya_yolu
    yeni_yol = filedialog.askdirectory(title="Kayıt Klasörünü Seç")
    if yeni_yol:
        dosya_yolu.set(yeni_yol)


pencere = tk.Tk()
pencere.title("Fotoğraf Yakalama Aracı")
pencere.geometry("400x350")


tk.Label(pencere, text="Kamera ID:").pack(pady=5)
kamera_id_giris = tk.Entry(pencere)
kamera_id_giris.insert(0, str(kamera_id))
kamera_id_giris.pack(pady=5)


tk.Label(pencere, text="Fotoğraf Aralığı (saniye):").pack(pady=5)
aralik_giris = tk.Entry(pencere)
aralik_giris.insert(0, str(aralik))
aralik_giris.pack(pady=5)


tk.Label(pencere, text="Kayıt Yolu:").pack(pady=5)
dosya_yolu = tk.StringVar(value=dosya_yolu)
dosya_yolu_etiket = tk.Label(pencere, textvariable=dosya_yolu, wraplength=350, anchor="w")
dosya_yolu_etiket.pack(pady=5)
tk.Button(pencere, text="Kayıt Klasörünü Seç", command=dosya_yolu_sectir).pack(pady=5)


tk.Button(pencere, text="Başlat", command=baslat, bg="green", fg="white").pack(pady=10)
tk.Button(pencere, text="Durdur", command=durdur, bg="red", fg="white").pack(pady=10)


pencere.mainloop()
