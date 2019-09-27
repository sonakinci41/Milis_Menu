import gi, subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk, Gdk


class AramaPencere(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)
		self.set_border_width(0)
		self.set_default_size(400,200)
		self.set_resizable(False)
		self.set_position(Gtk.WindowPosition.MOUSE)
		self.set_type_hint(Gdk.WindowTypeHint.UTILITY)

		self.list_program_sayisi = -1
		self.hb = Gtk.HeaderBar()
		self.hb.set_show_close_button(True)
		self.set_titlebar(self.hb)

		self.arama = Gtk.SearchEntry(max_width_chars=45)
		self.arama.connect("search-changed", self.arama_degisti)
		self.hb.pack_start(self.arama)

		self.islem_liste = Gtk.ListStore(Gio.ThemedIcon(), str, str)

		self.liste = Gtk.TreeView(model=self.islem_liste)
		self.scroll = Gtk.ScrolledWindow()
		self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		self.scroll.add(self.liste)
		self.add(self.scroll)
		self.liste_icerik = Gtk.ListStore(Gio.Icon, str)

		sutun_icon = Gtk.CellRendererPixbuf()
		sutun = Gtk.TreeViewColumn('Icon', sutun_icon, gicon=0)
		self.liste.append_column(sutun)

		sutun_text = Gtk.CellRendererText()
		sutun = Gtk.TreeViewColumn('Program Adı', sutun_text, text=1)
		self.liste.append_column(sutun)
		self.connect("key-press-event",self.tus_basildi)

		self.islem_liste_doldur()
		self.set_focus(self.arama)

	def tus_basildi(self, widget, event):
		if self.get_focus() != self.arama:
			self.set_focus(self.arama)
		basili_tus = event.keyval
		if basili_tus == Gdk.KEY_Return:
			selection = self.liste.get_selection()
			tree_model, tree_iter = selection.get_selected()
			subprocess.Popen(tree_model[tree_iter][2].split(), stdout=subprocess.PIPE)
			self.destroy()
		elif basili_tus == Gdk.KEY_Up:
			path_, coloumn_ = self.liste.get_cursor()
			secili = path_.get_indices()[0]
			if int(secili) > 0:
				self.liste.set_cursor(secili - 1)
		elif basili_tus == Gdk.KEY_Down:
			path_, coloumn_ = self.liste.get_cursor()
			secili = path_.get_indices()[0]
			if self.list_program_sayisi > int(secili):
				self.liste.set_cursor(secili + 1)

	def arama_degisti(self, kelime):
		self.islem_liste.clear()
		tamami = Gio.app_info_get_all()
		self.list_program_sayisi = -1
		for uyg in tamami:
			if uyg.get_name() != None and kelime.get_text().lower() in uyg.get_name().lower():
				self.islem_liste.append([uyg.get_icon(), uyg.get_name(),uyg.get_executable()])
				self.list_program_sayisi += 1
			elif uyg.get_executable() != None and kelime.get_text().lower() in uyg.get_executable().lower():
				self.islem_liste.append([uyg.get_icon(), uyg.get_name(),uyg.get_executable()])
				self.list_program_sayisi += 1
			elif uyg.get_description() != None and kelime.get_text().lower() in uyg.get_description().lower():
				self.islem_liste.append([uyg.get_icon(), uyg.get_name(),uyg.get_executable()])
				self.list_program_sayisi += 1
		self.liste.set_cursor(0)

	def islem_liste_doldur(self):
		tamami = Gio.app_info_get_all()
		self.list_program_sayisi = -1
		for uyg in tamami:
			self.islem_liste.append([uyg.get_icon(), uyg.get_name(),uyg.get_executable()])
			self.list_program_sayisi += 1


if __name__ == '__main__':
	pen = AramaPencere()
	pen.connect("destroy", Gtk.main_quit)
	pen.show_all()
	Gtk.main()