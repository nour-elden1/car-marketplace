# 🚗 Car Marketplace

A complete, beginner-friendly Flask-based web application for buying and selling cars online. Built with Python, Flask, SQLAlchemy ORM, MySQL, and Bootstrap 5.

---

## 📋 Project Overview

**Car Marketplace** is a full-stack web application that allows users to:

- **Register and Login** with different user roles
- **Buy Cars** - Browse, search, and view car details
- **Sell Cars** - Add, edit, and manage car listings
- **Manage Platform** (Admin) - Manage users and cars

### Key Features

#### 🔐 Authentication

- User registration with role selection (Buyer/Seller/Admin)
- Secure login/logout with session management
- Role-based access control
- Password hashing with Werkzeug security

#### 🛒 Buyer Features

- Browse all available cars with pagination
- Search cars by title, brand, or model
- View detailed car information with images
- See seller contact information

#### 🏪 Seller Features

- Add new car listings with images
- Edit existing car listings
- Delete own listings
- View all their own cars in a dashboard
- Upload car images

#### 👨‍💼 Admin Features

- Dashboard with platform statistics
- View all users with role badges
- Delete users or cars
- Manage platform content

---

## 🛠️ Tech Stack

| Component           | Technology              |
| ------------------- | ----------------------- |
| **Backend**         | Flask 3.0+              |
| **Database**        | MySQL 8.0+              |
| **ORM**             | SQLAlchemy 2.0+         |
| **Frontend**        | HTML5, CSS3, JavaScript |
| **CSS Framework**   | Bootstrap 5.3+          |
| **Authentication**  | Werkzeug Security       |
| **Database Driver** | PyMySQL                 |

---

## 📁 Project Structure

```
Car Marketplace/
│
├── app.py                          # Main Flask app - ALL backend code
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
│
├── templates/                      # HTML templates
│   ├── layout/
│   │   └── base.html              # Base template with navbar
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── admin/
│   │   └── dashboard.html
│   ├── seller/
│   │   ├── dashboard.html
│   │   ├── add_car.html
│   │   └── edit_car.html
│   ├── buyer/
│   │   ├── dashboard.html
│   │   ├── car_details.html
│   │   └── search.html
│   ├── errors/
│   │   ├── 404.html
│   │   └── 500.html
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── uploads/                   # Car images storage
│
└── README.md
```

---

## 🗄️ Database Schema

### Users Table

```sql
id (INT, PRIMARY KEY)
name (VARCHAR 100)
email (VARCHAR 120, UNIQUE)
password (VARCHAR 255) - hashed
role (VARCHAR 20) - 'admin', 'seller', 'buyer'
created_at (DATETIME)
```

### Cars Table

```sql
id (INT, PRIMARY KEY)
title (VARCHAR 200)
brand (VARCHAR 100)
model (VARCHAR 100)
year (INT)
price (FLOAT)
description (TEXT)
image (VARCHAR 255)
seller_id (INT, FOREIGN KEY -> users.id)
created_at (DATETIME)
updated_at (DATETIME)
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.8+** installed
- **MySQL Server 8.0+** running
- **pip** (Python package manager)
- **Git** (optional, for cloning)

### Step-by-Step Setup

#### 1. Clone/Download Project

```bash
cd "c:\Users\Administrator\Desktop\Car Marketplace"
```

#### 2. Create MySQL Database

```bash
mysql -u root -p
CREATE DATABASE car_marketplace;
EXIT;
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Database Connection

Edit `config.py` and update the database URI with your MySQL credentials:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:your_password@localhost/car_marketplace'
```

#### 5. Run the Application

```bash
python app.py
```

You should see:

```
Database tables created successfully!
✓ Admin created: admin@email.com / 123456
✓ Seller created: seller@email.com / 123456
✓ Buyer created: buyer@email.com / 123456
 * Running on http://127.0.0.1:5000
