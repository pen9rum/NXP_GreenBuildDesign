import serial
import serial.tools.list_ports
import json
import time
import random

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 初始化 Firebase Firestore
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# 列出所有可用的串口
ports = list(serial.tools.list_ports.comports())
for port in ports:
    print(port)

# 模擬四宮格光照度分佈，光照度在 200-400 Lux 之間，正中午日照情況
def simulateLight(windows):
    # 隨機生成基礎的勒克斯光照度值，範圍設置在 150 到 300 之間
    sunlight = {
        '位置 A': random.randint(150, 300),
        '位置 B': random.randint(150, 300),
        '位置 C': random.randint(150, 300),
        '位置 D': random.randint(150, 300)
    }

    # 正中午日照較強，因此會對應區域進行額外調整
    if windows.get('top', False):
        sunlight['位置 A'] += random.randint(50, 100)  # 增加 50 到 100 勒克斯
        sunlight['位置 B'] += random.randint(50, 100)

    if windows.get('left', False):
        sunlight['位置 A'] += random.randint(30, 70)  # 增加 30 到 70 勒克斯
        sunlight['位置 C'] += random.randint(30, 70)

    if windows.get('right', False):
        sunlight['位置 B'] += random.randint(30, 70)
        sunlight['位置 D'] += random.randint(30, 70)

    if windows.get('bottom', False):
        sunlight['位置 C'] += random.randint(50, 100)
        sunlight['位置 D'] += random.randint(50, 100)

    # 確保光照度不超過 400 勒克斯
    for key in sunlight:
        sunlight[key] = min(sunlight[key], 400)

    return sunlight

# 從 Firestore 中抓取最新的一筆資料
def getWindowData():
    windows = None
    try:
        # 抓取最後一筆資料，根據 timestamp 欄位進行升序排列並限制為1筆資料
        docs = db.collection('all_designs').order_by('createdAt', direction=firestore.Query.ASCENDING).limit(1).stream()

        # 迭代獲取最後的那筆資料
        last_doc = None
        for doc in docs:
            print(f'Document ID: {doc.id}')
            last_doc = doc.to_dict()
        
        if last_doc:
            return last_doc
        else:
            print("No documents found in the collection.")
            return None
        # for doc in docs:
        #     windows = doc.to_dict().get('windows', {})
        #     print(f"Fetched window data from the last document (ID: {doc.id}):", windows)
        #     break  # 只需要獲取一筆資料

    except Exception as e:
        print(f"Error fetching window data: {e}")
    
    return windows

# 讀取串口資料並模擬光照度
def read_from_serial(port='COM3', baudrate=115200, lines_to_read=10):
    
    ser = None  # 確保 ser 初始為 None
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        if ser.is_open:
            print(f"Connected to {port} at {baudrate} baudrate")
            windows_data = getWindowData()  # 獲取 windows 資訊
            if not windows_data:
                print("No window data found, exiting.")
                return

            json_data = {}  # 初始化為空字典
            positions = ['位置 A', '位置 B', '位置 C', '位置 D']  # 定義位置鍵
            data_count = 0  # 計數已產出的 JSON 資料筆數

            while data_count < 4:  # 設定最多產生四筆資料
                buffer = []  # 用于存储多行数据
                print(f"\nReading data for {positions[data_count]}...")
                for _ in range(lines_to_read):  # 读取指定行数
                    data = ser.readline().decode('utf-8', errors='ignore').strip()
                    if data:
                        buffer.append(data)  # 将数据添加到缓冲区
                        print(f"Received: {data}")

                if not buffer:
                    print("No data received. Retrying...")
                    time.sleep(1)  # 等待一秒後重試
                    continue

                # 模擬房間內四宮格光照度
                sunlight_simulation = simulateLight(windows_data)

                # 將串口讀取的數據轉為 JSON 格式並加入模擬光照度
                try:
                    # 假设每行数据都是有效的 JSON 对象字符串
                    # 例如，每行是 {"sensor1": "value1"} 等
                    data_list = json.loads("[" + ",".join(buffer) + "]")
                    
                    # 將多個傳感器數據合併為一個字典
                    merged_data = {}
                    for item in data_list:
                        if isinstance(item, dict):
                            merged_data.update(item)
                        else:
                            print(f"Unexpected data format: {item}")

                    # 加入模擬光照度數據
                    merged_data["sunlight"] = sunlight_simulation.get(positions[data_count], "N/A")
                    print(f"Generated JSON for {positions[data_count]}:", merged_data)

                    # 將當前資料存入 json_data 字典中，使用相應的位置鍵
                    json_data[positions[data_count]] = merged_data

                    # 產出一筆資料後增加計數
                    data_count += 1

                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print("Skipping this set of data.")
                    continue  # 跳過這次迭代，繼續下一次

            return json_data  # 在生成四筆資料後返回

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()  # 只有当 ser 已被初始化并且已经开启时，才进行关闭操作
            print(f"Closed serial port {port}.")

if __name__ == '__main__':
    data = read_from_serial(port='COM3', lines_to_read=4)  # 每次抓取 4 行
    print('最後',data)