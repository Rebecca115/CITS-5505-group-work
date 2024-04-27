# ** CITS5505 Flask Question and Answer Application**

This Flask application is a simple yet functional Question and Answer platform. It allows users to register, log in, post questions, and provide answers. The application uses Flask, Flask-SQLAlchemy, and Flask-Login for managing user sessions and interactions.

## **Features**

- User registration and authentication
- Post questions with descriptions and images
- Answer questions posted by other users
- View and manage user profiles
- Automatic tracking of views, answers, and likes for questions and answers

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite (default database)

## Project Structure

```
Copy codeproject/
├── app.py
├── conf.py
├── models.py
├── quest/
│   ├── __init__.py
│   └── view.py
├── static/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── mine.html
│   ├── question_detail.html
│   └── register.html
├── user/
│   ├── __init__.py
│   ├── forms.py
│   └── views.py
└── utils/
    ├── __init__.py
    ├── constants.py
    ├── database_creator.py
    └── validators.py

```


## **Installation**

Follow these steps to get your development environment set up:

1. **Clone the repository**

```bash
bashCopy code
git clone https://github.com/your-username/your-repository.git
cd your-repository

```

2. **Set up a virtual environment**

```bash
bashCopy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```

3. **Install dependencies**

```bash
bashCopy code
pip install -r requirements.txt

```

4. **Configuration**

Create a **`conf.py`** file in your project directory and update it with your settings:

```python
pythonCopy code
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///yourdatabase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

```

5. **Initialize the database**

Run the following commands in the Python shell to create your database tables:

```python
pythonCopy code
from yourapplication import db, create_app
app = create_app()
with app.app_context():
    db.create_all()

```

6. **Run the application**

```bash
bashCopy code
flask run

```

Your application should now be running on **`http://localhost:5000`**.

## **URL Endpoints**

The application is structured around several key routes:

- **`/`**: The home page.
- **`/user/register`**: Registration page where new users can create an account.
- **`/user/login`**: Login page for existing users.
- **`/user/logout`**: Logout endpoint that terminates the current user session.

## **User Registration and Login**

### **Registration Process**

To register a new user, navigate to **`/user/register`**. The registration form requires a username, nickname, password, and password confirmation. Upon submission, the application checks for existing usernames and validates the data. If successful, the user's password is encrypted for security and the new user account is created.

### **Login Process**

Existing users can log in by navigating to **`/user/login`**. The user must enter their username and password, which are validated against the stored data. If the credentials are correct, the user is authenticated and logged into the system. The application uses sessions to maintain the login state, ensuring that the user remains logged in while navigating between pages.

## **Contributing**

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (**`git checkout -b feature/AmazingFeature`**)
3. Commit your Changes (**`git commit -m 'Add some AmazingFeature'`**)
4. Push to the Branch (**`git push origin feature/AmazingFeature`**)
5. Open a Pull Request
