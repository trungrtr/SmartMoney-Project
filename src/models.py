import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# 1. Khởi tạo Base class của SQLAlchemy
Base = declarative_base()

# 2. Định nghĩa Class User (Bổ sung để hoàn thiện ERD)
class User(Base):
    __tablename__ = 'users' # Tên bảng trong DB
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    
    # Quan hệ 1-N: 1 User có nhiều wallets
    # cascade="all, delete-orphan" nghĩa là nếu xóa User, các Wallet của họ cũng bị xóa
    wallets = relationship("Wallet", back_populates="user", cascade="all, delete-orphan")

# 3. Định nghĩa Class Wallet
class Wallet(Base):
    __tablename__ = 'wallets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    
    # Khóa ngoại liên kết với User
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Mối quan hệ 2 chiều
    user = relationship("User", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet", cascade="all, delete-orphan")

    # --- Các phương thức OOP (Methods) ---
    def add_transaction(self, transaction):
        """Thêm giao dịch vào ví và cập nhật số dư"""
        self.transactions.append(transaction)
        self.balance += transaction.amount # amount âm nếu là chi tiêu, dương nếu là thu nhập
        
    def get_balance(self):
        """Lấy số dư hiện tại của ví"""
        return self.balance

# 4. Định nghĩa Class Transaction
class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, default=datetime.date.today)
    note = Column(String)
    
    # Khóa ngoại liên kết với Wallet
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    
    # Mối quan hệ 2 chiều
    wallet = relationship("Wallet", back_populates="transactions")

# 5. SCRIPT TẠO BẢNG TRONG DATABASE
if __name__ == "__main__":
    # Tạo engine kết nối tới file finance.db (nếu chưa có, nó sẽ tự tạo file này)
    # echo=False (có thể đổi thành True nếu bạn muốn xem các lệnh SQL được sinh ra chạy ngầm)
    engine = create_engine('sqlite:///finance.db', echo=False)
    
    # Lệnh này sẽ quét toàn bộ các class kế thừa từ Base và tạo bảng tương ứng
    Base.metadata.create_all(engine)
    
    print("✅ Đã khởi tạo thành công file finance.db và các cấu trúc bảng!")