import re
import json
from typing import Dict, List, Any
from datetime import datetime

def extract_room_locations(description: str) -> dict[str, List[str]]:
    room_locations = {}
    locations = ['位置A', '位置B', '位置C', '位置D']
    room_types = {
        'livingRoom': ['客廳', '起居室'],
        'bedroom': ['臥室', '房間'],
        'kitchen': ['廚房'],
        'bathroom': ['浴室', '衛生間', '廁所']
    }
    
    for room_type, room_names in room_types.items():
        matches = []
        for name in room_names:
            for location in locations:
                if f"{name}位於{location}" in description or f"{name}在{location}" in description:
                    matches.append(location)
        
        if matches:
            room_locations[room_type] = matches
        else:
            print(f"警告: 無法在描述中找到 {room_type} 的位置")
            room_locations[room_type] = []

    # 特殊處理臥室，因為它可能有多個
    bedroom_count = description.count("臥室")
    if bedroom_count > 1:
        bedroom_locations = []
        for location in locations:
            if f"臥室分別位於" in description and location in description.split("臥室分別位於")[1]:
                bedroom_locations.append(location)
        if bedroom_locations:
            room_locations['bedroom'] = bedroom_locations

    return room_locations

def repair_json(json_string: str) -> dict[str, Any]:
    """
    嘗試修復無效的 JSON 字符串。

    :param json_string: 可能無效的 JSON 字符串
    :return: 修復後的 JSON 對象，如果無法修復則返回 None
    """
    # 移除可能導致問題的尾隨逗號
    json_string = re.sub(r',\s*}', '}', json_string)
    json_string = re.sub(r',\s*]', ']', json_string)
    
    # 嘗試找到並提取 JSON 對象
    match = re.search(r'\{.*\}', json_string, re.DOTALL)
    if match:
        json_string = match.group()

    try:
        # 嘗試解析修復後的 JSON
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"無法修復 JSON: {str(e)}")
        return None

def validate_design_data(design_data: dict[str, Any]) -> bool:
    """
    驗證設計數據的有效性。

    :param design_data: 設計數據字典
    :return: 是否有效
    """
    required_fields = ['designName', 'length', 'width', 'rooms', 'windows']
    for field in required_fields:
        if field not in design_data:
            print(f"錯誤: 缺少必要的字段 '{field}'")
            return False
    
    if not isinstance(design_data['rooms'], dict) or not design_data['rooms']:
        print("錯誤: 'rooms' 必須是非空字典")
        return False
    
    if not isinstance(design_data['windows'], dict) or not design_data['windows']:
        print("錯誤: 'windows' 必須是非空字典")
        return False
    
    return True

def calculate_room_area_percentage(room_areas: dict[str, float], total_area: float) -> dict[str, float]:
    """
    計算每個房間的面積佔總面積的百分比。

    :param room_areas: 房間面積字典
    :param total_area: 總面積
    :return: 房間面積百分比字典
    """
    return {room: (area / total_area) * 100 for room, area in room_areas.items()}

def format_timestamp(timestamp: float) -> str:
    """
    格式化時間戳為可讀字符串。

    :param timestamp: 時間戳
    :return: 格式化的時間字符串
    """
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def calculate_aspect_ratio(length: float, width: float) -> float:
    """
    計算長寬比。

    :param length: 長度
    :param width: 寬度
    :return: 長寬比
    """
    return max(length, width) / min(length, width)

def is_valid_aspect_ratio(aspect_ratio: float, min_ratio: float = 1.0, max_ratio: float = 2.0) -> bool:
    """
    檢查長寬比是否在有效範圍內。

    :param aspect_ratio: 長寬比
    :param min_ratio: 最小允許比例
    :param max_ratio: 最大允許比例
    :return: 是否有效
    """
    return min_ratio <= aspect_ratio <= max_ratio

def calculate_window_area(room_area: float, window_percentage: float) -> float:
    """
    計算窗戶面積。

    :param room_area: 房間面積
    :param window_percentage: 窗戶佔牆面積的百分比
    :return: 窗戶面積
    """
    return room_area * (window_percentage / 100)

def estimate_natural_light(window_area: float, room_area: float) -> str:
    """
    估算自然光照程度。

    :param window_area: 窗戶面積
    :param room_area: 房間面積
    :return: 自然光照程度描述
    """
    ratio = window_area / room_area
    if ratio > 0.25:
        return "充足"
    elif ratio > 0.15:
        return "良好"
    elif ratio > 0.1:
        return "一般"
    else:
        return "不足"

def calculate_wall_area(length: float, width: float, height: float = 2.4) -> float:
    """
    計算牆壁面積。

    :param length: 房間長度
    :param width: 房間寬度
    :param height: 房間高度（默認2.4米）
    :return: 牆壁總面積
    """
    return 2 * (length + width) * height

def format_area(area: float) -> str:
    """
    格式化面積為易讀的字符串。

    :param area: 面積
    :return: 格式化的面積字符串
    """
    return f"{area:.2f} 平方米"

def generate_room_code(room_type: str, index: int) -> str:
    """
    生成房間代碼。

    :param room_type: 房間類型
    :param index: 房間索引
    :return: 房間代碼
    """
    type_codes = {
        "livingRoom": "LR",
        "bedroom": "BR",
        "kitchen": "KT",
        "bathroom": "BT"
    }
    return f"{type_codes.get(room_type, 'RM')}{index:02d}"

def parse_room_code(room_code: str) -> dict[str, Any]:
    """
    解析房間代碼。

    :param room_code: 房間代碼
    :return: 包含房間類型和索引的字典
    """
    type_codes = {
        "LR": "livingRoom",
        "BR": "bedroom",
        "KT": "kitchen",
        "BT": "bathroom"
    }
    room_type = type_codes.get(room_code[:2], "unknown")
    index = int(room_code[2:]) if room_code[2:].isdigit() else 0
    return {"type": room_type, "index": index}