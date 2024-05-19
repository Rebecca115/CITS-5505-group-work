#  Study Perth Assistant

Study Perth Assistant is a web application designed to assist students in Perth with managing and accessing educational resources. The application allows users to register, log in, and manage their profiles, as well as browse and post questions.


## **Features**

- **Responsive Design**: Built with Bootstrap 5 for a fully responsive design, ensuring the application works well on all devices.
- **Dynamic Content**: Utilizes Jinja2 templating for dynamic content generation.
- **User Interface**: Modern UI with FontAwesome icons and custom CSS for a sleek look.
- **User Authentication and Authorization**
    - Registration with email verification
    - Login and logout functionality
    - Password reset with email link
    - Profile management including avatar upload
- **Question and Answer Management**
    - Post, edit, and delete questions
    - Post, edit, and delete answers
    - Like and unlike answers
- **Content Browsing and Search**
    - Paginated lists of questions
    - Detailed question and answer pages
    - Search functionality across questions and answers

## **Technical Highlights**

1. **Modular Design**:
    - Utilizes Flask's Jinja2 templating engine with template inheritance to maintain a clean and organized code structure.
    - Different blocks (e.g., **`title`**, **`head`**, **`maincontent`**, **`scripts`**) are defined for flexible reuse and overriding.
2. **Responsive Design**:
    - Built with Bootstrap 5 framework for a fully responsive design.
    - Navigation bar adapts for different screen sizes with a hamburger menu for smaller screens.
3. **User Authentication and Authorization**:
    - Supports user login, registration, and logout features.
    - Displays different navigation menu items based on user authentication status using the **`current_user`** object.
4. **Dynamic Content Loading**:
    - Dynamic content generation using Jinja2 template engine with conditionals and loops for user information and navigation items.
    - Dynamic URL generation with Flask's **`url_for`** function ensures correct and maintainable resource linking.
5. **Form Handling**:
    - Manages forms with Flask-WTF extension, including form validation and rendering.
    - Provides user profile update forms with multiple fields and Bootstrap styling for a clean and user-friendly interface.
6. **Front-End Interactivity**:
    - JavaScript is used for front-end interactions, such as toggling the sidebar.
    - FontAwesome icons are incorporated for enhanced visual aesthetics.
7. **User Experience**:
    - Navigation bar includes a search form for quick access to content.
    - Layout and typography are enhanced using Bootstrap's grid system and custom CSS for an improved user experience.
8. **Compatibility and Performance**:
    - Utilizes CDN for loading Bootstrap and FontAwesome, improving page load speed and resource availability.
    - Static resources (CSS and images) are organized in the **`static`** folder and referenced with Flask's **`url_for`** function for reliable loading.

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

Due to the email verification feature, you need to set the email server environment variables. Missing these may cause the project to fail to start successfully:

