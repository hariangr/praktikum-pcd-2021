from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QFileDialog, QInputDialog
from PyQt5.QtCore import QSize
import sys
import os
import math

uiFile = os.path.join(os.path.dirname(__file__), 'basic.ui')


def remap(v, min, max, newMin, newMax):
    OldRange = (max - min)
    NewRange = (newMax - newMin)
    NewValue = (((v - min) * NewRange) / OldRange) + newMin
    return NewValue


def doPxOperation(inQImage, pxOperation):
    if not inQImage:
        return None

    w, h = inQImage.width(), inQImage.height()
    res = QImage(w, h, QImage.Format_RGB32)
    for i in range(h):
        for j in range(w):
            px = QColor(inQImage.pixel(j, i))
            pxNew = pxOperation(px)
            res.setPixel(j, i, pxNew.rgb())
    return res


def pxCvGray(src):
    v = (src.red() + src.green() + src.blue()) / 3
    return QColor(v, v, v)


def pxToBinerHOF(thres):
    def _higherOrderFunction(src):
        v = src.red()  # Input adalah gambar gs, ketiga channel sama
        if v < thres:
            return QColor(0, 0, 0)
        else:
            return QColor(255, 255, 255)

    return _higherOrderFunction

def pxAddBrighness(c):
    def _higherOrderFunction(src):
        v = src.red()  # Input adalah gambar gs, ketiga channel sama
        _new_v = min(max(v + c, 0), 255)
        return QColor(_new_v, _new_v, _new_v)

    return _higherOrderFunction


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(uiFile, self)
        self.show()

        self.srcQimg = None
        self.gsQimg = None

        self.findChild(QtWidgets.QPushButton, 'btnOpen').clicked.connect(
            self.btnOpenClicked)
        self.findChild(QtWidgets.QPushButton, 'btnExit').clicked.connect(
            self.btnExitClicked)

        self.findChild(QtWidgets.QPushButton, 'btnGs').clicked.connect(
            self.btnGsClicked)
        self.findChild(QtWidgets.QPushButton, 'btnBiner').clicked.connect(
            self.btnBinerClicked)
        self.findChild(QtWidgets.QPushButton, 'btnBg').clicked.connect(
            self.btnBgClicked)
        # self.findChild(QtWidgets.QPushButton, 'btnBg').clicked.connect(
        #     self.btnCopyClicked)
        # self.findChild(QtWidgets.QPushButton, 'btnBiner').clicked.connect(
        #     self.btnCopyClicked)

        self.imgGs = self.findChild(QtWidgets.QLabel, 'imgGs')
        self.imgBiner = self.findChild(QtWidgets.QLabel, 'imgBiner')
        self.imgSrc = self.findChild(QtWidgets.QLabel, 'imgSrc')

    def btnOpenClicked(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Jpeg (*.jpeg);;BMP (*.bmp)", options=options)
        if not fileName:
            return
        # self.srcQimg = QImage(fileName=fileName, format=QImage.Format_RGB32)
        with open(fileName, 'rb') as f:
            self.srcQimg = QImage.fromData(f.read())
            self.imgSrc.setPixmap(QPixmap.fromImage(
                self.srcQimg).scaledToWidth(self.imgSrc.size().width()))

    def btnExitClicked(self):
        self.close()

    def btnGsClicked(self):
        res = doPxOperation(self.srcQimg, pxCvGray)
        self.gsQimg = res
        if res:
            self.imgGs.setPixmap(QPixmap.fromImage(
                res).scaledToWidth(self.imgGs.size().width()))

    def btnBgClicked(self):
        _c, ok = QInputDialog.getInt(self, 'Offset Brighness',
                                         'Masukkan nilai offset (-255 -> 255)?', min=-255, max=255, step=1)

        if not ok:
            return

        _operation = pxAddBrighness(_c)

        res = doPxOperation(self.gsQimg, _operation)
        if res:
            self.imgBiner.setPixmap(QPixmap.fromImage(
                res).scaledToWidth(self.imgBiner.size().width()))

    def btnBinerClicked(self):
        _thres, ok = QInputDialog.getInt(self, 'Threshold Biner',
                                         'Masukkan nilai ambang (0-255)?', min=0, max=255, step=1)

        if not ok:
            return

        _operation = pxToBinerHOF(_thres)

        res = doPxOperation(self.gsQimg, _operation)
        if res:
            self.imgBiner.setPixmap(QPixmap.fromImage(
                res).scaledToWidth(self.imgBiner.size().width()))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
