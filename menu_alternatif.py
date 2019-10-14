import gi, subprocess, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk, Gdk, GdkPixbuf


class AramaPencere(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)
		#Pencere için gerekli bayraklar boyut vs.
		self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.set_size_request(440,30)
		self.set_border_width(5)
		self.set_resizable(False)
		self.set_decorated(False)
		self.connect('notify::is-active', self.aktif_pencere_degisti)
		self.connect("key-press-event",self.tus_basildi)

		tasiyici_kutu = Gtk.HBox()
		tasiyici_kutu.set_spacing(5)
		self.add(tasiyici_kutu)

		self.arama_entry = Gtk.SearchEntry(max_width_chars=45)
		self.arama_entry.connect("search-changed", self.arama_entry_degisti)
		tasiyici_kutu.pack_start(self.arama_entry,True,True,0)

		self.kapat_dugme = Gtk.Button()
		self.kapat_dugme.connect("clicked",self.kapat_basildi)
		self.kapat_dugme.set_always_show_image(True)
		resim = Gtk.Image.new_from_icon_name("system-log-out",Gtk.IconSize.LARGE_TOOLBAR)
		self.kapat_dugme.set_image(resim)
		tasiyici_kutu.pack_end(self.kapat_dugme,True,True,0)

		self.liste_pencere = ListePencere(self)
		self.uygulama_bilgileri_olustur()


	def aktif_pencere_degisti(self,pencere,param):
		"""Aktif pencere değiştiğinde programı kapatıyoruz."""
		if not self.is_active():
			self.arama_entry.set_text("")
			self.destroy()

	def arama_entry_degisti(self,aranan):
		"""Aranan kelimeye uygun olan uygulamaları listeye ekleyerek
		uygulama listesinin gösterildiği pencereyi çalıştırıyoruz."""
		if aranan.get_text() == "":
			self.liste_pencere.hide()
		else:
			uygun_uygulamalar = []
			for uygulama_bilgi in self.uygulama_bilgileri:
				uygun = False
				adi = uygulama_bilgi.get("Adi", False)
				adi_turkce = uygulama_bilgi.get("Adi_Turkce", False)
				aciklama = uygulama_bilgi.get("Aciklama", False)
				aciklama_turkce = uygulama_bilgi.get("Aciklama_Turkce", False)
				aranan_ = aranan.get_text().lower()
				if not adi:
					continue
				elif aranan_ in adi.lower():
					uygun = True
				elif adi_turkce and aranan_ in adi_turkce.lower():
					uygun = True
				elif aciklama and aranan_ in aciklama.lower():
					uygun = True
				elif aciklama_turkce and aranan_ in aciklama_turkce.lower():
					uygun = True
				if uygun:
					uygun_uygulamalar.append(uygulama_bilgi)

			arama_x,arama_y = self.get_position()
			arama_w,arama_h = self.get_size()
			self.liste_pencere.liste_tree_doldur(uygun_uygulamalar)
			if not self.liste_pencere.get_property("visible"):
				self.liste_pencere.show_all()
				self.liste_pencere.move(arama_x,arama_y+65)

	def kapat_basildi(self,widget):
		subprocess.Popen(["xfce4-session-logout"], stdout=subprocess.PIPE)
		self.destroy()

	def uygulama_dosyasi_ayikla(self,okunan):
		"""Application dosyalarını okuyarak gerekli kısımları ayıkladıktan
		sonra uygulama_bilgi sözlüğüne kaydederek sözlüğü fonksiyonla geri
		döndürüyoruz"""
		uygulama_bilgi = {}
		#Birden fazla exec olması durumunda desktop entry altında olan
		#komutu almak istiyoruz. Bu sebeple kontrol ekliyoruz.
		desktop_entry_kontrol = False
		for satir in okunan:
			#Satır sonu karakterlerini temizliyoruz
			satir = satir.replace("\n","")
			if len(satir) > 13 and satir[0] == "[" and satir[-1] == "]":
				if satir == "[Desktop Entry]":
					desktop_entry_kontrol = True
				else:
					desktop_entry_kontrol = False
			elif satir[:5] == "Name=":
				if desktop_entry_kontrol:
					uygulama_bilgi["Adi"] = satir[5:]
			elif satir[:9] == "Name[tr]=":
				uygulama_bilgi["Adi_Turkce"] = satir[9:]
			elif satir[:8] == "Comment=":
				uygulama_bilgi["Aciklama"] = satir[8:]
			elif satir[:12] == "Comment[tr]=":
				uygulama_bilgi["Aciklama_Turkce"] = satir[12:]
			elif satir[:5] == "Icon=":
				uygulama_bilgi["Simge"] = satir[5:]
			elif satir[:5] == "Exec=" and desktop_entry_kontrol:
				#Belirtilen kontrolü yapıyoruz
				if desktop_entry_kontrol:
					uygulama_bilgi["Calistir"] = satir[5:].split(" %")[0]
		return uygulama_bilgi

	def uygulama_bilgileri_olustur(self):
		"""/usr/share/applications/ altındaki .desktop dosyalarını okuyoruz
		gerekli bilgileri self.uygulama_bilgileri altına kaydediyoruz."""
		self.uygulama_bilgileri = []
		uygulamalar_dizini = "/usr/share/applications/"
		uygulamalar = os.listdir(uygulamalar_dizini)
		for uygulama in uygulamalar:
			dosya = open(uygulamalar_dizini+uygulama,"r")
			okunan = dosya.readlines()
			ayiklanan = self.uygulama_dosyasi_ayikla(okunan)
			self.uygulama_bilgileri.append(ayiklanan)
			dosya.close()

	def tus_basildi(self, widget, event):
		basili_tus = event.keyval
		if basili_tus == Gdk.KEY_Return:
			self.liste_pencere.liste_tree_tiklandi()
		elif basili_tus == Gdk.KEY_Up:
			path_, coloumn_ = self.liste_pencere.liste_tree.get_cursor()
			secili = path_.get_indices()[0]
			if int(secili) > 0:
				self.liste_pencere.liste_tree.set_cursor(secili - 1)
		elif basili_tus == Gdk.KEY_Down:
			path_, coloumn_ = self.liste_pencere.liste_tree.get_cursor()
			secili = path_.get_indices()[0]
			if self.liste_pencere.liste_toplam_uygulama-1 > int(secili):
				self.liste_pencere.liste_tree.set_cursor(secili + 1)

