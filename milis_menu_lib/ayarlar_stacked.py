from PyQt5.QtWidgets import (QWidget,QGridLayout,QLabel,QPushButton,QLineEdit, QTreeWidget, QTreeWidgetItem, QDialog)
from PyQt5.QtCore import Qt

class Ayarlar_Stacked(QWidget):
    def __init__(self, ebeveyn=None):
        super(Ayarlar_Stacked, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        kutu = QGridLayout()
        self.setLayout(kutu)
        self.setContentsMargins(0,0,0,0)
        boyut_genislik_lab = QLabel("Menu Genişliği")
        kutu.addWidget(boyut_genislik_lab,0,0,1,1)
        self.boyut_genislik_le = QLineEdit()
        kutu.addWidget(self.boyut_genislik_le,0,1,1,1)

        boyut_yukseklik_lab = QLabel("Menu Yüksekliği")
        kutu.addWidget(boyut_yukseklik_lab,0,2,1,1)
        self.boyut_yukseklik_le = QLineEdit()
        kutu.addWidget(self.boyut_yukseklik_le,0,3,1,1)

        konum_x_lab = QLabel("Menu Konum X")
        kutu.addWidget(konum_x_lab,1,0,1,1)
        self.konum_x_le = QLineEdit()
        kutu.addWidget(self.konum_x_le,1,1,1,1)

        konum_y_lab = QLabel("Menu Konum Y")
        kutu.addWidget(konum_y_lab,1,2,1,1)
        self.konum_y_le = QLineEdit()
        kutu.addWidget(self.konum_y_le,1,3,1,1)

        konsol_vars_lab = QLabel("Terminal")
        kutu.addWidget(konsol_vars_lab,2,0,1,1)
        self.konsol_vars_le = QLineEdit()
        kutu.addWidget(self.konsol_vars_le,2,1,1,1)

        tarayici_vars_lab = QLabel("Tarayıcı")
        kutu.addWidget(tarayici_vars_lab,2,2,1,1)
        self.tarayici_vars_le = QLineEdit()
        kutu.addWidget(self.tarayici_vars_le,2,3,1,1)

        icon_b_vars_lab = QLabel("İcon Boyutu")
        kutu.addWidget(icon_b_vars_lab,3,0,1,1)
        self.icon_b_vars_le = QLineEdit()
        kutu.addWidget(self.icon_b_vars_le,3,1,1,3)

        sagtik_lab = QLabel("Sağtık Menü")
        kutu.addWidget(sagtik_lab,4,0,1,1)
        self.sagtik_tw = QTreeWidget()
        self.sagtik_tw.setColumnCount(2)
        self.sagtik_tw.headerItem().setText(0, "Menü Adı")
        self.sagtik_tw.headerItem().setText(1, "Komut")
        kutu.addWidget(self.sagtik_tw,4,1,3,3)

        ekle_dugme = QPushButton()
        ekle_dugme.setText("Ekle")
        ekle_dugme.clicked.connect(self.ekle_dumge_basildi)
        kutu.addWidget(ekle_dugme,5,0,1,1)

        sil_dugme = QPushButton()
        sil_dugme.setText("Sil")
        sil_dugme.clicked.connect(self.sil_dugme_basildi)
        kutu.addWidget(sil_dugme,6,0,1,1)

        uygula_dugme = QPushButton()
        uygula_dugme.setText("Uygula")
        uygula_dugme.clicked.connect(self.uygula_fonk)
        kutu.addWidget(uygula_dugme,7,0,1,4)

    def showEvent(self, event):
        self.boyut_genislik_le.setText(str(self.ebeveyn.pencere_boyut[0]))
        self.boyut_yukseklik_le.setText(str(self.ebeveyn.pencere_boyut[1]))
        self.konum_x_le.setText(str(self.ebeveyn.pencere_konum[0]))
        self.konum_y_le.setText(str(self.ebeveyn.pencere_konum[1]))
        self.konsol_vars_le.setText(self.ebeveyn.konsol_vars)
        self.tarayici_vars_le.setText(self.ebeveyn.tarayici_vars)
        self.icon_b_vars_le.setText(str(self.ebeveyn.icon_boyutu))
        self.treeWidgetDoldur()


    def treeWidgetDoldur(self):
        self.sagtik_tw.clear()
        for i in self.ebeveyn.uyg_sagtik_gerekler.keys():
            item = QTreeWidgetItem()
            item.setText(0, i)
            item.setText(1, self.ebeveyn.uyg_sagtik_gerekler[i])
            item.setData(0, Qt.UserRole, i)
            self.sagtik_tw.addTopLevelItem(item)

    def ekle_dumge_basildi(self):
        ekle_pencere = EklePencere(self)
        ekle_pencere.show()

    def sil_dugme_basildi(self):
        del self.ebeveyn.uyg_sagtik_gerekler[self.sagtik_tw.currentItem().text(0)]
        self.sagtik_tw.clear()
        self.treeWidgetDoldur()

    def uygula_fonk(self):
        self.ebeveyn.pencere_boyut = (int(self.boyut_genislik_le.text()),int(self.boyut_yukseklik_le.text()))
        self.ebeveyn.ayarlar.setValue("pencere_boyutu",self.ebeveyn.pencere_boyut)
        self.ebeveyn.pencere_konum = (int(self.konum_x_le.text()),int(self.konum_y_le.text()))
        self.ebeveyn.ayarlar.setValue("pencere_konum",self.ebeveyn.pencere_konum)
        self.ebeveyn.konsol_vars = self.konsol_vars_le.text()
        self.ebeveyn.ayarlar.setValue("konsol_vars", self.ebeveyn.konsol_vars)
        self.ebeveyn.tarayici_vars = self.tarayici_vars_le.text()
        self.ebeveyn.ayarlar.setValue("tarayici_vars", self.ebeveyn.tarayici_vars)
        self.ebeveyn.icon_boyutu = int(self.icon_b_vars_le.text())
        self.ebeveyn.ayarlar.setValue("icon_boyutu",self.ebeveyn.icon_boyutu)
        self.ebeveyn.ayarlar.setValue("uyg_sagtik_gerekler",self.ebeveyn.uyg_sagtik_gerekler)


class EklePencere(QDialog):
    def __init__(self, ebeveyn=None):
        super(EklePencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        self.setWindowFlags(Qt.Popup)
        kutu = QGridLayout()
        self.setLayout(kutu)
        self.setContentsMargins(0,0,0,0)
        aciklama_lab = QLabel()
        aciklama_lab.setText("komut alanına exec komutu\nolan yere #exec ad.desktop\ndosyası olan yere #desktop\nyazınız")
        kutu.addWidget(aciklama_lab,0,0,1,2)
        ad_lab = QLabel()
        ad_lab.setText("Menü Adı")
        kutu.addWidget(ad_lab,1,0,1,1)
        self.ad_le = QLineEdit()
        kutu.addWidget(self.ad_le,1,1,1,1)
        komut_lab = QLabel()
        komut_lab.setText("Komut")
        kutu.addWidget(komut_lab,2,0,1,1)
        self.komut_le = QLineEdit()
        kutu.addWidget(self.komut_le,2,1,1,1)
        uyg_dugme = QPushButton()
        uyg_dugme.clicked.connect(self.uygula_basildi)
        uyg_dugme.setText("Uygula")
        kutu.addWidget(uyg_dugme,3,0,1,2)

    def uygula_basildi(self):
        self.ebeveyn.ebeveyn.uyg_sagtik_gerekler[self.ad_le.text()] = self.komut_le.text()
        self.ebeveyn.treeWidgetDoldur()
        QDialog.accept(self)