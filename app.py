from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pbs_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    cnic = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    whatsapp = db.Column(db.String(15), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    mailing_address = db.Column(db.Text)
    nationality = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    data_requests = db.relationship('DataRequest', backref='user', lazy=True)

class DataRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dataset_name = db.Column(db.String(200), nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    pbs_section = db.Column(db.String(100), nullable=False)
    data_format = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requested_date = db.Column(db.Date, nullable=False)
    urgency_level = db.Column(db.String(20), nullable=False)
    deadline = db.Column(db.Date)
    comments = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')
    priority = db.Column(db.String(20), default='Medium')
    payment_status = db.Column(db.String(20), default='Unpaid')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    format = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(500))
    download_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    organization = db.Column(db.String(100))
    user_type = db.Column(db.String(50), nullable=False)
    feedback_type = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20))
    overall_rating = db.Column(db.Integer, nullable=False)
    usability_rating = db.Column(db.Integer)
    data_quality_rating = db.Column(db.Integer)
    subject = db.Column(db.String(200), nullable=False)
    feedback_message = db.Column(db.Text, nullable=False)
    suggestions = db.Column(db.Text)
    data_sets_used = db.Column(db.String(200))
    frequency_of_use = db.Column(db.String(50))
    contact_preference = db.Column(db.String(10), default='no')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    datasets = Dataset.query.filter_by(is_active=True).limit(6).all()
    return render_template('home.html', datasets=datasets)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        cnic = request.form.get('cnic')
        phone = request.form.get('phone')
        whatsapp = request.form.get('whatsapp')
        department = request.form.get('department')
        city = request.form.get('city')
        district = request.form.get('district')
        province = request.form.get('province')
        mailing_address = request.form.get('mailing_address')
        nationality = request.form.get('nationality')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            cnic=cnic,
            phone=phone,
            whatsapp=whatsapp,
            department=department,
            city=city,
            district=district,
            province=province,
            mailing_address=mailing_address,
            nationality=nationality
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    user_requests = DataRequest.query.filter_by(user_id=current_user.id).order_by(DataRequest.created_at.desc()).all()
    return render_template('dashboard.html', requests=user_requests)

@app.route('/request-data', methods=['GET', 'POST'])
@login_required
def request_data():
    if request.method == 'POST':
        dataset_name = request.form.get('dataset_name')
        purpose = request.form.get('purpose')
        pbs_section = request.form.get('pbs_section')
        data_format = request.form.get('data_format')
        description = request.form.get('description')
        requested_date = datetime.strptime(request.form.get('requested_date'), '%Y-%m-%d').date()
        urgency_level = request.form.get('urgency_level')
        deadline_str = request.form.get('deadline')
        comments = request.form.get('comments')
        
        deadline = None
        if deadline_str:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        
        # Set priority based on urgency
        priority_map = {'High': 'High', 'Medium': 'Medium', 'Low': 'Low'}
        priority = priority_map.get(urgency_level, 'Medium')
        
        data_request = DataRequest(
            user_id=current_user.id,
            dataset_name=dataset_name,
            purpose=purpose,
            pbs_section=pbs_section,
            data_format=data_format,
            description=description,
            requested_date=requested_date,
            urgency_level=urgency_level,
            deadline=deadline,
            comments=comments,
            priority=priority
        )
        
        db.session.add(data_request)
        db.session.commit()
        
        flash('Data request submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('request_data.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    requests = DataRequest.query.order_by(DataRequest.created_at.desc()).all()
    return render_template('admin_dashboard.html', requests=requests)

@app.route('/admin/update-request/<int:request_id>', methods=['POST'])
@login_required
def update_request(request_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    data_request = DataRequest.query.get_or_404(request_id)
    data_request.status = request.form.get('status')
    data_request.payment_status = request.form.get('payment_status')
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/open-data')
def open_data():
    datasets = Dataset.query.filter_by(is_active=True).all()
    return render_template('open_data.html', datasets=datasets)

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        try:
            feedback = Feedback(
                name=request.form.get('name'),
                email=request.form.get('email'),
                organization=request.form.get('organization'),
                user_type=request.form.get('user_type'),
                feedback_type=request.form.get('feedback_type'),
                priority=request.form.get('priority'),
                overall_rating=int(request.form.get('overall_rating')),
                usability_rating=int(request.form.get('usability_rating')) if request.form.get('usability_rating') else None,
                data_quality_rating=int(request.form.get('data_quality_rating')) if request.form.get('data_quality_rating') else None,
                subject=request.form.get('subject'),
                feedback_message=request.form.get('feedback_message'),
                suggestions=request.form.get('suggestions'),
                data_sets_used=request.form.get('data_sets_used'),
                frequency_of_use=request.form.get('frequency_of_use'),
                contact_preference=request.form.get('contact_preference', 'no')
            )
            db.session.add(feedback)
            db.session.commit()
            flash('Thank you for your feedback! We appreciate your input.', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('An error occurred while submitting feedback. Please try again.', 'error')
            db.session.rollback()
    
    return render_template('feedback.html')

@app.route('/api/datasets')
def api_datasets():
    datasets = Dataset.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'description': d.description,
        'category': d.category,
        'format': d.format,
        'download_count': d.download_count
    } for d in datasets])