class ListePencere(Gtk.Window):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		#Pencere için gerekli bayraklar boyut vs.
		self.set_type_hint(Gdk.WindowTypeHint.NOTIFICATION)
		self.set_size_request(440,290)
		self.set_border_width(5)
		self.set_resizable(False)
		self.set_decorated(False)

		tasiyici_kutu = Gtk.HBox()
		tasiyici_kutu.set_spacing(5)
		self.add(tasiyici_kutu)

		self.liste_store = Gtk.ListStore(GdkPixbuf.Pixbuf, str,str)
		self.liste_tree = Gtk.TreeView(model=self.liste_store)
		self.liste_tree.set_property('activate-on-single-click', True)#Tek tıklama için
		self.liste_tree.connect("row-activated",self.liste_tree_tiklandi)
		self.liste_scroll = Gtk.ScrolledWindow()
		self.liste_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		self.liste_scroll.add(self.liste_tree)
		tasiyici_kutu.pack_end(self.liste_scroll,True,True,1)

		liste_sutun_icon = Gtk.CellRendererPixbuf()
		liste_sutun_icon.set_fixed_size(32,32)
		liste_sutun = Gtk.TreeViewColumn('Icon', liste_sutun_icon, gicon=0)
		self.liste_tree.append_column(liste_sutun)
		liste_sutun_text = Gtk.CellRendererText()
		liste_sutun = Gtk.TreeViewColumn('Program Adı', liste_sutun_text, text=1)
		liste_sutun.set_sort_column_id(1)
		self.liste_store.set_sort_column_id(1,Gtk.SortType.ASCENDING)
		self.liste_tree.append_column(liste_sutun)
		self.liste_tree.set_headers_visible(False)

	def liste_tree_tiklandi(self,widget=None,path=None,coloumn=None):
		selection = self.liste_tree.get_selection()
		tree_model, tree_iter = selection.get_selected()
		subprocess.Popen(tree_model[tree_iter][2].split(), stdout=subprocess.PIPE)
		self.ebeveyn.destroy()

	def liste_tree_doldur(self,uygulamalar):
		"""Ebeveyn pencere tarafından gönderilen uygulamaları listeye
		ekliyoruz"""
		self.liste_store.clear()
		self.liste_toplam_uygulama = len(uygulamalar)
		icon_tema = Gtk.IconTheme().get_default()
		for uygulama_bilgi in uygulamalar:
			adi = uygulama_bilgi.get("Adi", False)
			adi_turkce = uygulama_bilgi.get("Adi_Turkce", False)
			aciklama = uygulama_bilgi.get("Aciklama", False)
			aciklama_turkce = uygulama_bilgi.get("Aciklama_Turkce", False)
			simge = uygulama_bilgi.get("Simge", False)
			calistir = uygulama_bilgi.get("Calistir", False)

			#Varsayılan olarak uygulama adı ve simge ekliyoruz
			#Simge veya ad gelmemesi durumunda hatadan kurtulmak için
			uyg_adi = adi
			#Temadan simge adına uygun simge istiyoruz
			if simge:
				if os.path.isfile(simge):
					uyg_simge = GdkPixbuf.Pixbuf.new_from_file(simge)
				else:
					uyg_simge = icon_tema.load_icon(simge,32,Gtk.IconLookupFlags.FORCE_SIZE)
			#Türkçe veya diğer açıklamayı uygulama adına ekliyoruz
			if aciklama_turkce:
				uyg_adi += "\n"+aciklama_turkce
			elif aciklama:
				uyg_adi += "\n"+aciklama

			#Açıklama bazen çok uzun olabiliyor 60 karakterle sınırlıyoruz
			if len(uyg_adi) > 60:
				uyg_adi = uyg_adi[:60] + "..."
			else:
				uyg_adi = uyg_adi.ljust(63," ")
			self.liste_store.append([uyg_simge,uyg_adi,calistir])
		self.liste_tree.set_cursor(0)

if __name__ == '__main__':
	pencere = AramaPencere()
	pencere.connect("destroy", Gtk.main_quit)
	pencere.show_all()
	Gtk.main()
