from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'change-this-to-something-random'

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = sqlite3.connect('player_data.db')
        cursor = conn.cursor()

        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        user_row = cursor.fetchone()

        if user_row and user_row[2] == password:
            session['username'] = username
            return redirect(url_for('game'))
        else:
            return render_template('login.html', error="Invalid username or password")

    else:
        return render_template('login.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        conn = sqlite3.connect('player_data.db')
        cursor = conn.cursor()

        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('sign_up.html', error="That username is already taken.")

        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
        conn.commit()


        return redirect(url_for('home'))

    else:
        return render_template('sign_up.html')

SKILL_STATS = {
    "athletics": "strength",
    "climb": "strength",
    "attack": "strength",
    "acrobatics": "dexterity",
    "sleight": "dexterity",
    "steal": "dexterity",
    "sneak": "dexterity",
    "stealth": "dexterity",
    "hide": "dexterity",
    "arcana": "intelligence",
    "history": "intelligence",
    "investigate": "intelligence",
    "search": "intelligence",
    "nature": "intelligence",
    "religion": "intelligence",
    "animal": "wisdom",
    "insight": "wisdom",
    "medicine": "wisdom",
    "perception": "wisdom",
    "notice": "wisdom",
    "survival": "wisdom",
    "deceive": "charisma",
    "lie": "charisma",
    "intimidate": "charisma",
    "threaten": "charisma",
    "perform": "charisma",
    "persuade": "charisma",
    "convince": "charisma",
}

STORY_STEPS = {
    0: {
        "text": "A member of the royal family has disappeared. This member was recently under investigation for conspiracy against the people. It is said that this member of the royal family was working with a group of many aristocratic individuals. This group is called The Hollow Crown Society because, while most of its members are not royalty, they hold most of the power due to their wealth. These people have, for centuries, found ways to address their issues with other people; they are known to hire the most expensive assassins in all the lands. While much of the royal family is aware of this, they have no clue who the true identities of these people are. This one member was working with the Hollow Crown Society to try and overthrow the current monarchy and take over. Many believe this is just some while rummor, and it is believed to be such a crazy rumor that when people do go missing, most just assume that they died for a reasonable reason. ",
        "type": "auto",
        "next_step": 1
    },
    
    1: {
        "text": "One day after a long, hard day of work at your job, you are in a tavern hearing rumors about the disappearance of this royal. This is followed by the normal skiptisum and the occasional bar fight, but nothing that is not out of the ordinary. Until you hear that one of the people who recently went missing was a prominent member of Eyes of the Night. Eyes of the Night is a local spy network that does any job that pays, from finding out if your boss is planning to fire you all the way to revealing the most scandalous rumors. Recently, they revealed a rumor that looked like evidence for the truth about The Hollow Crown Society. As you make your way to the bar, you are approached by a spy from this network who would like your services. They need help locating the missing member.",
        "type": "buttons",
        "options": {
            "refuse": {
                "label": "Walk Away",
                "result_text": "As you go to leave, you get kidnapped. They bring you into a dark room and say that if you do not help with the mission, they will kill you. They have little trust in you, always worrying they are going to double-cross them. ",
                "feelings_change": -20,
                "next_step": 2
            },
            "freelance": {
                "label": "Agree, but with terms",
                "result_text": "You agree to work with them as a freelancer; you only listen to yourself and have full control. With this control also come the full responsibility of your actions, their is no one to blame is the boss gets unhappy. ",
                "feelings_change": 0,
                "next_step": 2
            },
            "join": {
                "label": "Agree",
                "result_text": "You agree to work with them by joining their organization; you don't have much say on what you do, but you are safe; they will go to the end of the world to protect their members.",
                "feelings_change": 30,
                "next_step": 2
            }
        }
    },
    
    2: {
        "text": "You are briefed on the events; you learn that the missing royal is not just some random member; it is the second-born child of the current ruling family. This child has historically been forced to hide in their siblings' shadow for much of their life. Many believed they joined the Hallow Crown as an act of both defiance and as a way to gain respect. It is unclear if the royal family knows about their child’s involvement within the Hallow Crown, but they are a rising member. Many fear one day the royal might turn their back and reveal all the secrets she has learned. As a way of protecting themselves, they forced the secondborn to kidnap the rising star within the  Eyes of the Night. Members learned soon after the disappearance thatbelieve that this member had found out about the conspiracy to overturn the moncarcy was true and who was involved. As a way of both getting blackmail on the young royal and to silence the truth, the Hollow Crown kidnapped the member of the Eyes of the Night who knew the truth.",
        "type": "auto",
        "next_step": 3
    },
    
    3: {
        "text": "The easiest way to find where the member of the Eyes of the Night is being held is to find a way into the castle. This can be done through different paths, such as getting a job as an employee, using your access to get close to the second born. Or break into the palace, kidnap and replace the second born using a disguise in hopes that their friends will come knocking and bring you to where they are keeping the missing member. Lastly, you could break into the palace and confront the second born, offering to help her if she helps you.",
        "type": "buttons",
        "options": {
            "staff": {
                "label": "Join as Staff",
                "result_text": "While cleaning one of the rooms in the palace, you find something interesting.",
                "feelings_change": 0,
                "next_step": 4.1
            },
            "impersonate": {
                "label": "Sneak into the building",
                "result_text": "You sneak into the palace at night, making your way to the young royal's room.",
                "feelings_change": 0,
                "next_step": 4.2
            },
            "confront": {
                "label": "Confront Them Directly",
                "result_text": "On one of the young royal adventures, you make your way to her location. When you get there, you put your hand over their mouth. \“We can do this the easy way or the hard way,\” you say. They agree, staying quiet. You switch places on the way back to the palace, with a stop at the Eyes of the Night headquarters, where you drop the royal off.",
                "feelings_change": 0,
                "next_step": 4.3
            }
        }
    },
    
    4.1: {
        "text": "Looks like maybe a passageway. You can break down the wall to see what it looks like, or make an investigation check to see if you can figure out how to get into the passageway.",
        "type": "auto",
        "next_step": 5
    },
    
    4.2: {
        "text": "You see a light glowing from within the wall; curious, you look closer. It looks to be a passageway of some type. You listen to see if there is someone currently within the passageway; it sounds empty. Only the sound of a candle dying can be heard.",
        "type": "auto",
        "next_step": 5
    },
    
    4.3: {
        "text": "On the way back to the palace, you find a compass inside one of the bags. When you get inside, you follow the compass to what looks like a passageway. ",
        "type": "auto",
        "next_step": 5
    },

    5: {
        "text": "You discover it is not a passageway but a secret door, but the key to the door is locked away in a different location. You need more inofmration to get in.",
        "type": "buttons",
        "options": {
            "investigate": {
                "label": "Investigate",
                "next_step": 5.05
            },
            "break_door": {
                "label": "Break Down the Door",
                "next_step": 5.3
            }
        }
    },
    
    5.05: {
        "text": "You must make an invesitgation check to see if you can find anything helpfull on the door",
        "type": "check",
        "stat": "intelligence",
        "difficulty": 12,
        "success_text": "You succesd on the investigation, and manage to find out that their is a peace up paper stuck in the door hidge, but you will need to role slight of hand to get it out.",
        "fail_text": "Everything about the door looks normal to you",
        "success_step": 5.1,
        "fail_step": 5
    },
    
    5.1: {
        "text": "Lucky for you, the young royal can not remember where they keep anything and the location of the key is the answer to the riddle on the peace of paper.",
        "type": "auto",
        "next_step": 5.3
    },
    
    5.3: {
        "text": "When the sun is out, but the past is dark, only the strongest will hold the crown. History has been plagued by those of unworthy blood leading the path; to rewrite history is to find the truth. ",
        "type": "buttons",
        "options": {
            "answer_a": {
                "label": "Check the history book",
                "next_step": 5.4
            },
            "answer_b": {
                "label": "Check the sundial",
                "next_step": 5
            },
            "answer_c": {
                "label": "Check the drawer in the desk",
                "next_step": 5
            }
        }
    },
    
    5.4: {
        "text": "When you pull out the history book from the shelf, the door opens, and revealed a room of great treasures and maps. One of the maps is the plan that was used for kidnapping the missing member, and on this map sits the location of were the member is being held. The missing member is being held at the headquarters.",
        "type": "auto",
        "next_step": 6
    },

    6: {
        "text": '''You make your way to this location when you walk in you see a tall half-orc standing over the missing member.
        \“You will reveal what you know,\” says the half-orc 
        \“Never; the truth will only hold me to your lies,\” says the member
        The member notices you, but so does the half-orc. You are brought into a battle. ''',
        "type": "combat",
        "boss_max_hp": 30,
        "boss_ac": 12,
        "win_step": 999,
        "lose_step": 998
    },
}

def get_stat_modifier(stat_value):
    return (stat_value - 10) // 2

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('player_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (session['username'],))
    user_row = cursor.fetchone()
    user_number = user_row[0]

    cursor.execute("SELECT * FROM characters WHERE user_ID = ?", (user_number,))
    character = cursor.fetchone()

    if character is None:
        conn.close()
        return redirect(url_for('create_a_character'))

    character_id = character[0]

    cursor.execute("SELECT * FROM game_state WHERE character_ID = ?", (character_id,))
    game_state = cursor.fetchone()
    mission_step = game_state[2]
    npc1_feelings = game_state[3]
    conn.close()

    current_step = STORY_STEPS[mission_step]
    outcome = None

    if request.method == 'POST':

        if current_step["type"] == "buttons":
            chosen_option = request.form['chosen_option']
            if chosen_option and chosen_option in current_step.get("options", {}):
                option_data = current_step["options"][chosen_option]
            else:
                outcome = "Invalid option selected for this step."

            base_feelings_change = option_data.get("feelings_change", 0)

            roll = random.randint(1, 20)
            roll_bonus = (roll - 10) * 2
            total_feelings_change = base_feelings_change + roll_bonus

            npc1_feelings += total_feelings_change
            mission_step = option_data["next_step"]

            conn = sqlite3.connect('player_data.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE game_state SET mission_step = ?, npc1_feelings = ? WHERE character_ID = ?",
                (mission_step, npc1_feelings, character_id)
            )
            conn.commit()
            conn.close()

            outcome = option_data.get("result_text", "")

            

        elif current_step["type"] == "auto":
            mission_step = current_step["next_step"]

            conn = sqlite3.connect('player_data.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE game_state SET mission_step = ? WHERE character_ID = ?",
                (mission_step, character_id)
            )
            conn.commit()
            conn.close()

        elif current_step["type"] == "check":
            stat_columns = ["id", "user_ID", "character_name", "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
            stat_index = stat_columns.index(current_step["stat"])
            stat_value = character[stat_index]
            modifier = get_stat_modifier(stat_value)

            roll = random.randint(1, 20)
            total = roll + modifier

            if total >= current_step["difficulty"]:
                mission_step = current_step["success_step"]
                outcome = current_step["success_text"]
            else:
                mission_step = current_step["fail_step"]
                outcome = current_step["fail_text"]

            conn = sqlite3.connect('player_data.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE game_state SET mission_step = ? WHERE character_ID = ?",
                (mission_step, character_id)
            )
            conn.commit()
            conn.close()

        elif current_step["type"] == "combat":
            chosen_option = request.form['chosen_option']

            boss_hp = session.get('boss_hp', current_step["boss_max_hp"])
            player_current_hp = character[9]
            player_max_hp = character[10]

            strength_mod = get_stat_modifier(character[3])
            dex_mod = get_stat_modifier(character[4])

            round_log = []

            if chosen_option == "attack":
                attack_roll = random.randint(1, 20)
                attack_total = attack_roll + strength_mod

                if attack_roll == 20 or attack_total >= current_step["boss_ac"]:
                    if attack_roll == 20:
                        damage = 3 + sum(random.randint(1, 6) for _ in range(2))
                        random_num = random.randint(1, 4)
                        if random_num == 4:
                            round_log.append(f"You slide tackled the orc, and hit him in the head. You delt {damage} damage")
                        elif random_num == 3:
                            round_log.append(f"You rolled really well great job, you got a {damage}")
                        elif random_num == 2:
                            round_log.append(f"You shot the enemy from across the room, dealing {damage} damage")
                        elif random_num == 1:
                            round_log.append(f"You stabbed the orc in the side, opening a hug gash, you delt {damage} damage")
                    else:
                        damage = sum(random.randint(1, 6) for _ in range(2))
                        random_num = random.randint(1, 4)
                        if random_num == 4:
                            round_log.append(f"You hit the orc but slid when trying to do a trick. You delt {damage} damage")
                        elif random_num == 3:
                            round_log.append(f"You stabbed the orc in the leg. You got a {damage}")
                        elif random_num == 2:
                            round_log.append(f"You shot the enemy from across the room but you aim was not great, dealing {damage} damage")
                        elif random_num == 1:
                            round_log.append(f"You had no wepon you could get access to so you hit the orc with your hands, you delt {damage} damage")

                    if npc1_feelings > 0:
                        damage += random.randint(1, 6) + 2
                        round_log.append(f"You allies within the fight helped you, they delt {damage} dmaage")

                    boss_hp -= damage
                else:
                    round_log.append(f"You missed, you rolled a {attack_roll}")
            else:
                round_log.append("You are going to try and dodge the next enemy attack")

            if boss_hp > 0:
                boss_dodge_roll = random.randint(1, 4)

                if boss_dodge_roll == 1:
                    round_log.append("The boss dodge your attack")
                else:
                    boss_attack_roll = random.randint(1, 20) + 2

                    if chosen_option == "dodge":
                        player_defense = 10 + (dex_mod * 2)
                    else:
                        player_defense = 10 + dex_mod

                    if boss_attack_roll >= player_defense:
                        damage = random.randint(1, 6) + 3
                        player_current_hp -= damage
                        round_log.append(f"The boss hit you and delt {damage} ")
                    else:
                        round_log.append("You got lucky the boss missed their attack")

            conn = sqlite3.connect('player_data.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE characters SET current_hp = ? WHERE id = ?",
                (player_current_hp, character_id)
            )
            conn.commit()
            conn.close()

            session['boss_hp'] = boss_hp

            if boss_hp <= 0:
                return redirect(url_for('win'))
            elif player_current_hp <= 0:
                return redirect(url_for('loss'))

            conn = sqlite3.connect('player_data.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE game_state SET mission_step = ? WHERE character_ID = ?",
                (mission_step, character_id)
            )
            conn.commit()
            conn.close()

            outcome = " ".join(round_log) + f" (Your HP: {player_current_hp}/{player_max_hp}, Boss HP: {max(boss_hp, 0)}/{current_step['boss_max_hp']})"
        if current_step["type"] != "combat" and STORY_STEPS[mission_step]["type"] == "combat":
            session['boss_hp'] = STORY_STEPS[mission_step]["boss_max_hp"]

        current_step = STORY_STEPS[mission_step]

    return render_template(
        'main_page.html',
        user=session['username'],
        mission_step=mission_step,
        step=current_step,
        outcome=outcome
    )

@app.route('/character')
def character():

    username = session['username']

    conn = sqlite3.connect('player_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    user_row = cursor.fetchone()
    user_number = user_row[0]
    cursor.execute("SELECT * FROM characters WHERE user_ID = ?", (user_number,))
    character = cursor.fetchone()
    conn.close()

    if character == None:
        return redirect(url_for('create_a_character'))
    else:
        return render_template('character.html', character=character)

@app.route('/create_a_character', methods=['GET', 'POST'])
def create_a_character():
    if request.method == 'POST':
        username = session['username']
        character_name = request.form['character_name']

        strength = int(request.form['strength'])
        dexterity = int(request.form['dexterity'])
        constitution = int(request.form['constitution'])
        intelligence = int(request.form['intelligence'])
        wisdom = int(request.form['wisdom'])
        charisma = int(request.form['charisma'])

        constitution_modifier = get_stat_modifier(constitution)
        max_hp = 28 + constitution_modifier
        current_hp = max_hp

        stats = [strength, dexterity, constitution, intelligence, wisdom, charisma]

        if any(stat < 8 or stat > 18 for stat in stats):
            return render_template('create_a_character.html', error="Stats must be between 8 and 18.")

        total_spent = sum(stat - 8 for stat in stats)

        if total_spent > 20:
            return render_template('create_a_character.html', error="You spent more than 20 points.")

        conn = sqlite3.connect('player_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        user_row = cursor.fetchone()
        user_number = user_row[0]

        cursor.execute(
            "INSERT INTO characters (user_ID, character_name, strength, dexterity, constitution, intelligence, wisdom, charisma, current_hp, max_hp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_number, character_name, strength, dexterity, constitution, intelligence, wisdom, charisma, current_hp, max_hp)
        )

        new_character_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO game_state (character_ID, mission_step, npc1_feelings) VALUES (?, ?, ?)",
            (new_character_id, 0, 0)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('character'))

    else:
        return render_template('create_a_character.html')

@app.route('/account')
def account():

    username = session['username']

    conn = sqlite3.connect('player_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    user_row = cursor.fetchone()
    user_name = user_row[1]
    user_password = user_row[2]
    user_number = user_row[0]
    conn.close()

    if not user_row:
        return redirect(url_for('logout'))

    return render_template('account.html', user=user_name, user_pass=user_password, user_num=user_number)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/loss')
def loss():
    return render_template('loss.html')

@app.route('/win')
def win():
    return render_template('win.html')

@app.route('/delete_character', methods=['GET', 'POST'])
def delete_character():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('player_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (session['username'],))
    user_row = cursor.fetchone()
    user_number = user_row[0]

    cursor.execute("SELECT * FROM characters WHERE user_ID = ?", (user_number,))
    character = cursor.fetchone()

    if character is None:
        conn.close()
        return redirect(url_for('create_a_character'))

    character_id = character[0]

    if request.method == 'POST':
        # game_state has a foreign key back to character_ID, so delete it
        # first, then delete the character row itself.
        cursor.execute("DELETE FROM game_state WHERE character_ID = ?", (character_id,))
        cursor.execute("DELETE FROM characters WHERE id = ?", (character_id,))
        conn.commit()
        conn.close()

        # clear any leftover combat state so a fresh character doesn't
        # accidentally inherit a stale boss_hp from the old playthrough
        session.pop('boss_hp', None)

        return redirect(url_for('create_a_character'))

    else:
        conn.close()
        # show a confirmation page instead of deleting immediately on GET,
        # so a stray link click / page refresh can't wipe out a character
        return render_template('delete_character.html', character=character)


if __name__ == '__main__':
    app.run(debug=True)