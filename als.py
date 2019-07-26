# !/usr/bin/python3
# -*- coding: utf-8 -*-

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

import os
from datetime import datetime
import shutil
import numpy as np
import gettext
from PyQt5 import QtCore, QtGui, QtWidgets
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from alsui import Ui_stack_window  # import du fichier alsui.py généré par : pyuic5 alsui.ui -x -o alsui.py
from astropy.io import fits
from qimage2ndarray import array2qimage
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
import threading


# Local stuff
from Config import Config
import stack as stk
import preprocess as prepro
import resource_rc


name_of_tiff_image = "stack_image.tiff"
name_of_jpeg_image = "stack_image.jpg"
gettext.install('als', 'locale')
save_type = "jpeg"

class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath


class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""
    def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class image_ref_save:
    def __init__(self):
        self.image = []
        self.status = "stop"
        self.stack_image = []



class MyEventHandler(FileSystemEventHandler, QtCore.QThread, image_ref_save):
    created_signal = QtCore.pyqtSignal()
    new_image_path = ""

    def __init__(self):
        super().__init__()

    def on_created(self, event):
        # if not event.is_directory:
        if event.event_type == 'created':
            print("New image arrive: %s" % event.src_path)
            self.new_image_path = event.src_path
            self.created_signal.emit()


# ------------------------------------------------------------------------------


