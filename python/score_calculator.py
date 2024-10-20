from typing import Dict, List, Any

class ScoreCalculator:
    def __init__(self):
        self.room_importance = {
            "livingRoom": 0.4,
            "bedroom": 0.3,
            "kitchen": 0.2,
            "bathroom": 0.1
        }
        self.room_light_importance = {
            "livingRoom": 0.4,
            "bedroom": 0.2,
            "kitchen": 0.3,
            "bathroom": 0.1
        }
        self.room_humidity_importance = {
            "livingRoom": 0.3,
            "bedroom": 0.3,
            "kitchen": 0.2,
            "bathroom": 0.2
        }

    def calculate_total_score(self, rooms: dict[str, float], windows: dict[str, bool],
                              light_data: dict[str, List[float]], temperature_data: dict[str, List[float]],
                              humidity_data: dict[str, List[float]], room_environment_rules: dict[str, Dict]) -> dict[str, float]:
        """
        計算總體分數。

        :param rooms: 房間面積字典
        :param windows: 窗戶位置字典
        :param light_data: 光照數據字典
        :param temperature_data: 溫度數據字典
        :param humidity_data: 濕度數據字典
        :param room_environment_rules: 房間環境規則字典
        :return: 包含總分和各項分數的字典
        """
        temp_score = self.calculate_temperature_score(rooms, temperature_data, room_environment_rules)
        light_score = self.calculate_light_score(rooms, windows, light_data, room_environment_rules)
        humidity_score = self.calculate_humidity_score(rooms, humidity_data, room_environment_rules)

        total_score = temp_score + light_score + humidity_score

        return {
            "total_score": round(total_score, 2),
            "temperature_score": round(temp_score, 2),
            "light_score": round(light_score, 2),
            "humidity_score": round(humidity_score, 2)
        }
    def calculate_temperature_score(self, rooms: dict[str, float], temperature_data: dict[str, List[float]],
                                    room_environment_rules: dict[str, Dict]) -> float:
        score = 50
        for room, area in rooms.items():
            if room not in room_environment_rules or room not in temperature_data:
                print(f"警告: 缺少 {room} 的環境規則或溫度數據")
                continue

            ideal_temp = room_environment_rules[room]["temperature"]["ideal"]
            temp_range = room_environment_rules[room]["temperature"]["range"][1] - room_environment_rules[room]["temperature"]["range"][0]
            actual_temps = temperature_data[room]

            if not actual_temps:
                print(f"警告: {room} 沒有溫度數據")
                continue

            room_score = 0
            for actual_temp in actual_temps:
                difference = abs(actual_temp - ideal_temp) / temp_range
                room_score += max(2, 10 - difference * 20)  # 確保最低分為 2

            average_room_score = room_score / len(actual_temps)
            score += (average_room_score - 6) * self.room_importance.get(room, 0.1) * 5  # 使用默認重要性 0.1

        return max(10, min(score, 50))  # 確保最終分數在 10-50 之間

    def calculate_light_score(self, rooms: dict[str, float], windows: dict[str, bool],
                              light_data: dict[str, List[float]], room_environment_rules: dict[str, Dict]) -> float:
        """
        計算光照得分。

        :param rooms: 房間面積字典
        :param windows: 窗戶位置字典
        :param light_data: 光照數據字典
        :param room_environment_rules: 房間環境規則字典
        :return: 光照得分
        """
        score = 30
        for room, area in rooms.items():
            ideal_light = room_environment_rules[room]["sunlight"]["ideal"]
            light_range = room_environment_rules[room]["sunlight"]["range"][1] - room_environment_rules[room]["sunlight"]["range"][0]
            actual_lights = light_data[room]
            room_score = 0
            for actual_light in actual_lights:
                difference = min(abs(actual_light - ideal_light) / light_range, 1)
                room_score += max(2, 10 - difference * 16)  # 確保最低分為 2
            average_room_score = room_score / len(actual_lights)
            score += (average_room_score - 6) * self.room_light_importance[room] * 3  # 調整基準和乘數

        window_bonus = len([w for w in windows.values() if w]) * 1.5
        score = min(30, score + window_bonus)

        return max(5, score)  # 確保最低分為 5

    def calculate_humidity_score(self, rooms: dict[str, float], humidity_data: dict[str, List[float]],
                                 room_environment_rules: dict[str, Dict]) -> float:
        """
        計算濕度得分。

        :param rooms: 房間面積字典
        :param humidity_data: 濕度數據字典
        :param room_environment_rules: 房間環境規則字典
        :return: 濕度得分
        """
        score = 20
        for room, area in rooms.items():
            ideal_humidity = room_environment_rules[room]["humidity"]["ideal"]
            humidity_range = room_environment_rules[room]["humidity"]["range"][1] - room_environment_rules[room]["humidity"]["range"][0]
            actual_humidities = humidity_data[room]
            room_score = 0
            for actual_humidity in actual_humidities:
                difference = min(abs(actual_humidity - ideal_humidity) / humidity_range, 1)
                room_score += max(2, 10 - difference * 16)  # 確保最低分為 2
            average_room_score = room_score / len(actual_humidities)
            score += (average_room_score - 6) * self.room_humidity_importance[room] * 2  # 調整基準和乘數

        return max(5, min(score, 20))  # 確保分數在 5-20 之間

    def get_efficiency_grade(self, score: float) -> str:
        """
        根據得分獲取效率等級。

        :param score: 總分
        :return: 效率等級
        """
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        elif score >= 50:
            return "E"
        else:
            return "F"

    def generate_energy_efficiency_report(self, scores: Dict[str, float]) -> dict[str, Any]:
        """
        生成能源效率報告。

        :param scores: 包含各項分數的字典
        :return: 能源效率報告字典
        """
        grade = self.get_efficiency_grade(scores['total_score'])

        report = {
            "energy_efficiency_grade": grade,
            "total_score": scores['total_score'],
            "detailed_scores": {
                "temperature_adaptation": scores['temperature_score'],
                "natural_light_utilization": scores['light_score'],
                "humidity_control": scores['humidity_score']
            },
            "explanation": self.generate_score_explanation(
                scores['temperature_score'],
                scores['light_score'],
                scores['humidity_score']
            )
        }

        return report

    def generate_score_explanation(self, temp_score: float, light_score: float, humidity_score: float) -> List[str]:
        """
        生成分數說明。

        :param temp_score: 溫度得分
        :param light_score: 光照得分
        :param humidity_score: 濕度得分
        :return: 說明列表
        """
        explanation = []

        if temp_score >= 40:
            explanation.append("溫度控制優秀，可大幅減少空調使用。")
        elif temp_score >= 30:
            explanation.append("溫度控制良好，空調使用需求適中。")
        else:
            explanation.append("溫度控制有待改善，可能需要頻繁使用空調。")

        if light_score >= 25:
            explanation.append("自然光利用度高，可顯著減少照明用電。")
        elif light_score >= 20:
            explanation.append("自然光利用度良好，照明需求適中。")
        else:
            explanation.append("自然光利用度不足，可能增加照明用電。")

        if humidity_score >= 15:
            explanation.append("濕度控制優秀，幾乎不需要使用除濕機。")
        elif humidity_score >= 10:
            explanation.append("濕度控制良好，除濕需求較低。")
        else:
            explanation.append("濕度控制有待改善，可能需要頻繁使用除濕機。")

        return explanation

    def get_improvement_suggestions(self, scores: dict[str, float]) -> List[str]:
        """
        根據分數提供改進建議。

        :param scores: 包含各項分數的字典
        :return: 改進建議列表
        """
        suggestions = []

        if scores['temperature_score'] < 30:
            suggestions.append("考慮增加隔熱材料或優化窗戶位置以改善溫度控制。")
        if scores['light_score'] < 20:
            suggestions.append("增加窗戶或調整房間佈局以提高自然光利用率。")
        if scores['humidity_score'] < 10:
            suggestions.append("考慮安裝除濕系統或改善通風以控制濕度。")
        if scores['total_score'] < 60:
            suggestions.append("整體能源效率較低，建議全面審視房間設計並考慮使用更多節能設備。")

        return suggestions