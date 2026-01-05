class Config:
    # Kết nối tới MongoDB trên localhost (Windows Docker Desktop)
    MONGO_URI = "mongodb://root:password@localhost:27017/?authSource=admin"
    DB_NAME = "traffic_db"
    
    # HÃY DÁN KEY TOMTOM CỦA BẠN VÀO ĐÂY
    TOMTOM_API_KEY = "ongdJdbk2vMblJsUqljZ9PUmflEntbzI" 
    
    SECRET_KEY = "dev_secret_key"
    DEBUG = True