#  CITS5505 Flask Task and Answer Application

This Flask application is a simple yet functional Task and Answer platform. It allows users to register, log in, post tasks, and provide answers. The application uses Flask, Flask-SQLAlchemy, and Flask-Login for managing user sessions and interactions.

## **Features**

- **User Registration and Authentication**: Secure signup and login system for users.
- **Post Tasks**: Users can post tasks including descriptions and optionally attach images.
- **Provide Answers**: Users can answer tasks posted by others.
- **Profile Management**: Users can view and manage their profiles.
- **Interactive Elements**: Automatic tracking of views, answers, and likes for tasks and answers.

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
│   ├── task_detail.html
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

Create a `conf.py` file in your project directory and update it with your settings:

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

Your application should now be running on `http://localhost:5000`.

## **URL Endpoints**

### **User Endpoints**

- `/`: Home page, displays all tasks.
- `/user/register`: User registration page.
- `/user/login`: User login page.
- `/user/logout`: Logs out the current user.

### **Quest Endpoints**

- `/post`: Allows logged-in users to post new tasks. Accessible through the `Post` button once logged in.
- `/q/list`: Provides a paginated list of all tasks. This can be accessed to view tasks in a list format.
- `/detail/<int:t_id>`: Displays the detail page for a specific task, where users can view all the answers and post their own answer.
- `/answer/like/<int:answer_id>`: Endpoint for liking an answer. Only accessible to logged-in users and increases the like count for the specified answer.

## **User Registration and Login**

### **Registration Process**

To register a new user, navigate to `/user/register`. The registration form requires a username, nickname, password, and password confirmation. Upon submission, the application checks for existing usernames and validates the data. If successful, the user's password is encrypted for security and the new user account is created.

### **Login Process**

Existing users can log in by navigating to `/user/login`. The user must enter their username and password, which are validated against the stored data. If the credentials are correct, the user is authenticated and logged into the system. The application uses sessions to maintain the login state, ensuring that the user remains logged in while navigating between pages.

