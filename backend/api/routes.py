from flask import Blueprint, jsonify, request
from backend.services.mongo_service import mongo_service
from backend.config import Config
import requests
import urllib.parse

api_bp = Blueprint('api', __name__, url_prefix='/api')

def get_coords(name):
    try:
        headers = {'User-Agent': 'TrafficApp/1.0'}
        q = urllib.parse.quote(f"{name}, Hà Nội, Việt Nam")
        url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1"
        res = requests.get(url, headers=headers).json()
        if res: return float(res[0]['lat']), float(res[0]['lon'])
        return None, None
    except: return None, None

@api_bp.route('/find-route', methods=['POST'])
def find_route():
    data = request.json
    start, end = data.get('start'), data.get('end')
    
    lat1, lon1 = get_coords(start)
    lat2, lon2 = get_coords(end)
    
    if not lat1 or not lat2:
        return jsonify({"status": "error", "message": "Không tìm thấy địa điểm"}), 404

    url = f"https://api.tomtom.com/routing/1/calculateRoute/{lat1},{lon1}:{lat2},{lon2}/json?key={Config.TOMTOM_API_KEY}&traffic=true"
    res = requests.get(url).json()
    
    if 'routes' not in res:
        return jsonify({"status": "error", "message": "Không tìm được đường"}), 404

    points = res['routes'][0]['legs'][0]['points']
    monitored_segments = []
    
    # Bước nhảy: Càng nhỏ thì càng mịn nhưng nặng DB. 20 là số ổn định.
    step = max(1, len(points) // 20) 
    
    for i in range(0, len(points) - step, step):
        # Lấy điểm giữa để đo traffic
        mid_point = points[i]
        
        # --- SỬA ĐỔI QUAN TRỌNG: Cắt lấy toàn bộ các điểm nhỏ trong đoạn này ---
        # Điều này giúp giữ nguyên độ cong của con đường
        segment_shape = points[i : i + step + 1] 

        monitored_segments.append({
            "id": f"SEG_{i}",
            "name": f"Đoạn {i}",
            # Lưu mảng shape chứa tất cả các điểm uốn lượn
            "shape": segment_shape, 
            "lat": mid_point['latitude'], 
            "lon": mid_point['longitude']
        })

    mongo_service.update_monitored_roads(monitored_segments)

    return jsonify({
        "status": "success",
        "route": points,
        "segments": monitored_segments
    })

@api_bp.route('/traffic-data', methods=['GET'])
def get_traffic():
    return jsonify(mongo_service.get_latest_traffic())

@api_bp.route('/statistics', methods=['GET'])
def get_stats():
    return jsonify(mongo_service.get_statistics())