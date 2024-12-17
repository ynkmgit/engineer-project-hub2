from datetime import date
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.models import Engineer, Project, SalesStaff

def seed_data():
    db = SessionLocal()
    try:
        # 営業担当者のテストデータ
        sales_staff_data = [
            {
                "name": "山田太郎",
                "email": "yamada@example.com",
                "phone": "090-1111-2222"
            },
            {
                "name": "佐藤花子",
                "email": "sato@example.com",
                "phone": "090-3333-4444"
            }
        ]
        
        for staff_data in sales_staff_data:
            staff = SalesStaff(**staff_data)
            db.add(staff)
        db.commit()

        # エンジニアのテストデータ
        engineer_data = [
            {
                "name": "鈴木一郎",
                "email": "suzuki@example.com",
                "phone": "090-5555-6666",
                "skills": {
                    "languages": ["Python", "JavaScript", "Java"],
                    "frameworks": ["FastAPI", "React", "Spring Boot"],
                    "databases": ["PostgreSQL", "MongoDB"]
                },
                "status": "稼働可能",
                "available_date": date(2025, 1, 15)
            },
            {
                "name": "田中二郎",
                "email": "tanaka@example.com",
                "phone": "090-7777-8888",
                "skills": {
                    "languages": ["PHP", "Python", "TypeScript"],
                    "frameworks": ["Laravel", "Django", "Vue.js"],
                    "databases": ["MySQL", "Redis"]
                },
                "status": "案件中",
                "available_date": date(2025, 3, 1)
            }
        ]
        
        for eng_data in engineer_data:
            engineer = Engineer(**eng_data)
            db.add(engineer)
        db.commit()

        # プロジェクトのテストデータ
        project_data = [
            {
                "name": "ECサイトリニューアル",
                "description": "既存ECサイトのフルリニューアルプロジェクト",
                "required_skills": {
                    "languages": ["Python", "JavaScript"],
                    "frameworks": ["FastAPI", "React"],
                    "databases": ["PostgreSQL"]
                },
                "start_date": date(2025, 2, 1),
                "end_date": date(2025, 7, 31),
                "status": "準備中",
                "sales_id": 1
            },
            {
                "name": "社内システム刷新",
                "description": "レガシーシステムの最新化プロジェクト",
                "required_skills": {
                    "languages": ["Java", "TypeScript"],
                    "frameworks": ["Spring Boot", "Angular"],
                    "databases": ["Oracle"]
                },
                "start_date": date(2025, 3, 1),
                "end_date": date(2025, 8, 31),
                "status": "準備中",
                "sales_id": 2
            }
        ]
        
        for proj_data in project_data:
            project = Project(**proj_data)
            db.add(project)
        db.commit()

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("テストデータを投入します...")
    seed_data()
    print("テストデータの投入が完了しました。")