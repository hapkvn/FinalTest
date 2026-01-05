from pymongo import MongoClient
import logging
from backend.config import Config

logger = logging.getLogger(__name__)

class MongoService:
    def __init__(self):
        try:
            self.client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
            self.db = self.client[Config.DB_NAME]
            self.traffic_col = self.db['traffic_data']
            self.config_col = self.db['monitored_roads']
            logger.info("✅ MongoDB Connected Successfully!")
        except Exception as e:
            logger.error(f"❌ DB Error: {e}")

    # --- THÊM HÀM NÀY ĐỂ XÓA DỮ LIỆU CŨ ---
    def reset_database(self):
        try:
            self.traffic_col.delete_many({})
            self.config_col.delete_many({})
            logger.info("🧹 Đã dọn sạch Database khởi động!")
        except Exception as e:
            logger.error(f"Lỗi dọn DB: {e}")

    def update_monitored_roads(self, roads_list):
        try:
            self.config_col.delete_many({}) 
            self.config_col.insert_one({"roads": roads_list})
            return True
        except Exception as e:
            logger.error(e)
            return False

    def get_latest_traffic(self):
        try:
            # Chỉ lấy dữ liệu của các đoạn đường đang kích hoạt
            current_config = self.config_col.find_one({}, sort=[('_id', -1)])
            if not current_config: return []
            
            active_ids = [r['id'] for r in current_config.get('roads', [])]

            pipeline = [
                {"$match": {"road_id": {"$in": active_ids}}},
                {"$sort": {"timestamp": -1}},
                {"$group": {"_id": "$road_id", "doc": {"$first": "$$ROOT"}}},
                {"$replaceRoot": {"newRoot": "$doc"}}
            ]
            
            data = list(self.traffic_col.aggregate(pipeline))
            for item in data:
                item['_id'] = str(item['_id'])
                item['timestamp'] = str(item['timestamp'])
            return data
        except Exception:
            return []

    def get_statistics(self):
        try:
            data = self.get_latest_traffic()
            total = len(data)
            danger = sum(1 for x in data if x.get('congestion_level', 0) > 0.5)
            safe = total - danger
            return {"total": total, "danger": danger, "safe": safe}
        except:
            return {"total": 0, "danger": 0, "safe": 0}

mongo_service = MongoService()