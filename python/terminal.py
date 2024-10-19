import serial
import serial.tools.list_ports
import json
import time  # Import time module

# 列出所有可用的串口
ports = list(serial.tools.list_ports.comports())
for port in ports:
    print(port)

def read_from_serial(port='COM3', baudrate=115200, lines_to_read=10):
    ser = None  # 确保 ser 初始为 None
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        if ser.is_open:
            print(f"Connected to {port} at {baudrate} baudrate")

            while True:
                buffer = []  # 用于存储多行数据
                for _ in range(lines_to_read):  # 读取指定行数
                    data = ser.readline().decode('utf-8', errors='ignore').strip()
                    if data:
                        buffer.append(data)  # 将数据添加到缓冲区
                        print(buffer)

                # 在这里可以处理整个缓冲区的数据
                # 例如将数据转为 JSON 格式
                json_data = json.loads("[" + ",".join(buffer) + "]")  # 假设数据是有效的 JSON 字符串
                return json_data

                # 每 10 秒读取一次
                # time.sleep(10)
    except serial.SerialException as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {json_data}")
    finally:
        if ser and ser.is_open:
            ser.close()  # 只有当 ser 已被初始化并且已经开启时，才进行关闭操作

if __name__ == '__main__':
    data = read_from_serial(port='COM3', lines_to_read=10)  # 每次抓取 10 行
    # print(data)
