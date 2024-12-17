from ..database import SessionLocal
from ..models.models import Engineer, Project, SalesStaff

def check_data():
    db = SessionLocal()
    try:
        print("\n=== 営業担当者一覧 ===")
        sales_staff = db.query(SalesStaff).all()
        for staff in sales_staff:
            print(f"ID: {staff.id}, 名前: {staff.name}, メール: {staff.email}")

        print("\n=== エンジニア一覧 ===")
        engineers = db.query(Engineer).all()
        for eng in engineers:
            print(f"ID: {eng.id}, 名前: {eng.name}, スキル: {eng.skills}")

        print("\n=== プロジェクト一覧 ===")
        projects = db.query(Project).all()
        for proj in projects:
            print(f"ID: {proj.id}, 名前: {proj.name}, 状態: {proj.status}")

    finally:
        db.close()

if __name__ == "__main__":
    check_data()