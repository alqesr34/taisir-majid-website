import os
import json
import uuid
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_change_in_production')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MESSAGES_FILE = os.path.join(BASE_DIR, 'messages.json')
ACTIVITIES_FILE = os.path.join(BASE_DIR, 'activities.json')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/img/news')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ADMIN_USER = 'muk'
ADMIN_PASS = '12395'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_data(file_path, data):
    existing_data = load_data(file_path)
    existing_data.append(data)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)


def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_all_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    activities = load_data(ACTIVITIES_FILE)
    # Sort: Pinned first, then by date (newest first)
    # Assuming date is YYYY-MM-DD, string comparison works for sorting
    # We want pinned=True to be before pinned=False
    # And within that, newer dates first.
    activities.sort(key=lambda x: (not x.get('pinned', False), x.get('date', '')), reverse=True)
    return render_template('index.html', activities=activities)


@app.route('/contact', methods=['POST'])
def contact():
    data = request.form.to_dict()
    save_data(MESSAGES_FILE, data)
    return jsonify({'status': 'success', 'message': 'تم استلام رسالتك، شكراً'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='بيانات الدخول غير صحيحة')
    return render_template('login.html')


@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    messages = load_data(MESSAGES_FILE)
    activities = load_data(ACTIVITIES_FILE)
    # Sort activities for admin view as well (Newest first)
    activities.sort(key=lambda x: x.get('date', ''), reverse=True)
    return render_template('admin.html', messages=messages, activities=activities)


@app.route('/admin/add_activity', methods=['POST'])
def add_activity():
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    title = request.form.get('title')
    date = request.form.get('date')
    text = request.form.get('text')
    file = request.files.get('image')

    if not title or not date or not text:
        return jsonify({'status': 'error', 'message': 'جميع الحقول مطلوبة'})

    image_path = ''
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        image_path = f"img/news/{unique_filename}"

    activity = {
        'id': str(uuid.uuid4()),
        'title': title,
        'date': date,
        'text': text,
        'image': image_path,
        'pinned': False
    }
    save_data(ACTIVITIES_FILE, activity)
    return jsonify({'status': 'success', 'message': 'تم إضافة النشاط بنجاح'})


@app.route('/admin/edit_activity/<activity_id>', methods=['POST'])
def edit_activity(activity_id):
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    activities = load_data(ACTIVITIES_FILE)
    activity = next((a for a in activities if a['id'] == activity_id), None)
    
    if not activity:
        return jsonify({'status': 'error', 'message': 'Activity not found'}), 404

    title = request.form.get('title')
    date = request.form.get('date')
    text = request.form.get('text')
    file = request.files.get('image')

    if title: activity['title'] = title
    if date: activity['date'] = date
    if text: activity['text'] = text

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        activity['image'] = f"img/news/{unique_filename}"

    save_all_data(ACTIVITIES_FILE, activities)
    return jsonify({'status': 'success', 'message': 'تم تعديل النشاط بنجاح'})


@app.route('/admin/pin_activity/<activity_id>', methods=['POST'])
def pin_activity(activity_id):
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    activities = load_data(ACTIVITIES_FILE)
    activity = next((a for a in activities if a['id'] == activity_id), None)
    
    if not activity:
        return jsonify({'status': 'error', 'message': 'Activity not found'}), 404
    
    # Toggle pinned status
    activity['pinned'] = not activity.get('pinned', False)
    
    save_all_data(ACTIVITIES_FILE, activities)
    return jsonify({'status': 'success', 'message': 'تم تحديث حالة التثبيت', 'pinned': activity['pinned']})


@app.route('/admin/delete_activity/<activity_id>', methods=['POST'])
def delete_activity(activity_id):
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    activities = load_data(ACTIVITIES_FILE)
    updated_activities = [a for a in activities if a['id'] != activity_id]
    
    save_all_data(ACTIVITIES_FILE, updated_activities)
    return jsonify({'status': 'success', 'message': 'تم حذف النشاط'})


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    # Get environment settings
    is_production = os.environ.get('ENVIRONMENT') == 'production'
    port = int(os.environ.get('PORT', 8000))
    
    # Show startup info
    print("\n" + "="*60)
    print("✅ التطبيق يعمل الآن!")
    if not is_production:
        print("\n📍 الروابط المتاحة:")
        print("   🏠 الصفحة الرئيسية (محلي): http://localhost:%d" % port)
        print("   🏠 الصفحة الرئيسية (الشبكة): http://192.168.1.108:%d" % port)
        print("\n   🔐 لوحة التحكم (محلي): http://localhost:%d/login" % port)
        print("   🔐 لوحة التحكم (الشبكة): http://192.168.1.108:%d/login" % port)
        print("\n👤 بيانات الدخول:")
        print("   اسم المستخدم: muk")
        print("   كلمة المرور: 12395")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=not is_production)


