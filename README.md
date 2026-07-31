Aurelia - A Text Based RPG Adventure
An explorative game, where you will learn the truth about the Hollow Crown, a conspiracy to overthrow the monarchy. You will be solving puzzles and battling to the end to find the truth — can you make it through?
Features

The game saves all user data, so players can resume their game even after leaving.
One of the main mechanics of D&D is the use of dice — to simulate this, the game uses random number generation for all rolls.
When a player creates a character, all stats start at 8, but they have 20 points to spend increasing them, up to a max of 18.
A full combat system handles encounter actions: checking whether an attack roll beats the enemy's defense score, then dealing damage and subtracting it from the enemy's health. Combat also features descriptive flavor text based on the roll you get.
The game features choice-driven storytelling — the story changes based on your choices early on, so your actions affect what happens later.

Installation
To install the game, clone or download this repository from GitHub.

Make sure Python is installed on your machine.
Open a command prompt in the project folder.
Create a virtual environment:
python -m venv venv
Activate the virtual environment:
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate
Install Flask:
pip install flask
Since player_data.db is excluded from this repository, you'll need to manually create the database and its three tables before running the game. Each table needs the following columns:

user table:

ID (unique identifier for each account)
username
password

characters table:

ID (unique identifier for each character)
user_ID (links back to the account that owns this character)
character_name
strength
dexterity
constitution
intelligence
wisdom
charisma
current_hp
max_hp

game_state table:

ID (unique identifier for each game state entry)
character_ID (links back to the character this progress belongs to)
mission_step
npc1_feelings


Once the database and tables are created, run the app:
python Aurilla.py
Open a browser and go to:
http://127.0.0.1:5000

You should now be able to sign up and start playing.
How to Play
When you first open the game, you'll need to make an account. To create an account, choose a username and password. Once you've created an account, you'll need to return to the login page, where you can now log in using your username and password.
Once logged in, you'll be asked to create a character — this includes your character's name and their stats. All stats start at a base of 8, but you're given 20 points to raise any of the 6 stats. You can raise each stat to a max of 18, but you can't use more than 20 points total; each point of increase costs one point. The stats you choose will affect your character for the rest of the game, so choose wisely.
Once you've created your character, you can now play the game. In the game, you'll be presented with a short descriptive section, followed by an action you need to take — this could be to continue, make a choice, or take part in combat. No matter the choice you make, it affects the rest of the game. Once the story has finished, whether your character lived or died, you can try again by deleting your old character and creating a new one.
Limitations
The only known limitation of the website/game is an error that occurs due to combined factors. When a user quickly reloads a page after clicking an answer choice button, an error occurs because the system had not had enough time to log the answer choice, but the game state had already moved on. This error is avoidable by not reloading the page within 5 seconds of clicking an option.
Credits / Acknowledgments
This app was created during [program name/dates to be filled in]. I would like to give thanks to the professor for helping guide the process.
This app was created by Codeagirl, aka Violet Collins. This was a solo project — all code, story, and design were created by Codeagirl.
In the creation process, AI (Claude) was used to understand complex errors, Flask was used as the Python web framework, SQLite was used for the database, and Pico CSS was used for styling.
