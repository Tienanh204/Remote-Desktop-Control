
"""
    <--------REMOTE DESKTOP-------->
         Created: Truong Tien Anh
         Coded: Truong Tien Anh
         Language: Python
    <------------------------------>
"""

import os
import sys #Truy cập các tham số dòng lệnh và thoát ứng dụng
import cv2
import socket#Tao và quản lý kết nối socket
import json
import struct
import numpy as np
from random import randint
from PIL import Image
import pyautogui
import threading
from PyQt6.QtCore import Qt,QCoreApplication,QByteArray,QRect,QThread
from PyQt6.uic import load_ui#Tải các tệp UI từ PyQt Designer
from PyQt6.QtGui import QPixmap, QImage
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication,QLabel,QGraphicsScene, QGraphicsPixmapItem, QDialog, QMessageBox, QFileDialog,QMainWindow#Xây dựng gaio diện người dùng và hiển thị các cửa sổ thông báo

# Import các UI files
from app_ui import Ui_Dialog_app
from kill_ui import Ui_Dialog_Kill
from start_ui import Ui_Dialog_start
from client_ui import Ui_Dialog_client
from keystroke_ui import Ui_Dialog_keystroke
from screenshot_ui import Ui_Dialog_screenshot
from display_ui import Ui_Dialog_thread

class Window(QDialog, Ui_Dialog_client):
    def __init__(self, parent=None):#Thiết lập giao diện và kết nối tới các tín hiệu của các nút.
        super().__init__(parent)
        self.setupUi(self)
        self.lineEdit.setText('192.168.112.129:8080')
        self.disable_buttons()
        self.connect_signals()

    def connect_signals(self):#Kết nối các nút tới các hàm xử lý tương ứng.
        self.btn_cap.clicked.connect(self.capture)
        self.btn_app.clicked.connect(self.app)
        self.btn_key.clicked.connect(self.keystroke)
        self.btn_display.clicked.connect(self.display)
        self.btn_connect.clicked.connect(self.connect_to_server)
        self.btn_shutdown.clicked.connect(self.shutdown)
        self.btn_exit.clicked.connect(self.exit)

    def connect_to_server(self):#Kết nối tới server thông qua socket.
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tmp = self.lineEdit.text().split(':')
        HOST = tmp[0]
        PORT = int(tmp[1])
        server_address = (HOST, PORT)
        try:
            s.connect(server_address)
            self.label.setText('Connect: ' + self.lineEdit.text())
            QMessageBox.about(self, "Thông báo", "Connect thành công")
            self.enable_buttons()
        except Exception as e:
            print(e)
            self.label.setText('No connection')
            QMessageBox.about(self, "Thông báo", "Connect không thành công")

    #Các hàm capture, app, keystroke: Mở các cửa sổ giao diện để chụp màn hình, điều khiển ứng dụng, và nhập phím từ xa.
    def app(self):
        if not self._ping():
            QMessageBox.about(self, "Thông báo", "Connect không thành công")
            return
        dialog = Dialog_app(self)
        dialog.exec()

    def keystroke(self):
        if not self._ping():
            QMessageBox.about(self, "Thông báo", "Connect không thành công")
            return
        dialog = Dialog_keystroke(self)#Hiển thị giao diện người dùng
        dialog.exec()#Chờ đợi người dùng thao tác với cửa sổ dao diện và két thúc khi của sổ đóng lại

    def capture(self):
        if not self._ping():
            QMessageBox.about(self, "Thông báo", "Connect không thành công")
            return
        dialog = Dialog_capture(self)
        dialog.exec()
    def display(self):
        if not self._ping():
             QMessageBox.about(self, "Thông báo", "Connect không thành công")
             return
        dialog = Dialog_thread(self)
        dialog.exec()

    def shutdown(self):#Gửi tin nhắn 'shutdown' tới server để tắt máy.
        if not self._ping():
            QMessageBox.about(self, "Thông báo", "Connect không thành công")
            return
        send_msg('shutdown')

    def exit(self):# Gửi tin nhắn 'quit' tới server và đóng kết nối trước khi thoát chương trình.
        try:
            s.sendall(bytes('quit', "utf8"))
            s.close()
        except:
            s.close()
        sys.exit()

    def _ping(self):# Gửi tin nhắn 'ping' tới server để kiểm tra kết nối.
        try:
            s.sendall(b'ping')
            return True
        except:
            self.label.setText("No Connection")
            self.disable_buttons()
        return False
    #Bật/tắt các nút trên giao diện tùy theo tình trạng kết nối.
    def enable_buttons(self):
        self.btn_cap.setEnabled(True)
        self.btn_app.setEnabled(True)
        self.btn_key.setEnabled(True)
        self.btn_shutdown.setEnabled(True)
        self.btn_display.setEnabled(True)

    def disable_buttons(self):
        self.btn_cap.setEnabled(False)
        self.btn_app.setEnabled(False)
        self.btn_key.setEnabled(False)
        self.btn_shutdown.setEnabled(False)
        self.btn_display.setEnabled(False)

