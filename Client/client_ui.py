# Form implementation generated from reading ui file 'client.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_client(object):
    def setupUi(self, Dialog_client):
        Dialog_client.setObjectName("Dialog_client")
        Dialog_client.resize(325, 323)
        Dialog_client.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog_client)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_key = QtWidgets.QPushButton(parent=Dialog_client)
        self.btn_key.setObjectName("btn_key")
        self.gridLayout.addWidget(self.btn_key, 9, 0, 1, 1)
        self.btn_shutdown = QtWidgets.QPushButton(parent=Dialog_client)
        self.btn_shutdown.setObjectName("btn_shutdown")
        self.gridLayout.addWidget(self.btn_shutdown, 10, 0, 1, 1)
        self.btn_file = QtWidgets.QPushButton(parent=Dialog_client)
        self.btn_file.setObjectName("btn_file")
        self.gridLayout.addWidget(self.btn_file, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(parent=Dialog_client)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btn_connect = QtWidgets.QPushButton(parent=Dialog_client)
        self.btn_connect.setObjectName("btn_connect")
        self.horizontalLayout.addWidget(self.btn_connect)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(parent=Dialog_client)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.btn_cap = QtWidgets.QPushButton(parent=Dialog_client)
        self.btn_cap.setObjectName("btn_cap")
        self.verticalLayout.addWidget(self.btn_cap)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.btn_display = QtWidgets.QPushButton(parent=Dialog_client)
        self.btn_display.setObjectName("btn_display")
        self.gridLayout.addWidget(self.btn_display, 2, 0, 1, 1)

        self.retranslateUi(Dialog_client)
        QtCore.QMetaObject.connectSlotsByName(Dialog_client)

    def retranslateUi(self, Dialog_client):
        _translate = QtCore.QCoreApplication.translate
        Dialog_client.setWindowTitle(_translate("Dialog_client", "Dialog"))
        self.btn_key.setText(_translate("Dialog_client", "Keystroke"))
        self.btn_shutdown.setText(_translate("Dialog_client", "Shutdow"))
        self.btn_file.setText(_translate("Dialog_client", "File Transfer"))
        self.btn_connect.setText(_translate("Dialog_client", "Connect"))
        self.label.setText(_translate("Dialog_client", "No Connection"))
        self.btn_cap.setText(_translate("Dialog_client", "Screenshot"))
        self.btn_display.setText(_translate("Dialog_client", "Display"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_client = QtWidgets.QDialog()
    ui = Ui_Dialog_client()
    ui.setupUi(Dialog_client)
    Dialog_client.show()
    sys.exit(app.exec())
