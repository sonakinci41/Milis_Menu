import sys,os
import uyg_stacked, int_stacked, dosya_stacked
from PyQt5.QtWidgets import (QWidget,QApplication,QLineEdit,QGridLayout,QPushButton,QStackedWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

class MerkezPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(MerkezPencere, self).__init__(ebeveyn)
        self.pencere_boyut = (500,200)
        self.pencere_konum = (250,250)
        self.setFixedSize(QSize(self.pencere_boyut[0],self.pencere_boyut[1]))

        self.sistem_dili = "tr"
        self.aranacak_dizin = os.path.expanduser("~")

        kutu = QGridLayout()
        kutu.setContentsMargins(0,0,0,0)
        self.setLayout(kutu)

        self.arama_le = QLineEdit()
        self.arama_le.textChanged.connect(self.aranan_degisti)
        kutu.addWidget(self.arama_le,0,0,1,2)

        self.uygulamalar_pb = QPushButton()
        self.uygulamalar_pb.setCheckable(True)
        self.uygulamalar_pb.setChecked(True)
        self.uygulamalar_pb.setIcon(QIcon("simgeler/uygulama.svg"))
        self.uygulamalar_pb.setFixedSize(QSize(48,48))
        self.uygulamalar_pb.setIconSize(QSize(44,44))
        kutu.addWidget(self.uygulamalar_pb,1,0,1,1)

        self.dosyalar_pb = QPushButton()
        self.dosyalar_pb.setCheckable(True)
        self.dosyalar_pb.setIcon(QIcon("simgeler/dosya.svg"))
        self.dosyalar_pb.setFixedSize(QSize(48,48))
        self.dosyalar_pb.setIconSize(QSize(44,44))
        kutu.addWidget(self.dosyalar_pb,2,0,1,1)

        self.internet_pb = QPushButton()
        self.internet_pb.setCheckable(True)
        self.internet_pb.setIcon(QIcon("simgeler/internet.svg"))
        self.internet_pb.setFixedSize(QSize(48,48))
        self.internet_pb.setIconSize(QSize(44,44))
        kutu.addWidget(self.internet_pb,3,0,1,1)

        self.aktif_bolum = "uygulama"

        self.arama_sk = QStackedWidget()
        kutu.addWidget(self.arama_sk,1,1,3,1)
        self.uygulama_bolumu = uyg_stacked.Uyg_Stacked(self)
        self.arama_sk.addWidget(self.uygulama_bolumu)
        self.dosya_bolumu = dosya_stacked.Dosya_Stacked(self)
        self.arama_sk.addWidget(self.dosya_bolumu)
        self.internet_bolumu = int_stacked.Int_Stacked(self)
        self.arama_sk.addWidget(self.internet_bolumu)

        #Sinyaller
        self.uygulamalar_pb.clicked.connect(self.uyg_pb_basildi)
        self.dosyalar_pb.clicked.connect(self.dosyalar_pb_basildi)
        self.internet_pb.clicked.connect(self.internet_pb_basildi)

    def button_ayarla(self,secilen):
        if secilen == 1:
            self.uygulamalar_pb.setChecked(True)
            self.dosyalar_pb.setChecked(False)
            self.internet_pb.setChecked(False)
        elif secilen == 2:
            self.uygulamalar_pb.setChecked(False)
            self.dosyalar_pb.setChecked(True)
            self.internet_pb.setChecked(False)
        elif secilen == 3:
            self.uygulamalar_pb.setChecked(False)
            self.dosyalar_pb.setChecked(False)
            self.internet_pb.setChecked(True)

    def internet_pb_basildi(self):
        self.button_ayarla(3)
        self.aktif_bolum = "internet"
        self.arama_sk.setCurrentIndex(2)
        self.arama_le.setFocus()
        self.aranan_degisti(self.arama_le.text())

    def dosyalar_pb_basildi(self):
        self.button_ayarla(2)
        self.aktif_bolum = "dosya"
        self.arama_sk.setCurrentIndex(1)
        self.arama_le.setFocus()
        self.aranan_degisti(self.arama_le.text())

    def uyg_pb_basildi(self):
        self.button_ayarla(1)
        self.aktif_bolum = "uygulama"
        self.arama_sk.setCurrentIndex(0)
        self.arama_le.setFocus()
        self.aranan_degisti(self.arama_le.text())

    def aranan_degisti(self,kelime):
        """Arama barındaki kelime değişince bu fonksiyon çalışıp ilgili fonkisyonu çağırıyor"""
        if self.aktif_bolum == "uygulama":
            self.uygulama_bolumu.aranan_degisti(kelime)
        elif self.aktif_bolum == "dosya":
            self.dosya_bolumu.aranan_degisti(kelime)
        elif self.aktif_bolum == "internet":
            self.internet_bolumu.aranan_degisti(kelime)

    def keyPressEvent(self, olay):
        if olay.key() == Qt.Key_Return:
            if self.aktif_bolum == "uygulama":
                self.uygulama_bolumu.enter_basildi()
            elif self.aktif_bolum == "dosya":
                self.dosya_bolumu.enter_basildi()
            elif self.aktif_bolum == "internet":
                self.internet_bolumu.enter_basildi()
        elif olay.key() == Qt.Key_Up:
            if self.aktif_bolum == "uygulama":
                self.uygulama_bolumu.yukari_basildi()
            elif self.aktif_bolum == "dosya":
                self.dosya_bolumu.yukari_basildi()
            elif self.aktif_bolum == "internet":
                self.internet_bolumu.yukari_basildi()
        elif olay.key() == Qt.Key_Down:
            if self. aktif_bolum == "uygulama":
                self.uygulama_bolumu.asagi_basildi()
            elif self.aktif_bolum == "dosya":
                self.dosya_bolumu.asagi_basildi()
            elif self.aktif_bolum == "internet":
                self.internet_bolumu.asagi_basildi()

if __name__ == "__main__":
    app_ = QApplication(sys.argv)
    app_.setOrganizationName('Milis Menu')
    app_.setApplicationName('milis_menu')
    pencere = MerkezPencere()
    pencere.show()
    sys.exit(app_.exec_())