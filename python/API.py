from flask import Flask, request, jsonify
from flask_cors import CORS  # 引入 CORS
import time

# from google.cloud import firestore
# import os

# # 設置 Google Cloud 認證環境變量
# import firebase_admin
# from firebase_admin import credentials

# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

app = Flask(__name__)
CORS(app) 
# db = firestore.Client()

# 創建新設計
@app.route('/api/designs', methods=['POST'])
def create_design():
    design_info = request.json
    
    # 將設計信息添加到 Firestore 中
    # designs_ref = db.collection('designs')
    # new_design_ref = designs_ref.add(design_info)  # 添加設計信息

    # # 自動抓取 Firestore 中的所有設計
    # all_designs = []
    # all_designs_stream = designs_ref.stream()  # 獲取所有設計
    # for design in all_designs_stream:
    #     design_data = design.to_dict()
    #     all_designs.append({
    #         'id': design.id,  # 獲取設計的 ID
    #         'pic': design_data.get('pic', ''),  # 獲取 pic，默認為空字符串
    #         'score': design_data.get('score', 1),  # 獲取 score，默認為 1
    #         'description': design_data.get('description', '')  # 獲取 description，默認為空字符串
    #     })
    response = {
            "designName": "sdfsdf",
            "length": "1",
            "width": "1",
            "rooms": {
                "livingRoom": 1,
                "bathroom": 1,
                "bedroom": 1,
                "kitchen": 1
            },
            "specialRequest": "",
            "windows": {
                "top": False,
                "right": False,
                "bottom": False,
                "left": False
            }
        }

    # 返回創建的設計的 ID 和所有設計
    return jsonify(response), 201

# 獲取歷史紀錄
@app.route('/api/getHistoryDesigns', methods=['GET'])
def getHistoryDesign():
    # designs_ref = db.collection('designs')  # 替換 'designs' 為您的集合名稱
    # designs = designs_ref.stream()

    # history_designs = []
    # for design in designs:
    #     history_designs.append(design.to_dict())  # 將每個設計轉換為字典格式

    return jsonify(
        [
            {
                'id':0,
                'designName': 'test',   
            }
        ]
    ), 200  # 返回歷史紀錄，狀態碼 200


if __name__ == '__main__':
    app.run(debug=True)  # 啟動 Flask 應用
