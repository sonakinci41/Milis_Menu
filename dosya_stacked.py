from PyQt5.QtWidgets import (QWidget,QGridLayout,QComboBox,QListWidget,QListWidgetItem)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer,QThread,pyqtSignal, QMimeDatabase, QProcess
import contextlib,subprocess

class Dosya_Stacked(QWidget):
    def __init__(self, ebeveyn=None):
        super(Dosya_Stacked, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        kutu = QGridLayout()
        kutu.setContentsMargins(0,0,0,0)
        self.setLayout(kutu)

        self.dosya_sonuc_lw = QListWidget()
        self.dosya_sonuc_lw.itemDoubleClicked.connect(self.enter_basildi)
        kutu.addWidget(self.dosya_sonuc_lw,0,0,1,1)

        self.zamanlayici = QTimer()
        self.zamanlayici.timeout.connect(self.thread_baslat)

    def thread_baslat(self):
        self.zamanlayici.stop()
        th = Arama_Thread(self)
        th.start()
        self.liste_uyg_say = 0
        self.dosya_sonuc_lw.clear()

    def aranan_degisti(self,kelime):
        if kelime != "":
            self.aranacak_kelime = kelime
            self.zamanlayici.stop()
            self.zamanlayici.start(1000)

    def listeye_ekle(self,dosya):
        if dosya != "":
            db = QMimeDatabase()
            db_1 = db.mimeTypeForFile(dosya)
            mimeTipi = db_1.name()
            if mimeTipi != None:
                iconTipi = mimeTipi.replace("/", "-")
                icon = QIcon.fromTheme(iconTipi)
                lm = QListWidgetItem(icon, dosya)
                self.dosya_sonuc_lw.addItem(lm)
            self.dosya_sonuc_lw.setCurrentRow(0)
            self.liste_uyg_say += 1

    def enter_basildi(self):
        secili_item = self.dosya_sonuc_lw.currentItem()
        if secili_item != None:
            secili = secili_item.text()
            pro = QProcess()
            pro.startDetached("xdg-open",[secili])

    def yukari_basildi(self):
        secili_sira = self.dosya_sonuc_lw.currentRow()
        if secili_sira > 0:
            self.dosya_sonuc_lw.setCurrentRow(secili_sira - 1)

    def asagi_basildi(self):
        secili_sira = self.dosya_sonuc_lw.currentRow()
        if 0 <= secili_sira < self.liste_uyg_say - 1:
            self.dosya_sonuc_lw.setCurrentRow(secili_sira + 1)


class Arama_Thread(QThread):
    islem_tamam = pyqtSignal(str)
    def __init__(self, ebeveyn=None):
        super(Arama_Thread, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        self.kelime = self.ebeveyn.aranacak_kelime
        self.islem_tamam.connect(self.ebeveyn.listeye_ekle)
        self.newlines = ['\n', '\r\n', '\r']

    def unbuffered(self,proc, stream='stdout'):
        stream = getattr(proc, stream)
        with contextlib.closing(stream):
            while True:
                out = []
                last = stream.read(1)
                # Don't loop forever
                if last == '' and proc.poll() is not None:
                    break
                while last not in self.newlines:
                    # Don't loop forever
                    if last == '' and proc.poll() is not None:
                        break
                    out.append(last)
                    last = stream.read(1)
                out = ''.join(out)
                yield out

    def run(self):
        aranan = ["find",self.ebeveyn.ebeveyn.aranacak_dizin,
                  "-iname","*{}*".format(self.ebeveyn.aranacak_kelime)]
        proc = subprocess.Popen(
            aranan,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            # Make all end-of-lines '\n'
            universal_newlines=True,
        )
        for line in self.unbuffered(proc):
            self.islem_tamam.emit(line)