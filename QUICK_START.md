# ⚡ Quick Start Guide

Get the Car Marketplace running in 5 minutes!

---

## 🎯 Prerequisites

- Python 3.8+ installed
- MySQL Server running
- `pip` (usually comes with Python)

---

## 🚀 5-Minute Setup

### Step 1: Create Database

```bash
mysql -u root -p
CREATE DATABASE car_marketplace;
EXIT;
```

### Step 2: Install Dependencies

```bash
cd "c:\Users\Administrator\Desktop\Car Marketplace"
pip install -r requirements.txt
```

### Step 3: Update Config (if needed)

Edit `config.py` - change database password if your MySQL password is different:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/car_marketplace'
```

### Step 4: Run Application

```bash
python app.py
```

### Step 5: Open in Browser

```
http://localhost:5000
```

---

## 🔐 Login Credentials

Use any of these to test:

```
Admin:  admin@email.com / 123456
Seller: seller@email.com / 123456
Buyer:  buyer@email.com / 123456
```

---

## 🎮 Quick Test

1. **Home Page**: `http://localhost:5000` - Browse featured cars
2. **Login**: Use admin credentials above
3. **Admin Dashboard**: See statistics and manage users
4. **Add Car**: Switch to seller role and add a car
5. **Search**: Search for cars on buyer dashboard

---

## ✅ Verify It's Working

You should see:

- Home page with featured cars
- Login/Register working
- Admin dashboard showing statistics
- Ability to add/edit/delete cars
- Search functionality
- Beautiful Bootstrap UI

---

## 📁 Important Files

| File                   | What to Edit         |
| ---------------------- | -------------------- |
| `config.py`            | Database credentials |
| `app.py`               | Add new features     |
| `templates/`           | UI changes           |
| `static/css/style.css` | Styling              |

---

## ⚠️ Common Issues

**Flask not found?**

```bash
pip install -r requirements.txt
```

**MySQL connection error?**

- Check MySQL is running
- Verify username/password in `config.py`
- Check database `car_marketplace` exists

**Port 5000 in use?**
Edit `app.py` last line:

```python
app.run(debug=True, port=5001)  # Use 5001 instead
```

---

## 📚 Next Steps

1. **Explore the Code**: Open `app.py` and read the comments
2. **Modify Features**: Add new fields or features
3. **Customize UI**: Edit templates and CSS
4. **Deploy**: Follow deployment section in README.md

---

**You're all set! 🎉**

## 🎯 One-Minute Setup

### Step 1: Install Dependencies

```bash
cd "Car Marketplace"
pip install -r requirements.txt
```

### Step 2: Create MySQL Database

```sql
CREATE DATABASE car_marketplace;
```

### Step 3: Run the App

```bash
python app.py
```

### Step 4: Open Browser

Go to: **http://localhost:5000**

---

## 🔑 Demo Login Credentials

| Role   | Email            | Password |
| ------ | ---------------- | -------- |
| Buyer  | buyer@email.com  | 123456   |
| Seller | seller@email.com | 123456   |
| Admin  | admin@email.com  | 123456   |

Create these accounts by registering through the website.

---

## 📋 What's Included

✅ **app.py** - 500+ lines of backend code with everything integrated
✅ **7 HTML Templates** - For all pages and user roles
✅ **Bootstrap 5** - Beautiful responsive design
✅ **SQLAlchemy ORM** - Database models and queries
✅ **MySQL Integration** - Production-ready database
✅ **Session Authentication** - Manual login/logout
✅ **File Uploads** - Car image handling
✅ **CRUD Operations** - Full create, read, update, delete

---

## 🧭 Navigation

**Home Page**: Browse featured cars
**Register**: Create buyer or seller account
**Login**: Access your account
**Browse Cars**: Search and filter listings
**My Cars** (Seller): Manage your listings
**Admin Dashboard**: View all users and cars

---

## 🔧 Configuration

**Database**: `config.py`

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/car_marketplace'
```

Change if your MySQL credentials are different.

---

## 📁 Key Files Explained

| File                     | Purpose                                      |
| ------------------------ | -------------------------------------------- |
| **app.py**               | All Flask routes, models, and business logic |
| **config.py**            | Database and app configuration               |
| **templates/**           | HTML files for all pages                     |
| **static/css/style.css** | Custom styling                               |
| **static/uploads/**      | Uploaded car images                          |

---

## ❓ Common Issues & Solutions

**Issue**: "No module named 'flask'"

```bash
pip install -r requirements.txt
```

**Issue**: "Can't connect to MySQL"

- Verify MySQL is running
- Check credentials in config.py
- Run: `CREATE DATABASE car_marketplace;`

**Issue**: Port 5000 in use

```bash
flask run --port 5001
```

---

## 🎓 Learning Notes

This project is perfect for learning:

- Flask basics and routing
- SQLAlchemy ORM
- MySQL database design
- Session-based authentication
- Bootstrap responsive design
- CRUD operations
- File handling in Flask

---

## 📚 Code Structure

```
Backend (app.py):
├── Models (User, Car)
├── Authentication (register, login, logout)
├── Routes (all endpoints)
├── Decorators (@login_required, @admin_required)
└── CRUD Operations

Frontend (templates/):
├── Base layout
├── Auth pages
├── Buyer pages
├── Seller pages
└── Admin pages
```

---

## 🚀 Next Steps

1. Start the app: `python app.py`
2. Register an account
3. Explore all features
4. Review `app.py` to understand the code
5. Try adding more features!

---

**Enjoy your Car Marketplace! Happy coding! 🚗**
