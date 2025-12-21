import requests
import json

# 1. Cấu hình
API_KEY = "YOUR_TOMTOM_API_KEY_HERE"
LAT = 21.0025  # Ví dụ: Ngã Tư Sở, Hà Nội
LON = 105.8200
ZOOM = 10

# 2. Tạo URL
url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key=ongdJdbk2vMblJsUqljZ9PUmflEntbzI&point=21.0025,105.8200"

# 3. Gửi Request
try:
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # 4. Bóc tách dữ liệu quan trọng (Parsing)
        flow_data = data.get('flowSegmentData', {})
        
        # Tốc độ xe hiện tại (đang di chuyển thực tế)
        current_speed = flow_data.get('currentSpeed')
        
        # Tốc độ lý tưởng (khi đường thông thoáng)
        free_flow_speed = flow_data.get('freeFlowSpeed')
        
        # Thời gian di chuyển hết đoạn đường này (giây)
        current_travel_time = flow_data.get('currentTravelTime')
        
        # Tọa độ vẽ đường (Shape): Dùng để vẽ line lên bản đồ Grafana nếu cần
        coordinates = flow_data.get('coordinates', {}).get('coordinate', [])
        
        print(f"--- Tình trạng giao thông tại {LAT}, {LON} ---")
        print(f"Tốc độ hiện tại: {current_speed} km/h")
        print(f"Tốc độ chuẩn: {free_flow_speed} km/h")
        
        # Logic phát hiện tắc đường đơn giản
        if current_speed < (free_flow_speed * 0.5):
            print("=> CẢNH BÁO: Đang tắc đường nghiêm trọng!")
        elif current_speed < (free_flow_speed * 0.8):
             print("=> Lưu ý: Đường đông.")
        else:
            print("=> Đường thông thoáng.")
            
    else:
        print(f"Lỗi API: {response.status_code} - {response.text}")

except Exception as e:
    print(f"Lỗi kết nối: {e}")