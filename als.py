# ALS - Astro Live Stacker
# Copyright (C) 2019  Sébastien Durand (Dragonlost) - Gilles Le Maréchal (Gehelem)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime
import shutil
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from alsui import Ui_stack_window  # import du fichier alsui.py généré par : pyuic5 alsui.ui -x -o alsui.py

# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import stack as stk


class MyEventHandler(FileSystemEventHandler, QtCore.QThread):
    created_signal = QtCore.pyqtSignal()
    new_image_path = ""

    def __init__(self):
        super(MyEventHandler, self).__init__()

    def on_created(self, event):
        # if not event.is_directory:
        if event.event_type == 'created':
            print("New image arrive: %s" % event.src_path)
            self.new_image_path = event.src_path
            self.created_signal.emit()


# ------------------------------------------------------------------------------


class WatchOutForFileCreations(QtCore.QThread):
    print_image = QtCore.pyqtSignal()

    def __init__(self, path, work_folder, align_on, save_on, stack_methode):
        super(WatchOutForFileCreations, self).__init__()
        self.path = path
        self.work_folder = work_folder
        self.first = 0
        self.counter = 0
        print(self.work_folder)
        print(self.path)
        self.observer = Observer()
        self.event_handler = MyEventHandler()
        self.observer.schedule(self.event_handler, self.path, recursive=False)
        self.observer.start()
        self.event_handler.created_signal.connect(lambda: self.created(self.event_handler.new_image_path,
                                                                       align_on, save_on, stack_methode))

    def run(self):
        pass

    def created(self, new_image_path, align_on, save_on, stack_methode):
        self.counter = self.counter + 1
        if self.first == 0:
            stk.create_first_ref_im(self.work_folder, new_image_path, "stack_ref_image.fit", save_im=save_on)
            print("first file created : %s" % self.work_folder + "/stack_ref_image.fit")
            self.first = 1
        else:
            # appelle de la fonction stack live
            stk.stack_live(self.work_folder, new_image_path, "stack_ref_image.fit", self.counter,
                           save_im=save_on, align=align_on, stack_methode=stack_methode)
            print("file created : %s" % self.work_folder + "/stack_ref_image.fit")
        self.print_image.emit()


# ------------------------------------------------------------------------------


class als_main_window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(als_main_window, self).__init__(parent)
        self.ui = Ui_stack_window()
        self.ui.setupUi(self)
        self.check_folders()

        self.connect_actions()
        self.running = False
        self.counter = 0
        self.align = False
        self.dark = False

    def check_folders(self):
        if not os.path.exists(os.path.expanduser(self.ui.tWork.text())):
            self.cb_browse_work()

        if not os.path.exists(os.path.expanduser(self.ui.tFolder.text())):
            self.cb_browse_folder()

    def connect_actions(self):

        self.ui.pbPlay.clicked.connect(self.cb_play)
        self.ui.pbStop.clicked.connect(self.cb_stop)
        self.ui.pbReset.clicked.connect(self.cb_reset)
        self.ui.pbSave.clicked.connect(self.cb_save)
        self.ui.bBrowseFolder.clicked.connect(self.cb_browse_folder)
        self.ui.bBrowseDark.clicked.connect(self.cb_browse_dark)
        self.ui.bBrowseWork.clicked.connect(self.cb_browse_work)

    # ------------------------------------------------------------------------------
    # Callbacks
    def cb_save(self):
        timestamp = str(datetime.fromtimestamp(datetime.timestamp(datetime.now())))
        self.ui.log.append("Saving : stack-"+timestamp+".fit")
        shutil.copy(os.path.expanduser(self.ui.tWork.text())+"/stack_ref_image.fit",
                    os.path.expanduser(self.ui.tWork.text())+"/stack-"+timestamp+".fit")

    def update_image(self):
        self.counter = self.counter+1
        self.ui.cnt.setText(str(self.counter))
        effect = QtWidgets.QGraphicsColorizeEffect(self.ui.image_stack)
        effect.setStrength(0.0)
        self.ui.image_stack.setGraphicsEffect(effect)
        pixmap_tiff = QtGui.QPixmap(os.path.expanduser(self.ui.tWork.text() + "/" + "stack_image.tiff"))
        if pixmap_tiff.isNull():
            print("Image non valide !")
        pixmap_tiff_resize = pixmap_tiff.scaled(self.ui.image_stack.frameGeometry().width(),
                                                self.ui.image_stack.frameGeometry().height(),
                                                QtCore.Qt.KeepAspectRatio)
        self.ui.image_stack.setPixmap(pixmap_tiff_resize)

    def cb_browse_folder(self):
        DirName = QtWidgets.QFileDialog.getExistingDirectory(self, "Veuillez indiquer le répertoire à scanner", self.ui.tFolder.text())
        if DirName:
            self.ui.tFolder.setText(DirName)
            self.ui.pbPlay.setEnabled(True)

    def cb_browse_dark(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Fichier de Dark", "",
                                                            "Fit Files (*.fit);;All Files (*)")
        if fileName:
            self.ui.tDark.setText(fileName)

    def cb_browse_work(self):
        DirName = QtWidgets.QFileDialog.getExistingDirectory(self, "Veuillez indiquer votre répertoire de travail", self.ui.tWork.text())
        if DirName:
            self.ui.tWork.setText(DirName)

    def cb_play(self):
        if self.ui.tFolder.text() != "":

            # Print scan folder
            self.ui.log.append("Dossier a scanner : " + os.path.expanduser(self.ui.tFolder.text()))
            # Print work folder
            self.ui.log.append("Dossier de travail : " + os.path.expanduser(self.ui.tWork.text()))

            # check align
            if self.ui.cbAlign.isChecked():
                self.align = True

            # check dark
            if (self.ui.cbDark.isChecked()) & (self.ui.tDark.text() != ""):
                self.ui.log.append("Dark : " + os.path.expanduser(self.ui.tDark.text()))
                self.dark = True

            # Print live method
            if self.align and self.dark:
                self.ui.log.append("Play with alignement type: " + self.ui.cmMode.currentText() + " and Dark")
            elif self.align:
                self.ui.log.append("Play with alignement type: " + self.ui.cmMode.currentText())
            else:
                self.ui.log.append("Play with NO alignement")

            # Lancement du watchdog
            self.fileWatcher = WatchOutForFileCreations(os.path.expanduser(self.ui.tFolder.text()),
                                                        os.path.expanduser(self.ui.tWork.text()),
                                                        self.align,
                                                        self.ui.cbKeep.isChecked(),
                                                        self.ui.cmMode.currentText())

            if os.path.exists(os.path.expanduser(self.ui.tWork.text())):
                shutil.rmtree(os.path.expanduser(self.ui.tWork.text())+"/")
            os.mkdir(os.path.expanduser(self.ui.tWork.text())) 

            self.fileWatcher.start()
            self.running = True

            # desactivate play button
            self.ui.pbPlay.setEnabled(False)
            # activate stop button
            self.ui.pbStop.setEnabled(True)
            self.counter = 0
            self.fileWatcher.print_image.connect(lambda: self.update_image())
        else:
            self.ui.log.append("No have path")

    def cb_stop(self):
        self.fileWatcher.observer.stop()
        self.running = False
        self.ui.pbStop.setEnabled(False)
        self.ui.pbPlay.setEnabled(True)
        self.ui.log.append("Stop")

    def cb_reset(self):
        self.ui.log.append("Reset")

    def main(self):
        self.show()


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = als_main_window()
    window.main()
    sys.exit(app.exec_())