```bash
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

### **User Routes**

- **GET /login**
    - Display the login form.
- **POST /login**
    - Handle login form submission.
- **GET /logout**
    - Log out the current user.
- **GET /register**
    - Display the registration form.
- **POST /register**
    - Handle registration form submission.
- **GET /int:id/info/**
    - Display user profile information.
- **GET /int:id/posted**
    - List questions posted by the user.
- **GET /change_password**
    - Display the change password form.
- **POST /change_password**
    - Handle change password form submission.
- **GET /confirm-email/<token>**
    - Confirm user's email address.
- **GET /forget-password**
    - Display the forget password form.
- **POST /forget-password**
    - Handle forget password form submission.
- **GET /reset-password/<token>**
    - Display the reset password form.
- **POST /reset-password/<token>**
    - Handle reset password form submission.
- **GET /int:id/answers**
    - List answers posted by the user.
- **GET /int:id/update_profile**
    - Display the update profile form.
- **POST /int:id/update_profile**
    - Handle update profile form submission.
- **GET /int:id/update_avatar**
    - Display the update avatar form.
- **POST /int:id/update_avatar**
    - Handle update avatar form submission.

### **Question Routes**

- **GET /**
    - Display the home page with a list of questions.
- **GET /question**
    - List questions in JSON format.
- **GET /post**
    - Display the form to post a new question.
- **POST /post**
    - Handle the form submission to post a new question.
- **GET /browse**
    - List questions with pagination.
- **GET /question/int:q_id**
    - Display a specific question and its answers.
- **POST /answer/like/int:answer_id**
    - Like an answer.
- **POST /answer/dislike/int:answer_id**
    - Unlike an answer.
- **POST /answer/delete/int:answer_id**
    - Delete an answer.
- **GET /answer/edit/int:answer_id**
    - Display the form to edit an answer.
- **POST /answer/edit/int:answer_id**
    - Handle the form submission to edit an answer.
- **GET /answer/int:answer_id**
    - Display details of an answer.
- **GET /answer/list/int:q_id**
    - List answers to a question.
- **GET /search**
    - Search questions and answers.
- **POST /question/delete/int:q_id**
    - Delete a question.
- **GET /question/edit/int:q_id**
    - Display the form to edit a question.
- **POST /question/edit/int:q_id**
    - Handle the form submission to edit a question.

## **Database Schema**

The database for this Flask Q&A platform uses SQLAlchemy for ORM (Object-Relational Mapping) and consists of the following primary tables: **`User`**, **`Question`**, **`Answer`**, and **`AnswerLike`**. Below is a detailed description of each table and its relationships.

### **User Table**

The **`User`** table stores information about the users of the platform.

- **id** (Integer, Primary Key, Auto-increment): Unique identifier for each user.
- **username** (String, 64, Unique, Not Null): The username chosen by the user.
- **DOB** (DateTime): The date of birth of the user.
- **password** (String, 256, Not Null): The hashed password of the user.
- **avatar** (String, 256): Path to the user's avatar image.
- **gender** (String, 16): The gender of the user.
- **email** (String, 64, Unique): The email address of the user.
- **email_verified** (Boolean, Default False): Indicates if the user's email has been verified.
- **created_at** (DateTime, Default datetime.now): The date and time when the user was created.
- **updated_at** (DateTime, Default datetime.now, OnUpdate datetime.now): The date and time when the user was last updated.
- **school** (String, 64): The school of the user.
- **signature** (String, 256): The user's signature or personal quote.

### **Question Table**

The **`Question`** table stores information about the questions posted on the platform.

- **id** (Integer, Primary Key, Auto-increment): Unique identifier for each question.
- **title** (String, 128, Not Null): The title of the question.
- **img** (String, 256): Path to an optional image associated with the question.
- **content** (Text): The content or body of the question.
- **category** (String, 64): The category to which the question belongs.
- **created_at** (DateTime, Default datetime.now): The date and time when the question was created.
- **updated_at** (DateTime, Default datetime.now, OnUpdate datetime.now): The date and time when the question was last updated.
- **user_id** (Integer, Foreign Key **`user.id`**): The ID of the user who posted the question.

### **Answer Table**

The **`Answer`** table stores information about the answers posted to questions on the platform.

- **id** (Integer, Primary Key, Auto-increment): Unique identifier for each answer.
- **content** (Text, Not Null): The content or body of the answer.
- **created_at** (DateTime, Default datetime.now): The date and time when the answer was created.
- **updated_at** (DateTime, Default datetime.now, OnUpdate datetime.now): The date and time when the answer was last updated.
- **user_id** (Integer, Foreign Key **`user.id`**): The ID of the user who posted the answer.
- **q_id** (Integer, Foreign Key **`question.id`**): The ID of the question to which the answer belongs.

### **AnswerLike Table**

The **`AnswerLike`** table stores information about the likes given to answers on the platform.

- **id** (Integer, Primary Key, Auto-increment): Unique identifier for each like.
- **created_at** (DateTime, Default datetime.now): The date and time when the like was created.
- **user_id** (Integer, Foreign Key **`user.id`**): The ID of the user who liked the answer.
- **answer_id** (Integer, Foreign Key **`answer.id`**): The ID of the answer that was liked.
- **q_id** (Integer, Foreign Key **`question.id`**): The ID of the question to which the answer belongs.

### **Relationships**

- **User** to **Question**: One-to-Many relationship. A user can post multiple questions.
- **User** to **Answer**: One-to-Many relationship. A user can post multiple answers.
- **User** to **AnswerLike**: One-to-Many relationship. A user can like multiple answers.
- **Question** to **Answer**: One-to-Many relationship. A question can have multiple answers.
- **Answer** to **AnswerLike**: One-to-Many relationship. An answer can have multiple likes.

## **Group members**


  UWA ID   | Name         | GitHub Username |
|--------- |--------------|-----------------|
| 23992836 | Fudong Qin   | qincode         |
| 23856227 | Ziqi Chen    | ziqichen55555   |
| 23918117 | Clare Li     | ClareUWA        |
| 23766091 | Yunzhi Chen  | Rebecca115      |
