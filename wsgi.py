import os
import json
import uuid
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename

# Flask app setup
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_change_in_production')
app.config['JSON_AS_ASCII'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MESSAGES_FILE = os.path.join(BASE_DIR, 'messages.json')
ACTIVITIES_FILE = os.path.join(BASE_DIR, 'activities.json')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/img/news')
VIDEO_FOLDER = os.path.join(BASE_DIR, 'static/videos/news')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'avi', 'mov', 'mkv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

ADMIN_USER = os.environ.get('ADMIN_USER', 'muk')
ADMIN_PASS = os.environ.get('ADMIN_PASS', '12395')

# Ensure necessary directories exist
for directory in [app.config['UPLOAD_FOLDER'], app.config['VIDEO_FOLDER'], os.path.dirname(MESSAGES_FILE), os.path.dirname(ACTIVITIES_FILE)]:
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not create directory {directory}: {e}", flush=True)


def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def allowed_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS


def save_data(file_path, data):
    try:
        existing_data = load_data(file_path)
        existing_data.append(data)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")
        return False
    return True


def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")
            return []
    return []


def save_all_data(file_path, data):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving all data to {file_path}: {e}")
        return False
    return True


@app.route('/')
def index():
    activities = load_data(ACTIVITIES_FILE)
    # Sort: Pinned first with media (video/image), then by date (newest first)
    # Separate activities: pinned with media, pinned without media, unpinned with media, unpinned without media
    has_media = lambda a: a.get('video') or a.get('image')
    pinned_with_media = [a for a in activities if a.get('pinned', False) and has_media(a)]
    pinned_without_media = [a for a in activities if a.get('pinned', False) and not has_media(a)]
    unpinned_with_media = [a for a in activities if not a.get('pinned', False) and has_media(a)]
    unpinned_without_media = [a for a in activities if not a.get('pinned', False) and not has_media(a)]
    
    # Sort each group by date (newest first)
    for group in [pinned_with_media, pinned_without_media, unpinned_with_media, unpinned_without_media]:
        group.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Combine: pinned with media, pinned without, unpinned with media, unpinned without
    activities = pinned_with_media + pinned_without_media + unpinned_with_media + unpinned_without_media
    return render_template('index.html', activities=activities)


@app.route('/contact', methods=['POST'])
def contact():
    data = request.form.to_dict()
    data['id'] = str(uuid.uuid4())
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
    
    activities = load_data(ACTIVITIES_FILE)
    messages = load_data(MESSAGES_FILE)

    # Backfill IDs for messages that don't have them
    messages_updated = False
    for msg in messages:
        if 'id' not in msg:
            msg['id'] = str(uuid.uuid4())
            messages_updated = True
    
    if messages_updated:
        save_all_data(MESSAGES_FILE, messages)
    # Sort activities: Pinned first with media, then by date (newest first)
    # Separate activities: pinned with media, pinned without media, unpinned with media, unpinned without media
    has_media = lambda a: a.get('video') or a.get('image')
    pinned_with_media = [a for a in activities if a.get('pinned', False) and has_media(a)]
    pinned_without_media = [a for a in activities if a.get('pinned', False) and not has_media(a)]
    unpinned_with_media = [a for a in activities if not a.get('pinned', False) and has_media(a)]
    unpinned_without_media = [a for a in activities if not a.get('pinned', False) and not has_media(a)]
    
    # Sort each group by date (newest first)
    for group in [pinned_with_media, pinned_without_media, unpinned_with_media, unpinned_without_media]:
        group.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Combine: pinned with media, pinned without, unpinned with media, unpinned without
    activities = pinned_with_media + pinned_without_media + unpinned_with_media + unpinned_without_media
    return render_template('admin.html', messages=messages, activities=activities)


@app.route('/admin/add_activity', methods=['POST'])
def add_activity():
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    title = request.form.get('title')
    date = request.form.get('date')
    text = request.form.get('text')
    image_file = request.files.get('image')
    video_file = request.files.get('video')

    if not title or not date or not text:
        return jsonify({'status': 'error', 'message': 'جميع الحقول مطلوبة'})

    image_path = ''
    video_path = ''
    
    # Handle image upload
    if image_file and allowed_image(image_file.filename):
        filename = secure_filename(image_file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        image_path = f"img/news/{unique_filename}"
    
    # Handle video upload
    if video_file and allowed_video(video_file.filename):
        filename = secure_filename(video_file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        video_file.save(os.path.join(app.config['VIDEO_FOLDER'], unique_filename))
        video_path = f"videos/news/{unique_filename}"

    activity = {
        'id': str(uuid.uuid4()),
        'title': title,
        'date': date,
        'text': text,
        'image': image_path,
        'video': video_path,
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
    image_file = request.files.get('image')
    video_file = request.files.get('video')

    if title: activity['title'] = title
    if date: activity['date'] = date
    if text: activity['text'] = text

    if image_file and allowed_image(image_file.filename):
        filename = secure_filename(image_file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        activity['image'] = f"img/news/{unique_filename}"
    
    if video_file and allowed_video(video_file.filename):
        filename = secure_filename(video_file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        video_file.save(os.path.join(app.config['VIDEO_FOLDER'], unique_filename))
        activity['video'] = f"videos/news/{unique_filename}"

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


@app.route('/admin/delete_message/<message_id>', methods=['POST'])
def delete_message(message_id):
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    messages = load_data(MESSAGES_FILE)
    updated_messages = [m for m in messages if m.get('id') != message_id]
    
    save_all_data(MESSAGES_FILE, updated_messages)
    return jsonify({'status': 'success', 'message': 'تم حذف الرسالة'})


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'status': 'error', 'message': 'الصفحة غير موجودة'}), 404


@app.errorhandler(500)
def internal_error(error):
    print(f"Internal Server Error: {error}")
    return jsonify({'status': 'error', 'message': 'خطأ في الخادم'}), 500


if __name__ == '__main__':
    # Get environment settings
    is_production = os.environ.get('ENVIRONMENT') == 'production'
    port = int(os.environ.get('PORT', 8000))
    
    # Show startup info
    print("\n" + "="*60)
    print("Application Starting...")
    print("Environment:", "PRODUCTION" if is_production else "DEVELOPMENT")
    print("Port:", port)
    if not is_production:
        print("\nLocal URLs:")
        print("   Homepage: http://localhost:%d" % port)
        print("   Admin: http://localhost:%d/login" % port)
        print("\nCredentials:")
        print("   Username: muk")
        print("   Password: 12395")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=not is_production)
