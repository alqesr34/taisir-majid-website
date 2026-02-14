import os
import json
import uuid
from flask import Flask, request, jsonify, session, redirect, url_for, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')
app.secret_key = 'super_secret_key_change_this'

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

# --- ASSETS ---

CSS_CONTENT = """
/* 
   Modern Design System
   For: Tayseer Majid Al-Qaisi Website
*/

:root {
    --primary-color: #0f172a;
    --accent-color: #cca43b;
    --text-dark: #1e293b;
    --text-light: #64748b;
    --bg-light: #f8fafc;
    --bg-white: #ffffff;
    --white: #ffffff;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    --transition: all 0.3s ease;
}

* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { font-family: 'Cairo', sans-serif; color: var(--text-dark); line-height: 1.6; background-color: var(--bg-white); overflow-x: hidden; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
h1, h2, h3, h4, h5, h6 { font-weight: 700; line-height: 1.2; }
a { text-decoration: none; color: inherit; transition: var(--transition); }
ul { list-style: none; }
.btn { display: inline-block; padding: 12px 30px; border-radius: 50px; font-weight: 600; cursor: pointer; font-size: 1rem; transition: var(--transition); border: 2px solid transparent; }
.btn-primary { background-color: var(--accent-color); color: var(--white); box-shadow: 0 4px 15px rgba(204, 164, 59, 0.4); }
.btn-primary:hover { background-color: #b08d32; transform: translateY(-2px); }
.btn-outline { border-color: var(--white); color: var(--white); }
.btn-outline:hover { background-color: var(--white); color: var(--primary-color); }
.btn-block { width: 100%; display: flex; justify-content: center; align-items: center; gap: 10px; }
#loader { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--primary-color); display: flex; justify-content: center; align-items: center; z-index: 9999; transition: opacity 0.5s ease, visibility 0.5s ease; }
.spinner { width: 50px; height: 50px; border: 5px solid rgba(255, 255, 255, 0.3); border-radius: 50%; border-top-color: var(--accent-color); animation: spin 1s ease-in-out infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.loaded #loader { opacity: 0; visibility: hidden; }
.navbar { position: fixed; top: 0; left: 0; width: 100%; padding: 15px 0; background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(10px); z-index: 1000; box-shadow: var(--shadow-md); }
.navbar .container { display: flex; justify-content: space-between; align-items: center; }
.logo { font-size: 1.5rem; font-weight: 700; color: var(--white); display: flex; align-items: center; gap: 10px; }
.logo i { color: var(--accent-color); }
.nav-links { display: flex; gap: 30px; align-items: center; }
.nav-links a { color: rgba(255, 255, 255, 0.8); font-size: 1rem; position: relative; padding: 5px 0; }
.nav-links a:hover, .nav-links a.active { color: var(--white); }
.nav-links a:not(.btn-primary)::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; width: 0; height: 2px; background: var(--accent-color); transition: var(--transition); }
.nav-links a:not(.btn-primary):hover::after, .nav-links a.active:not(.btn-primary)::after { width: 100%; }
.menu-toggle { display: none; background: none; border: none; color: var(--white); font-size: 1.5rem; cursor: pointer; }
.hero { position: relative; height: 100vh; display: flex; align-items: center; justify-content: center; text-align: center; color: var(--white); background: url('https://images.unsplash.com/photo-1596395818833-875f7823e20e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80') center/cover no-repeat; margin-top: 0; }
.hero-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(15, 23, 42, 0.6) 100%); }
.hero-content { position: relative; z-index: 2; max-width: 800px; }
.hero h2 { font-size: 1.5rem; color: var(--accent-color); margin-bottom: 15px; font-weight: 400; }
.hero h1 { font-size: 3.5rem; margin-bottom: 20px; line-height: 1.1; }
.hero p { font-size: 1.2rem; margin-bottom: 40px; color: rgba(255, 255, 255, 0.9); }
.hero-buttons { display: flex; gap: 20px; justify-content: center; }
.section { padding: 100px 0; }
.section-header { text-align: center; margin-bottom: 60px; }
.section-header h3 { color: var(--accent-color); font-size: 1rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; }
.section-header h2 { font-size: 2.5rem; color: var(--primary-color); margin-bottom: 20px; }
.line { width: 80px; height: 4px; background: var(--accent-color); margin: 0 auto; border-radius: 2px; }
.bg-light { background-color: var(--bg-light); }
.bg-dark { background-color: var(--primary-color); color: var(--white); }
.bg-dark .section-header h2 { color: var(--white); }
.about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }
.about-image { position: relative; }
.profile-img { width: 100%; height: 500px; object-fit: cover; border-radius: 20px; box-shadow: var(--shadow-lg); transition: var(--transition); }
.profile-img:hover { transform: scale(1.02); }
.about-text p { font-size: 1.1rem; margin-bottom: 20px; color: var(--text-light); }
.features-list { margin-top: 30px; }
.features-list li { display: flex; align-items: center; gap: 15px; font-size: 1.1rem; margin-bottom: 15px; font-weight: 600; }
.features-list i { color: var(--accent-color); }
.cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; }
.card { background: var(--white); padding: 30px; border-radius: 15px; box-shadow: var(--shadow-sm); transition: var(--transition); text-align: center; }
.card:hover { transform: translateY(-10px); box-shadow: var(--shadow-lg); }
.card-icon { width: 70px; height: 70px; background: rgba(204, 164, 59, 0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 1.8rem; color: var(--accent-color); }
.card h4 { font-size: 1.3rem; margin-bottom: 15px; color: var(--primary-color); }
.card p { color: var(--text-light); font-size: 0.95rem; }
.news-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; justify-content: center; }
.news-item { cursor: pointer; position: relative; border-radius: 12px; overflow: hidden; height: 180px; box-shadow: var(--shadow-md); transition: transform 0.3s ease, box-shadow 0.3s ease; }
.news-item:hover { box-shadow: var(--shadow-lg); transform: translateY(-5px); }
.news-img { height: 100%; width: 100%; display: block; }
.news-img img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
.news-item:hover .news-img img { transform: scale(1.1); }
.date { display: block; font-size: 0.85rem; color: var(--accent-color); margin-bottom: 10px; font-weight: 600; }
.contact-wrapper { display: grid; grid-template-columns: 1fr 1.5fr; gap: 50px; background: rgba(255, 255, 255, 0.05); padding: 50px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); }
.contact-info h3 { font-size: 2rem; margin-bottom: 20px; }
.contact-info p { color: rgba(255, 255, 255, 0.7); margin-bottom: 40px; }
.info-item { display: flex; align-items: center; gap: 20px; margin-bottom: 25px; font-size: 1.1rem; }
.info-item i { color: var(--accent-color); font-size: 1.2rem; width: 30px; text-align: center; }
.social-links { margin-top: 40px; display: flex; gap: 15px; }
.social-links a { width: 45px; height: 45px; background: rgba(255, 255, 255, 0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: var(--white); transition: var(--transition); }
.social-links a:hover { background: var(--accent-color); transform: translateY(-3px); }
.contact-form h3 { margin-bottom: 30px; font-size: 1.5rem; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: rgba(255, 255, 255, 0.9); }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 12px 15px; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; color: var(--white); font-family: inherit; transition: var(--transition); font-size: 1rem; }
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { outline: none; border-color: var(--accent-color); background: rgba(255, 255, 255, 0.15); }
.form-message { margin-top: 15px; text-align: center; font-weight: 600; }
.form-message.success { color: #4ade80; }
.form-message.error { color: #f87171; }
footer { background: #0b1120; padding: 40px 0; color: var(--white); text-align: center; border-top: 1px solid rgba(255, 255, 255, 0.05); }
@media (max-width: 991px) { .hero h1 { font-size: 2.5rem; } .about-grid, .contact-wrapper { grid-template-columns: 1fr; } .menu-toggle { display: block; } .nav-links { position: fixed; top: 70px; left: 0; width: 100%; background: var(--primary-color); flex-direction: column; padding: 30px 0; transform: translateY(-150%); transition: var(--transition); box-shadow: var(--shadow-lg); } .nav-links.active { transform: translateY(0); } }
.animate-up { opacity: 0; transform: translateY(30px); animation: fadeInUp 0.8s forwards; }
.reveal-up, .reveal-left, .reveal-right { opacity: 0; transition: all 0.8s ease-out; }
.reveal-up { transform: translateY(50px); } .reveal-left { transform: translateX(-50px); } .reveal-right { transform: translateX(50px); }
.reveal-active { opacity: 1; transform: translate(0, 0); }
.delay-1 { animation-delay: 0.2s; transition-delay: 0.2s; } .delay-2 { animation-delay: 0.4s; transition-delay: 0.4s; } .delay-3 { animation-delay: 0.6s; transition-delay: 0.6s; }
@keyframes fadeInUp { to { opacity: 1; transform: translateY(0); } }
.modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0, 0, 0, 0.8); backdrop-filter: blur(5px); opacity: 0; transition: opacity 0.3s ease; }
.modal.show { opacity: 1; }
.modal-content { background-color: #fefefe; margin: 5% auto; border-radius: 15px; width: 90%; max-width: 800px; position: relative; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4); animation: modalSlideUp 0.4s ease; overflow: hidden; max-height: 90vh; display: flex; flex-direction: column; }
@keyframes modalSlideUp { from { transform: translateY(50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
.close-modal { color: #333; position: absolute; top: 15px; left: 20px; font-size: 28px; font-weight: bold; z-index: 100; cursor: pointer; background: rgba(255, 255, 255, 0.9); width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; transition: 0.3s; }
.modal-text-content { padding: 30px; text-align: right; background: #fff; }
.news-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.4); display: flex; justify-content: center; align-items: center; opacity: 0; transition: opacity 0.3s ease; z-index: 2; }
.news-item:hover .news-overlay { opacity: 1; }
.news-content-mini { position: absolute; bottom: 0; left: 0; width: 100%; padding: 20px; background: linear-gradient(to top, rgba(15, 23, 42, 0.9), transparent); color: white; z-index: 3; text-align: right; }
.pinned-badge { position: absolute; top: 10px; right: 10px; background: var(--accent-color); color: white; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-size: 0.9rem; z-index: 5; }
"""

