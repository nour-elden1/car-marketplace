from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
from datetime import datetime
from config import Config

# =====================
# Flask App Initialization
# =====================
app = Flask(__name__)
app.config.from_object(Config)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# =====================
# Database Setup
# =====================
db = SQLAlchemy(app)

# =====================
# Database Models
# =====================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='buyer')  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to cars
    cars = db.relationship('Car', backref='seller', lazy=True, cascade='all, delete-orphan', foreign_keys='Car.seller_id')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches"""
        return check_password_hash(self.password, password)


class Car(db.Model):
    __tablename__ = 'cars'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), default='default_car.jpg')
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Car {self.title}>'


class PurchaseRequest(db.Model):
    """Model for car purchase requests from buyers"""
    __tablename__ = 'purchase_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_name = db.Column(db.String(100), nullable=False)
    buyer_email = db.Column(db.String(120), nullable=False)
    buyer_phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Pending')  # Pending, Accepted, Rejected
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    car = db.relationship('Car', backref='requests')
    seller = db.relationship('User', foreign_keys=[seller_id], backref='seller_requests')
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='buyer_requests')
    
    def __repr__(self):
        return f'<PurchaseRequest {self.id}>'


# =====================
# Helper Functions
# =====================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function


def seller_required(f):
    """Decorator to check if user is seller"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role not in ['seller', 'admin']:
            flash('Only sellers can access this page.', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function


# =====================
# Authentication Routes
# =====================

@app.route('/')
def index():
    """Home page"""
    cars = Car.query.all()
    return render_template('index.html', cars=cars)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'buyer')
        
        # Validation
        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return redirect(url_for('register'))
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))
        
        # Set session
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_role'] = user.role
        session.permanent = True
        app.permanent_session_lifetime = app.config['PERMANENT_SESSION_LIFETIME']
        
        flash(f'Welcome, {user.name}!', 'success')
        
        # Redirect based on role
        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user.role == 'seller':
            return redirect(url_for('seller_dashboard'))
        else:
            return redirect(url_for('buyer_dashboard'))
    
    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# =====================
# Buyer Routes
# =====================

@app.route('/buyer/dashboard')
@login_required
def buyer_dashboard():
    """Buyer dashboard - view all cars"""
    if session.get('user_role') not in ['buyer', 'admin']:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    search = request.args.get('search', '')
    brand_filter = request.args.get('brand', '')
    
    query = Car.query
    
    if search:
        query = query.filter(
            (Car.title.ilike(f'%{search}%')) |
            (Car.brand.ilike(f'%{search}%')) |
            (Car.model.ilike(f'%{search}%'))
        )
    
    if brand_filter:
        query = query.filter(Car.brand.ilike(f'%{brand_filter}%'))
    
    cars = query.all()
    brands = [car.brand for car in Car.query.all()]
    brands = list(set(brands))
    
    return render_template('buyer/dashboard.html', cars=cars, search=search, brand_filter=brand_filter, brands=brands)


@app.route('/car/<int:car_id>')
def view_car_details(car_id):
    """View car details"""
    car = Car.query.get_or_404(car_id)
    seller = User.query.get(car.seller_id)
    return render_template('buyer/car_details.html', car=car, seller=seller)


# =====================
# Seller Routes
# =====================

@app.route('/seller/dashboard')
@seller_required
def seller_dashboard():
    """Seller dashboard - view own cars"""
    user_id = session.get('user_id')
    cars = Car.query.filter_by(seller_id=user_id).all()
    return render_template('seller/dashboard.html', cars=cars)


@app.route('/seller/add-car', methods=['GET', 'POST'])
@seller_required
def add_car():
    """Add a new car"""
    if request.method == 'POST':
        title = request.form.get('title')
        brand = request.form.get('brand')
        model = request.form.get('model')
        year = request.form.get('year')
        price = request.form.get('price')
        description = request.form.get('description')
        
        # Validation
        if not all([title, brand, model, year, price]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('add_car'))
        
        try:
            year = int(year)
            price = float(price)
        except ValueError:
            flash('Year and price must be valid numbers.', 'danger')
            return redirect(url_for('add_car'))
        
        # Handle image upload
        image_filename = 'default_car.jpg'
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{datetime.utcnow().timestamp()}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        # Create new car
        new_car = Car(
            title=title,
            brand=brand,
            model=model,
            year=year,
            price=price,
            description=description,
            image=image_filename,
            seller_id=session.get('user_id')
        )
        
        db.session.add(new_car)
        db.session.commit()
        
        flash('Car added successfully!', 'success')
        return redirect(url_for('seller_dashboard'))
    
    return render_template('seller/add_car.html')


