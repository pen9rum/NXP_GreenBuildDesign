import serial
import serial.tools.list_ports

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('serviceAccount.json')

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)

# 初始化firestore
db = firestore.client()

ports = list(serial.tools.list_ports.comports())
for port in ports:
    print(port)

def read_from_serial(port='COM3', baudrate=12500, lines_to_read=5):
    ser = None  # 確保 ser 初始為 None
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        if ser.is_open:
            
            print(f"Connected to {port} at {baudrate} baudrate")
            
            buffer = []  # 用來存儲多行資料

            while True:
                data = ser.readline().decode('utf-8').strip()
                if data:
                    print(f"Received data: {data}")
                    buffer.append(data)  # 將讀取到的資料加入緩衝區
                    designs_ref = db.collection('sensorData').document()
                    designs_ref.set(data)  # 使用 set() 方法添加設計信息

                    # 當緩衝區達到指定行數時，寫入文件並清空緩衝區
                    if len(buffer) >= lines_to_read:
                        with open("sensor_data.txt", "a") as f:
                            f.write("\n".join(buffer) + "\n")
                        buffer.clear()  # 清空緩衝區
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()  # 只有當 ser 已被初始化並且已經開啟時，才進行關閉操作

if __name__ == '__main__':
    read_from_serial(port='COM3', lines_to_read=5)  # 每次抓取 5 行