JS_CONTENT = """
document.addEventListener('DOMContentLoaded', () => {
    window.addEventListener('load', () => { document.body.classList.add('loaded'); });
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = menuToggle.querySelector('i');
            if (navLinks.classList.contains('active')) { icon.classList.replace('fa-bars', 'fa-times'); }
            else { icon.classList.replace('fa-times', 'fa-bars'); }
        });
    }
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                menuToggle.querySelector('i').classList.replace('fa-times', 'fa-bars');
            }
        });
    });
    const revealElements = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) { entry.target.classList.add('reveal-active'); observer.unobserve(entry.target); }
        });
    }, { threshold: 0.15 });
    revealElements.forEach(el => revealObserver.observe(el));
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = contactForm.querySelector('button[type="submit"]');
            const formMessage = document.getElementById('formMessage');
            btn.disabled = true;
            try {
                const response = await fetch('/contact', { method: 'POST', body: new FormData(contactForm) });
                const result = await response.json();
                if (result.status === 'success') {
                    formMessage.innerText = result.message;
                    formMessage.className = 'form-message success';
                    contactForm.reset();
                }
            } catch (error) {
                formMessage.innerText = 'حدث خطأ. حاول مرة أخرى.';
                formMessage.className = 'form-message error';
            } finally {
                btn.disabled = false;
                setTimeout(() => { formMessage.innerText = ''; formMessage.className = 'form-message'; }, 5000);
            }
        });
    }
    const modal = document.getElementById("newsModal");
    window.openNewsModal = function (element) {
        document.getElementById("modalTitle").innerText = element.getAttribute('data-title');
        document.getElementById("modalDate").innerText = element.getAttribute('data-date');
        document.getElementById("modalText").innerHTML = element.getAttribute('data-text').replace(/\\n/g, '<br>');
        const img = document.getElementById("modalImg");
        const imgSrc = element.getAttribute('data-image');
        if (imgSrc) { img.src = imgSrc; img.parentElement.style.display = "block"; }
        else { img.parentElement.style.display = "none"; }
        modal.style.display = "flex";
        setTimeout(() => modal.classList.add("show"), 10);
    }
    const closeModal = document.querySelector(".close-modal");
    if (closeModal) {
        closeModal.onclick = () => { modal.classList.remove("show"); setTimeout(() => modal.style.display = "none", 300); }
    }
    window.onclick = (event) => { if (event.target == modal) { modal.classList.remove("show"); setTimeout(() => modal.style.display = "none", 300); } }
});
"""

