from PyQt5.QtWidgets import (QWidget,QGridLayout,QLabel,QPushButton,QLineEdit)

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
        kutu.addWidget(self.konsol_vars_le,2,1,1,3)

        tarayici_vars_lab = QLabel("Tarayıcı")
        kutu.addWidget(tarayici_vars_lab,3,0,1,1)
        self.tarayici_vars_le = QLineEdit()
        kutu.addWidget(self.tarayici_vars_le,3,1,1,3)

        uygula_dugme = QPushButton()
        uygula_dugme.setText("Uygula")
        uygula_dugme.clicked.connect(self.uygula_fonk)
        kutu.addWidget(uygula_dugme,4,0,1,4)

    def showEvent(self, event):
        self.boyut_genislik_le.setText(str(self.ebeveyn.pencere_boyut[0]))
        self.boyut_yukseklik_le.setText(str(self.ebeveyn.pencere_boyut[1]))
        self.konum_x_le.setText(str(self.ebeveyn.pencere_konum[0]))
        self.konum_y_le.setText(str(self.ebeveyn.pencere_konum[1]))
        self.konsol_vars_le.setText(self.ebeveyn.konsol_vars)
        self.tarayici_vars_le.setText(self.ebeveyn.tarayici_vars)

    def uygula_fonk(self):
        self.ebeveyn.pencere_boyut = (int(self.boyut_genislik_le.text()),int(self.boyut_yukseklik_le.text()))
        self.ebeveyn.ayarlar.setValue("pencere_boyutu",self.ebeveyn.pencere_boyut)
        self.ebeveyn.pencere_konum = (int(self.konum_x_le.text()),int(self.konum_y_le.text()))
        self.ebeveyn.ayarlar.setValue("pencere_konum",self.ebeveyn.pencere_konum)
        self.ebeveyn.konsol_vars = self.konsol_vars_le.text()
        self.ebeveyn.ayarlar.setValue("konsol_vars", self.ebeveyn.konsol_vars)
        self.ebeveyn.tarayici_vars = self.tarayici_vars_le.text()
        self.ebeveyn.ayarlar.setValue("tarayici_vars", self.ebeveyn.tarayici_vars)