import tkinter as tk
import random
import string

# Kelime listesi
kelimeler = ["PYTHON", "KOD", "OYUN", "BILGISAYAR", "INTERAKTIF", "ARAYUZ", "PROGRAM", "GELISTIRICI"]

# 10x10 oyun tahtası boyutu
boyut = 10
secili_koordinatlar = []  # Seçilen hücrelerin koordinatları
bulunan_kelimeler = set()  # Bulunan kelimeleri kaydetmek için

# Oyun tahtasını ve kelimeleri rastgele harflerle doldur
def oyun_tahtasini_olustur():
    tahtadaki_harfler = [["" for _ in range(boyut)] for _ in range(boyut)]
    for kelime in kelimeler:
        kelimeyi_yerlestir(tahtadaki_harfler, kelime)
    
    # Boş kutucuklara rastgele harfler koy
    for i in range(boyut):
        for j in range(boyut):
            if tahtadaki_harfler[i][j] == "":
                tahtadaki_harfler[i][j] = random.choice(string.ascii_uppercase)
    return tahtadaki_harfler

# Kelimeyi tahtada rastgele bir pozisyona yerleştir
def kelimeyi_yerlestir(tahta, kelime):
    yonler = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    yerlesebilir = False
    deneme_sayisi = 0

    while not yerlesebilir and deneme_sayisi < 100:
        satir = random.randint(0, boyut - 1)
        sutun = random.randint(0, boyut - 1)
        yon = random.choice(yonler)
        
        if yer_kontrol(tahta, kelime, satir, sutun, yon):
            for k in range(len(kelime)):
                tahta[satir + k * yon[0]][sutun + k * yon[1]] = kelime[k]
            yerlesebilir = True
        deneme_sayisi += 1

# Kelimenin belirli bir yönde yerleşebilir olup olmadığını kontrol et
def yer_kontrol(tahta, kelime, satir, sutun, yon):
    for k in range(len(kelime)):
        yeni_satir = satir + k * yon[0]
        yeni_sutun = sutun + k * yon[1]
        
        if not (0 <= yeni_satir < boyut and 0 <= yeni_sutun < boyut):
            return False
        if tahta[yeni_satir][yeni_sutun] != "" and tahta[yeni_satir][yeni_sutun] != kelime[k]:
            return False
    return True

# Yanlış seçilen hücreleri kırmızı yanıp sönerek eski renge döndür
def yanip_son(satir, sutun):
    butonlar[satir][sutun].config(bg="red")
    root.after(300, lambda: butonlar[satir][sutun].config(bg="lightgrey"))

# Seçilen hücreleri kontrol et
def kontrol_et():
    secili_kelime = "".join([tahta[satir][sutun] for satir, sutun in secili_koordinatlar])
    ters_kelime = secili_kelime[::-1]
    
    # Kelimeyi doğru bulduysak renk yeşile döner
    if secili_kelime in kelimeler or ters_kelime in kelimeler:
        bulunan_kelimeler.add(secili_kelime if secili_kelime in kelimeler else ters_kelime)
        
        for satir, sutun in secili_koordinatlar:
            butonlar[satir][sutun].config(bg="green")

        # Listede bulunan kelimeyi yeşil renge döndür
        for widget in kelime_labels:
            if widget.cget("text") == secili_kelime or widget.cget("text") == ters_kelime:
                widget.config(fg="green")

    # Yanlış kelime seçilmişse yanıp söner ve eski haline döner
    else:
        for satir, sutun in secili_koordinatlar:
            yanip_son(satir, sutun)

    # Seçim listesini temizle
    secili_koordinatlar.clear()

# Hücre tıklama işlemi
def hucre_tikla(satir, sutun):
    butonlar[satir][sutun].config(bg="lightblue")
    secili_koordinatlar.append((satir, sutun))

# Tkinter ile oyun tahtası arayüzünü oluştur
def oyun_baslat():
    global tahta, butonlar, kelime_labels
    tahta = oyun_tahtasini_olustur()
    butonlar = [[None for _ in range(boyut)] for _ in range(boyut)]
    kelime_labels = []

    for i in range(boyut):
        for j in range(boyut):
            harf = tahta[i][j]
            button = tk.Button(root, text=harf, width=2, height=1, font=("Arial", 14), bg="lightgrey",
                               fg="darkblue", activebackground="lightblue", activeforeground="darkred",
                               command=lambda i=i, j=j: hucre_tikla(i, j))
            button.grid(row=i, column=j, padx=1, pady=1)
            butonlar[i][j] = button

    # Sağ tarafta kelimeleri listele
    for idx, kelime in enumerate(kelimeler):
        label = tk.Label(root, text=kelime, font=("Arial", 12, "bold"), bg="white", fg="black")
        label.grid(row=idx, column=boyut + 1, padx=5, pady=2, sticky="w")
        kelime_labels.append(label)

    # Kontrol butonunu ve oyun başlatma butonunu alt tarafta yatay hizala
    kontrol_button = tk.Button(root, text="Kelimeyi Kontrol Et", font=("Arial", 10, "bold"), command=kontrol_et)
    kontrol_button.grid(row=boyut + 1, column=0, columnspan=boyut//2, pady=10, sticky="ew")

    baslat_button = tk.Button(root, text="Oyunu Başlat", font=("Arial", 10, "bold"), command=oyun_baslat)
    baslat_button.grid(row=boyut + 1, column=boyut//2, columnspan=boyut//2, pady=10, sticky="ew")

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Kelime Bulmaca Oyunu")
root.geometry(f"{boyut*30 + 200}x{boyut*30}")

# Uygulamayı başlat
oyun_baslat()
root.mainloop()
