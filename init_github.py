#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to initialize Git repository and push to GitHub
"""

import os
import sys
from pathlib import Path
from git import Repo, GitCommandError

def setup_git_repo():
    """Setup Git repository and push to GitHub"""
    
    repo_path = Path(__file__).parent
    os.chdir(repo_path)
    
    print("\n" + "="*60)
    print("🚀 GitHub Repository Setup")
    print("="*60 + "\n")
    
    # اسم المستخدم واسم المستودع
    github_username = "alqesr34"  # اسمك على GitHub
    repo_name = "taisir-majid-website"
    
    print(f"📁 المشروع: {repo_path}")
    print(f"👤 المستخدم: {github_username}")
    print(f"📦 المستودع: {repo_name}")
    print()
    
    try:
        # 1. إنشاء مستودع Git
        print("1️⃣  جاري إنشاء مستودع Git محلي...")
        try:
            repo = Repo(repo_path)
            print("   ✓ المستودع موجود بالفعل")
        except:
            repo = Repo.init(repo_path)
            print("   ✓ تم إنشاء المستودع الجديد")
        
        # 2. إضافة جميع الملفات
        print("2️⃣  جاري إضافة جميع الملفات...")
        repo.git.add(['-A'])
        print("   ✓ تمت إضافة الملفات")
        
        # 3. التحقق من وجود ملفات للالتزام
        if repo.is_dirty(untracked_files=True):
            print("3️⃣  جاري إنشاء التزام أول...")
            repo.index.commit("Initial commit: Add website project")
            print("   ✓ تم الالتزام")
        else:
            print("3️⃣  لا توجد تغييرات للالتزام بها")
        
        # 4. إضافة المستودع البعيد
        print("4️⃣  جاري إضافة المستودع البعيد...")
        remote_url = f"https://github.com/{github_username}/{repo_name}.git"
        
        try:
            # محاولة التحقق من وجود remote
            if 'origin' in repo.remotes:
                print("   ⓘ Remote موجود بالفعل")
                # تحديث الـ URL
                repo.remote('origin').set_url(remote_url)
            else:
                repo.create_remote('origin', remote_url)
            print(f"   ✓ Remote: {remote_url}")
        except Exception as e:
            print(f"   ⚠ تحذير: {e}")
        
        # 5. إعادة تسمية الفرع
        print("5️⃣  جاري إعادة تسمية الفرع إلى main...")
        try:
            repo.active_branch.rename('main')
            print("   ✓ تم إعادة التسمية")
        except:
            print("   ⓘ الفرع main موجود بالفعل")
        
        # 6. الدفع (Push)
        print("6️⃣  جاري دفع المشروع إلى GitHub...")
        print("   ⚠️  قد تحتاج إلى إدخال بيانات الاعتماد...")
        
        try:
            # محاولة الدفع
            origin = repo.remote('origin')
            origin.push(refspec='main:main', force=True)
            print("   ✓ تم الدفع بنجاح!")
        except GitCommandError as e:
            print(f"   ⚠️  خطأ في الدفع: {e}")
            print("\n   💡 الحل:")
            print(f"   يرجى التحقق من:")
            print(f"   1. وجود المستودع على GitHub: https://github.com/{github_username}/{repo_name}")
            print(f"   2. صحة بيانات الاعتماد")
            print(f"   3. أن المستودع ليس خاصاً بدون إذن الدفع")
            raise
        
        print("\n" + "="*60)
        print("✅ تم بنجاح!")
        print("="*60)
        print(f"\n📍 رابط المستودع:")
        print(f"   🔗 https://github.com/{github_username}/{repo_name}")
        print(f"\n🚀 الخطوة التالية:")
        print(f"   اذهب إلى: https://railway.app")
        print(f"   واختر 'Deploy from GitHub'")
        print(f"   ثم اختر هذا المستودع")
        print("\n" + "="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        print("\n💡 تلميح:")
        print("   تأكد من:")
        print("   1. إنشاء المستودع على: https://github.com/new")
        print("   2. اسم المستودع: taisir-majid-website")
        print("   3. ترك خيار 'Initialize with README' غير محدد")
        print("   4. اسم المستخدم صحيح\n")
        return False

if __name__ == '__main__':
    success = setup_git_repo()
    sys.exit(0 if success else 1)