@app.route('/seller/edit-car/<int:car_id>', methods=['GET', 'POST'])
@seller_required
def edit_car(car_id):
    """Edit a car"""
    car = Car.query.get_or_404(car_id)
    user_id = session.get('user_id')
    
    # Check if car belongs to current user
    if car.seller_id != user_id and session.get('user_role') != 'admin':
        flash('You do not have permission to edit this car.', 'danger')
        return redirect(url_for('seller_dashboard'))
    
    if request.method == 'POST':
        car.title = request.form.get('title', car.title)
        car.brand = request.form.get('brand', car.brand)
        car.model = request.form.get('model', car.model)
        
        try:
            year = request.form.get('year')
            price = request.form.get('price')
            if year:
                car.year = int(year)
            if price:
                car.price = float(price)
        except ValueError:
            flash('Year and price must be valid numbers.', 'danger')
            return redirect(url_for('edit_car', car_id=car_id))
        
        car.description = request.form.get('description', car.description)
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{datetime.utcnow().timestamp()}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                car.image = filename
        
        db.session.commit()
        flash('Car updated successfully!', 'success')
        return redirect(url_for('seller_dashboard'))
    
    return render_template('seller/edit_car.html', car=car)


@app.route('/seller/delete-car/<int:car_id>')
@seller_required
def delete_car(car_id):
    """Delete a car"""
    car = Car.query.get_or_404(car_id)
    user_id = session.get('user_id')
    
    # Check if car belongs to current user or user is admin
    if car.seller_id != user_id and session.get('user_role') != 'admin':
        flash('You do not have permission to delete this car.', 'danger')
        return redirect(url_for('seller_dashboard'))
    
    # Delete image if it exists and is not default
    if car.image and car.image != 'default_car.jpg':
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], car.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(car)
    db.session.commit()
    
    flash('Car deleted successfully!', 'success')
    
    if session.get('user_role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('seller_dashboard'))


# =====================
# Purchase Request Routes
# =====================

@app.route('/buyer/send-request/<int:car_id>', methods=['GET', 'POST'])
@login_required
def send_purchase_request(car_id):
    """Send a purchase request for a car"""
    if session.get('user_role') not in ['buyer', 'admin']:
        flash('Only buyers can send purchase requests.', 'danger')
        return redirect(url_for('index'))
    
    car = Car.query.get_or_404(car_id)
    
    if request.method == 'POST':
        buyer_name = request.form.get('buyer_name')
        buyer_email = request.form.get('buyer_email')
        buyer_phone = request.form.get('buyer_phone')
        message = request.form.get('message')
        
        # Validation
        if not all([buyer_name, buyer_email, buyer_phone]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('send_purchase_request', car_id=car_id))
        
        # Check if buyer already sent a request for this car
        existing_request = PurchaseRequest.query.filter_by(
            car_id=car_id,
            buyer_id=session.get('user_id'),
            status='Pending'
        ).first()
        
        if existing_request:
            flash('You already have a pending request for this car.', 'warning')
            return redirect(url_for('view_car_details', car_id=car_id))
        
        # Create new purchase request
        new_request = PurchaseRequest(
            buyer_name=buyer_name,
            buyer_email=buyer_email,
            buyer_phone=buyer_phone,
            message=message,
            car_id=car_id,
            seller_id=car.seller_id,
            buyer_id=session.get('user_id'),
            status='Pending'
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        flash('Purchase request sent successfully!', 'success')
        return redirect(url_for('buyer_requests'))
    
    return render_template('buyer/send_request.html', car=car)


@app.route('/buyer/requests')
@login_required
def buyer_requests():
    """View all purchase requests sent by buyer"""
    if session.get('user_role') not in ['buyer', 'admin']:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
    
    user_id = session.get('user_id')
    requests = PurchaseRequest.query.filter_by(buyer_id=user_id).order_by(PurchaseRequest.created_at.desc()).all()
    
    return render_template('buyer/my_requests.html', requests=requests)


@app.route('/seller/requests')
@seller_required
def seller_requests():
    """View all purchase requests for seller's cars"""
    user_id = session.get('user_id')
    
    # Get all requests for cars belonging to this seller
    requests = db.session.query(PurchaseRequest).join(Car).filter(
        Car.seller_id == user_id
    ).order_by(PurchaseRequest.created_at.desc()).all()
    
    return render_template('seller/requests.html', requests=requests)


@app.route('/seller/accept-request/<int:request_id>', methods=['POST'])
@seller_required
def accept_request(request_id):
    """Accept a purchase request"""
    purchase_request = PurchaseRequest.query.get_or_404(request_id)
    user_id = session.get('user_id')
    
    # Verify the request belongs to a car owned by this seller
    if purchase_request.car.seller_id != user_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('seller_requests'))
    
    purchase_request.status = 'Accepted'
    purchase_request.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash(f'Request from {purchase_request.buyer_name} accepted!', 'success')
    return redirect(url_for('seller_requests'))


@app.route('/seller/reject-request/<int:request_id>', methods=['POST'])
@seller_required
def reject_request(request_id):
    """Reject a purchase request"""
    purchase_request = PurchaseRequest.query.get_or_404(request_id)
    user_id = session.get('user_id')
    
    # Verify the request belongs to a car owned by this seller
    if purchase_request.car.seller_id != user_id:
        flash('Access denied.', 'danger')
        return redirect(url_for('seller_requests'))
    
    purchase_request.status = 'Rejected'
    purchase_request.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash(f'Request from {purchase_request.buyer_name} rejected.', 'info')
    return redirect(url_for('seller_requests'))


# =====================
# Admin Routes
# =====================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    total_users = User.query.count()
    total_cars = Car.query.count()
    total_sellers = User.query.filter_by(role='seller').count()
    total_buyers = User.query.filter_by(role='buyer').count()
    
    users = User.query.all()
    cars = Car.query.all()
    
    stats = {
        'total_users': total_users,
        'total_cars': total_cars,
        'total_sellers': total_sellers,
        'total_buyers': total_buyers
    }
    
    return render_template('admin/dashboard.html', stats=stats, users=users, cars=cars)


@app.route('/admin/delete-user/<int:user_id>')
@admin_required
def admin_delete_user(user_id):
    """Admin delete user"""
    if user_id == session.get('user_id'):
        flash('You cannot delete yourself.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.email} deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/delete-car/<int:car_id>')
@admin_required
def admin_delete_car(car_id):
    """Admin delete car"""
    car = Car.query.get_or_404(car_id)
    
    # Delete image if it exists and is not default
    if car.image and car.image != 'default_car.jpg':
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], car.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(car)
    db.session.commit()
    
    flash('Car deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# =====================
# Error Handlers
# =====================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('errors/500.html'), 500


# =====================
# Template Context Processor
# =====================

@app.context_processor
def inject_user():
    """Inject user data into all templates"""
    user_id = session.get('user_id')
    user = None
    if user_id:
        user = User.query.get(user_id)
    return {'current_user': user}


# =====================
# Database Initialization
# =====================

@app.before_request
def create_tables():
    """Create database tables if they don't exist"""
    db.create_all()


# =====================
# Main Application Entry Point
# =====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        
        # Create demo users if they don't exist
        if not User.query.filter_by(email='admin@email.com').first():
            admin = User(
                name='Admin User',
                email='admin@email.com',
                role='admin'
            )
            admin.set_password('123456')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin created: admin@email.com / 123456")
        
        if not User.query.filter_by(email='seller@email.com').first():
            seller = User(
                name='Seller Demo',
                email='seller@email.com',
                role='seller'
            )
            seller.set_password('123456')
            db.session.add(seller)
            db.session.commit()
            print("✓ Seller created: seller@email.com / 123456")
        
        if not User.query.filter_by(email='buyer@email.com').first():
            buyer = User(
                name='Buyer Demo',
                email='buyer@email.com',
                role='buyer'
            )
            buyer.set_password('123456')
            db.session.add(buyer)
            db.session.commit()
            print("✓ Buyer created: buyer@email.com / 123456")
    
    app.run(debug=True)
