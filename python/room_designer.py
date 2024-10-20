import json
from typing import Dict, List, Any, Tuple
from datetime import datetime
from gpt_interface import GPTInterface
from environment_rules import EnvironmentRules
from room_calculator import RoomCalculator
from score_calculator import ScoreCalculator
from data_models import DesignData, Location
from utils import extract_room_locations, repair_json
from config import Config
import os

class RoomDesigner:
    def __init__(self, api_key):
        self.gpt_interface = GPTInterface(Config.get_openai_api_key())

        self.environment_rules = EnvironmentRules()
        self.room_calculator = RoomCalculator()
        self.score_calculator = ScoreCalculator()
        self.result_filename = 'latest_room_design.json'
        self.history_folder = 'design_history'

   
    def design_room(self, design_data: DesignData, locations: dict[str, Location], current_time: datetime) -> dict[str, Any]:
        total_area = design_data.length * design_data.width
        room_areas, dynamic_ratios = self.room_calculator.calculate_room_areas(design_data.rooms, total_area)

        room_environment_rules, season, time_of_day = self.environment_rules.get_room_environment_rules(current_time)

        prompt = self.generate_gpt_prompt(design_data, room_areas, dynamic_ratios, locations, current_time)
        gpt_response = self.gpt_interface.chat_with_gpt(prompt)
        configurations = self.process_gpt_response(gpt_response)

        match configurations:
            case list() as valid_configs if valid_configs:
                for config in valid_configs:
                    room_locations = extract_room_locations(config['description'])
                    temp_data, humidity_data, light_data = self.assign_environment_data(room_locations, locations)
                    scores = self.score_calculator.calculate_total_score(
                        room_areas, design_data.windows, light_data, temp_data, humidity_data, room_environment_rules
                    )
                    config['energy_efficiency_report'] = self.score_calculator.generate_energy_efficiency_report(scores)
                
                summary = {
                    "total_area": total_area,
                    "room_count": sum(design_data.rooms.values()),
                    "configuration_count": len(valid_configs),
                    "best_energy_efficiency": max(config['energy_efficiency_report']['total_score'] for config in valid_configs)
                }
                
                result = {
                    "meta_info": {"timestamp": current_time.isoformat(), "version": "1.0"},
                    "design_data": design_data.__dict__,
                    "room_areas": room_areas,
                    "room_ratios": dynamic_ratios,
                    "locations": {k: v.to_dict() for k, v in locations.items()},
                    "environmental_conditions": {"season": season, "time_of_day": time_of_day},
                    "room_environment_rules": room_environment_rules,
                    "configurations": valid_configs,
                    "summary": summary
                }
            case _:
                print("警告: 沒有有效的配置生成")
                result = {
                    "error": "無法生成有效的房間配置",
                    "design_data": design_data.__dict__,
                    "timestamp": current_time.isoformat()
                }

        self.save_result(result, keep_history=True)
        return result
    
    def generate_gpt_prompt(self, design_data: DesignData, room_areas: dict, dynamic_ratios: dict, locations: dict[str, Location], current_time: datetime):
        character = self.generate_gpt_character()
        environment_rules, season, time_of_day = self.environment_rules.get_room_environment_rules(current_time)
        
        prompt = f"""
    作為 {character['name']}，{character['title']}，您的任務是為客戶提供三種獨特且高度節能的房間佈局方案。每種方案應具有其獨特的優勢，滿足客戶需求，並特別注重能源效率。請基於以下信息提供三種配置方案：

    1. 客戶設計需求：
    - 設計名稱：{design_data.designName}
    - 房屋尺寸：長 {design_data.length}m x 寬 {design_data.width}m（總面積：{design_data.length * design_data.width}平方米）
    - 房間需求：{json.dumps(design_data.rooms, ensure_ascii=False)}
    - 窗戶位置：{json.dumps(design_data.windows, ensure_ascii=False)}
    - 特殊要求：{design_data.specialRequest}

    注意：設計必須限制在四種房間類型內（客廳、臥室、浴室和廚房）。特殊要求中的其他空間應整合到這些房間中。

    2. 環境條件：
    - 當前季節：{season}
    - 當前時間：{'白天' if time_of_day == 'day' else '夜晚'}

    3. 房間面積分配：
    {json.dumps(room_areas, indent=3, ensure_ascii=False)}

    4. 房間面積比例：
    {json.dumps(dynamic_ratios, indent=3, ensure_ascii=False)}

    5. 環境數據：
    """
        for location, data in locations.items():
            prompt += f"   - {location}：溫度 {data.temperature}°C, 濕度 {data.humidity}%, 光照 {data.sunlight} 勒克斯\n"

        prompt += "\n6. 房間環境設計規則：\n"
        for room_type, room_data in environment_rules.items():
            prompt += f"   {room_type}:\n"
            for factor, info in room_data.items():
                prompt += f"   - {factor.capitalize()}: 理想值 {info['ideal']}, 可接受範圍 {info['range']}\n"

        prompt += f"""
    請提供三種獨特的高能源效率房間配置方案。每種方案必須包含以下結構：
    {{
    "name": "配置名稱（反映主要特點和節能特性）",
    "description": "詳細的佈局描述，必須使用以下固定格式描述每個房間的位置：
        - 客廳在位置X
        - 臥室在位置X,Y,Z (如果有多個臥室，用逗號分隔位置)
        - 廚房在位置X
        - 浴室在位置X,Y (如果有多個浴室，用逗號分隔位置)
        其中X,Y,Z是A、B、C或D中的一個。然後繼續描述如何根據環境數據優化每個房間的位置、自然光和通風的利用、空間利用的關鍵特點和節能設計。",
    "advantages": {{
        "client_requirements": "如何滿足客戶特殊要求的詳細解釋",
        "environment_optimization": "優化環境因素以最大化能源效率的具體描述",
        "space_utilization": "空間利用效率及其對能源節約的具體貢獻",
        "functionality": "功能性和實用性考量，特別是與能源使用相關的方面",
        "innovation": "具體的創新節能特點或設計描述"
    }},
    "considerations": {{
        "energy_efficiency": "與能源效率相關的具體注意事項",
        "comfort": "與舒適度相關的具體注意事項"
    }}
    }}

    請確保：
    1. 每個房間的具體位置都使用指定的固定格式明確指出。
    2. 解釋房間安排如何有利於節能。
    3. 為每種配置提供獨特的描述，避免重複。
    4. 以 {character['name']} 的專業角度設計，展現您在 {', '.join(character['expertise'])} 方面的專長。
    5. 特別強調能源效率和可持續設計。

    請將回答格式化為有效的 JSON，包含一個名為 'configurations' 的數組，其中包含三個配置對象。確保所有字符串值都用雙引號括起來，不要使用註釋或尾隨逗號。
    """
        return prompt
    def generate_gpt_character(self):
        return {
            "name": "Alex Chen",
            "title": "資深建築設計師 & 空間優化專家",
            "background": "擁有 20 年的建築設計經驗，專精於智能家居和永續建築設計。曾獲多項國際設計獎項。",
            "expertise": ["空間規劃", "永續設計", "智能家居集成", "人體工學", "光線與空氣流通優化"],
            "personality": "創新、注重細節，擅長將客戶的需求轉化為實用且美觀的設計方案。"
        }

    def process_gpt_response(self, gpt_response: str) -> list[dict[str, Any]]:
        print("Raw GPT response:", gpt_response)  # 打印原始響應
        try:
            parsed_response = json.loads(gpt_response)
            print("Parsed response:", parsed_response)  # 打印解析後的響應
            
            if 'configurations' in parsed_response and isinstance(parsed_response['configurations'], list):
                configurations = parsed_response['configurations']
                print("Extracted configurations:", configurations)  # 打印提取的配置
                return configurations
            else:
                print("No valid 'configurations' found in the response")
                return []
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            return []

    def process_configuration(self, config, design_data: DesignData, total_room_areas: dict, locations: dict[str, Location], room_environment_rules: dict):
        room_locations = extract_room_locations(config['description'])
        temp_data, humidity_data, light_data = self.assign_environment_data(room_locations, locations)
        
        scores = self.score_calculator.calculate_total_score(
            total_room_areas, design_data.windows, light_data, temp_data, humidity_data, room_environment_rules
        )
        energy_report = self.score_calculator.generate_energy_efficiency_report(scores)
        config['energy_efficiency_report'] = energy_report

        print(f"\n處理配置：{config['name']}")
        print(f"描述：{config['description']}")
        print("提取的房間位置：", room_locations)
        print("能源效率報告:")
        print(f"能源效率等級: {energy_report['energy_efficiency_grade']}")
        print(f"總分: {energy_report['total_score']}")
        print("詳細得分:")
        for key, value in energy_report['detailed_scores'].items():
            print(f"  {key}: {value}")
        print("說明:")
        for exp in energy_report['explanation']:
            print(f"  - {exp}")

    def assign_environment_data(self, room_locations: dict, locations: dict[str, Location]):
        temp_data = {}
        humidity_data = {}
        light_data = {}
        
        for room_type, locations_list in room_locations.items():
            temp_data[room_type] = []
            humidity_data[room_type] = []
            light_data[room_type] = []
            
            for location in locations_list:
                if location in locations:
                    temp_data[room_type].append(locations[location].temperature)
                    humidity_data[room_type].append(locations[location].humidity)
                    light_data[room_type].append(locations[location].sunlight)
                else:
                    print(f"警告：{room_type} 的位置 '{location}' 不在已知位置列表中，使用平均值")
                    temp_data[room_type].append(sum(loc.temperature for loc in locations.values()) / len(locations))
                    humidity_data[room_type].append(sum(loc.humidity for loc in locations.values()) / len(locations))
                    light_data[room_type].append(sum(loc.sunlight for loc in locations.values()) / len(locations))
        
        return temp_data, humidity_data, light_data

    def create_result(self, design_data: DesignData, total_room_areas: dict, dynamic_ratios: dict, 
                      locations: dict[str, Location], current_time: datetime, season: str, 
                      time_of_day: str, gpt_configurations: dict):
        return {
            "design_data": design_data.to_dict(),
            "room_areas": total_room_areas,
            "room_ratios": dynamic_ratios,
            "locations": {k: v.to_dict() for k, v in locations.items()},
            "current_time": current_time.isoformat(),
            "season": season,
            "time_of_day": time_of_day,
            "gpt_configurations": gpt_configurations
        }

    def save_result(self, result, filename='latest_room_design.json', keep_history=False):
        """
        保存設計結果到文件。

        :param result: 設計結果字典
        :param keep_history: 是否保留歷史記錄
        """
        if keep_history and os.path.exists(self.result_filename):
            self._save_history()

        try:
            with open(self.result_filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\n完整結果已保存到 {self.result_filename} 文件中")
        except IOError as e:
            print(f"保存結果到文件時發生錯誤: {str(e)}")

    def _save_history(self):
        """
        將當前的結果文件保存為歷史記錄。
        """
        if not os.path.exists(self.history_folder):
            os.makedirs(self.history_folder)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        historical_filename = f"design_{timestamp}.json"
        historical_path = os.path.join(self.history_folder, historical_filename)

        try:
            os.rename(self.result_filename, historical_path)
            print(f"歷史記錄已保存到 {historical_path}")
        except OSError as e:
            print(f"保存歷史記錄時發生錯誤: {str(e)}")
