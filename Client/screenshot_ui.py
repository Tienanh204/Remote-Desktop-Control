# Form implementation generated from reading ui file 'screenshotmp.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_screenshot(object):
    def setupUi(self, dialog_capture):
        dialog_capture.setObjectName("dialog_capture")
        dialog_capture.setGeometry(QtCore.QRect(0, 0, 650, 500))
        self.layoutWidget = QtWidgets.QWidget(parent=dialog_capture)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 600, 450))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(parent=self.layoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(dialog_capture)
        QtCore.QMetaObject.connectSlotsByName(dialog_capture)

    def retranslateUi(self, dialog_capture):
        _translate = QtCore.QCoreApplication.translate
        dialog_capture.setWindowTitle(_translate("Dialog_screenshot", "Dialog"))
        self.pushButton_2.setText(_translate("Dialog_screenshot", "Capture"))
        self.pushButton_3.setText(_translate("Dialog_screenshot", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_capture = QtWidgets.QDialog()
    ui = Ui_Dialog_screenshot()
    ui.setupUi(dialog_capture)
    dialog_capture.show()
    sys.exit(app.exec())
