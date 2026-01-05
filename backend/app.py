from flask import Flask, render_template
from backend.api.routes import api_bp
from backend.config import Config
from backend.services.mongo_service import mongo_service # Import service

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # --- THÊM DÒNG NÀY: Xóa sạch dữ liệu cũ khi Server khởi động ---
    print("🧹 Đang dọn dẹp hệ thống...")
    mongo_service.reset_database()
    
    app.run(debug=True, port=5000, use_reloader=False) 
    # use_reloader=False để tránh nó chạy lệnh xóa 2 lần