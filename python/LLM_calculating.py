class DesignService:
    def __init__(self):
        self.designer = RoomDesigner(Config.get_openai_api_key())
        self.history_file = 'design_history.json'
        self.latest_design_file = 'latest_room_design.json'  # 新增：保存最新設計的文件名
    
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
        self.save_latest_design(result)  # 新增：保存最新設計
        self.split_latest_design()       # 新增：分割最新設計
        
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
    
    def split_latest_design(self, shared_keys: List[str] = None, output_dir: str = 'output'):
        """
        根據配置分割最新的設計 JSON 文件成多個 JSON 文件。
        
        參數:
            shared_keys (list): 每個分割文件中應包含的共享鍵。
            output_dir (str): 分割後的 JSON 文件將保存到此目錄。
        """
        if shared_keys is None:
            shared_keys = ['meta_info', 'design_data', 'room_areas', 'room_ratios',
                           'locations', 'environmental_conditions', 'room_environment_rules', 'summary']
        
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

# 實例化設計服務
design_service = DesignService()

# 示例設計信息（請根據實際情況填充）
design_info_example = {
    'designName': '現代簡約風格',
    'length': 20,
    'width': 15,
    'rooms': {'客廳': 1, '臥室': 2, '廚房': 1},
    'windows': {'客廳': 2, '臥室': 1},
    'specialRequest': '希望有一個書房'
}

# 創建設計並自動分割 JSON
result = design_service.create_design(design_info_example)