import os
from dotenv import load_dotenv

# 加載 .env 文件中的環境變量
load_dotenv()

class Config:
    # OpenAI API 配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GPT_MODEL = "gpt-4"
    MAX_TOKENS = 3000
    TEMPERATURE = 0.7

    # Anthropic API 配置
    ANTHROPIC_API_KEY = os.getenv('Claude_API_KEY')
    ANTHROPIC_MODEL = "claude-3-opus-20240229"  # 根據需要調整模型名稱
    ANTHROPIC_MAX_TOKENS = 2000

    # 房間設計配置
    MIN_ROOM_SIZE = 5.0  # 最小房間尺寸（平方米）
    MAX_ASPECT_RATIO = 2.0  # 最大長寬比

    # 環境參數範圍
    TEMPERATURE_RANGE = (15, 30)  # 溫度範圍（攝氏度）
    HUMIDITY_RANGE = (30, 70)  # 濕度範圍（百分比）
    SUNLIGHT_RANGE = (0, 1000)  # 光照範圍（勒克斯）

    # 結果保存配置
    RESULT_DIRECTORY = "design_results"

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is not set. Please set it in the .env file.")

        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("Anthropic API key is not set. Please set it in the .env file.")

        if not os.path.exists(cls.RESULT_DIRECTORY):
            os.makedirs(cls.RESULT_DIRECTORY)

    @classmethod
    def get_openai_api_key(cls):
        return cls.OPENAI_API_KEY

    @classmethod
    def get_anthropic_api_key(cls):
        return cls.ANTHROPIC_API_KEY

# 在導入時驗證配置
Config.validate()