class WatchOutForFileCreations(QtCore.QThread):
    print_image = QtCore.pyqtSignal()

    def __init__(self, path, work_folder, align_on, save_on, stack_methode,
                 log, white_slider, black_slider, contrast_slider, brightness_slider,
                 R_slider, G_slider, B_slider, apply_button,
                 image_ref_save, dark_on, dark_path,
                 scnr_on, scnr_mode, scnr_value,
                 wavelets_on, wavelets_type, wavelets_use_luminance,
                 wavelet_1_value, wavelet_2_value, wavelet_3_value,
                 wavelet_4_value, wavelet_5_value):

        super().__init__()
        self.white_slider = white_slider
        self.black_slider = black_slider
        self.contrast_slider = contrast_slider
        self.brightness_slider = brightness_slider
        self.R_slider = R_slider
        self.G_slider = G_slider
        self.B_slider = B_slider
        self.apply_button = apply_button
        self.log = log
        self.path = path
        self.work_folder = work_folder
        self.first = 0
        self.counter = 0
        self.first_image = []
        self.image_ref_save = image_ref_save
        self.ref_image = []
        self.dark_on = dark_on  # need add dark in stack_live function
        self.dark_path = dark_path  # need add dark in stack_live function
        self.scnr_on = scnr_on
        self.scnr_mode = scnr_mode
        self.scnr_value = scnr_value
        self.wavelets_on = wavelets_on
        self.wavelets_type = wavelets_type
        self.wavelets_use_luminance = wavelets_use_luminance,
        self.wavelet_1_value = wavelet_1_value
        self.wavelet_2_value = wavelet_2_value
        self.wavelet_3_value = wavelet_3_value
        self.wavelet_4_value = wavelet_4_value
        self.wavelet_5_value = wavelet_5_value
        print(self.work_folder)
        print(self.path)

        # __ call watchdog __
        # call observer :
        self.observer = Observer()
        # call observer class :
        self.event_handler = MyEventHandler()
        self.observer.schedule(self.event_handler, self.path, recursive=False)
        self.observer.start()

        self.event_handler.created_signal.connect(lambda: self.created(self.event_handler.new_image_path,
                                                                       align_on, save_on, stack_methode))

    def created(self, new_image_path, align_on, save_on, stack_methode):
        if self.image_ref_save.status == "play" \
                and new_image_path.split("/")[-1][0] != "." \
                and new_image_path.split("/")[-1][0] != "~":
            self.counter = self.counter + 1
            self.log.append(_("Reading new frame..."))
            if self.first == 0:
                self.log.append(_("Reading first frame..."))
                self.first_image, limit, mode = stk.create_first_ref_im(self.work_folder, new_image_path,
                                                                        save_im=save_on)

                self.image_ref_save.image = self.first_image

                self.image_ref_save.stack_image = prepro.save_tiff(self.work_folder, self.image_ref_save.image,
                                                                   self.log,
                                                                   mode=mode, scnr_on=self.scnr_on,
                                                                   wavelets_on=self.wavelets_on,
                                                                   wavelets_type=str(self.wavelets_type.currentText()),
                                                                   wavelets_use_luminance=self.wavelets_use_luminance,
                                                                   param=[self.contrast_slider.value() / 10.,
                                                                          self.brightness_slider.value(),
                                                                          self.black_slider.value(),
                                                                          self.white_slider.value(),
                                                                          self.R_slider.value() / 100.,
                                                                          self.G_slider.value() / 100.,
                                                                          self.B_slider.value() / 100.,
                                                                          self.scnr_mode.currentText(),
                                                                          self.scnr_value.value(),
                                                                          {1: int(self.wavelet_1_value.text()) / 100.,
                                                                           2: int(self.wavelet_2_value.text()) / 100.,
                                                                           3: int(self.wavelet_3_value.text()) / 100.,
                                                                           4: int(self.wavelet_4_value.text()) / 100.,
                                                                           5: int(self.wavelet_5_value.text()) / 100.}],
                                                                   image_type=save_type)
                self.first = 1
                self.white_slider.setMaximum(np.int(limit))
                self.brightness_slider.setMaximum(np.int(limit) / 2.)
                self.brightness_slider.setMinimum(np.int(-1 * limit) / 2.)
                if self.white_slider.value() > limit:
                    self.white_slider.setSliderPosition(limit)
                elif self.white_slider.value() < -1 * limit:
                    self.white_slider.setSliderPosition(-1 * limit)
                self.black_slider.setMaximum(np.int(limit))
                if self.black_slider.value() > limit:
                    self.black_slider.setSliderPosition(limit)
                if self.brightness_slider.value() > limit / 2.:
                    self.brightness_slider.setSliderPosition(limit / 2.)
                if limit == 2. ** 16 - 1:
                    self.log.append(_("Read 16bit frame ..."))
                elif limit == 2. ** 8 - 1:
                    self.log.append(_("Read 8bit frame ..."))
                if mode == "rgb":
                    self.R_slider.setEnabled(True)
                    self.G_slider.setEnabled(True)
                    self.B_slider.setEnabled(True)
                self.white_slider.setEnabled(True)
                self.black_slider.setEnabled(True)
                self.contrast_slider.setEnabled(True)
                self.brightness_slider.setEnabled(True)
                self.apply_button.setEnabled(True)

            else:
                # appelle de la fonction stack live
                if align_on:
                    self.log.append(_("Stack and Align New frame..."))
                else:
                    self.log.append(_("Stack New frame..."))

                self.image_ref_save.image, limit, mode = stk.stack_live(self.work_folder, new_image_path,
                                                                        self.counter,
                                                                        ref=self.image_ref_save.image,
                                                                        first_ref=self.first_image,
                                                                        save_im=save_on,
                                                                        align=align_on,
                                                                        stack_methode=stack_methode)

                self.image_ref_save.stack_image = prepro.save_tiff(self.work_folder, self.image_ref_save.image,
                                                                   self.log,
                                                                   mode=mode, scnr_on=self.scnr_on,
                                                                   wavelets_on=self.wavelets_on,
                                                                   wavelets_type=str(self.wavelets_type.currentText()),
                                                                   wavelets_use_luminance=self.wavelets_use_luminance,
                                                                   param=[self.contrast_slider.value() / 10.,
                                                                          self.brightness_slider.value(),
                                                                          self.black_slider.value(),
                                                                          self.white_slider.value(),
                                                                          self.R_slider.value() / 100.,
                                                                          self.G_slider.value() / 100.,
                                                                          self.B_slider.value() / 100.,
                                                                          self.scnr_mode.currentText(),
                                                                          self.scnr_value.value(),
                                                                          {1: int(self.wavelet_1_value.text()) / 100.,
                                                                           2: int(self.wavelet_2_value.text()) / 100.,
                                                                           3: int(self.wavelet_3_value.text()) / 100.,
                                                                           4: int(self.wavelet_4_value.text()) / 100.,
                                                                           5: int(self.wavelet_5_value.text()) / 100.}],
                                                                   image_type=save_type)

                self.log.append(_("... Stack finished"))
            self.print_image.emit()
        else:
            self.log.append(_("New image detected but not considered"))


# ------------------------------------------------------------------------------


