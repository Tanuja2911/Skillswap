from app import app
from models.models import db, SkillCatalog, SkillTest
from sqlalchemy import func

with app.app_context():
    
    testable_skills = db.session.query(func.lower(SkillTest.skill_name)).distinct().all()
    valid_skill_names = {name[0] for name in testable_skills}
    
    SkillCatalog.query.delete()
    
    for name in valid_skill_names:
        db.session.add(SkillCatalog(name=name.capitalize()))

    db.session.commit()
    print("SkillCatalog updated with only testable skills.")
