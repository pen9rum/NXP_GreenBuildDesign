import serial
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for port in ports:
    print(port)

def read_from_serial(port='COM3', baudrate=12500):
    ser = None  # 確保 ser 初始為 None
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        if ser.is_open:
            print(f"Connected to {port} at {baudrate} baudrate")

            while True:
                data = ser.readline().decode('utf-8').strip()
                if data:
                    print(f"Received data: {data}")
                    # 將資料轉換為 JSON 格式
                    json_data = json.loads(data)  # 假設 data 是有效的 JSON 字串
                    return json_data  # 返回 JSON 格式的數據
    except serial.SerialException as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()  # 只有當 ser 已被初始化並且已經開啟時，才進行關閉操作

if __name__ == '__main__':
    read_from_serial(port='COM3', lines_to_read=1)  # 每次抓取 5 行