class als_main_window(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_stack_window()
        self.ui.setupUi(self)

        self.config = Config()
        self.ui.tFolder.setText(os.path.expanduser(self.config['Default']['folderscan']))
        self.ui.tDark.setText(os.path.expanduser(self.config['Default']['filedark']))
        self.ui.tWork.setText(os.path.expanduser(self.config['Default']['folderwork']))

        self.connect_actions()
        self.running = False
        self.counter = 0
        self.align = False
        self.dark = False
        self.pause = False
        self.image_ref_save = image_ref_save()

        self.setWindowTitle(_("Astro Live Stacker"))

    def closeEvent(self, event):
        super().closeEvent(event)



    def connect_actions(self):

        # connection for buttom
        self.ui.pbPlay.clicked.connect(self.cb_play)
        self.ui.pbStop.clicked.connect(self.cb_stop)
        self.ui.pbReset.clicked.connect(self.cb_reset)
        self.ui.pbPause.clicked.connect(self.cb_pause)
        self.ui.pbSave.clicked.connect(self.cb_save)
        self.ui.bBrowseFolder.clicked.connect(self.cb_browse_folder)
        self.ui.bBrowseDark.clicked.connect(self.cb_browse_dark)
        self.ui.bBrowseWork.clicked.connect(self.cb_browse_work)
        self.ui.pb_apply_value.clicked.connect(lambda: self.apply_value(self.counter, self.ui.tWork.text()))
        self.ui.cbWww.stateChanged.connect(self.wwwcheck)

        # update slider
        self.ui.contrast_slider.valueChanged['int'].connect(
            lambda: self.ui.contrast.setNum(self.ui.contrast_slider.value() / 10))
        self.ui.brightness_slider.valueChanged['int'].connect(self.ui.brightness.setNum)
        self.ui.black_slider.valueChanged['int'].connect(self.ui.black.setNum)
        self.ui.white_slider.valueChanged['int'].connect(self.ui.white.setNum)
        self.ui.R_slider.valueChanged['int'].connect(lambda: self.ui.R_value.setNum(self.ui.R_slider.value() / 100.))
        self.ui.G_slider.valueChanged['int'].connect(lambda: self.ui.G_value.setNum(self.ui.G_slider.value() / 100.))
        self.ui.B_slider.valueChanged['int'].connect(lambda: self.ui.B_value.setNum(self.ui.B_slider.value() / 100.))
        self.ui.SCNR_Slider.valueChanged['int'].connect(
            lambda: self.ui.SCNR_value.setNum(self.ui.SCNR_Slider.value() / 100.))

    # ------------------------------------------------------------------------------
    # Callbacks

    def wwwcheck(self):
        if (self.ui.cbWww.isChecked()):
            self.web_dir = os.path.join(os.path.dirname(__file__),
                                        os.path.expanduser(self.config['Default']['folderwork']))
            self.httpd = HTTPServer(self.web_dir, ("", 8000))
            self.thread = StoppableThread(target=self.httpd.serve_forever)
            self.thread.deamon = False
            self.thread.start()

        else:
            self.thread.stop(self)
            self.httpd.shutdown()

    def cb_save(self):
        timestamp = str(datetime.fromtimestamp(datetime.timestamp(datetime.now())))
        self.ui.log.append(_("Saving : ") + "stack_image_" + timestamp + ".fit")
        # save stack image in fit
        red = fits.PrimaryHDU(data=self.image_ref_save.image)
        red.writeto(self.ui.tWork.text() + "/" + "stack_image_" + timestamp + ".fit")
        # red.close()
        del red

    def apply_value(self, counter, work_folder):
        if counter > 0:
            self.ajuste_value(work_folder)
            self.update_image(work_folder, add=False)
        self.ui.log.append(_("Define new display value"))

    def ajuste_value(self, work_folder):

        # test rgb or gray
        if len(self.image_ref_save.image.shape) == 2:
            mode = "gray"
        elif len(self.image_ref_save.image.shape) == 3:
            mode = "rgb"
        else:
            raise ValueError(_("fit format not supported"))

        self.image_ref_save.stack_image = prepro.save_tiff(work_folder, self.image_ref_save.image, self.ui.log,
                                                           mode=mode,
                                                           scnr_on=self.ui.cbSCNR.isChecked(),
                                                           wavelets_on=self.ui.cbWavelets.isChecked(),
                                                           wavelets_type=str(self.ui.cBoxWaveType.currentText()),
                                                           wavelets_use_luminance=self.ui.cbLuminanceWavelet.isChecked(),
                                                           param=[self.ui.contrast_slider.value() / 10.,
                                                                  self.ui.brightness_slider.value(),
                                                                  self.ui.black_slider.value(),
                                                                  self.ui.white_slider.value(),
                                                                  self.ui.R_slider.value() / 100.,
                                                                  self.ui.G_slider.value() / 100.,
                                                                  self.ui.B_slider.value() / 100.,
                                                                  self.ui.cmSCNR.currentText(),
                                                                  self.ui.SCNR_Slider.value() / 100.,
                                                                  {1: int(self.ui.wavelet_1_label.text()) / 100.,
                                                                   2: int(self.ui.wavelet_2_label.text()) / 100.,
                                                                   3: int(self.ui.wavelet_3_label.text()) / 100.,
                                                                   4: int(self.ui.wavelet_4_label.text()) / 100.,
                                                                   5: int(self.ui.wavelet_5_label.text()) / 100.}],
                                                           image_type=save_type)

        self.ui.log.append(_("Adjust GUI image"))

    def update_image(self, work_folder, add=True):
        if add:
            self.counter = self.counter + 1
            self.ui.cnt.setText(str(self.counter))

        # read tiff ( need save_type = "tiff") :
        # pixmap_tiff = QtGui.QPixmap(os.path.expanduser(work_folder + "/" + name_of_tiff_image))

        # read tiff ( need save_type = "jpeg") :
        # pixmap_tiff = QtGui.QPixmap(os.path.expanduser(work_folder + "/" +

        # read image in RAM ( need save_type = "no"):
        qimage_tiff = array2qimage(self.image_ref_save.stack_image, normalize=(2**16-1))
        pixmap_tiff = QtGui.QPixmap.fromImage(qimage_tiff)

        if pixmap_tiff.isNull():
            self.ui.log.append(_("invalid frame"))

        pixmap_tiff_resize = pixmap_tiff.scaled(self.ui.image_stack.frameGeometry().width(),
                                                self.ui.image_stack.frameGeometry().height(),
                                                QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.ui.image_stack.setPixmap(pixmap_tiff_resize)
        self.ui.log.append(_("Updated GUI image"))
        print(_("Updated GUI image"))

    def cb_browse_folder(self):
        DirName = QtWidgets.QFileDialog.getExistingDirectory(self, _("Scan folder"), self.ui.tFolder.text())
        if DirName:
            self.ui.tFolder.setText(DirName)
            self.ui.pbPlay.setEnabled(True)
            self.config['Default']['folderscan'] = DirName

    def cb_browse_dark(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, _("Dark file"), "",
                                                            "Fit Files (*.fit);;All Files (*)")
        if fileName:
            self.ui.tDark.setText(fileName)
            self.config['Default']['filedark'] = fileName

    def cb_browse_work(self):
        DirName = QtWidgets.QFileDialog.getExistingDirectory(self, _("Work folder"), self.ui.tWork.text())
        if DirName:
            self.ui.tWork.setText(DirName)
            self.config['Default']['folderwork'] = DirName

    def cb_play(self):
        self.startwww()
        if self.ui.tFolder.text() != "":

            if self.image_ref_save.status == "stop":
                self.ui.white_slider.setEnabled(False)
                self.ui.black_slider.setEnabled(False)
                self.ui.contrast_slider.setEnabled(False)
                self.ui.brightness_slider.setEnabled(False)
                self.ui.R_slider.setEnabled(False)
                self.ui.G_slider.setEnabled(False)
                self.ui.B_slider.setEnabled(False)
                self.ui.pb_apply_value.setEnabled(False)
                self.ui.image_stack.setPixmap(QtGui.QPixmap(":/icons/dslr-camera.svg"))
                self.counter = 0
                self.ui.cnt.setText(str(self.counter))
                # Print scan folder
                self.ui.log.append(_("Scan folder : ") + os.path.expanduser(self.ui.tFolder.text()))
                # Print work folder
                self.ui.log.append(_("Work folder : ") + os.path.expanduser(self.ui.tWork.text()))

                # check align
                if self.ui.cbAlign.isChecked():
                    self.align = True

                # check dark
                if (self.ui.cbDark.isChecked()) & (self.ui.tDark.text() != ""):
                    self.ui.log.append("Dark : " + os.path.expanduser(self.ui.tDark.text()))
                    self.dark = True

                # Print live method
                if self.align and self.dark:
                    self.ui.log.append(_("Play with alignement type: ") + self.ui.cmMode.currentText() + " and Dark")
                elif self.align:
                    self.ui.log.append(_("Play with alignement type: ") + self.ui.cmMode.currentText())
                else:
                    self.ui.log.append(_("Play with NO alignement"))

                # Lancement du watchdog
                self.fileWatcher = WatchOutForFileCreations(os.path.expanduser(self.ui.tFolder.text()),
                                                            os.path.expanduser(self.ui.tWork.text()),
                                                            self.align,
                                                            self.ui.cbKeep.isChecked(),
                                                            self.ui.cmMode.currentText(),
                                                            self.ui.log,
                                                            self.ui.white_slider,
                                                            self.ui.black_slider,
                                                            self.ui.contrast_slider,
                                                            self.ui.brightness_slider,
                                                            self.ui.R_slider,
                                                            self.ui.G_slider,
                                                            self.ui.B_slider,
                                                            self.ui.pb_apply_value,
                                                            self.image_ref_save,
                                                            self.dark,
                                                            os.path.expanduser(self.ui.tDark.text()),
                                                            self.ui.cbSCNR,
                                                            self.ui.cmSCNR,
                                                            self.ui.SCNR_Slider,
                                                            self.ui.cbWavelets,
                                                            self.ui.cBoxWaveType,
                                                            self.ui.cbLuminanceWavelet,
                                                            self.ui.wavelet_1_label,
                                                            self.ui.wavelet_2_label,
                                                            self.ui.wavelet_3_label,
                                                            self.ui.wavelet_4_label,
                                                            self.ui.wavelet_5_label)

                if os.path.exists(os.path.expanduser(self.ui.tWork.text())):
                    shutil.rmtree(os.path.expanduser(self.ui.tWork.text()) + "/")
                    os.mkdir(os.path.expanduser(self.ui.tWork.text()))
                else:
                    os.mkdir(os.path.expanduser(self.ui.tWork.text()))

                self.fileWatcher.start()
                self.fileWatcher.print_image.connect(
                    lambda: self.update_image(self.ui.tWork.text(), name_of_tiff_image))
            else:
                self.ui.log.append("Play")

            self.image_ref_save.status = "play"
            self.image_ref_save.image = []
            self.image_ref_save.stack_image = []
            # desactivate play button
            self.ui.pbPlay.setEnabled(False)
            self.ui.pbReset.setEnabled(False)
            # activate stop button
            self.ui.pbStop.setEnabled(True)
            # activate pause button
            self.ui.pbPause.setEnabled(True)

        else:
            self.ui.log.append(_("No path"))

    def cb_stop(self):


        self.fileWatcher.observer.stop()
        self.image_ref_save.status = "stop"
        self.image_ref_save.image = []
        self.image_ref_save.stack_image = []
        self.ui.pbStop.setEnabled(False)
        self.ui.pbPlay.setEnabled(True)
        self.ui.pbReset.setEnabled(True)
        self.ui.pbPause.setEnabled(False)
        self.ui.log.append("Stop")

    def cb_pause(self):
        # self.fileWatcher.observer.stop()
        self.image_ref_save.status = "pause"
        self.ui.pbStop.setEnabled(False)
        self.ui.pbPlay.setEnabled(True)
        self.ui.pbReset.setEnabled(False)
        self.ui.pbPause.setEnabled(False)
        self.ui.log.append("Pause")

    def cb_reset(self):
        self.ui.log.append("Reset")
        # reset slider, label, image, global value

        self.ui.contrast_slider.setValue(10)
        self.ui.brightness_slider.setValue(0)
        self.ui.black_slider.setValue(0)
        self.ui.white_slider.setValue(65535)
        self.ui.R_slider.setValue(100)
        self.ui.G_slider.setValue(100)
        self.ui.B_slider.setValue(100)
        self.ui.image_stack.setPixmap(QtGui.QPixmap(":/icons/dslr-camera.svg"))
        self.image_ref_save.image = []
        self.image_ref_save.stack_image = []
        self.ui.contrast.setText(str(1))
        self.ui.brightness.setText(str(0))
        self.ui.black.setText(str(0))
        self.ui.white.setText(str(65535))
        self.counter = 0
        self.ui.cnt.setText(str(self.counter))
        self.ui.white_slider.setEnabled(False)
        self.ui.black_slider.setEnabled(False)
        self.ui.contrast_slider.setEnabled(False)
        self.ui.brightness_slider.setEnabled(False)
        self.ui.R_slider.setEnabled(False)
        self.ui.G_slider.setEnabled(False)
        self.ui.B_slider.setEnabled(False)
        self.ui.pb_apply_value.setEnabled(False)

    def main(self):
        self.show()


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = als_main_window()
    window.main()
    sys.exit(app.exec_())
