from datetime import datetime
from typing import Dict, Tuple, Any

class EnvironmentRules:
    def __init__(self):
        self.season_temps = {
            "spring": 21.12,
            "summer": 26.38,
            "autumn": 23.03,
            "winter": 16.51
        }
        self.season_humidity = {
            "spring": 79.59,
            "summer": 80.37,
            "autumn": 77.98,
            "winter": 78.42
        }

    def get_season(self, date: datetime) -> str:
        """
        根據日期確定季節。

        :param date: 日期時間對象
        :return: 季節名稱
        """
        month = date.month
        if 3 <= month <= 5:
            return "spring"
        elif 6 <= month <= 8:
            return "summer"
        elif 9 <= month <= 11:
            return "autumn"
        else:
            return "winter"

    def is_daytime(self, time: datetime) -> bool:
        """
        判斷是否為白天。

        :param time: 時間對象
        :return: 是否為白天
        """
        return 6 <= time.hour < 18

    def get_room_environment_rules(self, current_time: datetime) -> Tuple[dict[str, Any], str, str]:
        """
        獲取房間環境規則。

        :param current_time: 當前時間
        :return: 房間環境規則、季節和時間段（白天/夜晚）的元組
        """
        season = self.get_season(current_time)
        daytime = self.is_daytime(current_time)
        time_of_day = "day" if daytime else "night"

        rules = {
            "livingRoom": self._get_room_rules(season, daytime, is_living_room=True),
            "bedroom": self._get_room_rules(season, daytime, is_bedroom=True),
            "kitchen": self._get_room_rules(season, daytime, is_kitchen=True),
            "bathroom": self._get_room_rules(season, daytime, is_bathroom=True)
        }

        return rules, season, time_of_day

    def _get_room_rules(self, season: str, daytime: bool, 
                        is_living_room: bool = False, is_bedroom: bool = False, 
                        is_kitchen: bool = False, is_bathroom: bool = False) -> dict[str, Any]:
        """
        獲取特定房間的環境規則。

        :param season: 季節
        :param daytime: 是否為白天
        :param is_living_room: 是否為客廳
        :param is_bedroom: 是否為臥室
        :param is_kitchen: 是否為廚房
        :param is_bathroom: 是否為浴室
        :return: 房間環境規則字典
        """
        base_temp = self.season_temps[season]
        base_humidity = self.season_humidity[season]

        temp_adjust = 1 if daytime else -1
        if is_bedroom:
            temp_adjust -= 1

        ideal_temp = round(base_temp + temp_adjust, 1)
        temp_range = (round(ideal_temp - 2, 1), round(ideal_temp + 2, 1))

        humidity_adjust = -5 if is_bedroom else 0
        ideal_humidity = base_humidity + humidity_adjust
        humidity_range = (ideal_humidity - 10, ideal_humidity + 5)

        if is_living_room:
            light_ideal = 500 if daytime else 100
            light_range = (300, 750) if daytime else (50, 200)
        elif is_bedroom:
            light_ideal = 200 if daytime else 0
            light_range = (100, 300) if daytime else (0, 50)
        elif is_kitchen:
            light_ideal = 500 if daytime else 300
            light_range = (300, 750) if daytime else (200, 400)
        elif is_bathroom:
            light_ideal = 200 if daytime else 100
            light_range = (100, 300) if daytime else (50, 150)
        else:
            light_ideal = 300
            light_range = (200, 500)

        return {
            "temperature": {"ideal": ideal_temp, "range": temp_range},
            "humidity": {"ideal": ideal_humidity, "range": humidity_range},
            "sunlight": {"ideal": light_ideal, "range": light_range}
        }

    def get_environment_summary(self, rules: dict[str, Any], season: str, time_of_day: str) -> str:
        """
        生成環境規則摘要。

        :param rules: 房間環境規則
        :param season: 季節
        :param time_of_day: 時間段（白天/夜晚）
        :return: 環境規則摘要字符串
        """
        summary = f"環境規則摘要 (季節: {season}, 時間: {'白天' if time_of_day == 'day' else '夜晚'}):\n\n"
        for room, rule in rules.items():
            summary += f"{room}:\n"
            for factor, values in rule.items():
                summary += f"  {factor.capitalize()}: 理想值 {values['ideal']}, 範圍 {values['range']}\n"
            summary += "\n"
        return summary

    def adjust_rules_for_special_conditions(self, rules: dict[str, Any], special_conditions: dict[str, Any]) -> dict[str, Any]:
        """
        根據特殊條件調整環境規則。

        :param rules: 原始環境規則
        :param special_conditions: 特殊條件字典
        :return: 調整後的環境規則
        """
        adjusted_rules = rules.copy()

        if special_conditions.get("high_humidity_warning"):
            for room in adjusted_rules:
                adjusted_rules[room]["humidity"]["ideal"] -= 5
                adjusted_rules[room]["humidity"]["range"] = (
                    adjusted_rules[room]["humidity"]["range"][0] - 5,
                    adjusted_rules[room]["humidity"]["range"][1] - 5
                )

        if special_conditions.get("heat_wave"):
            for room in adjusted_rules:
                adjusted_rules[room]["temperature"]["ideal"] += 2
                adjusted_rules[room]["temperature"]["range"] = (
                    adjusted_rules[room]["temperature"]["range"][0] + 2,
                    adjusted_rules[room]["temperature"]["range"][1] + 2
                )

        return adjusted_rules

    def validate_environment_data(self, environment_data: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
        """
        驗證環境數據是否符合規則。

        :param environment_data: 實際環境數據
        :param rules: 環境規則
        :return: 驗證結果字典
        """
        validation_result = {}
        for room, data in environment_data.items():
            room_result = {}
            for factor, value in data.items():
                if factor in rules[room]:
                    ideal = rules[room][factor]["ideal"]
                    range_min, range_max = rules[room][factor]["range"]
                    if range_min <= value <= range_max:
                        status = "正常"
                    elif value < range_min:
                        status = "過低"
                    else:
                        status = "過高"
                    room_result[factor] = {
                        "value": value,
                        "ideal": ideal,
                        "status": status
                    }
            validation_result[room] = room_result
        return validation_result