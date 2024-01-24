
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
import pickle
import pyautogui
import threading
from PyQt6.QtCore import Qt,QCoreApplication,QByteArray,QRect,QThread
from PyQt6.uic import load_ui#Tải các tệp UI từ PyQt Designer
from PyQt6.QtGui import QPixmap, QImage
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication,QLabel,QGraphicsScene, QGraphicsPixmapItem, QDialog, QMessageBox, QFileDialog,QMainWindow#Xây dựng gaio diện người dùng và hiển thị các cửa sổ thông báo

# Import các UI files
from client_ui import Ui_Dialog_client
from keystroke_ui import Ui_Dialog_keystroke
from screenshot_ui import Ui_Dialog_screenshot
from display_ui import Ui_Dialog_thread
from file_ui import Ui_Dialog_file
from app_ui import Ui_Dialog_app
from kill_ui import Ui_Dialog_Kill
from start_ui import Ui_Dialog_start

class Window(QDialog, Ui_Dialog_client):
    def __init__(self, parent=None):#Thiết lập giao diện và kết nối tới các tín hiệu của các nút.
        super().__init__(parent)
        self.setupUi(self)
        self.lineEdit.text()
        self.disable_buttons()
        self.connect_signals()

    def connect_signals(self):#Kết nối các nút tới các hàm xử lý tương ứng.
        self.btn_cap.clicked.connect(self.capture)
        self.btn_key.clicked.connect(self.keystroke)
        self.btn_display.clicked.connect(self.display)
        self.btn_file.clicked.connect(self.File)
        self.btn_connect.clicked.connect(self.connect_to_server)
        self.btn_shutdown.clicked.connect(self.shutdown)

    def connect_to_server(self):#Kết nối tới server thông qua socket.
        global s
        global HOST
        global PORT
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

    #Các hàm capture, keystroke: Mở các cửa sổ giao diện để chụp màn hình, điều khiển ứng dụng, và nhập phím từ xa.
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
    
    def File(self):
        if not self._ping():
            QMessageBox.about(self, "Thông báo", "Connect không thành công")
            return
        dialog = Dialog_file(self)
        dialog.exec()
    

    def app(self):
        if (self._ping()==False):
            QMessageBox.about(self, "Thông báo", "Connect không thành công")
            return
        dialog = Dialog_app(self)
        dialog.exec()

    def shutdown(self):#Gửi tin nhắn 'shutdown' tới server để tắt máy.
        if not self._ping():
            QMessageBox.about(self, "Thông báo", "Connect không thành công")
            return
        send_msg('shutdown')

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
        self.btn_file.setEnabled(True)
        self.btn_key.setEnabled(True)
        self.btn_shutdown.setEnabled(True)
        self.btn_display.setEnabled(True)

    def disable_buttons(self):
        self.btn_cap.setEnabled(False)
        self.btn_file.setEnabled(False)
        self.btn_key.setEnabled(False)
        self.btn_shutdown.setEnabled(False)
        self.btn_display.setEnabled(False)

