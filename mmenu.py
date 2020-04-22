import gi, subprocess, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk, Gdk, GdkPixbuf


class MMenu(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)
		self.categories = {"All":[],
							"Favorites":[],
							"Development":[],
							"Education":[],
							"Favorites":[],
							"Game":[],
							"Graphics":[],
							"Multimedia":[],
							"Network":[],
							"Office":[],
							"Science":[],
							"System":[],
							"Utility":[],
							"Other":[],}
		self.get_applications()

		#Settings
		self.menu_with = 640
		self.menu_height = 400
		self.is_full_screen = True


		self.icon_dir = os.path.expanduser("~/.config/mmenu/icons/")
		if not os.path.exists(self.icon_dir):
			self.icon_dir = "./icons/"

		m_box = Gtk.VBox()
		#box.set_spacing(20)
		self.add(m_box)

		search_entry = Gtk.SearchEntry()
		search_entry.connect("search-changed",self.change_search_entry)
		s_box = Gtk.HBox()
		s_box.pack_start(search_entry,True,True,10)
		m_box.pack_start(s_box,False,True,10)

		switcher = Gtk.StackSwitcher()

		self.stack = Gtk.Stack()
		self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		self.stack.set_transition_duration(1000)
		self.mapp_stack = MAppStack(self)
		self.mbin_stack = MBinStack(self)
		self.stack.add_titled(self.mapp_stack,"apps","Applications")
		self.stack.add_titled(self.mbin_stack,"bins","Bins")

		switcher.set_stack(self.stack)
		s_box = Gtk.HBox()
		s_box.pack_start(switcher,True,False,0)
		m_box.pack_start(s_box,False,True,0)
		m_box.pack_end(self.stack,True,True,10)


		self.set_menu_position()


	def set_menu_position(self):
		if self.is_full_screen:
			self.fullscreen()
		else:
			x,y,w,h = self.get_global_pointer()
			if x < w/2:
				x = 10
			else:
				x = w - 10 - self.menu_with
			if y < h/2:
				y = 10
			else:
				y = h - 10 - self.menu_height
			self.move(x,y)
			self.set_default_size(self.menu_with,self.menu_height)		


	def get_global_pointer(self):
		root_win = Gdk.get_default_root_window()
		pointer = root_win.get_pointer()
		return (pointer.x, pointer.y,root_win.get_width(),root_win.get_height())


	def get_applications(self):
		"Applications get and set categories"
		apps = Gio.DesktopAppInfo.get_all()
		for app in apps:
			name_ = app.get_name()
			desc_ = app.get_description()
			icon_ = app.get_icon()
			mime_ = app.get_supported_types()
			exec_ = app.get_executable()
			cteg_ = app.get_categories()
			desktop_ = app.get_id()
			app = [name_,desc_,icon_,app,desktop_,exec_]
			self.set_categories(app,cteg_)


	def set_categories(self,app,cteg):
		if cteg == None:
			self.categories["Other"].append(app)
		else:
			ctegs = cteg.split(";")
			for c in ctegs:
				if c in self.categories.keys():
					self.categories[c].append(app)
				elif c == "AudioVideo" or c == "Audio" or c == "Video":
					if app not in self.categories["Multimedia"]:
						self.categories["Multimedia"].append(app)
		self.categories["All"].append(app)


	def change_search_entry(self,widget):
		search_text = widget.get_text().lower()
		stack_name = self.stack.get_visible_child_name()
		if stack_name == "apps":
			self.mapp_stack.cteg_list.set_cursor(0)
			if search_text != "":
				find_apps = []
				for app in self.categories["All"]:
					name = app[0]
					desc = app[1]
					if name == None:
						name = ""
					if desc == None:
						desc = ""
					name = name.lower()
					desc = desc.lower()
					if search_text in name or search_text in desc:
						find_apps.append(app)
				self.mapp_stack.set_apps(find_apps)
		elif stack_name == "bins":
			print(search_text)



