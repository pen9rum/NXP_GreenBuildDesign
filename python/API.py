from flask import Flask, request, jsonify
from flask_cors import CORS  # 引入 CORS
from datetime import datetime

# from google.cloud import firestore

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('serviceAccount.json')

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)

# 初始化firestore
db = firestore.client()
app = Flask(__name__)
CORS(app) 

# 創建新設計
@app.route('/api/designs', methods=['POST'])
def create_design():
    design_info = request.json
    design_info['createdAt'] = datetime.now()
    design_info['imageUrl'] = 'https://placehold.co/600x400?text='+ design_info.get('designName')
    
    # 使用 designName 作為 ID
    new_design_id = design_info.get("designName")  # 獲取 designName 作為 ID
    
    # 將設計信息添加到 Firestore 中
    designs_ref = db.collection('all_designs').document(new_design_id)
    designs_ref.set(design_info)  # 使用 set() 方法添加設計信息
    # history_ref = db.collection('designs').document()
    # history_ref.set({
    #     'createdAt': datetime.now(),
    #     'designName': design_info.get('designName'),
    #     'imageUrl': 'https://placehold.co/600x400?text='+ design_info.get('designName'),
    # })  # 使用 set() 方法添加設計信息

    # 自動抓取 Firestore 中的所有設計
    all_designs = []
    all_designs_stream = db.collection('all_designs').stream()  # 獲取所有設計
    for design in all_designs_stream:
        design_data = design.to_dict()  # 將 Firestore 資料轉成字典
        all_designs.append({
            'id': design.id,  # 使用 DocumentSnapshot 的 id 屬性
            "designName": design_data.get("designName"),
            "length": design_data.get("length"),
            "width": design_data.get("width"),
            "rooms": {
                "livingRoom": design_data.get("livingRoom"),
                "bathroom": design_data.get("bathroom"),
                "bedroom": design_data.get("bedroom"),
                "kitchen": design_data.get("kitchen"),
            },
            "specialRequest": design_data.get("specialRequest"),
            "windows": {
                "top": design_data.get("top"),
                "right": design_data.get("right"),
                "bottom": design_data.get("bottom"),
                "left": design_data.get("left")
            }
        })

    # 返回創建的設計的 ID 和所有設計
    return jsonify(design_info), 201


if __name__ == '__main__':
    app.run(debug=True)  # 啟動 Flask 應用
