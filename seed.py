from app import app
from models import db, Pet

with app.app_context():
    db.drop_all()
    db.create_all()

    pet1 = Pet(name="Rex", species="dog", age=4, notes="Loves walks.")
    pet2 = Pet(name="Whiskers", species="cat", photo_url="http://example.com/cat.jpg")

    db.session.add_all([pet1, pet2])
    db.session.commit()

    print("Database seeded!")
