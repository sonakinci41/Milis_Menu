import gi, subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk, Gdk


class AramaPencere(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)
		#Pencere özellikleri
		self.set_border_width(5)
		self.set_default_size(400,275)
		#self.set_resizable(False)
		self.set_position(Gtk.WindowPosition.MOUSE)
		self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
		self.connect('notify::is-active', self.aktif_degisti)

		#Kategorilerin türkçesi
		self.kategori_sozluk = {"Tümü":[None,"applications-other"],"Ayarlar":["Settings","utilities-tweak-tool"],"Çokluortam":["Audio","Video","applications-multimedia"],"Donatılar":["Utility","applications-utilities"],
					"Eğitim":["Education","applications-education"],"Geliştirme":["Development","applications-development"],"Grafikler":["Graphics","applications-graphics"],"İnternet":["Network","applications-internet"],
					"Ofis":["Office","applications-office"],"Sistem":["System","applications-system"]}

		#Listeye eklenen toplam program sayısını tutmak için bir değişken
		self.list_program_sayisi = -1

		self.hb = Gtk.HeaderBar()
		self.set_titlebar(self.hb)

		self.arama = Gtk.SearchEntry(max_width_chars=45)
		self.arama.connect("search-changed", self.arama_degisti)
		self.hb.pack_start(self.arama)

		self.kapat_dugme = Gtk.Button()
		self.kapat_dugme.connect("clicked",self.kapat_basildi)
		self.kapat_dugme.set_always_show_image(True)
		resim = Gtk.Image()
		resim.set_from_stock(Gtk.STOCK_QUIT,Gtk.IconSize.BUTTON)
		self.kapat_dugme.set_image(resim)
		self.hb.pack_end(self.kapat_dugme)

		kutu = Gtk.HBox(spacing=0)
		self.add(kutu)

		self.kategori_list_store = Gtk.ListStore(Gio.ThemedIcon(), str)
		self.kategori_tree = Gtk.TreeView(model=self.kategori_list_store)
		self.kategori_tree.set_property('activate-on-single-click', True)#Tek tıklama için
		self.kategori_tree.connect("row-activated",self.kategori_liste_tiklandi)
		scroll_1 = Gtk.ScrolledWindow()
		scroll_1.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		scroll_1.add(self.kategori_tree)
		kutu.pack_start(scroll_1,True,True,0)

		sutun_icon = Gtk.CellRendererPixbuf()
		sutun = Gtk.TreeViewColumn('Icon', sutun_icon, gicon=0)
		self.kategori_tree.append_column(sutun)
		sutun_text = Gtk.CellRendererText()
		sutun = Gtk.TreeViewColumn('Kategori', sutun_text, text=1)
		sutun.set_sort_column_id(1)
		self.kategori_tree.append_column(sutun)
		self.kategori_tree.set_headers_visible(False)


		for kategori in self.kategori_sozluk.keys():
			icon = Gio.ThemedIcon.new(self.kategori_sozluk[kategori][-1])
			self.kategori_list_store.append([icon,kategori])
		self.kategori_tree.set_cursor(0)

		self.uygulama_list_store = Gtk.ListStore(Gio.ThemedIcon(), str, str)
		self.uygulama_tree = Gtk.TreeView(model=self.uygulama_list_store)
		self.uygulama_tree.set_property('activate-on-single-click', True)#Tek tıklama için
		self.uygulama_tree.connect("row-activated",self.uygulama_tree_tiklandi)
		scroll_2 = Gtk.ScrolledWindow()
		scroll_2.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		scroll_2.add(self.uygulama_tree)
		kutu.pack_end(scroll_2,True,True,1)

		sutun_icon = Gtk.CellRendererPixbuf()
		sutun = Gtk.TreeViewColumn('Icon', sutun_icon, gicon=0)
		self.uygulama_tree.append_column(sutun)
		sutun_text = Gtk.CellRendererText()
		sutun = Gtk.TreeViewColumn('Program Adı', sutun_text, text=1)
		sutun.set_sort_column_id(1)
		self.uygulama_list_store.set_sort_column_id(1,Gtk.SortType.ASCENDING)
		self.uygulama_tree.append_column(sutun)
		self.uygulama_tree.set_headers_visible(False)
		self.connect("key-press-event",self.tus_basildi)

		self.uygulama_list_store_doldur()
		self.set_focus(self.arama)

	def kapat_basildi(self,widget):
		subprocess.Popen(["xfce4-session-logout"], stdout=subprocess.PIPE)
		self.destroy()
		 
	def aktif_degisti(self,pencere,param):
		if not self.is_active():
			self.destroy()

	def tus_basildi(self, widget, event):
		if self.get_focus() != self.arama:
			self.set_focus(self.arama)
		basili_tus = event.keyval
		if basili_tus == Gdk.KEY_Return:
			self.uygulama_tree_tiklandi()
		elif basili_tus == Gdk.KEY_Up:
			path_, coloumn_ = self.uygulama_tree.get_cursor()
			secili = path_.get_indices()[0]
			if int(secili) > 0:
				self.uygulama_tree.set_cursor(secili - 1)
		elif basili_tus == Gdk.KEY_Down:
			path_, coloumn_ = self.uygulama_tree.get_cursor()
			secili = path_.get_indices()[0]
			if self.list_program_sayisi > int(secili):
				self.uygulama_tree.set_cursor(secili + 1)

	def uygulama_tree_tiklandi(self,widget=None,path=None,coloumn=None):
		selection = self.uygulama_tree.get_selection()
		tree_model, tree_iter = selection.get_selected()
		subprocess.Popen(tree_model[tree_iter][2].split(), stdout=subprocess.PIPE)
		self.destroy()

	def kategori_liste_tiklandi(self,widget,path,coloumn):
		selection = self.kategori_tree.get_selection()
		tree_model, tree_iter = selection.get_selected()
		kategori = tree_model[tree_iter][1]
		self.uygulama_list_store_doldur(self.kategori_sozluk[kategori])

	def arama_degisti(self, aranan):
		self.kategori_tree.set_cursor(0)
		self.uygulama_list_store.clear()
		tamami = Gio.app_info_get_all()
		self.list_program_sayisi = -1
		for uyg in tamami:
			if uyg.get_name() != None and aranan.get_text().lower() in uyg.get_name().lower():
				self.uygulama_list_store.append([uyg.get_icon(), uyg.get_name(),uyg.get_executable()])
				self.list_program_sayisi += 1
			elif uyg.get_executable() != None and aranan.get_text().lower() in uyg.get_executable().lower():
				self.uygulama_list_store.append([uyg.get_icon(), uyg.get_name(),uyg.get_executable()])
				self.list_program_sayisi += 1
			elif uyg.get_description() != None and aranan.get_text().lower() in uyg.get_description().lower():
				self.uygulama_list_store.append([uyg.get_icon(), uyg.get_name(),uyg.get_executable()])
				self.list_program_sayisi += 1
			elif self.keywords_arama(uyg,aranan.get_text()):
				self.uygulama_list_store.append([uyg.get_icon(), uyg.get_name(),uyg.get_executable()])
				self.list_program_sayisi += 1
		self.uygulama_tree.set_cursor(0)

	def keywords_arama(self, app_info, aranan):
		for keyword in app_info.get_keywords():
			if aranan in keyword:
				return True
		return False
			

	def uygulama_list_store_doldur(self,kategoriler=None):
		self.uygulama_list_store.clear()
		tamami = Gio.app_info_get_all()
		self.list_program_sayisi = -1
		for uyg in tamami:
			if self.kategori_kontrol(uyg,kategoriler):
				self.uygulama_list_store.append([uyg.get_icon(), uyg.get_name(),uyg.get_executable()])
				self.list_program_sayisi += 1
		self.uygulama_tree.set_cursor(0)

	def kategori_kontrol(self,uygulama,kategoriler=None):
		if kategoriler == None or kategoriler[:-1] == [None]:
			return True
		for kategori in kategoriler[:-1]:
			if uygulama.get_categories() != None and kategori in uygulama.get_categories():
				return True
		return False

if __name__ == '__main__':
	pen = AramaPencere()
	pen.connect("destroy", Gtk.main_quit)
	pen.show_all()
	Gtk.main()