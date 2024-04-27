import hashlib
import os
from random import random

from werkzeug.security import generate_password_hash

from models import User, Question, Answer


def create_local_db(app, db):
    if not os.path.exists('instance/data.db'):
        with app.app_context():
            db.create_all()
            initialize_user(db)
            initialize_questions(db)
            initialize_answers(db)
            print('Database initialized successfully!')

def initialize_user(db):

        users = [
            User(username='alice123', nickname='Alice', password=hashlib.sha256("123".encode()).hexdigest(),
                 avatar='path/to/avatar1.jpg', gender='female', sex='female'),
            User(username='bob456', nickname='Bob', password=hashlib.sha256("123".encode()).hexdigest(),
                 avatar='path/to/avatar2.jpg', gender='male', sex='male'),
            User(username='charlie789', nickname='Charlie', password=hashlib.sha256("123".encode()).hexdigest(),
                 avatar='path/to/avatar3.jpg', gender='other', sex='other'),
            User(username='david101', nickname='David', password=hashlib.sha256("123".encode()).hexdigest(),
                 avatar='path/to/avatar4.jpg', gender='male', sex='male'),
            User(username='eve202', nickname='Eve', password=hashlib.sha256("123".encode()).hexdigest(),
                 avatar='path/to/avatar5.jpg', gender='female', sex='female'),
            User(username='frank303', nickname='Frank', password=hashlib.sha256("123".encode()).hexdigest(),
                 avatar='path/to/avatar6.jpg', gender='male', sex='male'),
            User(username='grace404', nickname='Grace', password=hashlib.sha256("123".encode()).hexdigest(),
                 avatar='path/to/avatar7.jpg', gender='female', sex='female'),
            User(username='hank505', nickname='Hank', password=hashlib.sha256("123".encode()).hexdigest(),
                 avatar='path/to/avatar8.jpg', gender='male', sex='male'),
            User(username='irene606', nickname='Irene', password=hashlib.sha256("123".encode()).hexdigest(),
                 avatar='path/to/avatar9.jpg', gender='female', sex='female'),
            User(username='jake707', nickname='Jake', password=hashlib.sha256("123".encode()).hexdigest(),
                 avatar='path/to/avatar10.jpg', gender='male', sex='male')
        ]

        for user in users:
            db.session.add(user)

        db.session.commit()



def initialize_questions(db):
    questions = [
        Question(title="Why do we never see baby pigeons?", desc="Exploring urban wildlife mysteries.",
                 content="It seems pigeons appear out of nowhere as adults. Where are all the baby pigeons hiding?",
                 user_id=1),
        Question(title="Is cereal soup?", desc="A culinary conundrum.",
                 content="What defines a soup? Does cereal qualify when served with milk?", user_id=2),
        Question(title="Why is there a light in the fridge but not in the freezer?",
                 desc="Household appliance mysteries.",
                 content="Have you ever wondered why refrigerators commonly have a light, but freezers do not?",
                 user_id=3),
        Question(title="What color is a mirror?", desc="A reflection on colors.",
                 content="Mirrors show us a multitude of colors, but what color are they inherently?", user_id=4),
        Question(title="Why do our noses run and our feet smell?", desc="A humorous look at human body expressions.",
                 content="The English language can be peculiar with expressions. Why do we say that noses run and feet smell?",
                 user_id=5),
        Question(title="Can you cry underwater?", desc="Physical reactions in different environments.",
                 content="What happens when you try to cry while submerged in water?", user_id=6),
        Question(title="Do fish ever get thirsty?", desc="Aquatic life curiosities.",
                 content="If fish live in water, do they experience thirst in the way land-dwelling creatures do?",
                 user_id=7),
        Question(title="Why do we park on driveways and drive on parkways?", desc="The ironies of English terminology.",
                 content="Exploring the peculiarities of English language in terms of space and movement.", user_id=8),
        Question(title="If vampires can't see their reflection, why is their hair always so neat?",
                 desc="A supernatural fashion mystery.",
                 content="Considering vampires’ lack of reflection, how do they manage to keep their appearance so meticulously groomed?",
                 user_id=9),
        Question(
            title="If an ambulance is on its way to save someone, and it runs someone over, does it stop to help them?",
            desc="Ethical and logistical dilemmas in emergencies.",
            content="A thought experiment on the complexities of emergency responses.", user_id=10)
    ]

    for question in questions:
        db.session.add(question)

    db.session.commit()


def initialize_answers(db):
    answers = [
        Answer(
            content="""Baby pigeons are usually not seen because they stay in their nests, which are often hidden in high and hard-to-reach places such as rooftops or building ledges. Additionally, baby pigeons grow rapidly and are capable of flying within a few weeks, so they may not stay in their nests for long periods.""",
            user_id=1, q_id=1),
        Answer(
            content="""Whether cereal qualifies as soup can be debated. While cereal and milk share some similarities with soup, such as being a mixture of solid and liquid ingredients, the key difference lies in their preparation and consumption. Soup is typically cooked and served hot as a savory dish, while cereal is eaten cold and is often considered a breakfast food.""",
            user_id=2, q_id=2),
        Answer(
            content="""The light in the fridge is designed to help users see the contents of the refrigerator when they open the door, making it easier to find what they need. However, freezers are usually smaller and less frequently accessed, so they may not have a built-in light. Additionally, the cold temperature in the freezer can make it more difficult and expensive to install and maintain lighting.""",
            user_id=3, q_id=3),
        Answer(
            content="""The color of a mirror is not inherent to the mirror itself, but rather the result of the reflective surface. Mirrors reflect all colors of light equally, which creates the appearance of a silver or gray color. However, if a mirror is made with a tinted or coated glass, it may have a different color.""",
            user_id=4, q_id=4),
        Answer(
            content="""The phrases "noses run" and "feet smell" are examples of linguistic quirks in the English language known as antanaclasis, where a word is repeated but with a different meaning each time. While the literal interpretation may seem odd, these phrases have become idiomatic expressions and are commonly used in everyday language.""",
            user_id=5, q_id=5),
        Answer(
            content="""Crying underwater is possible, but the tears would quickly mix with the surrounding water and may not be visible. Additionally, the pressure and sensation of being underwater may affect one's ability to produce tears in the same way as when crying on land.""",
            user_id=6, q_id=6),
        Answer(
            content="""Fish do not experience thirst in the same way as terrestrial animals because their bodies are adapted to extract oxygen and water from their aquatic environment through gills. However, they may still have mechanisms to regulate water intake and maintain internal balance, such as osmoregulation.""",
            user_id=7, q_id=7),
        Answer(
            content="""The terms "driveway" and "parkway" originated from their historical usage and have evolved over time. "Driveway" originally referred to a private road leading from a public street to a residence, where vehicles would drive slowly or park. "Parkway," on the other hand, was initially a landscaped road designed for recreational driving or strolling, often with scenic views and greenery.""",
            user_id=8, q_id=8),
        Answer(
            content="""Vampires are often depicted as having supernatural abilities, including the ability to maintain their appearance without the need for conventional grooming. In many vampire lore, their hair and overall appearance are magically preserved, regardless of whether they can see their reflection in a mirror.""",
            user_id=9, q_id=9),
        Answer(
            content="""The actions taken by an ambulance in such a scenario would depend on various factors, including the severity of the incident, the availability of medical personnel, and local regulations. In most cases, the primary priority would be to provide immediate medical assistance to the injured individual, whether they were struck by the ambulance or not.""",
            user_id=10, q_id=10)
    ]

    for answer in answers:
        db.session.add(answer)

    db.session.commit()

