# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.utils import secure_filename
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# import secrets
# import numpy as np
# from PIL import Image
# from datetime import datetime
# import csv
# from pathlib import Path
# import logging

# # PyTorch & model imports
# import torch
# from efficientnet_pytorch import EfficientNet
# import torchvision.transforms as transforms

# # Flask setup
# app = Flask(__name__)
# logging.basicConfig(level=logging.DEBUG)
# app.config['UPLOAD_FOLDER'] = 'static/uploads/'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# app.config['SECRET_KEY'] = secrets.token_hex(16)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # CSV paths
# USERS_CSV = 'data/users.csv'
# FEEDBACK_CSV = 'data/feedback.csv'
# Path('data').mkdir(exist_ok=True)
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# # Init CSVs
# def init_csv_files():
#     if not os.path.exists(USERS_CSV):
#         with open(USERS_CSV, 'w', newline='') as f:
#             csv.writer(f).writerow(['id', 'username', 'email', 'password', 'timestamp'])
#     if not os.path.exists(FEEDBACK_CSV):
#         with open(FEEDBACK_CSV, 'w', newline='') as f:
#             csv.writer(f).writerow(['id', 'username', 'message', 'timestamp'])

# init_csv_files()

# # DB setup
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

# class DetectionResult(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
#     image_path = db.Column(db.String(255), nullable=False)
#     prediction = db.Column(db.String(50), nullable=False)
#     confidence = db.Column(db.Float, nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

# class Feedback(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
#     message = db.Column(db.Text, nullable=False)

# with app.app_context():
#     try:
#         db.drop_all()
#         db.create_all()
#         app.logger.debug("Database tables created successfully!")
#     except Exception as e:
#         app.logger.error("Error creating database tables: %s", str(e))
#         raise RuntimeError("Error creating database tables: " + str(e))

# @app.context_processor
# def inject_logged_in():
#     return dict(logged_in='username' in session)

# # ✅ Load PyTorch model at startup
# MODEL_PATH = r'C:\Users\rohit\Downloads\Mini Project\eye_disease_model.pth'
# DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# CLASSES = ['cataract', 'DR', 'glaucoma', 'normal']

# if not os.path.exists(MODEL_PATH):
#     raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

# try:
#     model = EfficientNet.from_name('efficientnet-b3')
#     model._fc = torch.nn.Linear(model._fc.in_features, len(CLASSES))
#     checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)
#     model.load_state_dict(checkpoint['model_state_dict'])
#     model.to(DEVICE)
#     model.eval()
# except Exception as e:
#     app.logger.error("Error loading model: %s", str(e))
#     raise RuntimeError("Error loading model: " + str(e))

# transform = transforms.Compose([
#     transforms.Resize((300, 300)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406],
#                          [0.229, 0.224, 0.225])
# ])

# # Routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if 'username' not in session:
#         flash('Please login to upload images', 'error')
#         return redirect(url_for('login'))
    
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part', 'error')
#             return redirect(request.url)
        
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file', 'error')
#             return redirect(request.url)
        
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
            
#             # ✅ Predict using model with error handling
#             try:
#                 image = Image.open(filepath).convert('RGB')
#                 input_tensor = transform(image).unsqueeze(0).to(DEVICE)
#                 with torch.no_grad():
#                     output = model(input_tensor)
#                     probs = torch.nn.functional.softmax(output, dim=1)
#                     confidence, predicted_idx = torch.max(probs, 1)
#                     result = CLASSES[predicted_idx.item()]
#                     confidence = confidence.item()
#             except Exception as e:
#                 app.logger.error("Model prediction error: %s", str(e))
#                 flash("Error processing the image: " + str(e), "error")
#                 return redirect(url_for('upload_file'))
            
#             # ✅ Save result to database with error handling
#             try:
#                 new_result = DetectionResult(
#                     username=session['username'],
#                     image_path=filepath,
#                     prediction=result,
#                     confidence=confidence
#                 )
#                 db.session.add(new_result)
#                 db.session.commit()
#             except Exception as e:
#                 app.logger.error("Database error on saving detection result: %s", str(e))
#                 flash("Error saving detection result: " + str(e), "error")
#                 return redirect(url_for('upload_file'))
            
#             return render_template('results.html', 
#                                    result=result,
#                                    confidence=round(confidence * 100, 2),
#                                    image_path=filepath)
    
#     return render_template('upload.html')

# @app.route('/feedback', methods=['GET', 'POST'])
# def feedback():
#     if request.method == 'POST':
#         feedback_value = request.form.get('message')  
#         if feedback_value:
#             if 'username' in session:
#                 try:
#                     os.makedirs('data', exist_ok=True)
#                     next_id = 0
#                     if os.path.exists(FEEDBACK_CSV):
#                         with open(FEEDBACK_CSV, 'r', newline='') as f:
#                             next_id = sum(1 for row in csv.reader(f))
#                     with open(FEEDBACK_CSV, 'a', newline='') as f:
#                         csv.writer(f).writerow([
#                             next_id,
#                             session['username'],
#                             feedback_value,
#                             datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                         ])
#                     new_feedback = Feedback(
#                         username=session['username'],
#                         message=feedback_value
#                     )
#                     db.session.add(new_feedback)
#                     db.session.commit()
#                     flash('Thank you for your feedback!', 'success')
#                     return redirect(url_for('index'))
#                 except Exception as e:
#                     app.logger.error("Error saving feedback: %s", str(e))
#                     flash('Error saving feedback. Please try again.', 'error')
#             else:
#                 flash('Please login to submit feedback', 'error')
#         else:
#             flash('Please provide feedback', 'error')
#     return render_template('feedback.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username and password:
#             session['username'] = username
#             flash('Successfully logged in!', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash('Invalid username or password', 'error')
#     return render_template('login.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         if username and password and email:
#             with open(USERS_CSV, 'a', newline='') as f:
#                 csv.writer(f).writerow([
#                     len(open(USERS_CSV).readlines()),
#                     username,
#                     email,
#                     generate_password_hash(password),
#                     datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                 ])
#             flash('Registration successful! Please login.', 'success')
#             return redirect(url_for('login'))
#         else:
#             flash('Please fill in all fields', 'error')
#     return render_template('register.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     flash('You have been logged out', 'info')
#     return redirect(url_for('index'))

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

