#  CITS5505 Flask Questions and Answer Application

This Flask application is a simple yet functional Questions and Answer platform. It allows users to register, log in, post questions, and provide answers. The application uses Flask, Flask-SQLAlchemy, and Flask-Login for managing user sessions and interactions.



## **Features**

- **User Registration and Authentication**: Secure signup and login system for users.
- **Post Questions**: Users can post questions, including descriptions, and optionally attach images.
- **Provide Answers**: Users can answer questions posted by others.
- **Profile Management**: Users can view and manage their profiles.
- **Interactive Elements**: Automatic tracking of views, answers, and likes for questions and answers.

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite (default database)

## Project Structure

```
CITS5505-group-project/
app/
│   ├── question/
│   │   ├── form.py
│   │   └── views.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── answered-questions.css
│   │   │   ├── base.css
│   │   │   ├── base_profile.html.css
│   │   │   ├── browse-questions.css
│   │   │   ├── index.css
│   │   │   ├── posted-questions.css
│   │   │   ├── style_1.css
│   │   │   ├── update_avatar.css
│   │   │   └── user-info.css
│   │   ├── font/
│   │   │   └── Inter.ttf
│   │   ├── image/
│   │   │   └── photo-stream/
│   │   ├── js/
│   │   │   └── script.js
│   │   └── uploads/
│   ├── templates/
│   │   ├── answered-questions.html
│   │   ├── base.html
│   │   ├── base_profile.html
│   │   ├── browse-question.html
│   │   ├── change_password.html
│   │   ├── confirm_email.html
│   │   ├── detail.html
│   │   ├── forget_password.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── post_question.html
│   │   ├── posted-questions.html
│   │   ├── profile.html
│   │   ├── question_page.html
│   │   ├── register.html
│   │   ├── search.html
│   │   ├── update_avatar.html
│   │   ├── user-info.html
│   │   └── user_answers.html
│   ├── user/
│   ├── .DS_Store
│   ├── __init__.py
│   └── conf.py
│
├── deliverables/
│   ├── version1/
│   │   ├── homepage.png
│   │   ├── loginpage.png
│   │   ├── postpage.jpg
│   │   ├── questionpage.jpg
│   │   └── registerpage.png
│   ├── version2/
│   │   ├── browse_questions.jpg
│   │   ├── user_answered_questions.jpg
│   │   ├── user_avatar_change.jpg
│   │   └── user_posted_questions.jpg
│   └── version3/

├── migrations/
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── utils/
│   ├── __init__.py
│   ├── constants.py
│
├── README.md
├── models.py
└── requirements.txt
└── run.py

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

Before running the application, make sure to set up the following environment variables:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
export MAIL_SERVER=email-smtp.ap-southeast-2.amazonaws.com
export MAIL_PORT=587
export MAIL_USE_TLS=1
export MAIL_USERNAME=your_mail_username
export MAIL_PASSWORD=your_mail_password
export MAIL_DEFAULT_SENDER=confirm@fudongs.com


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

7. **Testing Database**

If you want to quickly test the application, we provide a simple SQLite testing database for you to use. You can follow these steps to use it:

Download the test database file data.db（https://drive.google.com/file/d/18a2zQ2vd96gkPifCYkYMYLA4948NT5wK/view?usp=sharing）.
After downloading the db file data.db, create a new folder named instance in the root directory of the project and place the data.db file inside this folder.
Ensure you have set up your development environment as described in the "Installation" section.
Run the application using the command provided in step 6.
You can now access the application by visiting http://localhost:5000 and start testing.
Please note that this testing database is only intended for development and testing purposes and should not be used in production. If you plan to deploy the application to a production environment, you will need to configure a real database and ensure it meets your requirements.

Your application should now be running on `http://localhost:5000`.

## **URL Endpoints**

### **User Endpoints**

- `/`: Homepage, displays all questions.
- `/user/register`: User registration page.
- `/user/login`: User login page.
- `/user/logout`: Logs out the current user.

### **Quest Endpoints**

- `/post`: Allows logged-in users to post new questions. Accessible through the `Post` button once logged in.
- `/q/list`: Provides a paginated list of all questions. This can be accessed to view questions in a list format.
- `/detail/<int:t_id>`: Displays the detail page for a specific question, where users can view all the answers and post their own answers.
- `/answer/like/<int:answer_id>`: Endpoint for liking an answer. Only accessible to logged-in users and increases the like count for the specified answer.

## **User Registration and Login**

### **Registration Process**

To register a new user, navigate to `/user/register`. The registration form requires a username, nickname, password, and password confirmation. Upon submission, the application checks for existing usernames and validates the data. If successful, the user's password is encrypted for security, and a new user account is created.

### **Login Process**

Existing users can log in by navigating to `/user/login`. The user must enter their username and password, which are validated against the stored data. If the credentials are correct, the user is authenticated and logged into the system. The application uses sessions to maintain the login state, ensuring that the user remains logged in while navigating between pages.


## **Group members**


  UWA ID   | Name         | GitHub Username |
|--------- |--------------|-----------------|
| 23992836 | Fudong Qin   | qincode         |
| 23856227 | Ziqi Chen    | ziqichen55555   |
| 23918117 | Clare Li     | ClareUWA        |
| 23766091 | Yunzhi Chen  | Rebecca115      |
