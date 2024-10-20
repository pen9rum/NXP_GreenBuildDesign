from openai import OpenAI
from typing import Dict, List, Any
import time
import json

class GPTInterface:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def chat_with_gpt(self, prompt: str, max_attempts: int = 3, retry_delay: int = 5) -> str:
        for attempt in range(max_attempts):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4",  
                    messages=[
                        {"role": "system", "content": "You are a professional room designer."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=3000,
                    temperature=0.7,
                )
                return response.choices[0].message.content
            except Exception as e:
                if attempt < max_attempts - 1:
                    print(f"嘗試 {attempt + 1} 失敗: {str(e)}. {retry_delay} 秒後重試...")
                    time.sleep(retry_delay)
                else:
                    raise Exception(f"無法完成請求: {str(e)}")


    def generate_room_design(self, design_requirements: dict[str, Any], environment_data: dict[str, Any]) -> str:
        """
        生成房間設計。

        :param design_requirements: 設計需求
        :param environment_data: 環境數據
        :return: 生成的房間設計
        """
        prompt = self.create_design_prompt(design_requirements, environment_data)
        return self.chat_with_gpt(prompt)

    def create_design_prompt(self, design_requirements: dict[str, Any], environment_data: dict[str, Any]) -> str:
        """
        創建設計提示。

        :param design_requirements: 設計需求
        :param environment_data: 環境數據
        :return: 格式化的提示字符串
        """
        prompt = f"""
        As a professional room designer, please create a room layout based on the following requirements and environmental data:

        Design Requirements:
        {json.dumps(design_requirements, indent=2)}

        Environmental Data:
        {json.dumps(environment_data, indent=2)}

        Please provide a detailed room layout description, including:
        1. The position and size of each room
        2. Furniture and equipment placement
        3. Color scheme
        4. Lighting design
        5. Energy efficiency and sustainability considerations

        Ensure the design is both aesthetically pleasing and practical, with a special focus on energy efficiency and environmental friendliness.

        Please format your response as a valid JSON object with the following structure:
        {{
            "layout_description": "Detailed description of the room layout",
            "room_positions": {{
                "living_room": "Position A",
                "bedroom": ["Position B", "Position C"],
                "kitchen": "Position D",
                "bathroom": ["Position B", "Position C"]
            }},
            "color_scheme": "Description of the color scheme",
            "lighting_design": "Description of the lighting design",
            "energy_efficiency_features": ["Feature 1", "Feature 2", "Feature 3"],
            "sustainability_aspects": ["Aspect 1", "Aspect 2", "Aspect 3"]
        }}
        """
        return prompt

    def analyze_design(self, design: str) -> dict[str, Any]:
        """
        分析生成的設計。

        :param design: 生成的設計
        :return: 設計分析結果
        """
        prompt = f"""
        Please analyze the following room design and provide a detailed evaluation:

        {design}

        Evaluate the design based on the following aspects:
        1. Functionality
        2. Aesthetics
        3. Energy efficiency
        4. Adherence to client requirements
        5. Innovation
        6. Feasibility

        For each aspect, provide a specific score (1-10) and a detailed explanation.

        Please format your response as a valid JSON object with the following structure:
        {{
            "functionality": {{ "score": 8, "explanation": "Detailed explanation" }},
            "aesthetics": {{ "score": 7, "explanation": "Detailed explanation" }},
            "energy_efficiency": {{ "score": 9, "explanation": "Detailed explanation" }},
            "client_requirements": {{ "score": 8, "explanation": "Detailed explanation" }},
            "innovation": {{ "score": 7, "explanation": "Detailed explanation" }},
            "feasibility": {{ "score": 9, "explanation": "Detailed explanation" }},
            "overall_score": 8,
            "summary": "Overall summary of the design analysis"
        }}
        """
        response = self.chat_with_gpt(prompt)
        return json.loads(response)

    def suggest_improvements(self, design: str, analysis: dict[str, Any]) -> List[dict[str, str]]:
        """
        根據分析結果提出改進建議。

        :param design: 原始設計
        :param analysis: 設計分析結果
        :return: 改進建議列表
        """
        prompt = f"""
        Based on the following room design and analysis results, please provide specific improvement suggestions:

        Original Design:
        {design}

        Analysis Results:
        {json.dumps(analysis, indent=2)}

        Please provide at least 5 specific improvement suggestions. Each suggestion should include:
        1. The specific content of the suggestion
        2. The aspect expected to be improved
        3. Possible challenges in implementing the suggestion
        4. Estimated impact on the overall design

        Ensure the suggestions are both practical and innovative, with a special focus on improving energy efficiency and sustainability.

        Please format your response as a valid JSON array of objects, where each object represents a suggestion with the following structure:
        [
            {{
                "suggestion": "Detailed description of the suggestion",
                "aspect_to_improve": "The aspect this suggestion aims to improve",
                "potential_challenges": "Description of potential challenges",
                "estimated_impact": "Description of the estimated impact on the overall design"
            }},
            ...
        ]
        """
        response = self.chat_with_gpt(prompt)
        return json.loads(response)

    def parse_gpt_response(self, response: str) -> dict[str, Any]:
        """
        解析 GPT 的 JSON 回應。

        :param response: GPT 的原始回應字符串
        :return: 解析後的 JSON 對象
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print("警告：GPT 回應不是有效的 JSON 格式。嘗試修復...")
            # 這裡可以添加一些基本的修復邏輯，例如:
            # - 移除不合法的控制字符
            # - 處理未閉合的括號
            # - 處理缺少逗號的情況
            # 但要注意，這種修復可能不總是成功或正確
            cleaned_response = response.replace('\n', '').replace('\r', '').strip()
            try:
                return json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                print(f"無法修復 JSON: {str(e)}")
                return {"error": "Invalid JSON response", "raw_response": response}