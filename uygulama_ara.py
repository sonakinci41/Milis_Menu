import os

class Ara(object):
    def __init__(self, ebeveyn=None):
        self.ebeveyn = ebeveyn
        self.uygulamalar = {}
        self.kategori_sozluk = {"Settings":[],"AudioVideo":[],"Education":[],"Development":[],
                                "Graphics":[],"Network":[],"Office":[],"System":[],"Other":[]}
        self.basla()

    def basla(self):
        """Ayiklam işlemini başlatıyoruz ve değerleri değişkenlere atıyoruz"""
        dizin = os.listdir("/usr/share/applications/")
        for dosya in dizin:
            okunan = self.ac_ve_oku(dosya)
            ayiklanmis = self.ayikla(okunan)
            if ayiklanmis[0] != None:
                control = self.uygulamalar.get(ayiklanmis[0], "No")
                if control == "No":
                    self.uygulamalar[ayiklanmis[0]] = ayiklanmis
                self.kategori_ekle(ayiklanmis)
        return  self.uygulamalar

    def ac_ve_oku(self,dosya_adi):
        """.desktop dosyasını açıp okuyoruz ve satırları döndürüyoruz"""
        try:
            dosya = open("/usr/share/applications/"+dosya_adi,"r")
            okunan = dosya.readlines()
            dosya.close()
            return okunan
        except:
            return []

    def kategori_ekle(self,liste):
        """Kategorileri düzenleyip ; e göre bölüp ilgili uygulamayı ekliyoruz"""
        kategoriler = liste[3]
        if kategoriler == None:
            kategoriler = ["Unknown"]
        else:
            kategoriler = kategoriler.split(";")
        for kategori in kategoriler:
            if kategori != "":
                kontrol = self.kategori_sozluk.get(kategori,"Yok")
                if kontrol == "Yok":
                    if liste[0] not in self.kategori_sozluk["Other"]:
                        self.kategori_sozluk["Other"].append(liste[0])
                else:
                    if liste[0] not in kontrol:
                        kontrol.append(liste[0])

    def ayikla(self,okunan_liste):
        isim = None
        komut = None
        simge = None
        kategoriler = None
        dongu = False
        tum_isimler = []
        for satir in okunan_liste:
            if satir[0:15] == "[Desktop Entry]":
                dongu = True
            elif satir[0] == "[":
                break
            if dongu:
                if satir[0:5] == "Name=":
                    isim = satir[5:-1]
                    tum_isimler.append(isim)
                elif satir[0:5] == "Exec=":
                    komut = satir[5:-1]
                elif satir[0:5] == "Icon=":
                    simge = satir[5:-1]
                elif satir[0:11] == "Categories=":
                    kategoriler = satir[11:-1]
                elif satir[0:9] == "Name[{}]=".format(self.ebeveyn.ebeveyn.sistem_dili):
                    tum_isimler.append(satir[9:-1])
                elif satir[0:8] == "Comment=":
                    tum_isimler.append(satir[8:-1])
                elif satir[0:12] == "Comment[{}]=".format(self.ebeveyn.ebeveyn.sistem_dili):
                    tum_isimler.append(satir[12:-1])
        return [isim,komut,simge,kategoriler,tum_isimler]