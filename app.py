
from flask import (
    Flask, render_template, request, redirect, session,
    url_for, flash, jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import os, random

from models.models import db, User, Skill, Connection, Message, Session, Notification, SkillTest, SkillCatalog

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillswap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dev'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if User.query.filter_by(username=username).first():
            flash(' Username already exists.')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash(' Email already in use.')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash(' Passwords do not match.')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash("Invalid credentials")
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.bio = request.form['bio']
        if 'profile_picture' in request.files:
            image = request.files['profile_picture']
            if image.filename:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_picture = f"/static/uploads/{filename}"
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

@app.route('/user/<username>')
def public_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    skills_teach = [s for s in user.skills if s.type == 'own' and s.verified]
    skills_learn = [s for s in user.skills if s.type == 'want']
    return render_template('public_profile.html', user=user, skills_teach=skills_teach, skills_learn=skills_learn)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    skills_teach = [s for s in user.skills if s.type == 'own' and s.verified]
    skills_learn = [s for s in user.skills if s.type == 'want']
    skill_catalog = SkillCatalog.query.all()

    return render_template('dashboard.html', user=user, skills_teach=skills_teach, skills_learn=skills_learn, skills=skill_catalog)


@app.route('/skill/add', methods=['GET', 'POST'])
def add_skill():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        skill_name = request.form['name'].strip()
        skill_type = request.form['type']
        user_id = session['user_id']

        if not skill_name:
            flash("Please select a skill.")
            return redirect(url_for('dashboard'))

        existing = Skill.query.filter(
            func.lower(Skill.name) == skill_name.lower(),
            Skill.type == skill_type,
            Skill.user_id == user_id
        ).first()

        if existing:
            flash("You already added this skill.")
            return redirect(url_for('dashboard'))

        if skill_type == 'own':
            session['pending_skill'] = {
                'name': skill_name,
                'type': skill_type,
                'user_id': user_id
            }
            return redirect(url_for('verify_skill', skill_name=skill_name))

        db.session.add(Skill(name=skill_name, type=skill_type, user_id=user_id, verified=False))
        db.session.commit()
        flash("Skill added!")
        return redirect(url_for('dashboard'))

    skills = SkillCatalog.query.all()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('add_skill.html', skills=skills)

    return render_template('layout.html', content=render_template('add_skill.html', skills=skills))


@app.route('/verify_skill/<skill_name>', methods=['GET', 'POST'])
def verify_skill(skill_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    skill_name = skill_name.lower()

    if 'test_progress' not in session or session['test_progress']['skill_name'] != skill_name:
        questions = SkillTest.query.filter_by(skill_name=skill_name).all()
        if not questions:
            flash("No verification test found for this skill.")
            return redirect(url_for('dashboard'))

        random.shuffle(questions)
        session['test_progress'] = {
            'skill_name': skill_name,
            'index': 0,
            'score': 0,
            'question_ids': [q.id for q in questions[:10]]
        }

    progress = session['test_progress']
    index = progress['index']
    question_ids = progress['question_ids']

    if index >= len(question_ids):
        score = progress['score']
        session.pop('test_progress')
        if score >= 7:
            skill_data = session.pop('pending_skill', None)
            if skill_data:
                db.session.add(Skill(
                    name=skill_data['name'],
                    type=skill_data['type'],
                    user_id=session['user_id'],
                    verified=True
                ))
                db.session.commit()
                flash(f" Skill verified! You scored {score}/10")
        else:
            flash(f" Test failed. Score: {score}/10")
        return redirect(url_for('dashboard'))

    question = db.session.get(SkillTest, question_ids[index])

    if request.method == 'POST':
        if request.form.get('answer') == question.correct_answer:
            progress['score'] += 1
        progress['index'] += 1
        session['test_progress'] = progress
        return redirect(url_for('verify_skill', skill_name=skill_name))

    return render_template('verify_skill.html', question=question, index=index + 1, total=len(question_ids))



@app.route('/matches')
def matches():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    all_skills = sorted({s.name.lower() for s in Skill.query.all()})
    vectorize = lambda skills: [1 if s.name.lower() in [sk.name.lower() for sk in skills] else 0 for s in SkillCatalog.query.all()]

    my_teach = vectorize([s for s in user.skills if s.type == 'own' and s.verified])
    my_learn = vectorize([s for s in user.skills if s.type == 'want'])
    potential_matches = []

    for other in User.query.filter(User.id != user.id).all():
        if Connection.query.filter(
            (
                ((Connection.requester_id == user.id) & (Connection.receiver_id == other.id)) |
                ((Connection.requester_id == other.id) & (Connection.receiver_id == user.id))
            ) & (Connection.status == 'accepted')
        ).first():
            continue

        teach = vectorize([s for s in other.skills if s.type == 'own' and s.verified])
        learn = vectorize([s for s in other.skills if s.type == 'want'])
        score = (cosine_similarity([my_teach], [learn])[0][0] + cosine_similarity([my_learn], [teach])[0][0]) / 2

        if score > 0:
            potential_matches.append({'user': other, 'score': round(score, 2)})

    potential_matches.sort(key=lambda x: x['score'], reverse=True)

    return render_template(
        'matches.html',
        user=user,
        matches=potential_matches,
        my_connections=Connection.query.filter(
            ((Connection.requester_id == user.id) | (Connection.receiver_id == user.id)) &
            (Connection.status == 'accepted')
        ).all(),
        pending_requests=Connection.query.filter_by(requester_id=user.id, status='pending').all(),
        incoming_requests=Connection.query.filter_by(receiver_id=user.id, status='pending').all()
    )


@app.route('/sessions')
def sessions():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    return render_template('sessions.html',
                           user=user,
                           teaching=Session.query.filter_by(teacher_id=user.id).order_by(Session.start_time).all(),
                           learning=Session.query.filter_by(learner_id=user.id).order_by(Session.start_time).all())

@app.route('/schedule', methods=['GET', 'POST'])
def schedule_session():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    current_user = db.session.get(User, session['user_id'])
    conns = Connection.query.filter(
        ((Connection.requester_id == current_user.id) | (Connection.receiver_id == current_user.id)) &
        (Connection.status == 'accepted')
    ).all()
    connected_users = [
        conn.receiver if conn.requester_id == current_user.id else conn.requester for conn in conns
    ]

    my_skills = {s.name.lower(): s for s in current_user.skills if s.type == 'own'}
    shared_skills = [s for s in Skill.query.filter(Skill.user_id != current_user.id) if s.name.lower() in my_skills]

    if request.method == 'POST':
        new_session = Session(
            teacher_id=current_user.id,
            learner_id=int(request.form['partner_id']),
            skill_id=int(request.form['skill_id']),
            start_time=datetime.fromisoformat(request.form['start_time']),
            end_time=datetime.fromisoformat(request.form['end_time'])
        )

        if Session.query.filter_by(
            teacher_id=new_session.teacher_id,
            learner_id=new_session.learner_id,
            skill_id=new_session.skill_id,
            start_time=new_session.start_time,
            end_time=new_session.end_time
        ).first():
            flash("This session already exists.")
        else:
            db.session.add(new_session)
            db.session.commit()
            flash("Session scheduled!")

        return redirect(url_for('sessions'))

    return render_template('schedule_session.html', connections=connected_users, shared_skills=shared_skills)
@app.route('/session/join/<int:session_id>')
def join_session(session_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    sess = db.session.get(Session, session_id)
    current_user = db.session.get(User, session['user_id'])

    if not sess or current_user.id not in [sess.teacher_id, sess.learner_id]:
        flash("You are not authorized to join this session.")
        return redirect(url_for('sessions'))

    partner = sess.learner if current_user.id == sess.teacher_id else sess.teacher

    return render_template('join_session.html', session=sess, partner=partner)


@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    return render_template('settings.html', user=user)

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    if not user.check_password(request.form['current_password']):
        flash("Current password is incorrect.")
    elif request.form['new_password'] != request.form['confirm_password']:
        flash("New passwords do not match.")
    else:
        user.set_password(request.form['new_password'])
        db.session.commit()
        flash("Password updated successfully.")
    return redirect(url_for('settings'))

@app.route('/update_notifications', methods=['POST'])
def update_notifications():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    user.notify_email = 'email_updates' in request.form
    user.notify_messages = 'new_message_alerts' in request.form
    user.notify_sessions = 'session_reminders' in request.form
    db.session.commit()
    flash("Notification preferences updated.")
    return redirect(url_for('settings'))

@app.route('/update_privacy', methods=['POST'])
def update_privacy():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    user.is_public = 'public_profile' in request.form
    db.session.commit()
    flash("Privacy settings updated.")
    return redirect(url_for('settings'))

@app.route('/deactivate_account', methods=['POST'])
def deactivate_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if 'confirm' not in request.form:
        flash("Please confirm before deactivating.")
        return redirect(url_for('settings'))

    try:
        user = db.session.get(User, session['user_id'])
        user.is_active = False
        db.session.commit()
        session.clear()
        flash("Your account has been deactivated.")
    except SQLAlchemyError:
        db.session.rollback()
        flash("Something went wrong. Please try again.")

    return redirect(url_for('home'))
@app.route('/messages')
def message_home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = db.session.get(User, user_id)

    connections = Connection.query.filter(
        ((Connection.requester_id == user_id) | (Connection.receiver_id == user_id)) &
        (Connection.status == 'accepted')
    ).all()

    chat_partners = [
        conn.receiver if conn.requester_id == user_id else conn.requester
        for conn in connections
    ]

    return render_template('message_list.html', user=user, partners=chat_partners)

@app.route('/chat/<int:partner_id>', methods=['GET', 'POST'])
def chat(partner_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = db.session.get(User, user_id)
    partner = db.session.get(User, partner_id)

    if not Connection.query.filter(
        (((Connection.requester_id == user_id) & (Connection.receiver_id == partner_id)) |
         ((Connection.requester_id == partner_id) & (Connection.receiver_id == user_id))) &
        (Connection.status == 'accepted')
    ).first():
        return "Not connected", 403

    if request.method == 'POST':
        content = request.form.get('message', '').strip()
        file = request.files.get('file')
        file_path = None

        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            file_path = f"/static/uploads/{filename}"

        if content or file_path:
            msg = Message(sender_id=user_id, receiver_id=partner_id, content=content, file_path=file_path)
            db.session.add(msg)
            db.session.commit()

    messages = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == partner_id)) |
        ((Message.sender_id == partner_id) & (Message.receiver_id == user_id))
    ).order_by(Message.timestamp).all()

    return render_template('chat.html', user=user, partner=partner, messages=messages)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

