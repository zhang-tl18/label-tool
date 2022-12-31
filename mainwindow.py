import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene
from PyQt5.QtGui import QImage, QPixmap
from skimage import io
import numpy as np

import Ui_mainwindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 信号与槽绑定
        self.ui.actionOpen.triggered.connect(self.open_file)
    
    # 槽函数
    def open_file(self):
        if(not hasattr(self, 'recent_path')):
            self.recent_path = '.'
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", self.recent_path, "Image files (*.jpg *.gif *.png *.jpeg *.tif)")
        self.recent_path, _ = os.path.split(file_name)
        print(file_name)
        self.show_img(file_name)

    def refresh_img(self, value):
        self.ui.horizontalSlider.setValue(value)
        self.ui.spinBox.setValue(value)
        img = np.array(self.img[value])
        img = np.uint8(255 * (img - self.img_min) / (self.img_max - self.img_min))
        h = img.shape[0]
        w = img.shape[1]
        frame = QImage(img, w, h, w, QImage.Format_Grayscale8)
        pix = QPixmap.fromImage(frame).scaled(w/2, h/2)
        scene = QGraphicsScene()
        scene.addPixmap(pix)
        self.ui.graphicsView.setScene(scene)

    # 成员函数
    def show_img(self, file_name):
        # 读入图片
        self.img = io.imread(file_name)  # img = img_as_ubyte(io.imread(file_name))
        self.img_min = np.min(self.img)
        self.img_max = np.max(self.img)
        band = self.img.shape[0]
        img = np.array(self.img[0])
        img = np.uint8(255 * (img - self.img_min) / (self.img_max - self.img_min))
        print(img.shape, img.dtype)
        h = img.shape[0]
        w = img.shape[1]
        frame = QImage(img, w, h, w, QImage.Format_Grayscale8)
        pix = QPixmap.fromImage(frame).scaled(w/2, h/2)
        scene = QGraphicsScene()
        scene.addPixmap(pix)
        # 构建部件
        if(not hasattr(self.ui, 'graphicsView')):
            self.ui.graphicsView = QtWidgets.QGraphicsView(self.ui.centralwidget)
            self.ui.graphicsView.setObjectName("graphicsView")
        self.ui.graphicsView.setScene(scene)
        self.ui.graphicsView.show()
        if(not hasattr(self.ui, 'horizontalSlider')):
            self.ui.horizontalSlider = QtWidgets.QSlider(self.ui.centralwidget)
            self.ui.horizontalSlider.setObjectName("horizontalSlider")
            self.ui.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.ui.horizontalSlider.setGeometry(QtCore.QRect(10, h/2 + 10, w/2 - 70, 16))
        self.ui.horizontalSlider.setMaximum(band - 1)
        self.ui.horizontalSlider.setValue(0)
        self.ui.horizontalSlider.valueChanged.connect(self.refresh_img)
        self.ui.horizontalSlider.show()
        if(not hasattr(self.ui, 'spinBox')):
            self.ui.spinBox = QtWidgets.QSpinBox(self.ui.centralwidget)
            self.ui.spinBox.setObjectName("spinBox")
        self.ui.spinBox.setGeometry(QtCore.QRect(w/2 - 50, h/2 + 10, 40, 16))
        self.ui.spinBox.setMaximum(band - 1)
        self.ui.spinBox.setValue(0)
        self.ui.spinBox.valueChanged.connect(self.refresh_img)
        self.ui.spinBox.show()
    

if __name__ =="__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
