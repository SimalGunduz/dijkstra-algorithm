import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

class MarketUygulamasiGUI:
    def _init_(self, root):
        self.root = root
        self.root.title("Market Uygulaması")

        # Yerler
        self.yerler = ["Giriş", "Şarküteri", "Kasap", "Manav", "Kişisel Bakım", 
                       "Temizlik", "Bakliyat", "Atıştırmalık", 
                       "Temel Gıda", "İçecek", "Fırın", "Dolap", "Kasa", "Çıkış"]

        # Başlık etiketi
        baslik = ttk.Label(root, text="Hoş Geldiniz!", font=('Helvetica', 20, 'bold'), foreground='darkblue')
        baslik.grid(row=0, column=0, columnspan=2, pady=20)

        # Gitmek istediğiniz yerler etiketi
        git_yerler_label = ttk.Label(root, text="Gitmek İstediğiniz Yerler:", font=('Helvetica', 16, 'italic'), foreground='darkblue')
        git_yerler_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Yer seçim kutusu
        self.yer_giris = tk.Listbox(root, selectmode=tk.MULTIPLE, font=('Helvetica', 16), selectbackground='darkblue', bg='lightcoral')
        for yer in self.yerler:
            self.yer_giris.insert(tk.END, yer)
        self.yer_giris.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Scrollbar ekle
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.yer_giris.yview)
        scrollbar.grid(row=2, column=2, sticky='ns')
        self.yer_giris.configure(yscrollcommand=scrollbar.set)

        # Butonlar
        self.gidilecek_yeri_sec_button = ttk.Button(root, text="Git", command=self.gidilecek_yeri_sec, style='TButton')
        self.gidilecek_yeri_sec_button.grid(row=3, column=0, pady=20)

        self.temizle_button = ttk.Button(root, text="Temizle", command=self.temizle, style='TButton')
        self.temizle_button.grid(row=3, column=1, pady=20)

        self.graf_buton = ttk.Button(root, text="Grafiği Göster", command=self.ciz_graf, style='TButton')
        self.graf_buton.grid(row=4, column=0, pady=20)

        self.matris_buton = ttk.Button(root, text="Matrisi Göster", command=self.matrisi_goster, style='TButton')
        self.matris_buton.grid(row=4, column=1, pady=20)

        # Stil tanımı
        self.stil = ttk.Style()
        self.stil.configure('TButton', font=('Helvetica', 14, 'bold'), foreground='blue', background='lightblue', padding=10)

    def gidilecek_yeri_sec(self):
        secilen_yerler = self.yer_giris.curselection()
        if secilen_yerler:
            secilen_yerler_text = [self.yerler[index] for index in secilen_yerler]
            messagebox.showinfo("Yerler Seçildi", f"Gideceğiniz yerleri seçiniz: {', '.join(secilen_yerler_text)}")

            # Rasgele mesafelerle bir matris oluştur
            mesafe_matrisi = np.zeros((len(secilen_yerler_text), len(secilen_yerler_text)), dtype=int)
            for i in range(len(secilen_yerler_text)):
                for j in range(i + 1, len(secilen_yerler_text)):
                    mesafe_matrisi[i, j] = random.randint(1, 10)  # Rasgele mesafe (örnek)
                    mesafe_matrisi[j, i] = mesafe_matrisi[i, j]

            # Mesafe matrisini çıktı olarak göster
            self.goster_matris(secilen_yerler_text, mesafe_matrisi)

            # Dijkstra algoritması ile en kısa yolu bul
            en_kisa_yol = nx.shortest_path(self.olustur_graf(secilen_yerler_text, mesafe_matrisi), source=secilen_yerler_text[0], target=secilen_yerler_text[-1], weight="weight")

            # Grafı çizme
            self.ciz_graf(secilen_yerler_text, mesafe_matrisi, en_kisa_yol)

        else:
            messagebox.showerror("Hata", "Lütfen en az bir yer seçin.")

    def olustur_graf(self, yerler, mesafe_matrisi):
        G = nx.Graph()
        for yer in yerler:
            G.add_node(yer)

        for i in range(len(yerler)):
            for j in range(i + 1, len(yerler)):
                G.add_edge(yerler[i], yerler[j], weight=mesafe_matrisi[i, j])

        return G

    def goster_matris(self, yerler, matris):
        matris_str = "\n".join(["\t".join(map(str, row)) for row in matris])
        messagebox.showinfo("Mesafe Matrisi", f"Yerler:\n{', '.join(yerler)}\n\nMesafe Matrisi:\n{matris_str}")

    def ciz_graf(self):
        secilen_yerler = self.yer_giris.curselection()
        if secilen_yerler:
            secilen_yerler_text = [self.yerler[index] for index in secilen_yerler]

            # Rasgele mesafelerle bir matris oluştur
            mesafe_matrisi = np.zeros((len(secilen_yerler_text), len(secilen_yerler_text)), dtype=int)
            for i in range(len(secilen_yerler_text)):
                for j in range(i + 1, len(secilen_yerler_text)):
                    mesafe_matrisi[i, j] = random.randint(1, 10)  # Rasgele mesafe (örnek)
                    mesafe_matrisi[j, i] = mesafe_matrisi[i, j]

            # Dijkstra algoritması ile en kısa yolu bul
            en_kisa_yol = nx.shortest_path(self.olustur_graf(secilen_yerler_text, mesafe_matrisi), source=secilen_yerler_text[0], target=secilen_yerler_text[-1], weight="weight")

            G = self.olustur_graf(secilen_yerler_text, mesafe_matrisi)
            pos = nx.spring_layout(G)

            # Grafikteki tüm yerleri çiz
            nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue')

            # Seçilen yerleri kırmızı çizgilerle vurgula
            nx.draw_networkx_edges(G, pos, edgelist=[(en_kisa_yol[i], en_kisa_yol[i+1]) for i in range(len(en_kisa_yol)-1)], edge_color='red', width=2)

            plt.title("Market Yolu")
            plt.show()

        else:
            messagebox.showerror("Hata", "Lütfen en az bir yer seçin.")

    def matrisi_goster(self):
        secilen_yerler = self.yer_giris.curselection()
        if secilen_yerler:
            secilen_yerler_text = [self.yerler[index] for index in secilen_yerler]
            # Rasgele mesafelerle bir matris oluştur
            mesafe_matrisi = np.zeros((len(secilen_yerler_text), len(secilen_yerler_text)), dtype=int)
            for i in range(len(secilen_yerler_text)):
                for j in range(i + 1, len(secilen_yerler_text)):
                    mesafe_matrisi[i, j] = random.randint(1, 10)  # Rasgele mesafe (örnek)
                    mesafe_matrisi[j, i] = mesafe_matrisi[i, j]

            # Mesafe matrisini çıktı olarak göster
            self.goster_matris(secilen_yerler_text, mesafe_matrisi)

        else:
            messagebox.showerror("Hata", "Lütfen en az bir yer seçin.")

    def temizle(self):
        self.yer_giris.selection_clear(0, tk.END)

# Uygulamayı başlat
root = tk.Tk()
uygulama = MarketUygulamasiGUI(root)

# Pencere boyutunu ayarla ve pencereyi ekranın ortasına yerleştir
window_width = 500
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

root.mainloop()