# --- TEMPLATES ---

INDEX_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الموقع الرسمي | تيسير ماجد القيسي</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{ css_content|safe }}</style>
</head>
<body>
    <div id="loader"><div class="spinner"></div></div>
    <nav class="navbar"><div class="container"><a href="#" class="logo"><i class="fas fa-landmark"></i> تيسير ماجد القيسي</a>
        <button class="menu-toggle" aria-label="Toggle navigation"><i class="fas fa-bars"></i></button>
        <ul class="nav-links">
            <li><a href="#home" class="active">الرئيسية</a></li>
            <li><a href="#about">من نحن</a></li>
            <li><a href="#vision">الرؤية والأهداف</a></li>
            <li><a href="#news">الأخبار</a></li>
            <li><a href="#contact" class="btn-primary">تواصل معنا</a></li>
        </ul>
    </div></nav>
    <header id="home" class="hero"><div class="hero-overlay"></div><div class="container hero-content">
        <h2 class="animate-up">عضو مجلس محافظة بغداد</h2>
        <h1 class="animate-up delay-1">تيسير ماجد القيسي</h1>
        <p class="animate-up delay-2">نعمل معاً من أجل بغداد أجمل ومستقبل أفضل لمدينتنا العريقة.</p>
        <div class="hero-buttons animate-up delay-3">
            <a href="#contact" class="btn btn-primary">قدم شكوى / مقترح</a>
            <a href="#about" class="btn btn-outline">تعرف علينا</a>
        </div>
    </div></header>
    <section id="about" class="section"><div class="container">
        <div class="section-header"><h3>من هو</h3><h2>تيسير ماجد القيسي</h2><div class="line"></div></div>
        <div class="about-grid">
            <div class="about-image reveal-right"><img src="{{ url_for('static', filename='img/profile.jpg') }}" class="profile-img"></div>
            <div class="about-text reveal-left">
                <p>عضو في مجلس محافظة بغداد، يسعى لخدمة أهالي العاصمة من خلال طرح المشاريع الخدمية ومراقبة الأداء الحكومي.</p>
                <ul class="features-list">
                    <li><i class="fas fa-check-circle"></i> الشفافية في العمل</li>
                    <li><i class="fas fa-check-circle"></i> النزاهة والإخلاص</li>
                    <li><i class="fas fa-check-circle"></i> خدمة المواطن أولاً</li>
                </ul>
            </div>
        </div>
    </div></section>
    <section id="news" class="section"><div class="container">
        <div class="section-header"><h3>المركز الإعلامي</h3><h2>آخر النشاطات والأخبار</h2><div class="line"></div></div>
        <div class="news-grid">
            {% if activities %}
            {% for activity in activities %}
            <article class="news-item reveal-up" data-title="{{ activity.title }}" data-date="{{ activity.date }}" data-text="{{ activity.text }}"
              data-image="{{ url_for('static', filename=activity.image) if activity.image else '' }}" onclick="openNewsModal(this)">
              <div class="news-img">
                {% if activity.image %}<img src="{{ url_for('static', filename=activity.image) }}">
                {% else %}<div style="height:100%; display:flex; align-items:center; justify-content:center; background:#e2e8f0; color:#94a3b8;"><i class="far fa-newspaper" style="font-size:3rem;"></i></div>{% endif %}
              </div>
              {% if activity.pinned %}<div class="pinned-badge"><i class="fas fa-thumbtack"></i></div>{% endif %}
              <div class="news-overlay"><i class="fas fa-search-plus" style="background:white; padding:20px; border-radius:50%; color:var(--accent-color);"></i></div>
              <div class="news-content-mini"><span class="date">{{ activity.date }}</span><h4>{{ activity.title }}</h4></div>
            </article>
            {% endfor %}
            {% else %}<p style="text-align:center; grid-column:1/-1;">لا توجد نشاطات حالياً.</p>{% endif %}
        </div>
    </div></section>
    <div id="newsModal" class="modal"><div class="modal-content"><span class="close-modal">&times;</span>
        <div class="modal-body"><div class="modal-img-container"><img id="modalImg" style="width:100%; max-height:500px; object-fit:contain;"></div>
            <div class="modal-text-content"><span id="modalDate" class="date"></span><h2 id="modalTitle"></h2><p id="modalText"></p></div>
        </div>
    </div></div>
    <section id="contact" class="section bg-dark"><div class="container"><div class="contact-wrapper reveal-up">
        <div class="contact-info"><h3>معلومات التواصل</h3><div class="info-item"><i class="fas fa-envelope"></i><span>taisirmajidnajm@gmail.com</span></div>
            <div class="info-item"><i class="fas fa-phone"></i><span>07838961231</span></div>
            <div class="social-links"><a href="https://www.facebook.com/taisirmajid" target="_blank"><i class="fab fa-facebook-f"></i></a></div>
        </div>
        <div class="contact-form"><h3>أرسل شكوى أو مقترح</h3><form id="contactForm">
            <div class="form-group"><label>الاسم الكامل</label><input type="text" name="name" required></div>
            <div class="form-group"><label>رقم الهاتف</label><input type="tel" name="phone" required></div>
            <div class="form-group"><label>الرسالة</label><textarea name="message" rows="4" required></textarea></div>
            <button type="submit" class="btn btn-primary btn-block"><span>إرسال</span><i class="fas fa-paper-plane"></i></button>
            <div id="formMessage" class="form-message"></div>
        </form></div>
    </div></div></section>
    <script>{{ js_content|safe }}</script>
