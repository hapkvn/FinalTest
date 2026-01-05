import time
import requests
import random
import logging
from datetime import datetime
from pymongo import MongoClient
from backend.config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_db():
    while True:
        try:
            client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=2000)
            client.server_info()
            logger.info("✅ Data Generator: Đã kết nối DB!")
            return client[Config.DB_NAME]
        except Exception:
            logger.warning("⏳ Đang tìm MongoDB...")
            time.sleep(3)

def get_real_traffic(lat, lon):
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={Config.TOMTOM_API_KEY}&point={lat},{lon}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            flow = data.get('flowSegmentData', {})
            current = flow.get('currentSpeed', 40)
            free = flow.get('freeFlowSpeed', 40)
            congestion = 1 - (current / free) if free > 0 else 0
            return int(current), max(0.0, congestion)
        return 40, 0
    except:
        return 40, 0

def run():
    db = connect_db()
    traffic_col = db['traffic_data']
    config_col = db['monitored_roads']

    logger.info("🚀 Data Generator đang chạy...")

    while True:
        try:
            config = config_col.find_one({}, sort=[('_id', -1)])
            roads = config.get('roads', []) if config else []

            if not roads:
                time.sleep(2)
                continue
            
            # Xóa log quét màn hình cho đỡ rối, chỉ in 1 dòng tổng
            print(f"📡 Đang cập nhật trạng thái cho {len(roads)} đoạn đường...")

            for road in roads:
                speed, congestion = get_real_traffic(road['lat'], road['lon'])
                
                traffic_col.insert_one({
                    "road_id": road['id'],
                    "name": road['name'],
                    
                    # --- SỬA ĐỔI: Copy mảng shape sang đây ---
                    "shape": road.get('shape', []),
                    
                    "lat": road['lat'],
                    "lon": road['lon'],
                    "speed": speed,
                    "congestion_level": congestion,
                    "timestamp": datetime.now()
                })
            
            time.sleep(5)
        except Exception as e:
            logger.error(f"Lỗi: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run() 