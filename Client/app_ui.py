# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_app(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setGeometry(QtCore.QRect(0, 0, 499, 464))
        self.layoutWidget_2 = QtWidgets.QWidget(parent=Dialog)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 10, 481, 441))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_kill = QtWidgets.QPushButton(parent=self.layoutWidget_2)
        self.btn_kill.setObjectName("btn_kill")
        self.horizontalLayout_2.addWidget(self.btn_kill)
        self.btn_xem = QtWidgets.QPushButton(parent=self.layoutWidget_2)
        self.btn_xem.setObjectName("btn_xem")
        self.horizontalLayout_2.addWidget(self.btn_xem)
        self.btn_xoa = QtWidgets.QPushButton(parent=self.layoutWidget_2)
        self.btn_xoa.setObjectName("btn_xoa")
        self.horizontalLayout_2.addWidget(self.btn_xoa)
        self.btn_start = QtWidgets.QPushButton(parent=self.layoutWidget_2)
        self.btn_start.setObjectName("btn_start")
        self.horizontalLayout_2.addWidget(self.btn_start)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(parent=self.layoutWidget_2)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog_app", "Dialog"))
        self.btn_kill.setText(_translate("Dialog_app", "Kill"))
        self.btn_xem.setText(_translate("Dialog_app", "Xem"))
        self.btn_xoa.setText(_translate("Dialog_app", "Xóa"))
        self.btn_start.setText(_translate("Dialog_app", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_app()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