</body>
</html>
"""

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><title>تسجيل الدخول</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <style>{{ css_content|safe }}
        body { background: var(--primary-color); display: flex; justify-content: center; align-items: center; height: 100vh; }
        .login-card { background: white; padding: 40px; border-radius: 15px; width: 400px; text-align: center; }
        .form-group { margin-bottom: 20px; text-align: right; }
        .form-group input { background: #f1f5f9; border: 1px solid #cbd5e1; width: 100%; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="login-card"><h2>تسجيل الدخول</h2>
        {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
        <form method="POST">
            <div class="form-group"><label>اسم المستخدم</label><input type="text" name="username" required></div>
            <div class="form-group"><label>كلمة المرور</label><input type="password" name="password" required></div>
            <button type="submit" class="btn btn-primary btn-block">دخول</button>
        </form>
    </div>
</body>
</html>
"""

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><title>لوحة التحكم</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{{ css_content|safe }}
        body { background: #f1f5f9; }
        .admin-header { background: white; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: var(--shadow-sm); }
        .tabs { display: flex; gap: 10px; margin: 20px; }
        .tab-btn { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; background: #e2e8f0; font-weight: 600; }
        .tab-btn.active { background: var(--primary-color); color: white; }
        .tab-content { display: none; padding: 20px; }
        .tab-content.active { display: block; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; }
        th, td { padding: 15px; border-bottom: 1px solid #eee; text-align: right; }
        th { background: #f8fafc; }
        .admin-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); align-items: center; justify-content: center; }
        .admin-modal-content { background: white; padding: 30px; border-radius: 10px; width: 500px; }
    </style>
</head>
<body>
    <header class="admin-header"><div><i class="fas fa-shield-alt"></i> لوحة الإدارة</div><a href="{{ url_for('logout') }}">تسجيل خروج</a></header>
    <div class="tabs">
        <button class="tab-btn active" onclick="openTab(event, 'messages-tab')">الرسائل</button>
        <button class="tab-btn" onclick="openTab(event, 'activities-tab')">النشاطات</button>
    </div>
    <div id="messages-tab" class="tab-content active">
        <table><thead><tr><th>الاسم</th><th>الهاتف</th><th>الرسالة</th></tr></thead>
            <tbody>{% for msg in messages|reverse %}<tr><td>{{ msg.name }}</td><td>{{ msg.phone }}</td><td>{{ msg.message }}</td></tr>{% endfor %}</tbody>
        </table>
    </div>
    <div id="activities-tab" class="tab-content">
        <form id="addForm" enctype="multipart/form-data" style="background:white; padding:20px; border-radius:10px; margin-bottom:20px;">
            <input type="text" name="title" placeholder="العنوان" required style="width:100%; margin-bottom:10px; padding:10px;">
            <input type="date" name="date" required style="width:100%; margin-bottom:10px; padding:10px;">
            <input type="file" name="image" accept="image/*" style="width:100%; margin-bottom:10px; padding:10px;">
            <textarea name="text" placeholder="التفاصيل" rows="4" required style="width:100%; margin-bottom:10px; padding:10px;"></textarea>
            <button type="submit" class="btn btn-primary">نشر</button>
        </form>
        <table><thead><tr><th>العنوان</th><th>التاريخ</th><th>إجراءات</th></tr></thead>
            <tbody>{% for act in activities|reverse %}
            <tr><td>{{ act.title }}</td><td>{{ act.date }}</td>
            <td><button onclick="deleteAct('{{ act.id }}')">حذف</button> <button onclick="togglePin('{{ act.id }}')">{{ 'إلغاء تثبيت' if act.pinned else 'تثبيت' }}</button></td></tr>
            {% endfor %}</tbody>
        </table>
    </div>
    <script>
        function openTab(e, t) {
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(t).classList.add('active');
            e.target.classList.add('active');
        }
        document.getElementById('addForm').onsubmit = async (e) => {
            e.preventDefault();
            await fetch('/admin/add_activity', { method: 'POST', body: new FormData(e.target) });
            location.reload();
        };
        async function deleteAct(id) { if(confirm('حذف؟')) { await fetch('/admin/delete_activity/'+id, {method:'POST'}); location.reload(); } }
        async function togglePin(id) { await fetch('/admin/pin_activity/'+id, {method:'POST'}); location.reload(); }
    </script>
</body>
</html>
"""

# --- LOGIC ---

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f: return json.load(f)
        except: return []
    return []

def save_data(file_path, data):
    existing = load_data(file_path)
    existing.append(data)
    with open(file_path, 'w', encoding='utf-8') as f: json.dump(existing, f, ensure_ascii=False, indent=2)

def save_all_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=2)

def allowed_file(filename): return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    activities = load_data(ACTIVITIES_FILE)
    activities.sort(key=lambda x: (not x.get('pinned', False), x.get('date', '')), reverse=True)
    return render_template_string(INDEX_HTML, activities=activities, css_content=CSS_CONTENT, js_content=JS_CONTENT)

@app.route('/contact', methods=['POST'])
def contact():
    data = request.form.to_dict()
    save_data(MESSAGES_FILE, data)
    return jsonify({'status': 'success', 'message': 'تم استلام رسالتك، شكراً'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return render_template_string(LOGIN_HTML, error='خطأ في الدخول', css_content=CSS_CONTENT)
    return render_template_string(LOGIN_HTML, css_content=CSS_CONTENT)

@app.route('/admin')
def admin():
    if not session.get('logged_in'): return redirect(url_for('login'))
    return render_template_string(ADMIN_HTML, messages=load_data(MESSAGES_FILE), activities=load_data(ACTIVITIES_FILE), css_content=CSS_CONTENT)

@app.route('/admin/add_activity', methods=['POST'])
def add_activity():
    if not session.get('logged_in'): return jsonify({'status': 'error'}), 401
    title, date, text = request.form.get('title'), request.form.get('date'), request.form.get('text')
    file = request.files.get('image')
    img_path = ''
    if file and allowed_file(file.filename):
        fname = secure_filename(file.filename)
        uname = str(uuid.uuid4()) + "_" + fname
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], uname))
        img_path = f"img/news/{uname}"
    activity = {'id': str(uuid.uuid4()), 'title': title, 'date': date, 'text': text, 'image': img_path, 'pinned': False}
    save_data(ACTIVITIES_FILE, activity)
    return jsonify({'status': 'success'})

@app.route('/admin/delete_activity/<aid>', methods=['POST'])
def delete_activity(aid):
    if not session.get('logged_in'): return jsonify({'status': 'error'}), 401
    acts = load_data(ACTIVITIES_FILE)
    save_all_data(ACTIVITIES_FILE, [a for a in acts if a['id'] != aid])
    return jsonify({'status': 'success'})

@app.route('/admin/pin_activity/<aid>', methods=['POST'])
def pin_activity(aid):
    if not session.get('logged_in'): return jsonify({'status': 'error'}), 401
    acts = load_data(ACTIVITIES_FILE)
    for a in acts:
        if a['id'] == aid: a['pinned'] = not a.get('pinned', False)
    save_all_data(ACTIVITIES_FILE, acts)
    return jsonify({'status': 'success'})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
