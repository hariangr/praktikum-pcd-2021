from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QSize
import sys
import os

from PIL import Image, ImageQt
import cv2  # Dipakai untuk load gambar saja
import numpy as np

uiFile = os.path.join(os.path.dirname(__file__), 'basic.ui')


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(uiFile, self)
        self.show()

        self.srcQimg = None
        self.copiedQimg = None

        self.findChild(QtWidgets.QPushButton, 'btnOpen').clicked.connect(
            self.btnOpenClicked)
        self.findChild(QtWidgets.QPushButton, 'btnCopy').clicked.connect(
            self.btnCopyClicked)
        self.findChild(QtWidgets.QPushButton, 'btnExit').clicked.connect(
            self.btnExitClicked)

        self.imgCopied = self.findChild(QtWidgets.QLabel, 'imgCopied')
        self.imgProcessed = self.findChild(QtWidgets.QLabel, 'imgProcessed')
        self.imgSrc = self.findChild(QtWidgets.QLabel, 'imgSrc')

        self.findChild(QtWidgets.QRadioButton,
                       'radioR').clicked.connect(self.radioRClicked)
        self.findChild(QtWidgets.QRadioButton,
                       'radioG').clicked.connect(self.radioGClicked)
        self.findChild(QtWidgets.QRadioButton,
                       'radioB').clicked.connect(self.radioBClicked)
        self.findChild(QtWidgets.QRadioButton,
                       'radioC').clicked.connect(self.radioCClicked)
        self.findChild(QtWidgets.QRadioButton,
                       'radioM').clicked.connect(self.radioMClicked)
        self.findChild(QtWidgets.QRadioButton,
                       'radioY').clicked.connect(self.radioYClicked)

    def radioRClicked(self):
        if not self.copiedQimg:
            return
        w, h = self.copiedQimg.width(), self.copiedQimg.height()
        res = QImage(w, h, QImage.Format_RGB32)
        for i in range(h):
            for j in range(w):
                px = QColor(self.copiedQimg.pixel(j, i)).red()
                pxNew = QColor(px, px, px)
                res.setPixel(j, i, pxNew.rgb())
        self.imgProcessed.setPixmap(QPixmap.fromImage(res))

    def radioGClicked(self):
        if not self.copiedQimg:
            return
        w, h = self.copiedQimg.width(), self.copiedQimg.height()
        res = QImage(w, h, QImage.Format_RGB32)
        for i in range(h):
            for j in range(w):
                px = QColor(self.copiedQimg.pixel(j, i)).green()
                pxNew = QColor(px, px, px)
                res.setPixel(j, i, pxNew.rgb())
        self.imgProcessed.setPixmap(QPixmap.fromImage(res))

    def radioBClicked(self):
        if not self.copiedQimg:
            return
        w, h = self.copiedQimg.width(), self.copiedQimg.height()
        res = QImage(w, h, QImage.Format_RGB32)
        for i in range(h):
            for j in range(w):
                px = QColor(self.copiedQimg.pixel(j, i)).blue()
                pxNew = QColor(px, px, px)
                res.setPixel(j, i, pxNew.rgb())
        self.imgProcessed.setPixmap(QPixmap.fromImage(res))

    def radioCClicked(self):
        if not self.copiedQimg:
            return
        w, h = self.copiedQimg.width(), self.copiedQimg.height()
        res = QImage(w, h, QImage.Format_RGB32)
        for i in range(h):
            for j in range(w):
                px = QColor(self.copiedQimg.pixel(j, i)).cyan()
                pxNew = QColor(px, px, px)
                res.setPixel(j, i, pxNew.rgb())
        self.imgProcessed.setPixmap(QPixmap.fromImage(res))

    def radioMClicked(self):
        if not self.copiedQimg:
            return
        w, h = self.copiedQimg.width(), self.copiedQimg.height()
        res = QImage(w, h, QImage.Format_RGB32)
        for i in range(h):
            for j in range(w):
                px = QColor(self.copiedQimg.pixel(j, i)).magenta()
                pxNew = QColor(px, px, px)
                res.setPixel(j, i, pxNew.rgb())
        self.imgProcessed.setPixmap(QPixmap.fromImage(res))

    def radioYClicked(self):
        if not self.copiedQimg:
            return
        w, h = self.copiedQimg.width(), self.copiedQimg.height()
        res = QImage(w, h, QImage.Format_RGB32)
        for i in range(h):
            for j in range(w):
                px = QColor(self.copiedQimg.pixel(j, i)).yellow()
                pxNew = QColor(px, px, px)
                res.setPixel(j, i, pxNew.rgb())
        self.imgProcessed.setPixmap(QPixmap.fromImage(res))

    def btnOpenClicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        if not fileName:
            return
        # self.srcQimg = QImage(fileName=fileName, format=QImage.Format_RGB32)
        with open(fileName, 'rb') as f:
            self.srcQimg = QImage.fromData(f.read())
            self.imgSrc.setPixmap(QPixmap.fromImage(self.srcQimg))

    def btnExitClicked(self):
        self.close()

    def btnCopyClicked(self):
        if not self.srcQimg:
            print("No source selected")
            return
        srcW, srcH = self.srcQimg.width(), self.srcQimg.height()

        # Buat blank canvas sesuai ukuran src
        self.copiedQimg = QImage(QSize(srcW, srcH), QImage.Format_ARGB32)

        for i in range(srcH):
            for j in range(srcW):
                srcPx = QColor(self.srcQimg.pixel(j, i))
                self.copiedQimg.setPixel(j, i, srcPx.rgb())

        self.imgCopied.setPixmap(QPixmap.fromImage(self.copiedQimg))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