#Các hàm chức năng
class Dialog_file(QDialog, Ui_Dialog_file):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.src_path=""
        self.dest_path=""
        self.btn_browser.clicked.connect(self.browser)
        self.btn_send.clicked.connect(self.upload_action)
        self.btn_rev.clicked.connect(self.download_action)
        self.out_stream = s.makefile('wb')
        self.in_stream = s.makefile('rb')
    
    def browser(self):
        # Chọn thư mục
        directory_path = QFileDialog.getExistingDirectory(self, "Chọn thư mục")
        if directory_path:
            # Lưu đường dẫn thư mục vào src_path
            self.src_path = self.src_path = directory_path.replace("\\", "/")
            self.lineEdit.setText(self.src_path)

            # Chọn file bên trong thư mục đã chọn
            file_path, _ = QFileDialog.getOpenFileName(self, "Chọn tệp", "", "All Files (*);;PDF Files (*.pdf);;Word Files (*.docx *.doc)")
            if file_path:
                self.src_path = file_path
                self.lineEdit.setText(self.src_path)    
    
    #Gui file tu Client->Server
    def upload_action(self):
        self.dest_path = self.lineEdit_2.text()
        if os.path.exists(self.src_path):
            try:
                print("Send upload file request")
                s.sendall(bytes('receive', "utf8"))
                self.out_stream.flush()
                print('o day ne 1')
                self.send_file(self.src_path, os.path.join(self.dest_path, os.path.basename(self.src_path)))
                QMessageBox.about(self, "Upload Success", "File uploaded successfully to server.")
            except Exception as e:
                print(f"Error: {e}")
                QMessageBox.about(self, "Upload Error", "Error uploading file to server.")

    def send_file(self, src_path, dest_path):
        try:
            with open(src_path, 'rb') as file_input:
                print("o day ne")
                self.out_stream.write(dest_path.encode('utf-8') + b'\n')
                self.out_stream.flush()
                file_size = os.path.getsize(src_path)
                self.out_stream.write(str(file_size).encode('utf-8') + b'\n')
                self.out_stream.flush()
                print(f"Sending file: {src_path} (Size: {file_size} bytes)")

                buffer_size = 1024
                while True:
                    buffer = file_input.read(buffer_size)
                    if not buffer:
                        break
                    self.out_stream.write(buffer)
                    self.out_stream.flush()

                print("File transfer completed")
        except Exception as e:
            print(f"Error: {e}")
    #Nhan File tu Server
    def download_action(self):
        try:
            self.dest_path = self.lineEdit_2.text()
            print("Send download file request")
            s.sendall(bytes('send', "utf8"))
            self.out_stream.flush()
            self.receive_file(os.path.join(self.src_path, os.path.basename(self.dest_path)), self.dest_path)
            QMessageBox.about(self, "Download Success", "File downloaded successfully from server.")
        except Exception as e:
            print(f"Error: {e}")
            QMessageBox.about(self, "Download Error", "Error downloading file from server.")

    def receive_file(self, src_path, dest_path):
      try:
        # Gửi đường dẫn tệp xuống server
        print(dest_path, src_path, ' o day ne')
        self.out_stream.write(dest_path.encode('utf-8') + b'\n')
        self.out_stream.flush()

        file_path = self.in_stream.readline().strip()
        file_size_str = self.in_stream.readline().strip()

        # Kiểm tra giá trị nhận được
        print(f"Received file path: {file_path}")
        print(f"Received file size: {file_size_str}")

        file_size = int(file_size_str)
        print(f"Received file: {file_path} (Size: {file_size} bytes)")

        # Gửi file_path xuống server
        self.out_stream.write(file_path + b'\n')
        self.out_stream.flush()

        # Tiếp tục với phần nhận dữ liệu tệp
        with open(src_path, 'wb') as file_output:
            buffer_size = 1024
            while file_size > 0:
                buffer = self.in_stream.read(min(file_size, buffer_size))
                if not buffer:
                    break
                file_output.write(buffer)
                file_size -= len(buffer)

        print("File transfer completed")

      except Exception as e:
        print(f"Error: {e}")

    
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
         size_bytes = s.recv(8)
         size = int.from_bytes(size_bytes, 'big')
         received_size=0
         with open('tmp_capture.jpg', 'wb') as f:
           while received_size < size:
              l = s.recv(4096)
              if not l:
                break
              f.write(l)
              received_size += len(l)
         print("Screenshot received successfully.")
       
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
        self.pushButton.clicked.connect(self.ok)
        self.label = QLabel(self.graphicsView)
        self.label_width = 1000 # Thêm khai báo cho label_width
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
        self.setGeometry(QRect(pyautogui.size()[0] // 4, pyautogui.size()[1] // 4, 800, 450))
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("[SERVER] Remote Desktop: " + str(randint(99999, 999999)))
    def ok(self):
        # Đặt cờ để thông báo rằng có yêu cầu chụp màn hình
        self.capture_requested = True

# Class Dialog_app kế thừa từ lớp QDialog và sử dụng UI từ Ui_Dialog_app
class Dialog_app(QDialog, Ui_Dialog_app):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect()

    def connect(self):
        # Kết nối các tín hiệu của nút với các khe cắm tương ứng
        self.btn_kill.clicked.connect(self.kill)
        self.btn_start.clicked.connect(self.start)
        self.btn_xem.clicked.connect(self.xem)
        self.btn_xoa.clicked.connect(self.xoa)

    def xem(self):
        # Lấy dữ liệu bằng cách sử dụng send_msg('app//list') và phân tích nó dưới dạng JSON
        data = json.loads(send_msg('app//list'))

        # Kiểm tra xem dữ liệu có phải là chuỗi không và phân tích nó lại nếu cần
        if isinstance(data, str):
            data = json.loads(data) 

        # Trích xuất dữ liệu 'app' từ kết quả
        data = data['app']

        # Lấy số hàng và số cột từ dữ liệu
        rows = len(data)
        cols = len(data[0])

        # Đặt các khóa cột để truy cập dữ liệu từ điểm dữ liệu
        keys = ['name', 'ID', 'TC']

        # Thiết lập số hàng và số cột cho bảng
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)

        # Đổ dữ liệu vào bảng
        for row in range(rows):
            for col in range(cols):
                item = QtWidgets.QTableWidgetItem()
                # Đặt giá trị cho mỗi ô và sử dụng '' nếu giá trị là None
                item.setText(data[row][keys[col]] or '')
                self.tableWidget.setItem(row, col, item)

        # Đổi tên các cột để in hoa chữ cái đầu
        keys = [item.title() for item in keys]
        self.tableWidget.setHorizontalHeaderLabels(keys)

        # Điều chỉnh kích thước các cột để vừa với nội dung
        self.tableWidget.resizeColumnsToContents()

    def xoa(self):
        # Đặt số hàng của bảng về 0 để xóa dữ liệu
        self.tableWidget.setRowCount(0)

    def kill(self):
        # Mở cửa sổ dialog để xử lý sự kiện 'kill'
        dialog = Dialog_kill('app', self)
        dialog.exec()

    def start(self):
        # Mở cửa sổ dialog để xử lý sự kiện 'start'
        dialog = Dialog_start('app', self)
        dialog.exec()

class Dialog_kill(QDialog, Ui_Dialog_Kill):
    def __init__(self , status, parent=None ):
        super().__init__(parent)
        self.status = status
        self.setupUi(self)       
        self.btn_kill.clicked.connect(self.kill)
    def kill(self):
        send_msg(self.status+'//'+'kill'+'//'+self.lineEdit.text())
class Dialog_start(QDialog, Ui_Dialog_start):
    def __init__(self, status, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.status = status
        self.btn_start.clicked.connect(self.start)
    def start(self):
        send_msg(self.status+'//'+'start'+'//'+self.lineEdit.text())

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

