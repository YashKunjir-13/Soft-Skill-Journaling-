import sqlite3
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask import Flask

# Initialize Flask and Bcrypt for password hashing
app = Flask(__name__)
app.secret_key = 'test-secret-key'
bcrypt = Bcrypt(app)

DATABASE = 'database.db'

def get_db():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def insert_test_data():
    """Insert test data into the database"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create a test user
    test_email = 'test@example.com'
    test_password = 'testpass123'
    test_name = 'Test User'
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(test_password).decode('utf-8')
    
    try:
        # Insert test user
        cursor.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (test_name, test_email, hashed_password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        print(f"✓ Created test user: {test_email} (ID: {user_id})")
    except sqlite3.IntegrityError:
        # User already exists, get their ID
        cursor.execute('SELECT id FROM users WHERE email = ?', (test_email,))
        user_id = cursor.fetchone()[0]
        print(f"✓ Test user already exists (ID: {user_id})")
    
    # Insert 15 daily entries over the past 30 days with various moods
    moods = ['Happy', 'Sad', 'Neutral', 'Excited', 'Calm']
    skills = [
        'Communication, Leadership',
        'Problem Solving, Teamwork',
        'Time Management',
        'Critical Thinking, Adaptability',
        'Creativity, Innovation',
        'Attention to Detail',
        'Collaboration',
        'Decision Making',
    ]
    
    print("\n📝 Inserting Daily Entries:")
    for i in range(15):
        days_ago = i * 2  # Every other day for past 30 days
        entry_date = datetime.now() - timedelta(days=days_ago)
        mood = moods[i % len(moods)]
        skills_text = skills[i % len(skills)]
        content = f"Day {i+1}: Today I worked on important tasks. I focused on {skills_text.lower()} and feel {mood.lower()}."
        
        try:
            cursor.execute(
                'INSERT INTO entries (user_id, content, mood, skills, created_at) VALUES (?, ?, ?, ?, ?)',
                (user_id, content, mood, skills_text, entry_date.isoformat())
            )
            print(f"  ✓ Entry {i+1}: {entry_date.strftime('%Y-%m-%d')} - Mood: {mood}")
        except Exception as e:
            print(f"  ✗ Error inserting entry {i+1}: {e}")
    
    conn.commit()
    
    # Insert 8 weekly entries over the past 8 weeks
    print("\n📊 Inserting Weekly Entries:")
    weekly_summaries = [
        "Great week! Made significant progress on team projects and improved communication skills.",
        "Challenging week but learned a lot about problem-solving and resilience.",
        "Productive week focused on developing leadership qualities and mentoring junior team members.",
        "Good week with focus on time management and meeting deadlines.",
        "Excellent week of collaboration and achieving team goals.",
        "Week with mixed results but valuable lessons in adaptability.",
        "Strong week focused on innovation and creative problem-solving.",
        "Great week concluding with successful project delivery and team recognition.",
    ]
    
    for i in range(8):
        weeks_ago = i * 7  # Each week
        entry_date = datetime.now() - timedelta(days=weeks_ago)
        score = (8 - i) % 10 + 1  # Scores from 1-10, varying pattern
        summary = weekly_summaries[i]
        
        try:
            cursor.execute(
                'INSERT INTO weekly_entries (user_id, summary, score, created_at) VALUES (?, ?, ?, ?)',
                (user_id, summary, score, entry_date.isoformat())
            )
            print(f"  ✓ Week {i+1}: {entry_date.strftime('%Y-%m-%d')} - Score: {score}/10")
        except Exception as e:
            print(f"  ✗ Error inserting weekly entry {i+1}: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Test data inserted successfully!")
    print(f"\nYou can now login with:")
    print(f"  Email: {test_email}")
    print(f"  Password: {test_password}")

if __name__ == '__main__':
    insert_test_data()
