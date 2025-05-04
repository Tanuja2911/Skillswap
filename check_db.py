
from app import app, db
with app.app_context():
        # 🧨 ONLY if you're okay losing test data
    db.create_all()