#Các hàm chức năng
# Class Dialog_app kế thừa từ lớp QDialog và sử dụng UI từ Ui_Dialog_app
class Dialog_app(QDialog, Ui_Dialog_app):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect()  # Kết nối các sự kiện

    # Kết nối các sự kiện của các nút
    def connect(self):
        self.btn_kill.clicked.connect(self.kill)
        self.btn_start.clicked.connect(self.start)
        self.btn_xem.clicked.connect(self.xem)
        self.btn_xoa.clicked.connect(self.xoa)

    # Hàm xem: Lấy danh sách ứng dụng và hiển thị trong bảng
    def xem(self):
        # Gửi thông điệp 'app//list' và chuyển đổi dữ liệu từ JSON sang danh sách
        data = json.loads(send_msg('app//list'))
        if isinstance(data, str):
              data = json.loads(data)  # Chuyển đổi chuỗi JSON thành đối tượng Python
        data = data['app']
        rows = len(data)
        cols = len(data[0])
        keys = ['name', 'ID', 'TC']  # Khóa cần hiển thị trong bảng

        # Thiết lập số hàng và số cột cho bảng
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)

        # Đưa dữ liệu vào bảng
        for row in range(rows):
            for col in range(cols):
                item = QtWidgets.QTableWidgetItem()  # Tạo một ô mới
                # Thiết lập dữ liệu cho từng ô trong bảng
                item.setText(data[row][keys[col]] or '')  # Đặt giá trị hoặc '' nếu giá trị là None
                self.tableWidget.setItem(row, col, item)  # Đặt ô vào bảng

        keys = [item.title() for item in keys]  # Chữ hoa chữ cái đầu của các khóa
        self.tableWidget.setHorizontalHeaderLabels(keys)  # Đặt tên cột
        self.tableWidget.resizeColumnsToContents()  # Điều chỉnh kích thước cột

    # Hàm xóa: Xóa tất cả các hàng trong bảng
    def xoa(self):
        self.tableWidget.setRowCount(0)

    # Hàm kill: Hiển thị Dialog_Kill khi nút "Kill" được nhấn
    def kill(self):
        dialog = Dialog_kill('app', self)
        dialog.exec()

    # Hàm start: Hiển thị Dialog_start khi nút "Start" được nhấn
    def start(self):
        # 'calc.exe', 'mspaint.exe', 'notepad.exe'..vv 
        dialog = Dialog_start('app', self)
        dialog.exec()

#-> Dang toi day noi chung roi lam vie truyen du lieu chua duoc
class Dialog_keystroke(QDialog, Ui_Dialog_keystroke):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Thiết lập giao diện từ file UI
        # Kết nối các nút với các phương thức tương ứng
        self.btn_hook.clicked.connect(self.hook)
        self.btn_unhook.clicked.connect(self.unhook)
        self.btn_key.clicked.connect(self.getkey)
        self.btn_delete.clicked.connect(self.delete)

    def hook(self):
        send_msg('key//hook')  # Gửi tin nhắn 'key//hook'

    def unhook(self):
        send_msg('key//unhook')  # Gửi tin nhắn 'key//unhook'

    def getkey(self):
        # Hiển thị kết quả từ hàm send_msg('key//getkey') trong textBrowser_2
        self.textBrowser_2.setText(send_msg('key//getkey'))

    def delete(self):
        self.textBrowser_2.setText("")  # Xóa nội dung trong textBrowser_2