```

#### 6. Open in Browser

```
http://localhost:5000
```

---

## 👥 Demo Credentials

Three demo users are automatically created on first run:

| Role       | Email            | Password |
| ---------- | ---------------- | -------- |
| **Admin**  | admin@email.com  | 123456   |
| **Seller** | seller@email.com | 123456   |
| **Buyer**  | buyer@email.com  | 123456   |

---

## 📚 Application Routes

### Public Routes

- `GET  /` - Home page
- `GET  /login` - Login page
- `POST /login` - Process login
- `GET  /register` - Registration page
- `POST /register` - Process registration
- `GET  /car/<id>` - View car details

### Buyer Routes

- `GET  /buyer/dashboard` - Browse all cars
- `GET  /search` - Search cars
- `GET  /logout` - Logout

### Seller Routes

- `GET  /seller/dashboard` - View own cars
- `GET  /seller/add-car` - Add car form
- `POST /seller/add-car` - Process car addition
- `GET  /seller/edit-car/<id>` - Edit car form
- `POST /seller/edit-car/<id>` - Process car update
- `POST /seller/delete-car/<id>` - Delete car
- `GET  /logout` - Logout

### Admin Routes

- `GET  /admin/dashboard` - Admin dashboard
- `POST /admin/delete-car/<id>` - Delete any car
- `POST /admin/delete-user/<id>` - Delete any user
- `GET  /logout` - Logout

### Error Routes

- `404` - Page not found
- `500` - Server error

---

## 🎯 Feature Walkthroughs

### 1. User Registration

1. Click "Register" on home or login page
2. Fill in Name, Email, Password, and select role (Buyer/Seller)
3. Click "Create Account"
4. Redirected to login page
5. Login with new credentials

### 2. Login

1. Enter email and password
2. (Optional) Check "Remember me"
3. Click "Login"
4. Redirected to role-specific dashboard

### 3. Seller - Add Car

1. Login as seller
2. Click "Add Car" in navbar or dashboard
3. Fill car details:
   - Title, Brand, Model, Year
   - Price, Description
   - Upload car image
4. Click "Add Car"
5. Car appears in seller dashboard

### 4. Seller - Edit Car

1. Go to seller dashboard
2. Click "Edit" on any car
3. Modify details
4. (Optional) Upload new image
5. Click "Update Car"

### 5. Buyer - Browse Cars

1. Login as buyer or stay on home page
2. View car cards with images and prices
3. Click "View Details" for more info
4. See seller information

### 6. Buyer - Search Cars

1. Use search bar in navbar
2. Enter keywords (brand, model, title)
3. Click "Search"
4. View filtered results with pagination

### 7. Admin - View Dashboard

1. Login as admin
2. See statistics cards:
   - Total Users, Total Cars
   - Total Sellers, Total Buyers
3. Browse recent cars
4. View all users in table
5. Delete users or cars if needed

---

## 🔒 Security Features

1. **Password Hashing** - Werkzeug security with salt
2. **Session Management** - Secure Flask sessions
3. **SQL Injection Prevention** - SQLAlchemy ORM parameterized queries
4. **CSRF Protection** - Flask built-in protection
5. **File Validation** - Only images allowed (PNG, JPG, JPEG, GIF)
6. **Role-Based Access** - Decorators enforce authorization
7. **Input Validation** - Form validation on all inputs

---

## 🎨 Frontend Features

- **Bootstrap 5** - Responsive grid system
- **Mobile-Friendly** - Works on all devices
- **Card Components** - Beautiful car display cards
- **Auto-Hiding Alerts** - Flash messages auto-dismiss
- **Pagination** - Split listings into pages
- **Form Validation** - Client & server-side validation
- **Navbar** - Context-aware navigation menu
- **Dark Footer** - Professional page footer

---

## 📊 Database Relationships

```
User (1) ──────┐
                ├─── (Many) Cars
                │    - seller_id FK
