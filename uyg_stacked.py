from PyQt5.QtWidgets import (QWidget,QGridLayout,QComboBox,QListWidget,QListWidgetItem)
from PyQt5.QtGui import QIcon
import uygulama_ara, os

class Uyg_Stacked(QWidget):
    def __init__(self, ebeveyn=None):
        super(Uyg_Stacked, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        self.uygulama_guncelle()
        uygulama_ara_kutu = QGridLayout()
        uygulama_ara_kutu.setContentsMargins(0,0,0,0)
        self.setLayout(uygulama_ara_kutu)

        self.uyg_kategoriler_cb = QComboBox()
        self.uyg_kategoriler_cb.addItems(["Tüm Uygulamalar","Ayarlar","Çoklu Ortam","Eğtim",
                                       "Geliştirme","Grafik","İnternet","Ofis","Sistem","Diğer"])
        uygulama_ara_kutu.addWidget(self.uyg_kategoriler_cb)

        self.uygulama_ara_lw = QListWidget()
        self.uygulama_ara_lw.itemDoubleClicked.connect(self.enter_basildi)
        uygulama_ara_kutu.addWidget(self.uygulama_ara_lw,1,0,1,1)

        #Sinyaller
        self.uyg_kategoriler_cb.currentTextChanged.connect(self.kategori_degisti)
        self.kategori_degisti("Tüm Uygulamalar")


    def kategori_degisti(self,kategori):
        self.uygulama_ara_lw.clear()
        if kategori == "Tüm Uygulamalar":
            uygulamalar = list(self.uygulamalar.keys())
            uygulamalar.sort()
            self.listeye_ekle(uygulamalar)
        elif kategori == "Ayarlar":
            kontrol = self.kategori_sozluk.get("Settings","Yok")
            if kontrol != "Yok":
                uygulamalar = list(kontrol)
                uygulamalar.sort()
                self.listeye_ekle(uygulamalar)
        elif kategori == "Çoklu Ortam":
            kontrol = self.kategori_sozluk.get("AudioVideo","Yok")
            if kontrol != "Yok":
                uygulamalar = list(kontrol)
                uygulamalar.sort()
                self.listeye_ekle(uygulamalar)
        elif kategori == "Eğitim":
            kontrol = self.kategori_sozluk.get("Education","Yok")
            if kontrol != "Yok":
                uygulamalar = list(kontrol)
                self.listeye_ekle(uygulamalar)
        elif kategori == "Geliştirme":
            kontrol = self.kategori_sozluk.get("Development","Yok")
            if kontrol != "Yok":
                uygulamalar = list(kontrol)
                self.listeye_ekle(uygulamalar)
        elif kategori == "Grafik":
            kontrol = self.kategori_sozluk.get("Graphics","Yok")
            if kontrol != "Yok":
                uygulamalar = list(kontrol)
                self.listeye_ekle(uygulamalar)
        elif kategori == "İnternet":
            kontrol = self.kategori_sozluk.get("Network","Yok")
            if kontrol != "Yok":
                uygulamalar = list(kontrol)
                self.listeye_ekle(uygulamalar)
        elif kategori == "Ofis":
            kontrol = self.kategori_sozluk.get("Office","Yok")
            if kontrol != "Yok":
                uygulamalar = list(kontrol)
                self.listeye_ekle(uygulamalar)
        elif kategori == "Sistem":
            kontrol = self.kategori_sozluk.get("System","Yok")
            if kontrol != "Yok":
                uygulamalar = list(kontrol)
                self.listeye_ekle(uygulamalar)
        elif kategori == "Diğer":
            kontrol = self.kategori_sozluk.get("Other","Yok")
            if kontrol != "Yok":
                uygulamalar = list(kontrol)
                self.listeye_ekle(uygulamalar)

    def uygulama_ara(self,kelime):
        """Aranmak istenen uygulamayı arayıp geri dönüt vereceğiz"""
        bulunanlar = []
        for uygulama in self.uygulamalar.keys():
            for isim in self.uygulamalar[uygulama][4]:
                if self.arama_kontrol(isim,kelime):
                    bulunanlar.append(uygulama)
                    break
        return bulunanlar

    def uygulama_guncelle(self):
        """Ara sınıfını kullnarak arama yapıp değişkenlere atıyoruz"""
        aranan = uygulama_ara.Ara(self)
        self.uygulamalar = aranan.uygulamalar
        self.kategori_sozluk = aranan.kategori_sozluk

    def uygulama_baslat(self,isim):
        """uygulamayı exec teki komutu kullanarak subprocess popen ile çalıştırıyorız"""
        komut = self.uygulamalar[isim][1].split(" %")[0]
        os.system(komut+"&")
#        subprocess.Popen(komut)

    def yukari_basildi(self):
        secili_sira = self.uygulama_ara_lw.currentRow()
        if secili_sira > 0:
            self.uygulama_ara_lw.setCurrentRow(secili_sira - 1)

    def asagi_basildi(self):
        secili_sira = self.uygulama_ara_lw.currentRow()
        if 0 <= secili_sira < self.liste_uyg_say - 1:
            self.uygulama_ara_lw.setCurrentRow(secili_sira + 1)

    def enter_basildi(self):
        secili_item = self.uygulama_ara_lw.currentItem()
        if secili_item != None:
            secili = secili_item.text()
            if secili != "":
                self.uygulama_baslat(secili)

    def aranan_degisti(self,kelime):
        self.uygulama_ara_lw.clear()
        if kelime != "":
            kelime = kelime.lower()
            self.uyg_kategoriler_cb.setDisabled(True)
            sonuc = self.uygulama_ara(kelime)
            self.listeye_ekle(sonuc)
        else:
            self.uyg_kategoriler_cb.setDisabled(False)
            self.uyg_kategoriler_cb.setCurrentText("Tüm Uygulamalar")

    def listeye_ekle(self,liste):
        self.liste_uyg_say = len(liste)
        if self.liste_uyg_say != 0:
            liste.sort()
            for i in liste:
                uygulama = self.uygulamalar[i]
                uygulama = self.uygulamalar[i]
                ikon=uygulama[2]
                paths=["/usr/share/pixmaps/","/usr/share/icons/Adwaita/48x48/apps/"]
                uzantilar=["png","svg","xpm"]
                bulundu=False
                for uzanti in uzantilar:
				    for path in paths:
                        if uygulama[2] != None and os.path.exists(path+ikon+uzanti):
                            liste_maddesi = QListWidgetItem(QIcon(path+ikon+uzanti), uygulama[0])
                            bulundu=True
                            break
                        else:
                            liste_maddesi = QListWidgetItem(QIcon.fromTheme(uygulama[2],QIcon("./simgeler/bilinmeyen.svg")), uygulama[0])
                        if bulundu:
                            break
                self.uygulama_ara_lw.addItem(liste_maddesi)
                self.uygulama_ara_lw.addItem(liste_maddesi)
            self.uygulama_ara_lw.setCurrentRow(0)


    def arama_kontrol(self,uygulama, aranacak):
        """Kelime içinde kelime arıyoruz varsa True Yoksa False"""
        uygulama = uygulama.lower()
        for i in range(len(uygulama)):
             if uygulama[i:i + len(aranacak)] == aranacak:
                return True
        return False
