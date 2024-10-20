import random
from typing import Dict, Tuple

class RoomCalculator:
    def __init__(self):
        self.area_ratio_rules = {
            "livingRoom": {"min": 0.25, "max": 0.40, "ideal": 0.30},
            "bedroom": {"min": 0.20, "max": 0.40, "ideal": 0.35},
            "kitchen": {"min": 0.08, "max": 0.15, "ideal": 0.12},
            "bathroom": {"min": 0.04, "max": 0.08, "ideal": 0.06}
        }
        self.aspect_ratio_rules = {
            "livingRoom": {"min": 1.2, "max": 1.8, "ideal": 1.5},
            "bedroom": {"min": 1.2, "max": 1.6, "ideal": 1.4},
            "kitchen": {"min": 1.0, "max": 1.5, "ideal": 1.3},
            "bathroom": {"min": 1.0, "max": 1.3, "ideal": 1.1}
        }

    def calculate_room_areas(self, rooms: dict[str, int], total_area: float) -> Tuple[dict[str, float], dict[str, float]]:
        """
        計算房間面積和動態比例。

        :param rooms: 房間數量字典
        :param total_area: 總面積
        :return: 房間面積字典和動態比例字典的元組
        """
        total_rooms = sum(rooms.values())
        dynamic_ratios = {}

        for room_type, count in rooms.items():
            min_val = self.area_ratio_rules[room_type]["min"]
            max_val = self.area_ratio_rules[room_type]["max"]
            ideal_val = self.area_ratio_rules[room_type]["ideal"]
            dynamic_ratios[room_type] = self._calculate_dynamic_ratio(min_val, max_val, ideal_val, count, total_rooms)

        total_ratio = sum(dynamic_ratios.values())
        if total_ratio > 0.9:
            scale_factor = 0.9 / total_ratio
            for room_type in dynamic_ratios:
                dynamic_ratios[room_type] *= scale_factor

        room_areas = {}
        for room_type, count in rooms.items():
            total_type_area = dynamic_ratios[room_type] * total_area
            room_areas[room_type] = total_type_area / count

        return room_areas, dynamic_ratios

    def _calculate_dynamic_ratio(self, min_val: float, max_val: float, ideal_val: float, room_count: int, total_rooms: int) -> float:
        """
        計算動態比例。

        :param min_val: 最小比例
        :param max_val: 最大比例
        :param ideal_val: 理想比例
        :param room_count: 房間數量
        :param total_rooms: 總房間數量
        :return: 計算得到的動態比例
        """
        base_ratio = ideal_val * room_count
        variation = (random.random() - 0.5) * (max_val - min_val) * 0.2 * room_count
        ratio = base_ratio + variation
        return max(min_val * room_count, min(max_val * room_count, ratio))

    def calculate_room_dimensions(self, room_area: float, room_type: str) -> Tuple[float, float]:
        """
        計算房間的長度和寬度。

        :param room_area: 房間面積
        :param room_type: 房間類型
        :return: 長度和寬度的元組
        """
        aspect_ratio = self.aspect_ratio_rules[room_type]["ideal"]
        width = (room_area / aspect_ratio) ** 0.5
        length = width * aspect_ratio
        return round(length, 2), round(width, 2)

    def adjust_room_layout(self, room_areas: dict[str, float], total_length: float, total_width: float) -> dict[str, Dict[str, float]]:
        """
        調整房間佈局以適應總長度和寬度。

        :param room_areas: 房間面積字典
        :param total_length: 總長度
        :param total_width: 總寬度
        :return: 調整後的房間佈局字典
        """
        adjusted_layout = {}
        remaining_length = total_length
        remaining_width = total_width
        
        for room_type, area in room_areas.items():
            length, width = self.calculate_room_dimensions(area, room_type)
            
            # 確保房間尺寸不超過剩餘空間
            length = min(length, remaining_length)
            width = min(width, remaining_width)
            
            adjusted_layout[room_type] = {
                "length": length,
                "width": width,
                "x": total_length - remaining_length,
                "y": total_width - remaining_width
            }
            
            # 更新剩餘空間
            if remaining_length > remaining_width:
                remaining_length -= length
            else:
                remaining_width -= width

        return adjusted_layout

    def validate_room_sizes(self, room_areas: dict[str, float], min_room_size: float = 5.0) -> bool:
        """
        驗證房間尺寸是否符合最小要求。

        :param room_areas: 房間面積字典
        :param min_room_size: 最小允許的房間尺寸（平方米）
        :return: 所有房間是否符合最小尺寸要求
        """
        return all(area >= min_room_size for area in room_areas.values())

    def optimize_room_layout(self, room_areas: dict[str, float], total_length: float, total_width: float) -> dict[str, dict[str, float]]:
        """
        優化房間佈局以最大化空間利用。

        :param room_areas: 房間面積字典
        :param total_length: 總長度
        :param total_width: 總寬度
        :return: 優化後的房間佈局字典
        """
        # 首先嘗試基本的調整
        layout = self.adjust_room_layout(room_areas, total_length, total_width)
        
        # 計算未使用的空間
        used_area = sum(room["length"] * room["width"] for room in layout.values())
        total_area = total_length * total_width
        unused_area = total_area - used_area

        # 如果有顯著未使用的空間，嘗試重新分配
        if unused_area > total_area * 0.05:  # 如果未使用空間超過5%
            # 按面積大小排序房間
            sorted_rooms = sorted(room_areas.items(), key=lambda x: x[1], reverse=True)
            
            for room_type, _ in sorted_rooms:
                # 嘗試增加房間尺寸
                if layout[room_type]["length"] < total_length:
                    extra_length = min(unused_area / layout[room_type]["width"], total_length - layout[room_type]["length"])
                    layout[room_type]["length"] += extra_length
                    unused_area -= extra_length * layout[room_type]["width"]
                
                if layout[room_type]["width"] < total_width:
                    extra_width = min(unused_area / layout[room_type]["length"], total_width - layout[room_type]["width"])
                    layout[room_type]["width"] += extra_width
                    unused_area -= extra_width * layout[room_type]["length"]
                
                if unused_area <= total_area * 0.01:  # 如果未使用空間減少到1%以下，停止優化
                    break

        return layout

    def get_room_layout_summary(self, layout: dict[str, dict[str, float]]) -> str:
        """
        生成房間佈局摘要。

        :param layout: 房間佈局字典
        :return: 房間佈局摘要字符串
        """
        summary = "房間佈局摘要:\n"
        for room_type, dimensions in layout.items():
            summary += f"{room_type}:\n"
            summary += f"  位置: (x: {dimensions['x']:.2f}, y: {dimensions['y']:.2f})\n"
            summary += f"  尺寸: {dimensions['length']:.2f}m x {dimensions['width']:.2f}m\n"
            summary += f"  面積: {dimensions['length'] * dimensions['width']:.2f} 平方米\n\n"
        return summary