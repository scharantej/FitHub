
## Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename  # For secure file handling
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3  # For database operations

## Define the Flask application
app = Flask(__name__)

## Database configuration
app.config['SECRET_KEY'] = 'secret_key'  # Secret key for session management
app.config['DATABASE'] = 'sports_channel.db'  # Database file name

## Connect to the database
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # Convert rows to dictionaries
    return conn

## Main page route
@app.route('/')
def index():
    """Main page of the website"""
    return render_template('index.html')

## Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration page"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='sha256')
        profile_pic = request.files['profile_pic']
        if profile_pic and allowed_file(profile_pic.filename):
            # Securely save file to uploads folder
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_pic_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            profile_pic_path = None
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password, profile_pic) VALUES (?, ?, ?, ?)',
                       (username, email, password, profile_pic_path))
        conn.commit()
        cursor.close()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('signup.html')

## Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        cursor.close()
        if not user or not check_password_hash(user['password'], password):
            flash('Invalid credentials!')
            return redirect(url_for('login'))
        session['user_id'] = user['user_id']
        flash('Login successful!')
        return redirect(url_for('profile'))
    return render_template('login.html')

## Profile route
@app.route('/profile')
def profile():
    """User profile page"""
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    cursor.close()
    return render_template('profile.html', user=user)

## Video upload route
@app.route('/video_upload', methods=['GET', 'POST'])
def video_upload():
    """Video upload page"""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        tags = request.form.getlist('tags')
        category = request.form['category']
        video = request.files['video']
        if video and allowed_file(video.filename):
            # Securely save video to uploads folder
            filename = secure_filename(video.filename)
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            video_path = None
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO videos (title, description, tags, category, video_path) VALUES (?, ?, ?, ?, ?)',
                       (title, description, ', '.join(tags), category, video_path))
        conn.commit()
        cursor.close()
        flash('Video uploaded successfully!')
        return redirect(url_for('videos'))
    return render_template('video_upload.html')

## Videos page route
@app.route('/videos')
def videos():
    """Page to view all videos"""
    conn = get_db_connection()
    cursor = conn.cursor()
    videos = cursor.execute('SELECT * FROM videos').fetchall()
    cursor.close()
    return render_template('videos.html', videos=videos)

## Video details route
@app.route('/video/<video_id>')
def video_details(video_id):
    """Page to view specific video details"""
    conn = get_db_connection()
    cursor = conn.cursor()
    video = cursor.execute('SELECT * FROM videos WHERE video_id = ?', (video_id,)).fetchone()
    cursor.close()
    return render_template('video_details.html', video=video)

## Search route
@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search for videos"""
    if request.method == 'POST':
        search_query = request.form['search_query']
        conn = get_db_connection()
        cursor = conn.cursor()
        videos = cursor.execute('SELECT * FROM videos WHERE title LIKE ? OR description LIKE ?', ('%' + search_query + '%',
                                                                                               '%' + search_query + '%')).fetchall()
        cursor.close()
        return render_template('search.html', videos=videos)
    return render_template('search.html')

## Run the application
if __name__ == '__main__':
    app.run(debug=True)