class Dialog_capture(QDialog, Ui_Dialog_screenshot):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.capture)
        self.pushButton_3.clicked.connect(self.save)

    def capture(self):
        try:
            s.sendall(bytes('capture', "utf8"))
            f = open('tmp_capture.jpg', 'wb')
            print("Receiving data...")

            total_received = 0
            while (True):
                l = s.recv(4096)
                if not l:
                    break
                if (l == b'ok'):
                    break
                f.write(l)
                total_received += len(l)
                print("Received", len(l), "bytes, Total received:", total_received)
            print("Data received successfully.")
            f.close()

            pix = QPixmap('tmp_capture.jpg')
            item = QtWidgets.QGraphicsPixmapItem(pix)
            scene = QtWidgets.QGraphicsScene(self)
            scene.addItem(item)
            self.graphicsView.setScene(scene)
            self.graphicsView.fitInView(scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

        except ConnectionAbortedError as e:
            print(f"ConnectionAbortedError: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def save(self):
        # Now proceed with saving
        path = QFileDialog.getSaveFileName(self, 'Save File', 'tmp_capture.jpg')
        print("Saving to:", path[0])
        file1 = open("tmp_capture.jpg", "rb")
        file2 = open(str(path[0]), "wb")
        l = file1.readline()
        while l:
            file2.write(l)
            l = file1.read()
        file1.close()
        file2.close()

class Dialog_thread(QDialog,Ui_Dialog_thread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.start_capture_thread)
        self.pushButton_3.clicked.connect(self.ok)
        self.label = QLabel(self.graphicsView)
        self.label_width = 500  # Thêm khai báo cho label_width
        self.label_height = 450
        self.capture_requested = False

    def start_capture_thread(self):
        # Tạo một luồng mới cho startcapture
        capture_thread = threading.Thread(target=self.startcapture)
        capture_thread.start()
    def startcapture (self):
        try:
            s.sendall(bytes('startcapture', "utf8"))
            while True:
                size_bytes = s.recv(4)
                size = int.from_bytes(size_bytes, byteorder='big')
                img_data = s.recv(size)
                print("Received data size:", size)

                # Sử dụng QByteArray để lưu trữ dữ liệu ảnh
                qbyte_array = QByteArray(img_data)

                # Chuyển đổi dữ liệu ảnh từ QByteArray sang QImage
                image = QImage.fromData(qbyte_array)

                # Kiểm tra nếu ảnh hợp lệ trước khi tiếp tục
                if image.isNull():
                    print("Invalid image data")
                    continue

                width_ratio = image.width() / self.label_width
                height_ratio = image.height() / self.label_height

                # Chỉnh sửa kích thước ảnh để vừa với khung giao diện
                if width_ratio > height_ratio:
                    image = image.scaledToWidth(self.label_width)
                else:
                    image = image.scaledToHeight(self.label_height)

                self.label.setFixedSize(image.width(), image.height())

                pixmap = QPixmap.fromImage(image)
                # Cập nhật QLabel trong luồng GUI chính
                self.label.setPixmap(pixmap)
                QCoreApplication.processEvents()

                 # Kiểm tra nếu có yêu cầu chụp màn hình
                if self.capture_requested:
                    break

        except ConnectionResetError as e:
            print("[CLIENT]: ConnectionResetError -", e)
            print("[CLIENT]: DISCONNECTED")
        except Exception as e:
            print("[CLIENT]: Exception -", e)
            print("[CLIENT]: DISCONNECTED")
            
    def initUI(self):
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.label.resize(self.width(), self.height())
        self.setGeometry(QRect(pyautogui.size()[0] // 4, pyautogui.size()[1] // 4, 500, 450))
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("[SERVER] Remote Desktop: " + str(randint(99999, 999999)))
    def ok(self):
        # Đặt cờ để thông báo rằng có yêu cầu chụp màn hình
        self.capture_requested = True
    
class Dialog_kill(QDialog, Ui_Dialog_Kill):
    def __init__(self, status, parent=None):
        super().__init__(parent)
        self.status = status  # Lưu trạng thái
        self.setupUi(self)  # Thiết lập giao diện từ file UI
        self.btn_kill.clicked.connect(self.kill)  # Kết nối nút kill với phương thức kill

    def kill(self):
        # Gửi tin nhắn gồm trạng thái, 'kill', và nội dung từ lineEdit qua send_msg()
        send_msg(self.status + '//' + 'kill' + '//' + self.lineEdit.text())

class Dialog_start(QDialog, Ui_Dialog_start):
    def __init__(self, status, parent=None):
        super().__init__(parent)
        self.status = status  # Lưu trạng thái
        self.setupUi(self)  # Thiết lập giao diện từ file UI
        self.btn_start.clicked.connect(self.start)  # Kết nối nút start với phương thức start

    def start(self):
        # Gửi tin nhắn gồm trạng thái, 'start', và nội dung từ lineEdit qua send_msg()
        send_msg(self.status + '//' + 'start' + '//' + self.lineEdit.text())

def send_msg(msg):
    # Gửi dữ liệu đến đích
    s.sendall(bytes(msg, "utf8"))  # Chuyển đổi chuỗi văn bản thành dạng byte và gửi đi

    received_data = ""  # Khởi tạo biến để lưu dữ liệu nhận được từ đích

    # Bắt đầu nhận phản hồi từ đích
    while True:
        part = s.recv(1024)  # Nhận dữ liệu từ đích, tối đa 1024 bytes mỗi lần nhận
        print(len(part))  # In ra kích thước của phần dữ liệu nhận được
        received_data += part.decode("utf8")  # Gắn dữ liệu nhận được vào biến received_data sau khi chuyển từ byte sang chuỗi

        # Kiểm tra xem dữ liệu còn tiếp theo không
        if len(part) < 1024:
            break  # Nếu không còn dữ liệu nữa, thoát khỏi vòng lặp

    print(received_data)  # In ra dữ liệu nhận được từ đích
    return received_data  # Trả về dữ liệu nhận được cho phần gọi hàm

if __name__ == "__main__":
    #Tạo một đối tượng Window, hiển thị giao diện và bắt đầu vòng lặp của ứng dụng PyQt6.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())

