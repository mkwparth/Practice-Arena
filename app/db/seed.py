from app.db.session import SessionLocal
from app.models.category import Category

db = SessionLocal()

categories = [
    Category(name="DSA"),
    Category(name="System Design"),
    Category(name="Python"),
    Category(name="Databases"),
    Category(name="Backend")
]

db.add_all(categories)
db.commit()

print("Categories seeded")