# if __name__ == '__main__':
#     try:
#         app.run(debug=True, host='0.0.0.0', port=5000)
#     except Exception as e:
#         app.logger.error("Error running the app: %s", str(e))
#         raise



#----------------------------------------------------------------------------------------------------------------------------------


from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
import numpy as np
from PIL import Image
from datetime import datetime
import csv
from pathlib import Path
import logging

# PyTorch & model imports
import torch
from efficientnet_pytorch import EfficientNet
import torchvision.transforms as transforms

# Flask setup
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CSV paths
USERS_CSV = 'data/users.csv'
FEEDBACK_CSV = 'data/feedback.csv'
Path('data').mkdir(exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Init CSVs
def init_csv_files():
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, 'w', newline='') as f:
            csv.writer(f).writerow(['id', 'username', 'email', 'password', 'timestamp'])
    if not os.path.exists(FEEDBACK_CSV):
        with open(FEEDBACK_CSV, 'w', newline='') as f:
            csv.writer(f).writerow(['id', 'username', 'message', 'timestamp'])

init_csv_files()

# DB setup
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class DetectionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    prediction = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    message = db.Column(db.Text, nullable=False)

with app.app_context():
    try:
        db.drop_all()
        db.create_all()
        app.logger.debug("Database tables created successfully!")
    except Exception as e:
        app.logger.error("Error creating database tables: %s", str(e))
        raise RuntimeError("Error creating database tables: " + str(e))

@app.context_processor
def inject_logged_in():
    return dict(logged_in='username' in session)

# Load PyTorch model at startup
MODEL_PATH = r'C:\Users\rohit\Downloads\Mini Project\eye_disease_model.pth'
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CLASSES = ['cataract', 'DR', 'glaucoma', 'normal']

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

try:
    model = EfficientNet.from_name('efficientnet-b3')
    model._fc = torch.nn.Linear(model._fc.in_features, len(CLASSES))
    checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(DEVICE)
    model.eval()
except Exception as e:
    app.logger.error("Error loading model: %s", str(e))
    raise RuntimeError("Error loading model: " + str(e))

transform = transforms.Compose([
    transforms.Resize((300, 300)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'username' not in session:
        flash('Please login to upload images', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                image = Image.open(filepath).convert('RGB')
                input_tensor = transform(image).unsqueeze(0).to(DEVICE)
                with torch.no_grad():
                    output = model(input_tensor)
                    probs = torch.nn.functional.softmax(output, dim=1)
                    confidence, predicted_idx = torch.max(probs, 1)
                    result = CLASSES[predicted_idx.item()]
                    confidence = confidence.item()
            except Exception as e:
                app.logger.error("Model prediction error: %s", str(e))
                flash("Error processing the image: " + str(e), "error")
                return redirect(url_for('upload_file'))

            try:
                new_result = DetectionResult(
                    username=session['username'],
                    image_path=filepath,
                    prediction=result,
                    confidence=confidence
                )
                db.session.add(new_result)
                db.session.commit()
            except Exception as e:
                app.logger.error("Database error on saving detection result: %s", str(e))
                flash("Error saving detection result: " + str(e), "error")
                return redirect(url_for('upload_file'))

            image_filename = os.path.basename(filepath)
            return render_template("results.html", 
                                   image_filename=image_filename,
                                   result=result,
                                   confidence=round(confidence * 100, 2))

    return render_template('upload.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_value = request.form.get('message')
        if feedback_value:
            if 'username' in session:
                try:
                    os.makedirs('data', exist_ok=True)
                    next_id = 0
                    if os.path.exists(FEEDBACK_CSV):
                        with open(FEEDBACK_CSV, 'r', newline='') as f:
                            next_id = sum(1 for row in csv.reader(f))
                    with open(FEEDBACK_CSV, 'a', newline='') as f:
                        csv.writer(f).writerow([
                            next_id,
                            session['username'],
                            feedback_value,
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        ])
                    new_feedback = Feedback(
                        username=session['username'],
                        message=feedback_value
                    )
                    db.session.add(new_feedback)
                    db.session.commit()
                    flash('Thank you for your feedback!', 'success')
                    return redirect(url_for('index'))
                except Exception as e:
                    app.logger.error("Error saving feedback: %s", str(e))
                    flash('Error saving feedback. Please try again.', 'error')
            else:
                flash('Please login to submit feedback', 'error')
        else:
            flash('Please provide feedback', 'error')
    return render_template('feedback.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            session['username'] = username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username and password and email:
            with open(USERS_CSV, 'a', newline='') as f:
                csv.writer(f).writerow([
                    len(open(USERS_CSV).readlines()),
                    username,
                    email,
                    generate_password_hash(password),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ])
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Please fill in all fields', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        app.logger.error("Error running the app: %s", str(e))
        raise