import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS # 用於處理跨域請求，如果前後端分開部署會需要

# 建立 Flask 應用程式實例
app = Flask(__name__)
# 啟用 CORS，允許所有來源的跨域請求
CORS(app)

# 定義首頁路由，用於渲染 HTML 模板
@app.route('/')
def index():
    # 渲染名為 'index.html' 的模板檔案
    return render_template('index.html')
 
# 定義 API 路由，用於生成資料點
@app.route('/generate_data', methods=['GET'])
def generate_data():
    # 從請求參數中獲取資料點數量 n，預設值為 100
    n = int(request.args.get('n', 100))
    # 從請求參數中獲取斜率 a，預設值為 2.0
    a = float(request.args.get('a', 2.0))
    # 從請求參數中獲取噪音變異數 var，預設值為 10.0
    var = float(request.args.get('var', 10.0))
    # 從請求參數中獲取截距 b，預設值為 10.0
    b = float(request.args.get('b', 10.0))

    # 生成 n 個介於 0 到 10 之間的 x 值
    x = np.linspace(0, 10, n)
    # 生成常態分佈的噪音，均值為 0，標準差為 sqrt(var)
    noise = np.random.normal(0, np.sqrt(var), n)
    # 根據線性迴歸模型 y = ax + b + noise 生成 y 值
    y = a * x + b + noise

    # 將 x 和 y 值轉換為列表，以便 JSON 序列化
    data = {
        'x': x.tolist(),
        'y': y.tolist(),
        'line_x': x.tolist(),
        'line_y': (a * x + b).tolist() # 理想的線性迴歸線
    }
    # 返回 JSON 格式的資料
    return jsonify(data)

# 如果直接執行此檔案，則啟動 Flask 應用程式
if __name__ == '__main__':
    # 在調試模式下運行，方便開發
    app.run(debug=True)