from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QFileDialog
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


def rgb2K(r, g, b):
    rMap = remap(r, 0, 255, 0, 1)
    gMap = remap(g, 0, 255, 0, 1)
    bMap = remap(b, 0, 255, 0, 1)
    return (1 - max(rMap, gMap, bMap))


def rgb2CMY(r, g, b):
    # px = (1-0.686275-0.098039)/(1-0.098039) = 0.23913
    K = rgb2K(r, g, b)
    # print(K)
    rMap = remap(r, 0, 255, 0.0, 1)
    gMap = remap(g, 0, 255, 0.0, 1)
    bMap = remap(b, 0, 255, 0.0, 1)
    if K == 1:
        cMap = 0
        mMap = 0
        yMap = 0
    else:
        cMap = (1 - rMap - K)/(1 - K)
        mMap = (1 - gMap - K)/(1 - K)
        yMap = (1 - bMap - K)/(1 - K)

    c = remap(cMap, 0, 1, 0, 255)
    m = remap(mMap, 0, 1, 0, 255)
    y = remap(yMap, 0, 1, 0, 255)
    return c, m, y


def cmy2RGB(c, m, y, k):
    # R = 255 × (1-C) × (1-K)
    # G = 255 × (1-M) × (1-K)
    # B = 255 × (1-Y) × (1-K)
    # px = (1-0.686275-0.098039)/(1-0.098039) = 0.23913
    cMap = remap(c, 0, 255, 0.0, 1)
    mMap = remap(m, 0, 255, 0.0, 1)
    yMap = remap(y, 0, 255, 0.0, 1)
    kMap = remap(k, 0, 255, 0.0, 1)
    if k == 1:
        rMap = 0
        gMap = 0
        bMap = 0
    else:
        rMap = (1 - cMap)/(1 - kMap)
        gMap = (1 - mMap)/(1 - kMap)
        bMap = (1 - yMap)/(1 - kMap)

    r = remap(rMap, 0, 1, 0, 255)
    g = remap(gMap, 0, 1, 0, 255)
    b = remap(bMap, 0, 1, 0, 255)
    return r, g, b


def pxOnlyRed(src):
    px = src.red()
    return QColor(px, 0, 0)


def pxOnlyGreen(src):
    px = src.green()
    return QColor(0, px, 0)


def pxOnlyBlue(src):
    px = src.blue()
    return QColor(0, 0, px)


def pxOnlyCyan(src):
    K = rgb2K(src.red(), src.green(), src.blue())
    c, m, y = rgb2CMY(src.red(), src.green(), src.blue())
    # print(c)
    # Representasikan channel c nya saja
    r, g, b = cmy2RGB(c, 0, 0, K)
    # print((r, g, b))
    return QColor(r, g, b)


def pxOnlyMagenta(src):
    K = rgb2K(src.red(), src.green(), src.blue())
    c, m, y = rgb2CMY(src.red(), src.green(), src.blue())
    # Representasikan channel c nya saja
    r, g, b = cmy2RGB(0, m, 0, K)
    return QColor(r, g, b)


def pxOnlyYellow(src):
    K = rgb2K(src.red(), src.green(), src.blue())
    c, m, y = rgb2CMY(src.red(), src.green(), src.blue())
    # Representasikan channel c nya saja
    r, g, b = cmy2RGB(0, 0, y, K)
    return QColor(r, g, b)


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
        res = doPxOperation(self.copiedQimg, pxOnlyRed)
        if res:
            self.imgProcessed.setPixmap(QPixmap.fromImage(res))

    def radioGClicked(self):
        res = doPxOperation(self.copiedQimg, pxOnlyGreen)
        if res:
            self.imgProcessed.setPixmap(QPixmap.fromImage(res))

    def radioBClicked(self):
        res = doPxOperation(self.copiedQimg, pxOnlyBlue)
        res.pixelColor(3, 3).cyan()
        if res:
            self.imgProcessed.setPixmap(QPixmap.fromImage(res))

    def radioCClicked(self):
        res = doPxOperation(self.copiedQimg, pxOnlyCyan)
        if res:
            self.imgProcessed.setPixmap(QPixmap.fromImage(res))

    def radioMClicked(self):
        res = doPxOperation(self.copiedQimg, pxOnlyMagenta)
        if res:
            self.imgProcessed.setPixmap(QPixmap.fromImage(res))

    def radioYClicked(self):
        res = doPxOperation(self.copiedQimg, pxOnlyYellow)
        if res:
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
