from PyQt5.QtWidgets import (QWidget,QGridLayout,QListWidget,QListWidgetItem,QPushButton,qApp)
from PyQt5.QtGui import QIcon
from milis_menu_lib import uygulama_ara
import os

class Uyg_Stacked(QWidget):
    def __init__(self, ebeveyn=None):
        super(Uyg_Stacked, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        self.uygulama_guncelle()
        uygulama_ara_kutu = QGridLayout()
        uygulama_ara_kutu.setContentsMargins(0,0,0,0)
        self.setLayout(uygulama_ara_kutu)

        tum_uyg_pb = QPushButton()
        tum_uyg_pb.setFixedHeight(24)
        tum_uyg_pb.setText("Tüm Uygulamalar")
        tum_uyg_pb.setIcon(QIcon(self.ebeveyn.icon_yolu+"uygulama.svg"))
        tum_uyg_pb.clicked.connect(self.tum_uyg_basildi)
        tum_uyg_pb.setStyleSheet("Text-align:left;border:none;")
        uygulama_ara_kutu.addWidget(tum_uyg_pb,0,0,1,1)

        ayar_uyg_pb = QPushButton()
        ayar_uyg_pb.setFixedHeight(24)
        ayar_uyg_pb.setText("Ayarlar")
        ayar_uyg_pb.setIcon(QIcon(self.ebeveyn.icon_yolu+"uyg_ayarlar.svg"))
        ayar_uyg_pb.clicked.connect(self.ayar_uyg_basildi)
        ayar_uyg_pb.setStyleSheet("Text-align:left;border:none;")
        uygulama_ara_kutu.addWidget(ayar_uyg_pb,1,0,1,1)

        cok_ort_uyg_pb = QPushButton()
        cok_ort_uyg_pb.setFixedHeight(24)
        cok_ort_uyg_pb.setText("Çoklu Ortam")
        cok_ort_uyg_pb.setIcon(QIcon(self.ebeveyn.icon_yolu+"uyg_cok_ort.svg"))
        cok_ort_uyg_pb.clicked.connect(self.cok_ort_uyg_basildi)
        cok_ort_uyg_pb.setStyleSheet("Text-align:left;border:none;")
        uygulama_ara_kutu.addWidget(cok_ort_uyg_pb,2,0,1,1)

        egitim_uyg_pb = QPushButton()
        egitim_uyg_pb.setFixedHeight(24)
        egitim_uyg_pb.setText("Eğitim")
        egitim_uyg_pb.setIcon(QIcon(self.ebeveyn.icon_yolu+"uyg_egitim.svg"))
        egitim_uyg_pb.clicked.connect(self.egitim_uyg_basildi)
        egitim_uyg_pb.setStyleSheet("Text-align:left;border:none;")
        uygulama_ara_kutu.addWidget(egitim_uyg_pb,3,0,1,1)

        gelistirme_uyg_pb = QPushButton()
        gelistirme_uyg_pb.setFixedHeight(24)
        gelistirme_uyg_pb.setText("Geliştirme")
        gelistirme_uyg_pb.setIcon(QIcon(self.ebeveyn.icon_yolu+"uyg_gelistirme.svg"))
        gelistirme_uyg_pb.clicked.connect(self.gelistirme_uyg_basildi)
        gelistirme_uyg_pb.setStyleSheet("Text-align:left;border:none;")
        uygulama_ara_kutu.addWidget(gelistirme_uyg_pb,4,0,1,1)

        grafik_uyg_pb = QPushButton()
        grafik_uyg_pb.setFixedHeight(24)
        grafik_uyg_pb.setText("Grafik")
        grafik_uyg_pb.setIcon(QIcon(self.ebeveyn.icon_yolu+"uyg_grafik.svg"))
        grafik_uyg_pb.clicked.connect(self.grafik_uyg_basildi)
        grafik_uyg_pb.setStyleSheet("Text-align:left;border:none;")
        uygulama_ara_kutu.addWidget(grafik_uyg_pb,5,0,1,1)

        internet_uyg_pb = QPushButton()
        internet_uyg_pb.setFixedHeight(24)
        internet_uyg_pb.setText("İnternet")
        internet_uyg_pb.setIcon(QIcon(self.ebeveyn.icon_yolu+"uyg_internet.svg"))
        internet_uyg_pb.clicked.connect(self.internet_uyg_basildi)
        internet_uyg_pb.setStyleSheet("Text-align:left;border:none;")
        uygulama_ara_kutu.addWidget(internet_uyg_pb,6,0,1,1)

        ofis_uyg_pb = QPushButton()
        ofis_uyg_pb.setFixedHeight(24)
        ofis_uyg_pb.setText("Ofis")
        ofis_uyg_pb.setIcon(QIcon(self.ebeveyn.icon_yolu+"uyg_ofis.svg"))
        ofis_uyg_pb.clicked.connect(self.ofis_uyg_basildi)
        ofis_uyg_pb.setStyleSheet("Text-align:left;border:none;")
        uygulama_ara_kutu.addWidget(ofis_uyg_pb,7,0,1,1)

        sistem_uyg_pb = QPushButton()
        sistem_uyg_pb.setFixedHeight(24)
        sistem_uyg_pb.setText("Sistem")
        sistem_uyg_pb.setIcon(QIcon(self.ebeveyn.icon_yolu+"uyg_sistem.svg"))
        sistem_uyg_pb.clicked.connect(self.sistem_uyg_basildi)
        sistem_uyg_pb.setStyleSheet("Text-align:left;border:none;")
        uygulama_ara_kutu.addWidget(sistem_uyg_pb,8,0,1,1)

        diger_uyg_pb = QPushButton()
        diger_uyg_pb.setFixedHeight(24)
        diger_uyg_pb.setText("Diğer")
        diger_uyg_pb.setIcon(QIcon(self.ebeveyn.icon_yolu+"uyg_diger.svg"))
        diger_uyg_pb.clicked.connect(self.diger_uyg_basildi)
        diger_uyg_pb.setStyleSheet("Text-align:left;border:none;")
        uygulama_ara_kutu.addWidget(diger_uyg_pb,9,0,1,1)


        self.uygulama_ara_lw = QListWidget()
        self.uygulama_ara_lw.itemDoubleClicked.connect(self.enter_basildi)
        uygulama_ara_kutu.addWidget(self.uygulama_ara_lw,0,1,10,1)

        #Sinyaller
        self.tum_uyg_basildi()

    def tum_uyg_basildi(self):
        self.uygulama_ara_lw.clear()
        uygulamalar = list(self.uygulamalar.keys())
        uygulamalar.sort()
        self.listeye_ekle(uygulamalar)
        self.uygulama_ara_lw.setFocus(True)

    def ayar_uyg_basildi(self):
        self.uygulama_ara_lw.clear()
        kontrol = self.kategori_sozluk.get("Settings", "Yok")
        if kontrol != "Yok":
            uygulamalar = list(kontrol)
            uygulamalar.sort()
            self.listeye_ekle(uygulamalar)
            self.uygulama_ara_lw.setFocus(True)

    def cok_ort_uyg_basildi(self):
        self.uygulama_ara_lw.clear()
        kontrol = self.kategori_sozluk.get("AudioVideo", "Yok")
        if kontrol != "Yok":
            uygulamalar = list(kontrol)
            uygulamalar.sort()
            self.listeye_ekle(uygulamalar)
            self.uygulama_ara_lw.setFocus(True)

    def egitim_uyg_basildi(self):
        self.uygulama_ara_lw.clear()
        kontrol = self.kategori_sozluk.get("Education", "Yok")
        if kontrol != "Yok":
            uygulamalar = list(kontrol)
            self.listeye_ekle(uygulamalar)
            self.uygulama_ara_lw.setFocus(True)

    def gelistirme_uyg_basildi(self):
        self.uygulama_ara_lw.clear()
        kontrol = self.kategori_sozluk.get("Development", "Yok")
        if kontrol != "Yok":
            uygulamalar = list(kontrol)
            self.listeye_ekle(uygulamalar)
            self.uygulama_ara_lw.setFocus(True)

    def grafik_uyg_basildi(self):
        self.uygulama_ara_lw.clear()
        kontrol = self.kategori_sozluk.get("Graphics", "Yok")
        if kontrol != "Yok":
            uygulamalar = list(kontrol)
            self.listeye_ekle(uygulamalar)
            self.uygulama_ara_lw.setFocus(True)

    def internet_uyg_basildi(self):
        self.uygulama_ara_lw.clear()
        kontrol = self.kategori_sozluk.get("Network", "Yok")
        if kontrol != "Yok":
            uygulamalar = list(kontrol)
            self.listeye_ekle(uygulamalar)
            self.uygulama_ara_lw.setFocus(True)

    def ofis_uyg_basildi(self):
        self.uygulama_ara_lw.clear()
        kontrol = self.kategori_sozluk.get("Office", "Yok")
        if kontrol != "Yok":
            uygulamalar = list(kontrol)
            self.listeye_ekle(uygulamalar)
            self.uygulama_ara_lw.setFocus(True)

    def sistem_uyg_basildi(self):
        self.uygulama_ara_lw.clear()
        kontrol = self.kategori_sozluk.get("System", "Yok")
        if kontrol != "Yok":
            uygulamalar = list(kontrol)
            self.listeye_ekle(uygulamalar)
            self.uygulama_ara_lw.setFocus(True)

    def diger_uyg_basildi(self):
        self.uygulama_ara_lw.clear()
        kontrol = self.kategori_sozluk.get("Other", "Yok")
        if kontrol != "Yok":
            uygulamalar = list(kontrol)
            self.listeye_ekle(uygulamalar)
            self.uygulama_ara_lw.setFocus(True)

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
                qApp.exit()

    def aranan_degisti(self,kelime):
        self.uygulama_ara_lw.clear()
        if kelime != "":
            kelime = kelime.lower()
            sonuc = self.uygulama_ara(kelime)
            self.listeye_ekle(sonuc)
        else:
            self.tum_uyg_basildi()

    def listeye_ekle(self,liste):
        self.liste_uyg_say = len(liste)
        if self.liste_uyg_say != 0:
            liste.sort()
            for i in liste:
                uygulama = self.uygulamalar[i]
                ikon=uygulama[2]
                paths=["/usr/share/pixmaps/","/usr/share/icons/Adwaita/32x32/apps/"]
                uzantilar=["png","svg","xpm"]
                ikinci = None
                for uzanti in uzantilar:
                    for path in paths:
                        if ikon != None and os.path.exists(path+ikon+"."+uzanti):
                           ikinci = QIcon(path+ikon+"."+uzanti)
                           break
                    if ikinci != None:
                       break
                if ikinci == None:
                    ikinci = QIcon(self.ebeveyn.icon_yolu+"bilinmeyen.svg")
                liste_maddesi = QListWidgetItem(QIcon.fromTheme(uygulama[2], ikinci), uygulama[0])
                self.uygulama_ara_lw.addItem(liste_maddesi)
            self.uygulama_ara_lw.setCurrentRow(0)


    def arama_kontrol(self,uygulama, aranacak):
        """Kelime içinde kelime arıyoruz varsa True Yoksa False"""
        uygulama = uygulama.lower()
        for i in range(len(uygulama)):
             if uygulama[i:i + len(aranacak)] == aranacak:
                return True
        return False
