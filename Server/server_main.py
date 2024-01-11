
"""
    <--------REMOTE DESKTOP-------->
         Created: Truong Tien Anh
         Coded: Truong Tien Anh
         Language: Python
    <------------------------------>
"""

import sys
import os
import cv2
import json
import struct
import io
import mss
import numpy as np
import socket
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
                    if not data:
                        break
                    data=data.decode()
                    x=data.split('//')
                    if x[0]=="quit":
                        break
                    if x[0]=="ping":
                        pass
                    if x[0]=="app":
                        if x[1]=="kill":
                            if check_app(x[2]):
                                os.kill(int(x[2]), 9)
                                conn.sendall(b'ok')
                            else:
                                conn.sendall(b'404')
                        if x[1]=="list":
                            app_list = list_apps()
                            json_data = json.dumps(app_list)
                            conn.sendall(json_data.encode())
                        if x[1]=="start":
                            DETACHED_PROCESS = 0x00000008
                            try:
                                results = subprocess.Popen([x[2]],close_fds=True, creationflags=DETACHED_PROCESS)
                                conn.sendall(b'ok')
                            except subprocess.CalledProcessError as e:
                                print(f'Error: {e}')
                                conn.sendall(b'404')
                            except OSError as e:
                                print(f'OSError: {e}')
                                conn.sendall(b'404')
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

                    if x[0] == "startcapture":
                        start_thread = Thread(target=ChangeImage, daemon=True)
                        start_thread.start()
                                
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

# Hàm lấy danh sách các ứng dụng đang chạy
def list_apps():
    jsend={ "app":[]}
    tmp_bfTC=[]
    cmd = 'powershell "Get-Process | where {$_.MainWindowTitle } | select ProcessName,Id"'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if line.rstrip():
            tmp=line.decode().rstrip()
            if tmp.endswith("Id") or tmp.endswith("-"):
                continue
            tmp_name=tmp.partition(" ")[0]
            tmp_ID=tmp.rpartition(" ")[2]
            tmp_app={}
            tmp_app["name"]=tmp_name
            tmp_app["ID"]=tmp_ID
            tmp_bfTC.append(tmp_app)
            #jsend["app"].append(tmp_app)
    for tmp_app in tmp_bfTC:
        cmd = 'powershell "(Get-Process -ID '+tmp_app['ID']+'|  Select-Object -ExpandProperty  Threads | Select-Object ID).Count"'
        #print(cmd)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            tmp_app["TC"]=line.decode().rstrip()
        jsend["app"].append(tmp_app)
    jsended=json.dumps(jsend)
    return jsended
def check_app(a):
    # Sử dụng lệnh PowerShell để lấy danh sách các tiến trình đang chạy với thông tin về tên tiến trình và Process ID (PID)
    cmd = 'powershell "Get-Process | where {$_.MainWindowTitle } | select ProcessName,Id"'
    
    # Chạy lệnh PowerShell và chứa kết quả vào biến proc
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    
    # Duyệt qua từng dòng kết quả trả về từ lệnh PowerShell
    for line in proc.stdout:
        if line.rstrip():
            # Trích xuất Process ID từ dòng kết quả
            tmp_ID = line.decode().rstrip().rpartition(" ")[2]
            
            # So sánh Process ID thu được từ dòng kết quả với 'a' (Process ID đang kiểm tra)
            if str(tmp_ID) == str(a):
                # Nếu tìm thấy Process ID tương ứng, trả về True, cho thấy rằng ứng dụng với Process ID đã cho đang chạy
                return True
    
    # Nếu không tìm thấy Process ID tương ứng với 'a' trong danh sách các tiến trình đang chạy, trả về False
    # Chỉ ra rằng ứng dụng không tồn tại hoặc không đang chạy
    return False
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