```

- Each user can have many cars (seller)
- Each car belongs to one user (seller)
- When user is deleted, their cars are cascaded deleted

---

## 🐛 Troubleshooting

### Issue: Flask module not found

```bash
pip install -r requirements.txt
```

### Issue: MySQL connection refused

```bash
# Windows - Start MySQL service
net start MySQL80

# Or check Services and restart MySQL80
```

### Issue: Port 5000 already in use

```python
# Edit app.py - last line
app.run(debug=True, port=5001)
```

### Issue: Images not uploading

- Check `static/uploads/` folder exists
- Verify folder has write permissions
- Check file size (max 16MB)
- Only PNG, JPG, JPEG, GIF allowed

### Issue: Database tables not creating

```bash
# Delete old database and recreate
mysql -u root -p
DROP DATABASE car_marketplace;
CREATE DATABASE car_marketplace;
EXIT;

# Restart app
python app.py
```

---

## 📈 Code Quality

- **Single File Architecture** - All backend in `app.py`
- **Clear Code Organization** - Sections separated by comments
- **PEP 8 Compliant** - Python best practices
- **Docstrings** - All functions documented
- **DRY Principle** - No code repetition
- **Error Handling** - Try-catch and error pages

---

## 🚀 Deployment

For production deployment:

1. **Security**
   - Set `DEBUG = False` in config
   - Use strong `SECRET_KEY`
   - Enable HTTPS

2. **Database**
   - Use production MySQL instance
   - Regular backups
   - Optimize indexes

3. **Server**
   - Use Gunicorn/Waitress instead of Flask dev server
   - Use Nginx as reverse proxy
   - Enable gzip compression

4. **Environment Variables**
   - Store secrets in `.env` file
   - Don't commit secrets to git

---

## 📚 Learning Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/
- **Bootstrap 5**: https://getbootstrap.com/
- **Werkzeug Security**: https://werkzeug.palletsprojects.com/security/

---

## 🎓 Perfect For

- ✅ Flask beginners learning full-stack development
- ✅ University/College students learning web development
- ✅ Portfolio projects showcasing Flask skills
- ✅ Practice with MVC architecture
- ✅ Understanding database relationships
- ✅ Learning Bootstrap responsive design

---

## 📝 Comments & Maintenance

The code is heavily commented and organized for easy understanding:

- Each route clearly explains its purpose
- Database models documented
- Helper functions commented
- Configuration file well-organized

---

## 📞 Common Questions

**Q: Can I modify the database?**
A: Yes! Edit the model classes in `app.py` then delete the database and restart.

**Q: How do I add more demo users?**
A: Edit the initialization code in `app.py` `if __name__ == '__main__':` section.

**Q: How do I change the site title?**
A: Update `templates/layout/base.html` and update brand text in navbar.

**Q: Can I deploy this on the internet?**
A: Yes! Use Heroku, AWS, or any cloud provider. Follow deployment section above.

---

## 📄 File Information

| File             | Size               | Purpose           |
| ---------------- | ------------------ | ----------------- |
| app.py           | ~600 lines         | All backend logic |
| config.py        | ~30 lines          | Configuration     |
| requirements.txt | ~6 lines           | Dependencies      |
| All templates    | ~50-200 lines each | UI pages          |
| style.css        | ~300 lines         | Styling           |
| script.js        | ~100 lines         | Interactivity     |

**Total Code**: ~2500 lines (Everything for a complete app!)

---

## ✨ Highlights

- ✅ Complete working application
- ✅ No external APIs required
- ✅ All code in single app.py file
- ✅ Responsive Bootstrap design
- ✅ Full CRUD operations
- ✅ User authentication & authorization
- ✅ Image upload functionality
- ✅ Search & pagination
- ✅ Error handling
- ✅ Database migrations

---

## 📅 Version History

**v1.0** - May 16, 2026

- Initial release with all core features
- Three demo users included
- Admin dashboard functional
- Search and pagination working
- Image upload enabled

---

**Happy Coding! 🚀**

Built as a complete learning project for Flask beginners.
