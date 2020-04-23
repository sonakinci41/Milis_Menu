#!/usr/bin/python3
from setuptools import setup, find_packages
import os

d = []
for icon in os.listdir("./icons"):
	d.append("icons/{}".format(icon))
datas = [("/usr/share/mmenu/icons",d),]




setup(
	name = "mmenu",
	scripts = ["mmenu"],
	packages = find_packages(),
	version = "1.0",
	description = "SoNAkıncı",
	author = ["Fatih Kaya"],
	author_email = "sonakinci41@gmail.com",
	url = "https://github.com/sonakinci41/Milis_Menu",
	data_files = datas
)
