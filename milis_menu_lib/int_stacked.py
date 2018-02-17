import requests
from PyQt5.QtWidgets import (QWidget,QGridLayout,QListWidget,qApp,QListWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QProcess, QSize

class Int_Stacked(QWidget):
    def __init__(self, ebeveyn=None):
        super(Int_Stacked, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        kutu = QGridLayout()
        kutu.setContentsMargins(0,0,0,0)
        self.setLayout(kutu)

        self.internet_sonuc_lw = QListWidget()
        self.internet_sonuc_lw.setIconSize(QSize(self.ebeveyn.icon_boyutu,self.ebeveyn.icon_boyutu))
        self.internet_sonuc_lw.itemDoubleClicked.connect(self.enter_basildi)
        kutu.addWidget(self.internet_sonuc_lw,0,0,1,1)

        self.zamanlayici = QTimer()
        self.zamanlayici.timeout.connect(self.thread_baslat)

    def thread_baslat(self):
        self.zamanlayici.stop()
        th = Arama_Thread(self)
        th.start()

    def aranan_degisti(self,kelime):
        if kelime != "":
            self.aranacak_kelime = kelime
            self.zamanlayici.stop()
            self.zamanlayici.start(500)

    def listeye_ekle(self,sozluk):
        self.listedikler = sozluk
        self.internet_sonuc_lw.clear()
        if sozluk:
            self.liste_uyg_say = 0
            for i in sozluk.keys():
                if sozluk[i][:3] != "?q=":
                    lm = QListWidgetItem(QIcon.fromTheme(self.ebeveyn.tarayici_vars),i)
                    self.internet_sonuc_lw.addItem(lm)
                    self.liste_uyg_say += 1
            self.internet_sonuc_lw.setCurrentRow(0)

    def enter_basildi(self):
        secili_item = self.internet_sonuc_lw.currentItem()
        if secili_item != None:
            secili = secili_item.text()
            pro = QProcess()
            pro.startDetached(self.ebeveyn.tarayici_vars,[self.listedikler[secili]])
            qApp.exit()

    def yukari_basildi(self):
        secili_sira = self.internet_sonuc_lw.currentRow()
        if secili_sira > 0:
            self.internet_sonuc_lw.setCurrentRow(secili_sira - 1)

    def asagi_basildi(self):
        secili_sira = self.internet_sonuc_lw.currentRow()
        if 0 <= secili_sira < self.liste_uyg_say - 1:
            self.internet_sonuc_lw.setCurrentRow(secili_sira + 1)


class Arama_Thread(QThread):
    islem_tamam = pyqtSignal(dict)
    def __init__(self, ebeveyn=None):
        super(Arama_Thread, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        self.kelime = self.ebeveyn.aranacak_kelime
        self.islem_tamam.connect(self.ebeveyn.listeye_ekle)

    def run(self):
        try:
            sonuc = {}
            url_ = "https://www.google.com.tr/search?q="+self.kelime
            session = requests.Session()
            r = session.get(url_, headers={'User-Agent': 'Mozilla/5.0'})
            text = r.text
            text = text.split('class="r"><a href="')
            for x in text[1:]:
                a = x.split("</a>")[0]
                yazi = a.split('">')[1]
                gidecek = x.split("&amp")[0][7:]
                gidecek = gidecek.replace("https://www.youtube.com/watch%3Fv%3D","https://www.youtube.com/watch?v=")
                sonuc[yazi.replace("<b>","").replace("</b>","")] = gidecek
            self.islem_tamam.emit(sonuc)
        except:
            return False