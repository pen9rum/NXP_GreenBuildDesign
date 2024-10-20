from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from typing import Dict, List, Any
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from config import Config
from room_designer import RoomDesigner
from data_models import DesignData, Location
import anthropic
import re
import cairosvg
import glob
import os
import base64

# 初始化 Firebase
cred = credentials.Certificate('python/serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)

class DesignService:
    def __init__(self):
        self.designer = RoomDesigner(Config.get_openai_api_key())
        self.history_file = 'design_history.json'
        self.latest_design_file = 'latest_room_design.json'  # 保存最新設計的文件名
        self.output_dir = 'output'  # 分割後 JSON 文件的輸出目錄
        self.svg_dir = 'svgs'        # 儲存生成的 SVG 文件的目錄
        
        # 初始化 Anthropic 客戶端
        self.anthropic_api_key = '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'  # 請將此 API 密鑰保存在安全的地方
        self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        
        # 定義預設 prompt
        self.default_prompt = (
            "你是平面設計師的程式撰寫者，會針對配置方案要求來設計平面圖，但是是透過給我svg語法的方式，"
            "現在我給你下面這個json檔，有房間的預設的面積規格，跟最後安排的要的面積比例，"
            "，你能給我這個方案的設計平面圖的程式撰寫嗎，"
            "越接近真實的平面圖感覺越好,svg。"
        )
        
        # 確保輸出目錄存在
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.svg_dir):
            os.makedirs(self.svg_dir)

    def create_design(self, design_info: Dict[str, Any]) -> Dict[str, Any]:
        design_data = DesignData(
            designName=design_info.get('designName', ''),
            length=float(design_info.get('length', 0)),
            width=float(design_info.get('width', 0)),
            rooms=design_info.get('rooms', {}),
            windows=design_info.get('windows', {}),
            specialRequest=design_info.get('specialRequest', '')
        )

        locations = {
            "位置A": Location(temperature=27, humidity=65, sunlight=600),
            "位置B": Location(temperature=25, humidity=55, sunlight=300),
            "位置C": Location(temperature=28, humidity=70, sunlight=450),
            "位置D": Location(temperature=26, humidity=60, sunlight=200)
        }

        current_time = datetime.now()
        result = self.designer.design_room(design_data, locations, current_time)
        
        self.save_design_history(result)
        self.save_latest_design(result)  # 保存最新設計
        self.split_latest_design()       # 分割最新設計
        self.generate_svgs()             # 生成 SVG 圖片
        
        return result

    def get_history_designs(self) -> List[Dict[str, Any]]:
        try:
            with open(self.history_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_design_history(self, design: Dict[str, Any]):
        history = self.get_history_designs()
        history.append(design)
        with open(self.history_file, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=2)

    def save_latest_design(self, design: Dict[str, Any]):
        """保存最新的設計到指定的 JSON 文件。"""
        with open(self.latest_design_file, 'w', encoding='utf-8') as file:
            json.dump(design, file, ensure_ascii=False, indent=2)

    def image_to_base64(self, image_path: str) -> str:
        """將圖片文件轉換為 base64 編碼的字符串。"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def split_latest_design(self, shared_keys: List[str] = None, output_dir: str = None):
        """
        根據配置分割最新的設計 JSON 文件成多個 JSON 文件。

        參數:
            shared_keys (list): 每個分割文件中應包含的共享鍵。
            output_dir (str): 分割後的 JSON 文件將保存到此目錄。
        """
        if shared_keys is None:
            shared_keys = ['meta_info', 'design_data', 'room_areas', 'room_ratios',
                           'locations', 'environmental_conditions', 'room_environment_rules', 'summary']
        if output_dir is None:
            output_dir = self.output_dir

        json_file = self.latest_design_file  # 讀取最新的設計文件

        # 步驟 1: 讀取 JSON 文件
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"文件 '{json_file}' 未找到。無法進行分割。")
            return

        # 步驟 2: 獲取配置列表
        configurations = data.get('configurations', [])
        if not configurations:
            print("沒有找到任何配置，無需分割。")
            return

        # 步驟 3: 創建輸出目錄（如果不存在）
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 步驟 4: 根據每個配置分割 JSON
        for idx, config in enumerate(configurations, start=1):
            new_data = {}

            # 添加共享數據
            for key in shared_keys:
                if key in data:
                    new_data[key] = data[key]

            # 添加特定的配置
            new_data['configuration'] = config

            # 如果配置中有圖片，轉換為 base64
            if 'image' in new_data['configuration']:
                image_path = new_data['configuration']['image']
                if os.path.exists(image_path):
                    new_data['configuration']['image_base64'] = self.image_to_base64(image_path)
                    print(f"圖片 '{image_path}' 已轉換為 base64")
                else:
                    print(f"圖片 '{image_path}' 不存在")

            # 生成輸出文件名
            config_name = config.get('name', f'configuration_{idx}').replace(" ", "_")
            output_filename = os.path.join(output_dir, f'separated_{config_name}.json')

            # 可選：打印每個分割後的 JSON 內容
            print(f"\n分割後的 JSON for {config_name}:")
            print(json.dumps(new_data, ensure_ascii=False, indent=2))

            # 保存分割後的 JSON 文件
            with open(output_filename, 'w', encoding='utf-8') as outfile:
                json.dump(new_data, outfile, ensure_ascii=False, indent=2)

        print(f"\n所有配置已成功分割並保存到 '{output_dir}' 目錄。")

    def extract_svg(self, content: str) -> str:
        """
        從 message.content 中提取 SVG 代碼。
        假設 SVG 代碼被包裹在 ```svg ... ``` 之間。
        """
        match = re.search(r'```svg\n(.*?)\n```', content, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return None

    def generate_svgs(self):
        """
        根據分割後的 JSON 文件，使用 Anthropic API 生成 SVG 圖片。
        將生成的 SVG 保存到指定的目錄，並更新 Firestore 中的設計記錄。
        """
        # 尋找所有分離後的 JSON 文件
        separated_json_files = glob.glob(os.path.join(self.output_dir, 'separated_*.json'))

        if not separated_json_files:
            print("沒有找到分離後的 JSON 文件。")
            return
        else:
            print(f"找到 {len(separated_json_files)} 個分離後的 JSON 文件。")

        # 迴圈處理每個分離後的 JSON 文件
        for json_file in separated_json_files:
            # 讀取 JSON 文件
            with open(json_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            print(f"\n正在處理文件: {json_file}")

            # 準備 prompt 內容
            prompt_content = self.default_prompt + "\n\n" + json.dumps(config_data, ensure_ascii=False, indent=2)

            # 發送請求到 Anthropic API 使用 Messages API
            try:
                response = self.anthropic_client.completions.create(
                    prompt=anthropic.HUMAN_PROMPT + prompt_content + anthropic.AI_PROMPT,
                    model="claude-3-opus-20240229",  # 使用支援的模型名稱
                    max_tokens=2000,  # 設置最大 tokens
                )
                ai_response = response['completion']
                print("Anthropic API 回應已獲取。")
            except Exception as e:
                print(f"調用 Anthropic API 時出錯: {e}")
                continue

            # 提取 SVG 代碼
            svg_code = self.extract_svg(ai_response)
            if svg_code:
                # 生成 SVG 文件名
                base_name = os.path.splitext(os.path.basename(json_file))[0]
                svg_filename = os.path.join(self.svg_dir, f"{base_name}.svg")

                # 保存 SVG 文件
                with open(svg_filename, 'w', encoding='utf-8') as svg_file:
                    svg_file.write(svg_code)
                print(f"SVG 文件已保存至 {svg_filename}")

                # 可選：將 SVG 轉換為 PNG 或其他格式
                # cairosvg.svg2png(url=svg_filename, write_to=svg_filename.replace('.svg', '.png'))
                # print(f"PNG 文件已保存至 {svg_filename.replace('.svg', '.png')}")
                
                # 更新 Firestore 中的設計記錄，添加 SVG 文件的 URL 或 base64 編碼
                design_name = config_data.get('designName', 'unknown_design')
                config_name = config_data.get('configuration', {}).get('name', 'unknown_configuration')
                document_id = f"{design_name}_{config_name}".replace(" ", "_")
                svg_base64 = self.image_to_base64(svg_filename)
                
                designs_ref = db.collection('all_designs').document(document_id)
                designs_ref.update({
                    'svgBase64': svg_base64,
                    'svgUrl': f"/svgs/{os.path.basename(svg_filename)}"  # 假設您會設置一個靜態路徑來提供 SVG 文件
                })
                print(f"Firestore 設計記錄已更新，添加了 SVG 信息。")
            else:
                print("未能從 Anthropic API 回應中提取 SVG 代碼。")
# 實例化設計服務
design_service = DesignService()
@app.route('/api/designs', methods=['POST'])
def create_design():
    design_info = request.json
    design_info['createdAt'] = datetime.now().isoformat()
    design_info['imageUrl'] = 'https://placehold.co/600x400?text=' + design_info.get('designName', '')

    new_design_id = design_info.get("designName")
    
    designs_ref = db.collection('all_designs').document(new_design_id)
    designs_ref.set(design_info)

    result = design_service.create_design(design_info)

    all_designs = []
    all_designs_stream = db.collection('all_designs').stream()
    for design in all_designs_stream:
        design_data = design.to_dict()
        all_designs.append({
            'id': design.id,
            "designName": design_data.get("designName"),
            "length": design_data.get("length"),
            "width": design_data.get("width"),
            "rooms": {
                "livingRoom": design_data.get("rooms", {}).get("livingRoom"),
                "bathroom": design_data.get("rooms", {}).get("bathroom"),
                "bedroom": design_data.get("rooms", {}).get("bedroom"),
                "kitchen": design_data.get("rooms", {}).get("kitchen"),
            },
            "specialRequest": design_data.get("specialRequest"),
            "windows": {
                "top": design_data.get("windows", {}).get("top"),
                "right": design_data.get("windows", {}).get("right"),
                "bottom": design_data.get("windows", {}).get("bottom"),
                "left": design_data.get("windows", {}).get("left")
            },
            "createdAt": design_data.get("createdAt"),
            "imageUrl": design_data.get("imageUrl"),
            "svgUrl": design_data.get("svgUrl", ""),           # 新增：SVG 文件的 URL
            "svgBase64": design_data.get("svgBase64", "")      # 新增：SVG 的 base64 編碼
        })

    return jsonify({"design": result, "allDesigns": all_designs}), 201

@app.route('/api/getHistoryDesigns', methods=['GET'])
def get_history_designs():
    all_designs = []
    all_designs_stream = db.collection('all_designs').stream()
    for design in all_designs_stream:
        design_data = design.to_dict()
        all_designs.append({
            'id': design.id,
            "designName": design_data.get("designName"),
            "length": design_data.get("length"),
            "width": design_data.get("width"),
            "rooms": design_data.get("rooms", {}),
            "specialRequest": design_data.get("specialRequest"),
            "windows": design_data.get("windows", {}),
            "createdAt": design_data.get("createdAt"),
            "imageUrl": design_data.get("imageUrl"),
            "svgUrl": design_data.get("svgUrl", ""),           # 新增：SVG 文件的 URL
            "svgBase64": design_data.get("svgBase64", "")      # 新增：SVG 的 base64 編碼
        })
    return jsonify(all_designs), 200

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Room Design API", 200

# 設置靜態路徑以提供 SVG 文件
@app.route('/svgs/<filename>', methods=['GET'])
def get_svg(filename):
    return app.send_static_file(os.path.join('svgs', filename))

if __name__ == '__main__':
    # 確保 SVG 目錄是靜態路徑的一部分
    app.static_folder = 'svgs'
    app.run(debug=True)
