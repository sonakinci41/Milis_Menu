
from setuptools import setup, find_packages
import glob

datas = [('/usr/share/applications', ['data/milismenu.desktop']),
         ('/usr/share/icons/hicolor/256x256/apps', ['simgeler/milis_menu.svg']),
         ('/usr/share/milis_menu/simgeler',glob.glob("simgeler/*.svg")),]


setup(
    name = "milismenu",
    scripts = ["milismenu"],
    packages = find_packages(),
    version = "0.1",
    description = "Milis Menu",
    author = ["Fatih Kaya"],
    author_email = "sonakinci41@gmail.com",
    url = "https://github.com/sonakinci41/Milis_Menu",
    data_files = datas
)
