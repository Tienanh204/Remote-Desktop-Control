# Form implementation generated from reading ui file 'keystroke.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_keystroke(object):
    def setupUi(self, dialog_keystroke):
        dialog_keystroke.setObjectName("dialog_keystroke")
        dialog_keystroke.setGeometry(QtCore.QRect(0, 0, 506, 359))
        self.layoutWidget = QtWidgets.QWidget(parent=dialog_keystroke)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 481, 341))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_hook = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.btn_hook.setObjectName("btn_hook")
        self.horizontalLayout_2.addWidget(self.btn_hook)
        self.btn_unhook = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.btn_unhook.setObjectName("btn_unhook")
        self.horizontalLayout_2.addWidget(self.btn_unhook)
        self.btn_key = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.btn_key.setObjectName("btn_key")
        self.horizontalLayout_2.addWidget(self.btn_key)
        self.btn_delete = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout_2.addWidget(self.btn_delete)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.textBrowser_2 = QtWidgets.QTextBrowser(parent=self.layoutWidget)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.gridLayout.addWidget(self.textBrowser_2, 1, 0, 1, 1)

        self.retranslateUi(dialog_keystroke)
        QtCore.QMetaObject.connectSlotsByName(dialog_keystroke)

    def retranslateUi(self, dialog_keystroke):
        _translate = QtCore.QCoreApplication.translate
        dialog_keystroke.setWindowTitle(_translate("Dialog_keystroke", "Dialog"))
        self.btn_hook.setText(_translate("Dialog_keystroke", "Hook"))
        self.btn_unhook.setText(_translate("Dialog_keystroke", "Unhook"))
        self.btn_key.setText(_translate("Dialog_keystroke", "In phím"))
        self.btn_delete.setText(_translate("Dialog_keystroke", "Xóa"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_keystroke = QtWidgets.QDialog()
    ui = Ui_Dialog_keystroke()
    ui.setupUi(dialog_keystroke)
    dialog_keystroke.show()
    sys.exit(app.exec())
