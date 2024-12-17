from ..database import engine
from ..models.models import Base

def create_tables():
    print("データベーステーブルを作成します...")
    Base.metadata.create_all(bind=engine)
    print("テーブルの作成が完了しました。")

if __name__ == "__main__":
    create_tables()