class MAppStack(Gtk.HPaned):
	def __init__(self,parent):
		Gtk.Window.__init__(self)
		self.parent = parent
		self.set_position(175)
		self.d_icon_theme = Gtk.IconTheme.get_default()

		#Settings
		self.icon_size = 32



		l_box = Gtk.HBox()
		r_box = Gtk.HBox()
		self.pack1(l_box)
		self.pack2(r_box)


		self.cteg_store = Gtk.ListStore(GdkPixbuf.Pixbuf,str)
		self.cteg_list = Gtk.TreeView(model=self.cteg_store)
		self.cteg_list.connect("cursor-changed",self.activated_cteg_list)
		renderer = Gtk.CellRendererPixbuf()
		coloumn = Gtk.TreeViewColumn("Icon",renderer, gicon = 0)
		self.cteg_list.append_column(coloumn)
		renderer = Gtk.CellRendererText()
		coloumn = Gtk.TreeViewColumn("Categories",renderer, text = 1)
		self.cteg_list.append_column(coloumn)
		l_box.pack_start(self.set_scroll_win(self.cteg_list),True,True,10)


		self.apps_store = Gtk.ListStore(str,GdkPixbuf.Pixbuf,Gio.DesktopAppInfo)
		self.apps_list = Gtk.IconView(model=self.apps_store)
		self.apps_list.connect("item-activated",self.activated_apps_list)
		self.apps_list.set_text_column(0)
		self.apps_list.set_pixbuf_column(1)
		r_box.pack_start(self.set_scroll_win(self.apps_list),True,True,10)

		self.set_categories()

		#Default Selection List
		self.cteg_list.set_cursor(0)


	def set_scroll_win(self,list_):
		scroll = Gtk.ScrolledWindow()
		scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scroll.add(list_)
		return scroll


	def set_categories(self):
		for category in self.parent.categories.keys():
			if len(self.parent.categories[category]) != 0:
				icon = GdkPixbuf.Pixbuf.new_from_file(self.parent.icon_dir+category+".svg")
				self.cteg_store.append([icon,category])
			elif category == "All":
				icon = GdkPixbuf.Pixbuf.new_from_file(self.parent.icon_dir+category+".svg")
				self.cteg_store.append([icon,category])


	def activated_cteg_list(self,widget):
		selection = widget.get_selection()
		tree_model, tree_iter = selection.get_selected()
		categories = tree_model[tree_iter][1]
		self.set_apps(self.parent.categories[categories])


	def activated_apps_list(self,widget,path):
		model = widget.get_model()
		app = model[path][2]
		app.launch(None,None)
		self.parent.destroy()


	def set_apps(self,apps):
		self.apps_store.clear()
		for app in apps:
			if app[2] == None:
				p_b = GdkPixbuf.Pixbuf.new_from_file_at_size(self.parent.icon_dir+"System.svg",
															self.icon_size,
															self.icon_size)
			else:
				p_b = self.get_icon(app[2].to_string())
			self.apps_store.append([app[0],p_b,app[3]])


	def get_icon(self,icon_name):
		try:
			icon = self.d_icon_theme.load_icon(icon_name,self.icon_size,Gtk.IconLookupFlags.FORCE_REGULAR)
		except:
			if os.path.exists(icon_name):
				icon =  GdkPixbuf.Pixbuf.new_from_file_at_size(icon_name,
																self.icon_size,
																self.icon_size)
			else:
				icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.parent.icon_dir+"System.svg",
																self.icon_size,
																self.icon_size)
		return icon


class MBinStack(Gtk.Grid):
	def __init__(self,parent):
		Gtk.Window.__init__(self)
		self.set_column_spacing(5)
		self.set_row_spacing(5)

		self.sistem_dili_label = Gtk.Label()
		self.sistem_dili_label.set_text("OFFF")
		self.sistem_dili_label.set_hexpand(True)
		self.attach(self.sistem_dili_label,0,0,1,1)
		



if __name__ == '__main__':
	pen = MMenu()
	pen.connect("destroy", Gtk.main_quit)
	pen.show_all()
	Gtk.main()