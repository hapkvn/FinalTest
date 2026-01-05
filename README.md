---Cách Clone dự án về máy: B1: Tải git -> Đăng nhập B2: Mở CMD ở folder muốn để -> Nhập lệnh git sau: -> git clone https://github.com/hapkvn/TheFinalBigData.git

---Cách Push lên github: B1: git add [Tên thư mục hay file mà chưa có trên github] -> VD: 'git add .', "." thêm tất cả file chưa có vào local git. B2: git commit -m "Mô Tả Những Gì Đã Làm Được" -> commit vào local git B3: git push -u origin main -> push lên main của github

---Chú ý: -> Trước khi code hãy ĐẢM BẢO đã lấy code mới nhất trên github, dùng lệnh 'git pull' để lấy code về máy sau đó mới code. -> Branch chính là 'main', đừng nhầm lẫn :>


# 1. Cấu hình hệ thống
Nếu dùng window sửa file docker-compose.yml thành:

    version: '3.8'
    services:
      mongo:
        image: mongo:latest
        container_name: mongodb_traffic
        restart: always
        ports:
          - "27017:27017"
        environment:
          MONGO_INITDB_ROOT_USERNAME: root
          MONGO_INITDB_ROOT_PASSWORD: password
        volumes:
          - mongodb_data:/data/db
    volumes:
      mongodb_data:
      
sửa file config.py

class Config:
  
    MONGO_URI = "mongodb://root:password@localhost:27017/?authSource=admin"
    DB_NAME = "traffic_db"
    
    # HÃY DÁN KEY TOMTOM CỦA BẠN VÀO ĐÂY
    TOMTOM_API_KEY = "HÃY DÁN KEY TOMTOM CỦA BẠN VÀO ĐÂY" 
    
    SECRET_KEY = "dev_secret_key"
    DEBUG = True

# 1. Bật Database (Chạy 1 lần duy nhất)
Mở Terminal (CMD/PowerShell/Ubuntu Terminal) tại thư mục dự án:

 PHẢI BẬT DOCKER DESKTOP TRONG SUỐT QUÁ TRÌNH CHẠY
 
 Lệnh này sẽ tự động tải MongoDB về và chạy.

    docker-compose up -d


# 2. Cài đặt thư viện Python (Chạy 1 lần duy nhất)
  Vẫn ở Terminal đó, chạy lần lượt:

  Windows:

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
 

  Ubuntu/Mac:
  
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
# 3. Chạy Dự án
  Bây giờ mọi thứ đã sẵn sàng, bạn mở 2 cửa sổ Terminal để chạy như bình thường:

Terminal 1 (Web Server):

# Nhớ activate venv trước nếu mở cửa sổ mới
    python -m backend.app
  (hoặc python3 ...)
  
  Terminal 2 (Data Generator):

    python data_generator.py
  (hoặc python3 ...)