@app.route('/api/datasets/<int:dataset_id>')
def api_dataset(dataset_id):
    dataset = Dataset.query.get_or_404(dataset_id)
    return jsonify({
        'id': dataset.id,
        'name': dataset.name,
        'description': dataset.description,
        'category': dataset.category,
        'format': dataset.format,
        'download_count': dataset.download_count,
        'files': [
            {
                'name': f"{dataset.name.replace(' ', '_')}.{dataset.format.lower()}",
                'type': dataset.format,
                'icon': f"fas fa-file-{get_file_icon(dataset.format)}"
            }
        ],
        'metadata': {
            'Source': f"https://www.pbs.gov.pk/{dataset.name.lower().replace(' ', '-')}",
            'Author': 'Pakistan Bureau of Statistics',
            'Last Updated': dataset.created_at.strftime('%B %d, %Y, %I:%M %p (UTC+05:00)'),
            'Created': dataset.created_at.strftime('%B %d, %Y, %I:%M %p (UTC+05:00)'),
            'Publisher': 'Pakistan Bureau of Statistics',
            'Data Type': 'non-geospatial',
            'Data Source': 'Primary Research',
            'Organization Type': 'Federal government',
            'Category': dataset.category
        }
    })

def get_file_icon(format_type):
    icon_map = {
        'CSV': 'csv',
        'Excel': 'excel',
        'PDF': 'pdf',
        'JSON': 'code',
        'Multiple': 'archive'
    }
    return icon_map.get(format_type, 'file')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(email='admin@pbs.gov.pk').first()
        if not admin:
            admin = User(
                name='Admin User',
                email='admin@pbs.gov.pk',
                password_hash=generate_password_hash('admin123'),
                cnic='12345-1234567-1',
                phone='+92XXXXXXXXX',
                whatsapp='+92XXXXXXXXX',
                department='IT Department',
                city='Islamabad',
                district='Islamabad',
                province='Federal',
                nationality='Pakistani',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
        
        # Add sample datasets
        existing_count = Dataset.query.count()
        if existing_count < 30:  # Only add if we have less than 30 datasets
            sample_datasets = [
                Dataset(
                    name='PSLM / HIES 2018-19 (Provincial Level Survey)', 
                    description='Pakistan Social and Living Standards Measurements (PSLM), 2018-19 is the eleventh round of a series of surveys, initiated in 2004. Current round of PSLM (Social & Household Integrated Economic Survey (HIES)) at provincial level survey covered 24809 households and provide detailed outcome indicators on Education, Health, Population Welfare, Housing, Water Sanitation & Hygiene, Information Communication & Technology (ICT), Food Insecurity Experience Scale (FIES) and Income & Expenditure.', 
                    category='Demographics', 
                    format='Multiple',
                    download_count=random.randint(5000, 25000)
                ),
                Dataset(
                    name='Basic Health Indicators, Pakistan and Other Countries of Region', 
                    description='Basic Health Indicators, Pakistan and Other Countries of Region', 
                    category='Health', 
                    format='Excel',
                    download_count=random.randint(3000, 15000)
                ),
                Dataset(name='Population Census', description='Complete population data from census', category='Demographics', format='CSV', download_count=random.randint(8000, 30000)),
                Dataset(name='Agriculture Survey', description='Agricultural production and land use data', category='Agriculture', format='Excel', download_count=random.randint(2000, 12000)),
                Dataset(name='Labour Force Survey', description='Employment and unemployment statistics', category='Labour', format='PDF', download_count=random.randint(4000, 18000)),
                Dataset(name='Economic Indicators', description='GDP, inflation, and economic growth data', category='Economics', format='JSON', download_count=random.randint(6000, 22000)),
                Dataset(name='Education Statistics', description='School enrollment and literacy rates', category='Education', format='CSV', download_count=random.randint(3000, 15000)),
                Dataset(name='Health Statistics', description='Healthcare facilities and disease statistics', category='Health', format='Excel', download_count=random.randint(2500, 12000)),
                # Additional datasets for realistic count
                Dataset(name='Industrial Production Index', description='Monthly industrial production data', category='Economics', format='Excel', download_count=random.randint(1500, 8000)),
                Dataset(name='Consumer Price Index', description='Monthly inflation and price data', category='Economics', format='CSV', download_count=random.randint(5000, 20000)),
                Dataset(name='Foreign Trade Statistics', description='Import and export data', category='Economics', format='Excel', download_count=random.randint(2000, 10000)),
                Dataset(name='Transport Statistics', description='Transportation and infrastructure data', category='Economics', format='PDF', download_count=random.randint(1000, 6000)),
                Dataset(name='Energy Statistics', description='Energy production and consumption data', category='Economics', format='Excel', download_count=random.randint(1500, 9000)),
                Dataset(name='Tourism Statistics', description='Tourism and travel data', category='Economics', format='CSV', download_count=random.randint(800, 5000)),
                Dataset(name='Housing Census', description='Housing and construction data', category='Demographics', format='PDF', download_count=random.randint(3000, 14000)),
                Dataset(name='Vital Statistics', description='Birth, death, and marriage data', category='Demographics', format='Excel', download_count=random.randint(2000, 10000)),
                Dataset(name='Migration Statistics', description='Internal and external migration data', category='Demographics', format='CSV', download_count=random.randint(1500, 8000)),
                Dataset(name='Urban Development Statistics', description='Urban planning and development data', category='Demographics', format='Excel', download_count=random.randint(1000, 6000)),
                Dataset(name='Rural Development Statistics', description='Rural development and agriculture data', category='Agriculture', format='PDF', download_count=random.randint(1200, 7000)),
                Dataset(name='Crop Production Statistics', description='Agricultural crop production data', category='Agriculture', format='Excel', download_count=random.randint(3000, 15000)),
                Dataset(name='Livestock Statistics', description='Livestock and animal husbandry data', category='Agriculture', format='CSV', download_count=random.randint(2000, 10000)),
                Dataset(name='Fisheries Statistics', description='Fisheries and aquaculture data', category='Agriculture', format='Excel', download_count=random.randint(800, 5000)),
                Dataset(name='Forestry Statistics', description='Forestry and natural resources data', category='Agriculture', format='PDF', download_count=random.randint(600, 4000)),
                Dataset(name='Employment Statistics', description='Employment and job market data', category='Labour', format='Excel', download_count=random.randint(4000, 18000)),
                Dataset(name='Wage Statistics', description='Wage and salary data', category='Labour', format='CSV', download_count=random.randint(2500, 12000)),
                Dataset(name='Occupational Statistics', description='Occupational and skill data', category='Labour', format='PDF', download_count=random.randint(1500, 8000)),
                Dataset(name='Workplace Statistics', description='Workplace safety and conditions data', category='Labour', format='Excel', download_count=random.randint(1000, 6000)),
                Dataset(name='Primary Education Statistics', description='Primary school enrollment and performance data', category='Education', format='CSV', download_count=random.randint(3000, 15000)),
                Dataset(name='Secondary Education Statistics', description='Secondary school enrollment and performance data', category='Education', format='Excel', download_count=random.randint(2500, 12000)),
                Dataset(name='Higher Education Statistics', description='University and college enrollment data', category='Education', format='PDF', download_count=random.randint(2000, 10000)),
                Dataset(name='Literacy Statistics', description='Literacy rates and educational attainment data', category='Education', format='Excel', download_count=random.randint(1500, 8000)),
                Dataset(name='Hospital Statistics', description='Hospital and healthcare facility data', category='Health', format='CSV', download_count=random.randint(2000, 10000)),
                Dataset(name='Disease Statistics', description='Disease prevalence and health indicators data', category='Health', format='Excel', download_count=random.randint(3000, 15000)),
                Dataset(name='Pharmaceutical Statistics', description='Pharmaceutical and medicine data', category='Health', format='PDF', download_count=random.randint(1500, 8000)),
                Dataset(name='Mental Health Statistics', description='Mental health and psychological data', category='Health', format='Excel', download_count=random.randint(1000, 6000))
            ]
            for dataset in sample_datasets:
                db.session.add(dataset)
            db.session.commit()
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 