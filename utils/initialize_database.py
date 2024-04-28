import hashlib
import os
from random import random

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
            content="""
            Baby pigeons are usually not seen because they stay in their nests, which are often hidden in high and hard-to-reach places such as rooftops or building ledges. Additionally, baby pigeons grow rapidly and are capable of flying within a few weeks, so they may not stay in their nests for long periods.
            """,
            user_id=1, q_id=1),
        Answer(
            content="""
            Whether cereal qualifies as soup can be debated. While cereal and milk share some similarities with soup, such as being a mixture of solid and liquid ingredients, the key difference lies in their preparation and consumption. Soup is typically cooked and served hot as a savory dish, while cereal is eaten cold and is often considered a breakfast food.
            """,
            user_id=2, q_id=2),
        Answer(
            content="""
The reason why there's usually a light in the fridge but not in the freezer is due to the way these
appliances are designed and used.

*Fridge Lights:*
	+ Fridges typically require a consistent temperature between 37°F and 40°F (3°C to 4°C) to keep food
fresh.
	+ The light in the fridge helps you see what's inside, making it easier to find the food you need without
having to open the door too many times. This reduces the cold air from escaping and keeps your food at a
consistent temperature.

*Freezer Lights:*
	+ Freezers are designed to maintain an extremely low temperature (usually around -18°C or 0°F) to
preserve food.
	+ The cold environment and low humidity in freezers make it more difficult for people to see inside.
Therefore, there's usually no need for a light in the freezer because you're not as likely to be searching
for something specific.

In summary, the fridge needs lighting to help maintain its temperature and make contents visible, while
the freezer doesn't require lighting due to its low temperatures and lack of food organization.
            """,
            user_id=3, q_id=3),
        Answer(
            content="""
The answer is: None!

Mirrors don't have a color because they reflect light, rather than absorbing or emitting it. When you look
into a mirror, you're seeing the reflection of your surroundings and yourself, not the actual color of the
mirror itself.

Think about it like this: when you take a picture with a camera, what's the color of the photograph? It's
whatever colors are reflected in the scene you're capturing! In the same way, mirrors reflect the colors
around them, so they don't have an inherent color themselves.
            """,
            user_id=4, q_id=4),
        Answer(
            content="""
A curious question!

The reasons behind our noses running and our feet smelling are quite different, but I'll try to provide
some insight:

**Noses Running:**

* When your nose runs, it's usually because of excess mucus production. This can be triggered by:
	+ Allergies or irritants in the air
	+ Cold or sinus infections
	+ Hormonal changes (e.g., pregnancy)
	+ Dry air or environmental factors

The mucus is produced to help trap dust, bacteria, and other unwanted particles, protecting your lungs
from harm. When there's an overproduction of mucus, it can't be cleared properly, leading to a runny nose.

**Feet Smelling:**

* Feet have thousands of sweat glands, which produce sebum (an oily substance) as part of the natural
cooling process. This sweat can mix with:
	+ Dead skin cells
	+ Bacteria
	+ Fungi (like athlete's foot)

The combination of these factors creates an ideal environment for odor-causing compounds to form. As your
feet warm up and move around, the bacteria on your skin break down the sweat and other substances,
releasing unpleasant-smelling compounds.

**Why Do Our Noses Run and Feet Smell?**

* In short, our noses run because our bodies are trying to protect ourselves from environmental stimuli or
internal changes.
* Our feet smell because they're a warm, humid environment that's perfect for bacteria and fungi to
thrive. Sweat and dead skin cells provide the necessary nutrients for these microorganisms to grow and
produce odors.

So, while it might seem like our noses and feet are somehow connected in terms of bodily functions,
they're actually just responding to different stimuli and environmental factors!
            """,
            user_id=5, q_id=5),
        Answer(
            content="""
Crying is a complex process that involves the release of tears from the lacrimal gland, which is located
under the eyebrow bone. These tears then flow through the tear ducts and out of the eye.

However, when you're underwater, the pressure and density of the water make it difficult for your eyes to
produce and drain tears normally. In fact, the pressure can cause the tear ducts to become blocked, making
it even harder for tears to come out.

So, can you cry underwater? Well, technically yes, but it's not exactly the same as crying on land. Here's
what happens:

1. **Tears don't flow**: When you're underwater, your eyes can still produce tears, but they won't flow
out of your eyes like they would on land.
2. **Water pressure**: The water pressure pushes the tears back into your eye, making it difficult for
them to drain properly.
3. **Emotions still present**: Even though your tears might not be flowing, you can still feel emotions
like sadness or joy underwater.

So, while you can technically cry underwater, it's not the same as crying on land. The pressure and
density of the water make it a unique experience!            """,
            user_id=6, q_id=6),
        Answer(
            content="""
Fish don't get thirsty in the same way humans do. Since they live in water, their bodies are adapted to
extract what they need from their aquatic environment.

Here's why:

1. **Water absorption**: Fish absorb water and its nutrients through their gills, skin, and scales. They
don't have a separate system for drinking water like humans do.
2. **Osmoregulation**: Fish regulate the concentration of salts and other solutes in their bodies to
maintain proper osmotic balance. This process helps them conserve water and prevent dehydration.
3. **Efficient metabolism**: Fish have highly efficient metabolic processes that allow them to extract
energy from their food without generating a lot of waste heat, which would require additional water
intake.

In short, fish don't need to drink water like humans do because they're constantly surrounded by it! Their
bodies are designed to thrive in an aquatic environment, and they've evolved to conserve water and manage
their bodily functions accordingly.

So, to answer your question: No, fish don't get thirsty!            """,
            user_id=7, q_id=7),
        Answer(
            content="""
The reason we "park on driveways" and "drive on parkways" lies in the historical development of urban
planning, transportation infrastructure, and language evolution.

In the early 20th century, cities began to develop separate road networks for different types of traffic.
Parkways were designed as scenic, high-speed routes for pleasure driving and commuting, while local
streets (now called "driveways") were intended for access to homes and businesses.

Initially, parkways were built with a focus on aesthetics and speed, featuring wide lanes, gentle curves,
and minimal intersections. They were meant for leisurely driving, not for everyday use. As cities grew and
traffic increased, these roadways became congested, but their design remained unchanged.

Meanwhile, local streets (driveways) were constructed as narrow, winding roads to serve residential areas.
They weren't designed for high-speed traffic or heavy commercial use.

Language has a way of adapting to reality, and our vocabulary followed the changes in urban
infrastructure. The terms "parkway" and "driveway" became entrenched in our collective consciousness, even
though their original meanings were lost over time.

Today, we park on driveways because they're designed for short-term stops, like loading and unloading
passengers or cargo. We drive on parkways (or highways) because they're built for higher speeds and longer
distances.

So, to summarize: the reason we "park on driveways" and "drive on parkways" is a result of historical
context, urban planning decisions, and linguistic evolution, which have led to our modern understanding of
these terms.""",            user_id=8, q_id=8),
        Answer(
            content="""
The idea that vampires can't see their reflection is a common myth or trope in folklore and popular
culture. However, this myth doesn't necessarily explain how vampires might maintain their hairstyles.

In reality, there's no inherent connection between a vampire's inability to see themselves in the mirror
and their hair being neat or messy. Vampires, as fictional creatures, can have any level of grooming skill
or preference just like humans do!

Perhaps you're thinking of certain depictions of vampires in fiction or art where they always seem to have
immaculate hairstyles? That might be due to artistic liberties taken by creators to enhance the
character's appearance and persona.

In some cases, the "no-reflection" myth could be used as a plot device or a symbol for something else. For
instance:

1. **Vulnerability**: A vampire's inability to see themselves in the mirror could represent their
vulnerability to certain weaknesses, like garlic or holy symbols.
2. **Egotistical nature**: The lack of self-awareness might symbolize a vampire's egoistic or narcissistic
tendencies, as they're more concerned with appearances than actual self-reflection.

In any case, the connection between vampires not seeing themselves in the mirror and their hair being neat
is purely fictional and doesn't hold water outside of creative storytelling!            """,
            user_id=9, q_id=9),
        Answer(
            content="""
In most cases, the answer would be "no," the ambulance would not stop to help the person they just ran
over. Here's why:

1. **Prioritization**: The ambulance is on its way to save someone else who needs urgent medical
attention. Its primary goal is to reach that patient as quickly and safely as possible.
2. **Limited resources**: Ambulances are designed to transport patients, not provide emergency care for
multiple individuals at once. Stopping to help the person they just ran over would divert their limited
resources away from the original mission: saving the life of the intended patient.
3. **Safety concerns**: If the ambulance stops to help someone they just ran over, it could compromise the
safety of both patients involved. The ambulance crew might be put in harm's way, and the already injured
person might not receive the best possible care.

However, there are some situations where an ambulance might need to stop to help someone they've just run
over:

1. **Extremely severe injuries**: If the person they ran over is critically injured or bleeding heavily,
the ambulance crew might need to intervene quickly to prevent further harm or even save their life.
2. **Special circumstances**: In rare cases, there might be specific circumstances that require an
ambulance to stop and assist someone they've just run over, such as a child or pet in distress.

In general, though, the answer would still be "no," the ambulance would not typically stop to help the
person they just ran over.            """,
            user_id=10, q_id=10)
    ]

    for answer in answers:
        db.session.add(answer)

    db.session.commit()
