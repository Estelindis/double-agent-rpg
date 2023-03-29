"""
Project Portfolio 3 (Python): "Double Agent"
Developed and written by Siobhán Mooney, April 2022.
Code is for a terminal of 80 characters wide and 24 rows high.
"""

from time import sleep
from getpass import getpass
from sys import stdout
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Credential values as per the Code Institute Love Sandwiches walkthrough
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("double-agent-rpg")
SAVES = SHEET.worksheet("savegames")

# The dictionary "game" stores all persistent game data.
# The value of "name" is a string.
# The value of "text_speed" is a float.
# The values of the other keys are ints.
# If these data types are changed, the savegame system may break.
# Add any new key-value pairs to the end of the dictionary.
# Do not insert new pairs between existing pairs.
# This ensures backwards compatibility with old saves.
game = {
    "name": "",
    "text_speed": 2.0,
    "checkpoint": 0,
    "information": 0,
    "legitimacy": 3,
    "trust_gov": 5,
    "trust_pref": 5,
    "obeyed_pref": 0,
    "under_duress": 0,
    "try_to_flee": 0,
    "travel_light": 0,
    "adari_knife": 0,
    "adari_poison": 0,
    "khell_poison": 0,
    "adari_outfit": 0,
    "khell_uniform": 0,
    "knife_taken": 0,
    "offended_gov": 0,
    "questioned_pref": 0,
    "basement_info": 0
}


def inc_game_value(key_name, value):
    """
    Increments a named key from game dictionary by value.

    If "under_duress" is true (i.e. greater than zero),
    "trust_pref" can only be decreased, not increased.
    (If you're spying because the Prefect threatened to kill you,
    events can decrease her trust, but never increase it.)
    """
    run_function = True
    if key_name == "trust_pref" and value > 0 and game["under_duress"]:
        run_function = False
    if run_function:
        game[key_name] = game.get(key_name) + value


# The following functions deal with how text is input and displayed.


def get_string(question):
    """
    Returns a non-empty string, input by the user.

    Runs a while loop, using the "question" parameter to seek user input.
    If an empty string is given (i.e. the user just presses ENTER),
    or if the user inputs only spaces,
    the loop will print an error message and request input again.
    Also removes extra whitespace from strings.
    """
    lines_to_delete = 2
    while True:
        input_string = input(f"{question}\n")
        input_string = " ".join(input_string.split())
        if input_string.strip() == "":
            input_string = ""
        if not input_string:
            delete_line(lines_to_delete)
            print("Please input something rather than nothing.")
            lines_to_delete = 3
        else:
            return input_string


def p_d(text):
    """
    Print a line of text, then delay for game["text_speed"].

    The function name is abbreviated to permit longer text strings.
    For clarity: "p_d" stands for "print, delay."
    Standard delay, stored in game["text_speed"], is 2 seconds.
    This delay can be quickened or slowed at the start of the game.
    Adapted from a function by Deanna Carina, P_S in functions.py:
    https://github.com/DeannaCarina/StarTrekTimeLoop
    """
    print(text)
    delay = game["text_speed"]
    sleep(delay)


def yes_no(question):
    """
    Returns true for yes, false for no.

    The "question" parameter is a string (should be a yes/no question)
    Example of use: print(yes_no("Do you like cake?"))
    Accepted user input: Yes, yes, Y, y, No, no, N, n.
    """
    print(question + " (Y/N):")
    choice_made = False
    lines_to_delete = 2
    answer = ""
    while not choice_made:
        answer = get_string("")
        if answer.lower() == "yes" or answer.lower() == "y":
            choice_made = True
            return True
        if answer.lower() == "no" or answer.lower() == "n":
            choice_made = True
            return False
        delete_line(lines_to_delete)
        print("It’s a yes or no question.")
        lines_to_delete = 3


def make_choice(choice_list):
    """
    Returns the user's choice from a list of options.

    Lists should have between two and four items.
    List items follow this format: "  [Choice number]: [Choice text.]"
    If the user inputs an invalid choice, they are asked again.
    Once the user inputs a valid choice, that choice is returned.
    """
    lines_to_delete = 2
    for numbered_choice in choice_list:
        print(numbered_choice)
    choice_num = len(choice_list)
    choice_made = False
    choice_final = ""
    while not choice_made and choice_num == 2:
        user_input_2 = get_string("")
        if user_input_2 == "1":
            choice_made = True
            choice_final = "1"
        elif user_input_2 == "2":
            choice_made = True
            choice_final = "2"
        else:
            delete_line(lines_to_delete)
            p_d("Please choose option 1 or 2.")
            lines_to_delete = 3
    while not choice_made and choice_num == 3:
        user_input_3 = get_string("")
        if user_input_3 == "1":
            choice_made = True
            choice_final = "1"
        elif user_input_3 == "2":
            choice_made = True
            choice_final = "2"
        elif user_input_3 == "3":
            choice_made = True
            choice_final = "3"
        else:
            delete_line(lines_to_delete)
            p_d("Please choose option 1, 2, or 3.")
            lines_to_delete = 3
    while not choice_made and choice_num == 4:
        user_input_4 = get_string("")
        if user_input_4 == "1":
            choice_made = True
            choice_final = "1"
        elif user_input_4 == "2":
            choice_made = True
            choice_final = "2"
        elif user_input_4 == "3":
            choice_made = True
            choice_final = "3"
        elif user_input_4 == "4":
            choice_made = True
            choice_final = "4"
        else:
            delete_line(lines_to_delete)
            p_d("Please choose option 1, 2, 3, or 4.")
            lines_to_delete = 3
    return choice_final


def decoration():
    """
    Prints a line of text decoration.
    """
    print("──────•✧✵✧•──────\n")


def delete_line(num_lines=1):
    """
    Deletes the last line in the STDOUT.

    Optionally, deletes more lines, if a higher number is given as argument.
    Originally by Aniket Navlur: https://stackoverflow.com/a/52590238
    Improved by Alper: https://stackoverflow.com/a/70072767
    """
    for _ in range(num_lines):
        stdout.write("\x1b[1A")  # cursor up one line
        stdout.write("\x1b[2K")  # delete the last line


def pause():
    """
    Lets the user pause before continuing.

    If many lines of text are printed without a pause,
    it may be an overwhelming or irritating user experience.
    This function allows the user to read back over printed text,
    or quickly move on with the game.
    The use of getpass prevents any non-Enter input being printed.
    Once Enter is pressed, the prompt is deleted.
    """
    getpass(prompt="[Press Enter to continue...]")
    delete_line()


def change_speed():
    """
    Called from within start_game to change text_speed.

    Maintain text_speed as a float even if speed could be an int.
    This is important for the savegame system.
    """
    p_d("What speed would you like?")
    speed_options = [
        "  1. Slow.",
        "  2. Standard.",
        "  3. Fast.",
        "  4. Very fast."
        ]
    speed_answer = make_choice(speed_options)
    if speed_answer == "1":
        p_d("Acknowledged.")
        game["text_speed"] = 4.0
    elif speed_answer == "2":
        p_d("Acknowledged.")
        game["text_speed"] = 2.0
    elif speed_answer == "3":
        p_d("Acknowledged.")
        game["text_speed"] = 1.0
    elif speed_answer == "4":
        p_d("Acknowledged.")
        game["text_speed"] = 0.1


# The following functions handle the Google Sheets savegame system


def next_available_row():
    """
    Gets next empty row in the column of the savegame worksheet.

    From Pedro Lobito: https://stackoverflow.com/a/42476314/18794218
    """
    str_list = list(filter(None, SAVES.col_values(1)))
    return str(len(str_list)+1)


def check_game(username):
    """
    Returns true if the given username has data in the savegame sheet.
    """
    # Gets row 1 of the sheet.
    name_list = SAVES.col_values(1)
    # Removes the first entry, which is the column heading ("name").
    name_list.pop(0)
    # Returns true if the username we're checking is in the name list.
    if username in name_list:
        return True


def new_savegame():
    """
    Makes a new entry for username in the savegame sheet.

    Use of enumerate from Mike Hordecki:
    https://stackoverflow.com/a/522578/18794218
    Animation inspired by AKX, LPby, and Warren:
    https://stackoverflow.com/a/7039175/18794218
    """
    progress_bar = [
        "─•✧✵✧•───────────",
        "───•✧✵✧•─────────",
        "─────•✧✵✧•───────",
        "───────•✧✵✧•─────",
        "─────────•✧✵✧•───",
        "───────────•✧✵✧•─",
        "─────────•✧✵✧•───",
        "───────•✧✵✧•─────",
        "─────•✧✵✧•───────",
        "───•✧✵✧•─────────"
        ]
    i = 0
    row_to_fill = next_available_row()
    game_values = list(game.values())
    for index, value in enumerate(game_values):
        print(progress_bar[i % len(progress_bar)], end="\r")
        sleep(.2)
        i += 1
        SAVES.update_cell(row_to_fill, index+1, value)


def load_game():
    """
    Updates "game" dictionary with existing info from savegame sheet.

    Savegame data is validated, then the dictionary is updated.
    """
    username = game["name"]
    name_cell = SAVES.find(username)
    name_row = name_cell.row
    name_data = SAVES.row_values(name_row)
    # Sheet info is stored as strings, so convert it to correct data types.
    # Remove username, to be re-added after using number methods.
    name_data.pop(0)
    # Convert remaining data to floats
    save_floats = [float(i) for i in name_data]
    # Save game_speed to a list, then remove it
    save_speed = save_floats[0]
    speed_list = []
    speed_list.append(save_speed)
    save_floats.pop(0)
    # Convert remaining data to ints
    save_ints = [int(i) for i in save_floats]
    # Rebuild savegame data as a new list from all the saved data
    full_savegame = []
    full_savegame.append(username)
    full_savegame.extend(speed_list)
    full_savegame.extend(save_ints)
    # Update game dictionary with new values from user's savegame
    game_keys = list(game.keys())
    game.update(zip(game_keys, full_savegame))


def save_game():
    """
    Writes "game" dictionary values to username row.

    Only works if username data already present in the sheet.
    For new usernames, use new_savegame() instead.
    This function is called at various checkpoints.
    It is also called if a returning user begins a new mission.
    In that case, default starting values are written to the sheet.
    Use of enumerate from Mike Hordecki:
    https://stackoverflow.com/a/522578/18794218
    Animation inspired by AKX, LPby, and Warren:
    https://stackoverflow.com/a/7039175/18794218
    """
    progress_bar = [
        "─•✧✵✧•───────────",
        "───•✧✵✧•─────────",
        "─────•✧✵✧•───────",
        "───────•✧✵✧•─────",
        "─────────•✧✵✧•───",
        "───────────•✧✵✧•─",
        "─────────•✧✵✧•───",
        "───────•✧✵✧•─────",
        "─────•✧✵✧•───────",
        "───•✧✵✧•─────────"
        ]
    i = 0
    username = game["name"]
    name_cell = SAVES.find(username)
    name_row = name_cell.row
    game_values = list(game.values())
    for index, value in enumerate(game_values):
        print(progress_bar[i % len(progress_bar)], end="\r")
        sleep(.2)
        i += 1
        SAVES.update_cell(name_row, index+1, value)
    p_d("───FILE UPDATED───\n")


# The following functions can be called by start_game to disply information.


def show_briefing():
    """
    Called from within start_game to print establishing text.
    """
    name = game["name"]
    p_d("An empire led by evil sorcerers has conquered most of your world.")
    p_d("The Khell Imperium defeated every nation that resisted its advance.")
    p_d("Faced with conquest, your nation, Adar, took an unprecedented step.")
    p_d("You surrendered without a fight.")
    p_d("The reason why is a tightly-guarded secret.")
    p_d("To gain the Imperium’s trust, your leaders sacrificed their pride.")
    p_d("Trusted as collaborators, chosen Adari would rise in Imperial ranks.")
    p_d("In time, they would strike decisively from within.")
    p_d("Now, perhaps, that time has come.\n")
    p_d("You are one of Adar’s secret agents.")
    p_d("Until today, you’ve served minor Khell bureaucrats.")
    p_d("Spying in the shadows. Reporting to the hidden leaders of Adar.")
    p_d("From the Imperial perspective, your record has been excellent.")
    p_d("But one thing always held you back in the eyes of the Khell.")
    p_d("Your open interest in the language and customs of your own people.")
    p_d("The ruling sorcerers profess the superiority of their culture.")
    p_d("All official business takes place in the Khell language.")
    p_d("Knowledge of Adari ways is disdained in the Imperial bureaucracy,")
    p_d("so most infiltrators hide their interest in such things.\n")
    pause()
    p_d(f"But you, {name}... You’re different.")
    p_d("You feel that serving your people in secret")
    p_d("doesn’t mean you have to openly disavow their past.")
    p_d("On free days, you wear Adari clothes, not the Imperial style.")
    p_d("You also let yourself be seen reading Adari books.")
    p_d("This has occasioned questions from the Khell, some of them sharp.")
    p_d("But your service is exceptionally competent.")
    p_d("You seem loyal to the Imperium in every other way.")
    p_d("As such, your strange proclivities haven’t landed you in jail")
    p_d("with the few remaining Adari dissidents.")
    p_d("However, your career has advanced slowly.")
    p_d("You've been limited to serving lesser Khell.\n")
    p_d("Until now.\n")
    p_d("───BRIEFING FINISHED───\n")
    pause()


def show_how_to_play():
    """
    Called from within start_game to print gameplay info.
    """
    p_d("GAMEPLAY\n")
    p_d("Once your mission begins, read story text.")
    p_d("Then choose options from a numbered list.")
    p_d("To choose an option, type its number (e.g. 1), then press ENTER.")
    p_d("Some choices will add or remove items from your inventory.")
    p_d("Some choices will increase or decrease your statistics.\n")
    p_d("INVENTORY\n")
    p_d("As a spy, choosing which equipment to carry is important.")
    p_d("There may be times when the best choice is none at all.\n")
    p_d("STATISTICS (hereafter, stats) \n")
    p_d("As a spy, your duty is to gather information.")
    p_d("You’ll need trust to maintain your cover.")
    p_d("But your efforts to gain trust may strengthen")
    p_d("the grasp of Khell rulership on your people.\n")
    pause()
    p_d("You have two known stats: Information, and Governor's Legitimacy.")
    p_d("You will be told when you gain or lose either of these stats.")
    p_d("Information starts at 0.")
    p_d("Bringing Information to high levels will empower the Adari to act.")
    p_d("Governor's Legitimacy starts at 3.")
    p_d("It’s hard to know what effects high or low Legitimacy may have.\n")
    p_d("You have two hidden stats: Governor’s Trust, and Prefect’s Trust.")
    p_d("You will not be told explicitly when you gain or lose Trust.")
    p_d("Due to your established reputation, both forms of Trust start at 5.")
    p_d("Bringing trust to high levels will open new possibilities.")
    p_d("If either form of Trust reaches 0, there will be... consequences.\n")
    p_d("If you survive to the end of your mission,")
    p_d("these stats will determine its possible outcomes.\n")
    p_d("───INFORMATION FINISHED───\n")
    pause()


# From this line down, all functions except start_game() are story content


def opening_scene():
    """
    Called from within start_game to begin the story proper.
    """
    name = game["name"]
    print("┌───── •✧✵✧• ─────┐")
    print("  DAY 1: MIDNIGHT ")
    p_d("└───── •✧✵✧• ─────┘\n")
    p_d("It begins on a quiet night, before second moonrise.")
    p_d("You’re working late, searching for secrets.")
    p_d("Then you hear a band of Runeguards at the door.")
    p_d("For a moment, you wonder if you’ve been discovered.")
    p_d("Then you bury your doubts, hide your work, and greet them.\n")
    p_d("The Runeguards escort you to the Governor’s Palace.")
    p_d("From here, a sorcerer rules your people on the Emperor’s behalf.")
    p_d("This building was once the seat of Adari democracy.")
    p_d("One day, you hope, it will be again.\n")
    p_d("When you arrive, the Governor is nowhere to be seen.")
    p_d("Instead, the Prefect of the Runeguard awaits you.")
    p_d("The Runeguard protects the Emperor and his Governors.")
    p_d("Bestowed with imbued magic items by the sorcerers,")
    p_d("Runeguards don’t need brute strength to be deadly.")
    p_d("Arms and raiment aside, most have the look of scholars.\n")
    pause()
    p_d("The Prefect is the leader of their local cohort.")
    p_d("She carries a powerful blade granted by the Emperor himself.")
    p_d("She also has the build of a professional athelete...")
    p_d("...which may tell you everything you need to know about her.")
    p_d("At a gesture, her subordinates leave. The two of you are alone.\n")
    p_d("“Adjunct,” she greets you crisply.\n")
    p_d("That’s all anyone’s allowed to call you now.")
    p_d("In the Imperium, only the sorcerous ruling class are granted names.")
    p_d("Everyone else, including the Prefect herself, has only a title.")
    p_d("Of course, your parents did name you in secret.")
    p_d(f"In the privacy of your mind, you always call yourself {name}.")
    p_d("But the Khell must never know that.\n")
    p_d("How do you greet the Prefect?")
    opening_options = [
        "  1. Respectfully.",
        "  2. Neutrally.",
        "  3. Playfully."
    ]
    opening_answer = make_choice(opening_options)
    if opening_answer == "1":  # Respectfully.
        p_d("You bow. “Prefect. How may I serve?”\n")
        p_d("The Prefect nods. “You ask precisely the right question.")
        p_d("I called you here for a very important reason.”")
    elif opening_answer == "2":  # Neutrally.
        p_d("You give a small nod. “Prefect.”\n")
        p_d("She meets your eyes directly. “I called you here for a reason.”")
    elif opening_answer == "3":  # Playfully.
        p_d("“Prefect. This is my first nocturnal invitation to the Palace.")
        p_d("Forgive me if I don't quite know what to do.” You smile.\n")
        p_d("The Prefect frowns, unamused. “My time is precious, Adjunct.")
        p_d("Don’t waste it. I called you here for a reason, after all.”")
    p_d("She gestures to the empty desk behind her.")
    p_d("“By the will of Xeth, Emperor of the Khell and their subjects,")
    p_d("the Governor has been recalled. The new one comes tomorrow.”\n")
    p_d("Imperial Governors are rarely replaced, and never so quickly.")
    p_d("Your mind races as you wonder what to make of this.\n")
    p_d("“This is where you come in,” the Prefect states.")
    p_d("“The new Governor, Ekkano, has requested... a cultural advisor.")
    p_d("It’s not my place to question his wishes.")
    p_d("It merely falls on me to choose someone. I choose you.”\n")
    p_d("What do you say?")
    advisor_options = [
        "  1. “I am honoured, Prefect. Of course I accept.”",
        "  2. “I don’t understand. Why me?”",
        "  3. “I cannot do this.”"
    ]
    advisor_answer = make_choice(advisor_options)
    if advisor_answer == "1":  # Of course I accept.
        p_d("You think you glimpse a satisfied gleam in her eyes.")
        p_d("“Excellent. I’m glad you didn’t disappoint me.”\n")
    elif advisor_answer == "2":  # Why me?
        p_d("“I hope you’re merely being polite,” she says.")
        p_d("“It should be obvious. The Imperium has many loyal servants.")
        p_d("But you’re the only one who fosters Adari traditions.")
        p_d("Others with such knowledge and customs are dangerous rebels.")
        p_d("Would you have me scour our prisons for an advisor?")
        p_d("I can’t inflict a ruffian on Governor Ekkano.”")
        p_d("It’s clear that she means for you to play this role.")
        p_d("She won’t take no for an answer.\n")
    elif advisor_answer == "3":  # I cannot do this.
        p_d("She shakes her head. “You can. And you will.")
        p_d("As we are commanded, so we all must obey.”")
        p_d("She won’t take no for an answer.\n")
    p_d("For a moment, in silence, you reflect on your new orders.")
    p_d("Working at a Governor’s side will be risky.")
    p_d("But it’s an unprecedented chance to gain vital information.")
    p_d("Then the Prefect says: “There is... one other thing.”\n")
    pause()
    p_d("“A Governor’s life is dangerous. We Runeguards do what we can.")
    p_d("But we fight an uphill battle. The Imperium has many foes.”")
    p_d("You make your face the blankest possible mask.")
    p_d("“I need your help, Adjunct,” she says. “To protect the Governor.")
    p_d("Report to me on every detail you witness in his company.")
    p_d("No matter how inconsequential.”\n")
    p_d("And, with that, all the pieces click into place.")
    p_d("You’ve been in the spy game long enough to know what’s happening.")
    p_d("Governors are second only to the Emperor in authority.")
    p_d("Yet the Prefect is demanding that you spy on Ekkano for her.")
    p_d("This has... implications.\n")
    p_d("Of course, you would have spied on him for the Adari.")
    p_d("But the Prefect too? That’s a dangerous dance.")
    p_d("It’s hard enough being an agent, without being a double agent.\n")
    p_d("What do you say?")
    spy_questioned = False
    spy_options = [
        "  1. “I fully understand. I will do as you command.”",
        "  2. “Will Governor Ekkano know I’m reporting to you?”",
        "  3. “You’re asking me to be a spy. I won’t do that.”"
    ]
    spy_answer = make_choice(spy_options)
    if spy_answer == "1":  # I will do it.
        inc_game_value("trust_pref", 1)  # Prefect's Trust +1
        inc_game_value("obeyed_pref", 1)  # No defiance, enables max trust
        p_d("She nods. “Good. Your obedience will be rewarded.")
        p_d("Doors open to those who serve the Imperium without question.")
    elif spy_answer == "2":  # Will he know?
        p_d("“No,” she says flatly. Then, grimacing, she elaborates.")
        p_d("“He’s a proud man. And why not? Spells can handle most threats.")
        p_d("But not everything. Those concerns fall to the Runeguard.")
        p_d("We shouldn’t trouble Governors with minor security matters.”")
        p_d("Although you’re alone, she lowers her voice.")
        p_d("“Keep your observations strictly secret.")
        p_d("Tell no one but me.”\n")
        spy_questioned = True
    elif spy_answer == "3":  # I will not be a spy.
        inc_game_value("trust_pref", -1)  # Prefect's Trust -1
        p_d("Her lip curls in contempt. “Be careful what you say, Adjunct.")
        p_d("I have asked no such thing. My order is perfectly legitimate.”\n")
    if spy_questioned:  # After asking if Governor will know you're reporting
        print("What do you say?")
        spy_query_options = [
            "  1. “I fully understand. I will do as you command.”",
            "  2. “You’re asking me to be a spy. I won’t do that.”"
            ]
        spy_query_answer = make_choice(spy_query_options)
        if spy_query_answer == "1":  # Accept.
            inc_game_value("trust_pref", 1)  # Prefect's Trust +1
            inc_game_value("obeyed_pref", 1)  # No defiance, enables max trust
            p_d("She nods. “Good. Your obedience will be rewarded.")
            p_d("Doors open to those who serve the Imperium without question.")
            p_d("Or, rather, those who ask only the right questions.")
            p_d("Questions that help them to obey.")
        elif spy_query_answer == "2":  # Refuse.
            inc_game_value("trust_pref", -1)  # Prefect's Trust -1
            p_d("Her lip curls in contempt. “Mind what you say, Adjunct.")
            p_d("I’ve asked no such thing. My order is fully legitimate.”\n")
    if game["trust_pref"] == 4:  # You didn't obey immediately
        print("What do you say?")
        spy_refused_options = [
            "  1. “Forgive me, Prefect. I misspoke. I’ll do as you command.”",
            "  2. “I said I won’t do it.”"
            ]
        spy_refused_answer = make_choice(spy_refused_options)
        if spy_refused_answer == "1":  # Accept after all.
            p_d("She frowns. “See that you do. I’ll accept no mistakes.”\n")
        elif spy_refused_answer == "2":  # Continue to refuse.
            inc_game_value("trust_pref", -1)  # Prefect's Trust -1
            p_d("She sighs. “What a shame. I hope you understand:")
            p_d("your career is over if you refuse.”\n")
    believe_prefect = False
    if game["trust_pref"] == 3:
        print("What do you do?")  # Your career is threatened
        spy_refuse_final_options = [
            "  1. Change you mind and accept.",
            "  2. Refuse, because you don’t want to do it.",
            "  3. Refuse, because you think she’s testing you."
            ]
        spy_refuse_final_answer = make_choice(spy_refuse_final_options)
        if spy_refuse_final_answer == "1":  # Accept after all.
            # No Prefect's Trust regained, she knows she had to force you
            p_d("You need to stay in your post, to keep serving your people.")
            p_d("Whatever her game is, you’ll have to play it.")
            p_d("“Forgive me, Prefect. I misspoke. I’ll do as you command.”\n")
            p_d("“See that you do,” she says. “I’ll be watching you.”\n")
        elif spy_refuse_final_answer == "2":  # Continue to refuse.
            inc_game_value("trust_pref", -1)  # Prefect's Trust -1
            game["under_duress"] = 1
            # From now on, Prefect's Trust can only go down, not up
            p_d("In your career, you’ve gathered plenty of information,")
            p_d("without actually helping the Imperium too much.")
            p_d("If you do what the Prefect wants, that’ll come to an end.")
            p_d("Helping her, or the Governor, or both of them,")
            p_d("might undo everything your people have worked for.")
            p_d("You can’t let that happen.\n")
            p_d("If refusing ends your career, perhaps it’s for the best.")
            p_d("Maybe you’ve had enough of the spy game anyway.")
            p_d("Reaching your decision, you meet her eyes and say:")
            p_d("“So be it.”\n")
            pause()
            p_d("The Prefect regards you with cold rage.")
            p_d("“You think you can refuse me and live, Adjunct?”")
            p_d("Before you can answer, she goes on:")
            p_d("“Perhaps you’re fool enough not to care for your own life.")
            p_d("But my reach is vast. If you think only you will suffer")
            p_d("for this disobedience, you can think again.”")
            p_d("She’ll kill you if you don’t do this. And not just you.\n")
        elif spy_refuse_final_answer == "3":  # Suspect a loyalty test.
            p_d("For an Adari, disloyalty means death.")
            p_d("Yet that’s precisely what she’s asking from you.")
            p_d("To obey a Khell in public, yet report on him in secret.")
            p_d("And not just any Khell but the Emperor’s chosen.")
            p_d("How could she trust anyone who agreed to this?")
            p_d("No. It must be a test. You’ll prove yourself by refusing.\n")
            p_d("“Before the vast Imperium, my career is a small thing.")
            p_d("Better I lose it than stain myself by disobeying the Khell.”")
            pause()
            p_d("The Prefect’s brows contort in frustrated rage.")
            p_d("“I’m telling you to obey. And you’re refusing.”\n")
            p_d("“You’re telling me to obey you specifically,” you reply.")
            p_d("“But the Governor is chosen by Xeth, Emperor of the Khell,")
            p_d("the Zhenko, the Varth, the Czuyd, the Taggadh...”")
            p_d("The Khell Imperium has dozens of dominions.")
            p_d("The list is commonly abbreviated, but you name them all,")
            p_d("eventually finishing with the Adari.")
            p_d("The Prefect doesn’t interrupt this extravagance.\n")
            p_d("You go on: “If the Governor asks what we just discussed,")
            p_d("am I to hide it from him? Lie, or tell a half-truth?")
            p_d("Wouldn’t that be an act of defiance and disloyalty?")
            p_d("If I refused to carry out even one of his orders,")
            p_d("wouldn’t I deserve death?” You pause.")
            p_d("“Against that, Prefect, by all means let me lose my career.”")
            # This extreme zeal regains 2 points of Prefect's Trust.
            # You are now only 1 point behind the trust
            # of someone who obeyed her immediately.
            # In both scenarios, she believes you loyal.
            # But in one, she's gratified that you believed her straight away.
            inc_game_value("trust_pref", 2)
            print("")
            pause()
            p_d("She curls her fingers into a fist.")
            p_d("Then, dragging out her words, she says:")
            p_d("“My blade was granted by Xeth, Emperor of the Khell")
            p_d("and their subjects. So were my orders.")
            p_d("Obey me, Adjunct. And thus obey our Emperor, Xeth.”\n")
            inc_game_value("information", 1)
            p_d("[Information has increased by 1.]")  # info gain
            p_d(f"[The new score is: {game['information']}.]\n")
            p_d("You’ve just learned something important.")
            p_d("Either the Prefect is under the Emperor’s direct command,")
            p_d("bypassing the Governor on some hidden matters.")
            p_d("Or she’s willing to commit to a treasonous lie.")
            p_d("What do you say?")
            belief_options = [
                "  1. “I believe you.”",
                "  2. “The punishment for lying about this is... gruesome.”"
                ]
            belief_answer = make_choice(belief_options)
            if belief_answer == "1":
                believe_prefect = True
            elif belief_answer == "2":
                p_d("“Rightly so,” she says. “I’m not lying.”")
                p_d("What do you say next?")
                belief_2_options = [
                    "  1. “Of course. I believe you.”",
                    "  2. “That’s between you and the Imperium.”"
                    ]
                belief_2_answer = make_choice(belief_2_options)
                if belief_2_answer == "1":
                    believe_prefect = True
                elif belief_2_answer == "2":
                    p_d("She blinks. “Are you questioning my loyalty?”")
                    p_d("Her voice is ominously soft.\n")
                    p_d("You shake your head. “Not at all, Prefect.")
                    p_d("One in my position simply cannot know the truth.")
                    p_d("If you’re not lying, may my actions help you.")
                    p_d("If you are... may justice find you.”")
                    p_d("You keep her gaze, the very picture of zeal.\n")
                    # If she was purely neutral, this should gain you trust
                    # However, she's hurt at not being actively believed
                    # This hurt makes her trust you less
                    inc_game_value("questioned_pref", 1)
                    inc_game_value("trust_pref", -1)  # trust lost
                    p_d("For a moment, the Prefect seems unsettled.")
                    p_d("Then she rallies. “I needn’t fear justice.")
                    p_d("So don’t concern yourself with my fate.")
                    p_d("Think only on the source of my orders.")
                    p_d("And how best you can obey.”")
    if believe_prefect:  # You said you believe the Emp. is ordering the Pref.
        p_d("“Good,” she says. “I’m glad your initial reluctance")
        p_d("was for an appropriate reason. But no more hesitation.")
        p_d("Now you know whose orders you ultimately follow,")
        p_d("I expect your full obedience.”")
    if game["under_duress"]:  # The Prefect is forcing you to obey.
        print("What do you do?")  # Your life is now under threat.
        spy_try_not_to_die_options = [
            "  1. Capitulate, to save yourself and others.",
            "  2. Pretend to agree, but flee at the first oppportunity."
            ]
        spy_try_not_to_die_answer = make_choice(spy_try_not_to_die_options)
        if spy_try_not_to_die_answer == "2":  # Pretend to agree.
            game["try_to_flee"] = 1  # You won't be able to escape yet.
        p_d("“I see I have no choice. As you wish, Prefect.”\n")
        p_d("“It didn’t have to come to this, Adjunct,” she says.")
        p_d("“You could have cooperated freely.”")
        p_d("Ah, yes. That’s what freedom means, isn’t it?")
        p_d("Freedom to serve the Khell. Nothing else.")
        p_d("She continues: “Some guards will escort you home.")
        p_d("And back here at noon. Don’t think you can escape your duty.”\n")
        if game["try_to_flee"]:  # Because you want to attempt escape.
            p_d("So much for fleeing at the first opportunity.")
            p_d("It looks like the Prefect’s not taking any chances.")
            p_d("Still, you know how to be patient.")
            p_d("You can wait.\n")
        p_d("The Prefect calls her Runeguards from outside.")
        p_d("They line up on either side of you.")
        p_d("For now, it seems, your audience is at an end.\n")
    if game["obeyed_pref"]:  # Quick return to obedience path.
        p_d("If you perform loyally and well, in a generation or two...")
        p_d("...perhaps members of your kind could even join the Runeguard.”")
        print("")
        p_d("You disguise your reaction to her bold suggestion.")
        p_d("Members of the Runeguard do not come from subject nations.")
        p_d("That “honour” is kept for the Khell.")
        p_d("Still, Adar is the first nation to capitulate without a fight.")
        p_d("New paths may open as Adari agents prove themselves “loyal.”")
        p_d("Perhaps, even now, you are paving the way")
        p_d("for future Adari to serve as Imperial bodyguards.")
        p_d("Who knows what might happen then?\n")
    if not game["under_duress"]:  # Explaining the accompanying guards.
        p_d("The Prefect calls her Runeguards from outside.")
        p_d("They line up on either side of you.")
        p_d("“For your safety, Adjunct,” she murmurs.")
        p_d("Apparently, you’ll be under more scrutiny from now on.")
        p_d("With that, it seems, your audience is at an end.\n")
    pause()
    p_d("The Runeguards escort you home.")
    p_d("Normally, you walk back through the side-streets.")
    p_d("Tonight, you take the main road.")
    p_d("At a certain point, as if by accident, you stumble.")
    p_d("Hunched over, hidden from sight, you reverse a small paving stone.")
    p_d("Nothing about it, before or after, would look unusual.")
    p_d("But to certain Adari, fellow agents, it sends a message.\n")
    p_d("When you get home, the Runeguards take positions outside.")
    p_d("Anyone wanting to get in or out will have to contend with them.")
    p_d("While they keep vigil, you prepare for what lies ahead.\n")
    p_d("Some agents have emergency channels to Adar’s hidden leaders:")
    p_d("precious Echo Stones repurposed for modern times.")
    p_d("But your rank isn’t high enough for that.")
    p_d("Instead, you write a letter with invisible ink,")
    p_d("detailing the Prefect’s orders and your new cirumstances.")
    p_d("Then you crumple the paper and put it in your wastepaper basket.")
    p_d("Your signal on the way home will alert your people to find it.")
    p_d("But how long that will take, you don’t know.\n")
    pause()
    inc_game_value("checkpoint", 1)
    save_game()
    first_morning()


def first_morning():
    """
    Lets the user choose inventory items on the first day.
    """
    print("┌───── •✧✵✧• ─────┐")
    print("    DAY 1: DAWN ")
    p_d("└───── •✧✵✧• ─────┘\n")
    p_d("The sun rises on your first day as a double agent.")
    p_d("You spend two hours on last-minute research, then take a timed nap.")
    p_d("When you wake, you take a stim shot and make yourself presentable.\n")
    p_d("What will you wear to the Palace?")
    clothing_options = [
        "  1. Imperial uniform.",
        "  2. Adari clothing."
    ]
    clothing_answer = make_choice(clothing_options)
    if clothing_answer == "1":  # Khell.
        p_d("The uniform is appropriate to your bureaucratic rank.")
        p_d("You wear one every work day - which is most days.")
        p_d("It signals your “loyalty” to the Khell. Or so you hope.\n")
        game["khell_uniform"] = 1  # Gives you a uniform
    elif clothing_answer == "2":  # Adari.
        p_d("The flowing cloth and intricate prints of the Adari")
        p_d("are the antithesis of the rigid formality of the Khell.")
        p_d("The new Governor wants an Adari cultural advisor.")
        p_d("Dressed like this, you’ll look the part.\n")
        game["adari_outfit"] = 1  # Gives you Adari clothing
    poison_query = False
    p_d("Will you bring any lethal force?")
    inventory_options = [
        "  1. None whatsoever.",
        "  2. Special poisons, disguised as fragrance sachets.",
        "  3. A traditional Adari knife, worn openly."
    ]
    inventory_answer = make_choice(inventory_options)
    if inventory_answer == "1":  # Nothing
        p_d("To seem harmless, this may be the safest option.")
        game["travel_light"] = 1  # You brought nothing
    elif inventory_answer == "2":  # Poison
        p_d("It’s normal among Khell and Adari to wear a fragrance sachet")
        p_d("in an inner clothing pocket. But more than one is unusual.")
        p_d("If searched, you may be able to pass off two as eccentricity.")
        p_d("Or maybe not.\n")
        poison_query = True  # This will later prompt poison selection
    elif inventory_answer == "3":  # Knife.
        p_d("A striking choice. It may seem fitting for your new role.")
        p_d("You attach the ceremonial sheath to your belt.\n")
        game["adari_knife"] = 1  # Gives you Adari knife
    if game["adari_knife"] == 1:
        p_d("Will you bring any other lethal force?")
        knife_chosen_options = [
            "  1. No, nothing else.",
            "  2. Special poisons, disguised as fragrance sachets."
            ]
        knife_chosen_answer = make_choice(knife_chosen_options)
        if knife_chosen_answer == "1":  # Nothing else
            p_d("So be it.")
        elif knife_chosen_answer == "2":  # Poison
            p_d("Many Khell and Adari wear a fragrance sachet")
            p_d("in an inner pocket. But more than one is unusual.")
            p_d("If searched, you may be able to pass off two as whimsy.")
            p_d("Or maybe not.\n")
            poison_query = True  # This will later prompt poison selection
    if poison_query:
        p_d("What do you bring?")
        poison_options = [
            "  1. One sachet of poison that only works on Adari.",
            "  2. One sachet of poison that only works on Khell.",
            "  3. Two sachets of poison, one of each type.",
            "  4. On second thoughts, you don’t bring any poison."
            ]
        poison_answer = make_choice(poison_options)
        if poison_answer == "1":  # Adari poison
            p_d("Your people developed this substance in secret.")
            p_d("A little causes illness; half or more causes death.")
            p_d("You think the Khell don't even know targeted poisons exist.")
            p_d("You handle it carefully, hoping you won’t need it.")
            game["adari_poison"] = 1  # Gives you Adari poison
        elif poison_answer == "2":  # Khell poison
            p_d("Your people developed this substance in secret.")
            p_d("A little causes illness; half or more causes death.")
            p_d("You think the Khell don't even know targeted poisons exist.")
            p_d("You don’t know if you’ll need to use this against them.")
            p_d("But better to have it than want it.")
            game["khell_poison"] = 1  # Gives you Khell poison
        elif poison_answer == "3":  # Both poisons
            p_d("Your people developed these substances in secret.")
            p_d("A little causes illness; half a sachet or more causes death.")
            p_d("You think the Khell don't even know targeted poisons exist.")
            p_d("With both Khell and Adari poisons in your possession,")
            p_d("interesting options for trickery open up.")
            p_d("You’ll just have to make sure you’re not caught.")
            game["adari_poison"] = 1  # Gives you Adari poison
            game["khell_poison"] = 1  # Gives you Khell poison
        elif poison_answer == "4":  # No poison
            p_d("Perhaps you’re better off without such things.")
            if not game["adari_knife"]:
                game["travel_light"] = 1  # You brought nothing
    if poison_query and game["adari_knife"] != 1:  # Want poison & knife?
        p_d("Will you bring any other lethal force?")
        poison_chosen_options = [
            "  1. No, nothing else.",
            "  2. A traditional Adari knife, worn openly."
            ]
        poison_chosen_answer = make_choice(poison_chosen_options)
        if poison_chosen_answer == "1":  # Nothing else
            p_d("So be it.")
            if not game["adari_poison"] and not game["khell_poison"]:
                game["travel_light"] = 1  # You brought nothing
        elif poison_chosen_answer == "2":  # Knife.
            p_d("A striking choice. It may seem fitting for your new role.")
            p_d("You attach the ceremonial sheath to your belt.")
            game['adari_knife'] = 1  # Gives you Adari knife
            game["travel_light"] = 0  # You brought something
    p_d("Your preparations complete, you walk to your door...")
    p_d("...before the Runeguards can summon you.\n")
    pause()
    inc_game_value("checkpoint", 1)
    save_game()
    governor_arrives()


def governor_arrives():
    """
    Story content for the Governor's arrival.
    """
    print("┌───── •✧✵✧• ─────┐")
    print("    DAY 1: NOON ")
    p_d("└───── •✧✵✧• ─────┘\n")
    p_d("You arrive at the Governor’s Palace as the sun reaches its zenith.")
    p_d("This day is only half over. It’s already the longest of your life.")
    p_d("Runeguards escort you to the teleportation circle in the main hall.")
    p_d("Only Khell sorcerers are capable of using such things.\n")
    # Checks for Khell uniform, but no knife
    if game["khell_uniform"] == 1 and game["adari_knife"] == 0:
        if not game["under_duress"]:
            p_d("The Prefect gives you a small nod.")
            p_d("“I see you’re ready to carry out your duty, Adjunct.”")
            p_d("What do you say?")
            uni_loyal_options = [
                "  1. “Of course, Prefect.”",
                "  2. “I have no idea what my duties are.”"
                ]
            uni_loyal_answer = make_choice(uni_loyal_options)
            if uni_loyal_answer == "1":
                p_d("“Good,” she says, looking away.")
            elif uni_loyal_answer == "2":
                p_d("You see the barest flicker of rueful sympathy.")
                p_d("“Of course you don’t. How are you supposed to know?")
                p_d("No Governor has ever asked such a thing.”")
                p_d("She looks away.")
            p_d("“Just make sure to treat him with the necessary respect.”")
        else:
            p_d("The Prefect glances at you with measured distaste.")
            p_d("“I hope you’re ready to carry out your duty, Adjunct.”")
            p_d("What do you say?")
            uni_disloyal_options = [
                "  1. “Of course, Prefect.”",
                "  2. “I have no idea what my duties are.”"
                ]
            uni_disloyal_answer = make_choice(uni_disloyal_options)
            if uni_disloyal_answer == "1":
                p_d("Her mouth twists down when you profess loyal obedience.")
            elif uni_disloyal_answer == "2":
                p_d("“Obey. That’s all you need to know.”")
                p_d("After a moment, reluctantly, she adds:")
            p_d("“Make sure you treat him with the necessary respect.”")
    # Checks for Adari clothing, but no knife
    elif game["adari_outfit"] == 1 and game["adari_knife"] == 0:
        if not game["under_duress"]:
            p_d("The prefect looks you up and down.")
            p_d("Her eyes linger on a unique detail of your clothing.")
            p_d("“Do you think this... costume is wise?”")
            p_d("How do you answer?")
            adari_loyal_options = [
                "  1. Defend your choice.",
                "  2. Side-step the issue."
                ]
            adari_loyal_answer = make_choice(adari_loyal_options)
            if adari_loyal_answer == "1":
                p_d("“I’m to be a cultural advisor,” you point out.")
                p_d("“I should look like one.”\n")
                p_d("She raises an eyebrow at that.")
            elif adari_loyal_answer == "2":
                p_d("“I’m sure you have more important concerns")
                p_d("than my choice of attire.”\n")
                p_d("She ignores this attempt at redirection.")
            p_d("“Your role is to tell the Governor about the Adari.")
            p_d("Or so I assume. You don’t have to dress like one.")
            p_d("But no matter. He’ll be here soon.”")
        else:
            p_d("Seeing your clothing, the Prefect stares in disbelief.")
            p_d("“What’s the meaning of this preposterous costume?”")
            p_d("How do you answer?")
            adari_disloyal_options = [
                "  1. Defend your choice.",
                "  2. Side-step the issue."
                ]
            adari_disloyal_answer = make_choice(adari_disloyal_options)
            if adari_disloyal_answer == "1":
                p_d("“I’m to be a cultural advisor,” you point out.")
                p_d("“I should look like one.”\n")
                p_d("She raises an eyebrow at that.")
            elif adari_disloyal_answer == "2":
                p_d("“I’m sure you have more important concerns")
                p_d("than my choice of attire.”\n")
                p_d("She ignores this attempt at redirection.")
            p_d("“Your role is to tell the Governor about the Adari.")
            p_d("Not to dress like one.")
            p_d("I’ll remember your insolence.”")
    # Checks for Khell uniform and Adari knife
    elif game["khell_uniform"] == 1 and game["adari_knife"] == 1:
        p_d("The Prefect stares at your knife. “You cannot wear that.”\n")
        p_d("What do you say?")
        knife_uniform_options = [
            "  1. “If you wish, Prefect, I’ll remove it.”",
            "  2. “What if I need it to protect the Governor?”",
            "  3. “This is a cultural symbol, worn as a gesture of respect.”",
            "  4. “Imperial uniform code permits a side-weapon.”"
            ]
        knife_uniform_answer = make_choice(knife_uniform_options)
        if knife_uniform_answer == "1":  # Acquiesce.
            p_d("“I do wish,” she says. “Hand it over, Adjunct.”")
            game["knife_taken"] = 1
        elif knife_uniform_answer == "2":  # Cite the Governor's safety.
            p_d("“You won’t,” she says. “That’s our job. Hand it over.”")
            game["knife_taken"] = 1
        elif knife_uniform_answer == "3":  # Cite culture.
            p_d("“Irrelevant,” she says. “Hand it over, Adjunct.”")
            game["knife_taken"] = 1
        elif knife_uniform_answer == "4":  # Object on a technicality.
            p_d("The Prefect blinks in seeming disbelief. Then she says:")
            p_d("“Code envisages a Khell weapon. Not some trinket.”\n")
            if not game["under_duress"]:
                p_d("You reply: “Respectfully, that’s not specified.”")
                p_d("Then, daringly, you add: “I humbly submit")
                p_d("that such weapons, worn with Imperial dress,")
                p_d("represent the Adari in loyal service of the Khell.”\n")
                p_d("The Prefect looks at you for a long moment.")
                p_d("Then she shrugs. “Very well. You may wear it.")
                p_d("But do not test me again, Adjunct.”")
            else:
                p_d("You reply: “Respectfully, that’s not specified.”\n")
                p_d("With a cold glare, the Prefect steps close to you.")
                p_d("Lowering her voice for your ears only, she says:")
                p_d("“You made me force this duty upon you, Adjunct.")
                p_d("Do not try to teach me the meaning of respect.”\n")
                game["knife_taken"] = 1
    # Checks for Adari clothing and Adari knife, 1 fewer option vs. uniform
    elif game["adari_outfit"] == 1 and game["adari_knife"] == 1:
        p_d("The Prefect stares at your knife. “You cannot wear that.”\n")
        p_d("What do you say?")
        knife_uniform_options = [
            "  1. “If you wish, Prefect, I’ll remove it.”",
            "  2. “What if I need it to protect the Governor?”",
            "  3. “This is a cultural symbol, worn as a gesture of respect.”"
            ]
        knife_uniform_answer = make_choice(knife_uniform_options)
        if knife_uniform_answer == "1":  # Acquiesce.
            p_d("“I do wish,” she says. “Hand it over, Adjunct.”")
            game["knife_taken"] = 1
        elif knife_uniform_answer == "2":  # Cite the Governor's safety.
            p_d("“You won’t,” she says. “That’s our job. Hand it over.”")
            game["knife_taken"] = 1
        elif knife_uniform_answer == "3":  # Cite culture.
            p_d("“Irrelevant,” she says. “Hand it over, Adjunct.”")
            game["knife_taken"] = 1
    if game["knife_taken"]:
        p_d("You have no choice but to give her the knife.")
        p_d("She hands it to a subordinate.\n")
    p_d("You gather around the teleportation circle.")
    p_d("A ripple distorts the air. Then a radiant rift opens.")
    p_d("A man steps through the portal and closes it behind him.\n")
    p_d("By his patrician Khell features and his use of magic,")
    p_d("you know this must be Governor Ekkano.")
    p_d("But you're surprised that he comes alone.")
    p_d("You expected someone of his rank to bring a vast entourage.\n")
    p_d("Ekkano’s gaze sweeps past you all.")
    p_d("Speaking formally, he proclaims:")
    p_d("“I come to claim dominion over Adar, as granted by Xeth,")
    p_d("Emperor of the Khell and all their subjects.”")
    p_d("He pauses, as if to let his power rest over your land.")
    p_d("Then he turns his attention to those who await him.\n")
    pause()
    p_d("“Greetings, Prefect,” Ekkano says.")
    p_d("“Loyal warriors of the Runeguard:")
    p_d("I will count on your service in the years to come.”")
    p_d("He glances at you, then back to the Prefect. “This is the one?”\n")
    p_d("“Yes, Ekkano,” she replies.\n")
    p_d("“Good,” he says.  “I’ll meet the bureaucracy tomorrow.”")
    p_d("Then he gestures in your direction. “Counsellor, with me.”")
    p_d("With that, he strides off.\n")
    p_d("“Adjunct,” the Prefect says sharply - not to you, but to Ekkano.\n")
    p_d("He stops, then slowly turns back.\n")
    p_d("“Your advisor is an Adjunct,” the Prefect clarifies.")
    p_d("You think you hear a note of fear in her voice.\n")
    p_d("Ekkano simply looks at her.\n")
    pause()
    p_d("The silence stretches. Then the Prefect lowers her head.")
    p_d("“Was an Adjunct,” she murmurs. “But is now a Counsellor.”\n")
    knife_chat_guard = False
    knife_chat_gov = False
    knife_chat_pref = False
    if not game["knife_taken"]:
        p_d("Ekkano nods. “Come,” he tells you, then turns to leave.")
        p_d("You follow him out.\n")
    else:
        p_d("Ekkano nods. Turning back, he spots the guard with your knife.")
        p_d("Looking at the weapon, he asks: “Is this Adari work?”\n")
        p_d("“Yes, Ekkano.” Bowing, the guard holds out your knife.\n")
        p_d("The Governor doesn’t take it. “Is it yours?”\n")
        p_d("“No, Ekkano. It belongs to the, uh, Counsellor.”\n")
        p_d("“I see. Then return it to the Counsellor.”\n")
        p_d("The guard bows again - and, without seeking")
        p_d("the Prefect’s approval, gives you back your weapon.")
        p_d("Do you say anything?\n")
        knife_back_options = [
            "  1. No - stay silent.",
            "  2. Speak to the guard who had your knife.",
            "  3. Speak to the Governor.",
            "  4. Speak to the Prefect."
            ]
        knife_back_answer = make_choice(knife_back_options)
        if knife_back_answer == "1":  # No further knife chat.
            p_d("“Come, Counsellor,” Ekkano tells you.")
            p_d("You follow him out.\n")
        elif knife_back_answer == "2":  # Guard.
            p_d("What do you say to the guard?")
            knife_chat_guard = True
        elif knife_back_answer == "3":  # Governor.
            p_d("What do you say to Ekkano?")
            knife_chat_gov = True
        elif knife_back_answer == "4":  # Prefect.
            p_d("What do you say to the Prefect?")
            knife_chat_pref = True
    if knife_chat_guard:
        guard_chat_options = [
            "  1. “Thank you.”",
            "  2. “As it should be.”",
            "  3. “Keep it if you wish.”"]
        guard_chat_answer = make_choice(guard_chat_options)
        if guard_chat_answer == "1":  # Thank the guard.
            p_d("The guard acknowledges you with a nod.")
            p_d("“Come, Counsellor,” Ekkano says. “There’s much to do.”")
            p_d("He turns to leave. You follow him out.\n")
        elif guard_chat_answer == "2":  # Be smug.
            p_d("Out of the corner of your eye, you see the Prefect twitch.")
            p_d("“Come, Counsellor,” Ekkano says. “There’s much to do.”")
            p_d("He turns to leave. You follow him out.\n")
        elif guard_chat_answer == "3":  # Offer knife back.
            p_d("“We’ve no time for this,” Ekkano says, turning to leave.")
            p_d("You hesitate for a moment.")
            p_d("Then you return the knife to your belt and follow him out.\n")
    elif knife_chat_gov:
        gov_chat_options = [
            "  1. “Thank you, Ekkano.”",
            "  2. “Thank you, Governor.”",
            "  3. “Far be it from me to take a weapon from the Runeguard.”"]
        gov_chat_answer = make_choice(gov_chat_options)
        if gov_chat_answer == "1":  # Use Gov name, correct protocol.
            p_d("Waving off your thanks, he turns to leave.")
            p_d("You follow him out.\n")
        elif gov_chat_answer == "2":  # Fail to call Gov by his name.
            p_d("You hear sharp intakes of breath all around you.\n")
            p_d("Ekkano’s gaze turns icy.")
            p_d("“I have the right to my Name. Counsellor.”\n")
            game["offended_gov"] = 1
        elif gov_chat_answer == "3":  # Vaguely offer knife back.
            p_d("“They have enough,” he replies. “Come, there’s much to do.”")
            p_d("He turns to leave. You follow him out.\n")
    elif knife_chat_pref:
        pref_chat_options = [
            "  1. “My apologies, Prefect.”",
            "  2. “I’m glad we could resolve this, Prefect.”",
            "  3. “This knife will serve Ekkano well, Prefect. I promise.”"]
        pref_chat_answer = make_choice(pref_chat_options)
        if pref_chat_answer == "1":  # Say sorry to Prefect.
            p_d("“Doing Ekkano’s will requires no apology,” she replies.")
            p_d("You could almost believe she didn’t ask you to spy on him.\n")
            p_d("“Indeed,” the Governor says. “Now, Counsellor, come.”")
            p_d("He turns to leave. You follow him out.\n")
        elif pref_chat_answer == "2" or pref_chat_answer == "3":  # Mind-games.
            p_d("She gives you a nod that almost looks gracious.")
            p_d("But you know what’s underneath.")
            p_d("“Come,” Ekkano tells you, turning to leave.")
            p_d("You follow him out.\n")
    if game["offended_gov"]:
        offended_options = [
            "  1. “Of course, Ekkano. I misspoke.”",
            "  2. “Forgive me. I’ve never been in the presence of a Name.”",
            "  3. “Do you?”"]
        offended_answer = make_choice(offended_options)
        if offended_answer == "1":  # You salvage the situation.
            p_d("He nods. “Very well. Now, with me.”")
            p_d("He turns to leave, and you follow him out.\n")
        elif offended_answer == "2":  # Not terrible, not great.
            p_d("He doesn’t quite seem appeased. Yet he doesn’t gainsay you.")
            p_d("“We’ll speak of this later.  Now, with me.”")
            p_d("He turns to leave, and you follow him out.\n")
            game["offended_gov"] = 2
        elif offended_answer == "3":  # This is the worst thing you can say.
            p_d("Anger flashes across his face.")
            p_d("Some of the Runeguards reach for their weapons.")
            p_d("But the Governor gives the Prefect a firm shake of his head.")
            p_d("She raises her hand, and the guards relax.\n")
            p_d("Ekkano says: “I hope you’re not as ignorant of Adari ways")
            p_d("as you are of the Khell. Or I will have no use for you.”")
            p_d("He tells the Prefect: “Assemble a list of other candidates.”")
            p_d("Then he sweeps out of the room.\n")
            game["offended_gov"] = 3
            inc_game_value("trust_gov", -2)
            inc_game_value("legitimacy", -1)
            p_d("[Governor’s Legitimacy has reduced by 1.]")
            new_score = game["trust_gov"]
            p_d(f"[The new score is: {new_score}.]")
            print("")
            # To some, the governor seems weak for not punishing this insult
            p_d("For a moment, you pause, frozen.")
            p_d("Then you follow him, lengthening your stride to keep up.\n")
    pause()
    inc_game_value("checkpoint", 1)
    save_game()
    cultural_advice()


def cultural_advice():
    """
    Story content in which the Governor seeks cultural advice
    """
    print("┌───── •✧✵✧• ─────┐")
    print(" DAY 1: AFTERNOON")
    p_d("└───── •✧✵✧• ─────┘\n")
    p_d("As far as you know, Ekkano has never been in Adar,")
    p_d("let alone in the Governor’s Palace.")
    p_d("Yet he walks straight to his office, without needing directions.\n")
    p_d("On arriving, he shuts the door behind you with a minor spell.")
    p_d("You try not to let his casual use of magic unsettle you.")
    p_d("He pauses for a moment, as if listening to something you can’t hear.")
    p_d("Then he nods, seeming satisfied.\n")
    if game["offended_gov"] == 3:
        p_d("When he turns to you, however, his look is grim.")
        p_d("“Before anything else, Counsellor, let me be clear.")
        p_d("Any public affronts to me are affronts to our Emperor, Xeth.")
        p_d("In front of the Khell, you will always address me by Name.”\n")
        p_d("On this point, he clearly won’t be moved.")
        p_d("What do you say?")
        mollify_gov_options = [
            "  1. “I understand.”",
            "  2. “Just in front of the Khell?”"
            ]
        mollify_gov_answer = make_choice(mollify_gov_options)
        if mollify_gov_answer == "1":
            p_d("He nods, seeming to consider the matter closed.\n")
        elif mollify_gov_answer == "2":
            p_d("“Yes,” he says. “With others, speak as you will.")
            p_d("It may not be wise. But I’m not your chaperon.”")
            p_d("With that, he seems to consider the matter closed.\n")
    p_d("Ekkano goes to sit at his desk.")
    p_d("He gestures that you may also sit, if you wish.")
    posture_options = [
        "  1. Sit.",
        "  2. Stay standing."]
    posture_answer = make_choice(posture_options)
    if posture_answer == "1":
        p_d("You take a seat. May as well enjoy what comforts you can.")
    elif posture_answer == "2":
        p_d("You keep a formal posture. He doesn’t seem to mind.")
    p_d("“Counsellor,” he says. “I know little of Adar and its people.")
    p_d("I want that to change. You are to help me.")
    p_d("At first, I’ll have general questions.")
    p_d("But I do not know what it is that I don’t know.”")
    p_d("He seems frustrated by this limitation.")
    p_d("“If I ask something, and there’s a better question,")
    p_d("you are to tell me. And answer it. Do you understand?”\n")
    p_d("Your true mission is to get information, not give it.")
    p_d("Yet this is an intriguing opportunity.")
    p_d("If you plant the right information in Ekkano’s mind...")
    p_d("...or misinformation, even... who knows what might happen?\n")
    p_d("What do you say?")
    scope_options = [
        "  1. “Yes, Ekkano. At least, I think I understand.”",
        "  2. You shake your head. “This is all happening so quickly.”",
        "  3. “Most Khell don’t care about Adari culture. Why do you?”",
        "  4. “What will you do with this knowledge?”"]
    scope_answer = make_choice(scope_options)
    if scope_answer == "1":
        p_d("“Good,” he says. “Then let’s proceed.”\n")
    elif scope_answer == "2":
        p_d("He looks away. “I understand this is quite a change for you.")
        p_d("But events in the world are moving quickly.")
        p_d("I don’t have time to let anyone adjust.”\n")
        p_d("You may not know what he’s talking about.")
        p_d("But even a hint is better than nothing.")
        # Info gain +1
        inc_game_value("information", 1)
        p_d("[Information has increased by 1.]")
        p_d(f"[The new score is: {game['information']}.]")
        print("")
    elif scope_answer == "3":
        p_d("His face is unreadable. “I have my reasons.”")
        p_d("It seems you won’t be learning them - at least, not today.\n")
    elif scope_answer == "4":
        p_d("He smiles faintly. “You’ll see, Counsellor.”\n")
    p_d("With that, the questions begin. Hours of them.")
    p_d("Ekkano quizzes you exhaustively about Adari traditions.")
    p_d("Language. Art. History. Religion. Songs and stories.")
    p_d("The things he asks clearly show him as an outsider.")
    p_d("But you’ve never had a more attentive student.\n")
    p_d("How do you answer?")
    sentimental_story = False
    culture_options = [
        "  1. Honestly and comprehensively, as he ordered.",
        "  2. Honestly, but not in great depth.",
        "  3. Selectively, focusing on sympathetic Adari qualities.",
        "  4. With a mix of misleading and false information."]
    culture_answer = make_choice(culture_options)
    if culture_answer == "1":
        p_d("You delve into all manner of subjects as the hours pass.")
        p_d("It feels a strange to speak of these things to a Khell.")
        p_d("And not just any Khell, but the Governor of your land.")
        p_d("Yet there’s something oddly freeing about it too.\n")
        p_d("At length, he holds up a hand. “Enough.”")
        p_d("He looks more energized than tired.")
        inc_game_value("trust_gov", 1)
        # Gov trust +1, he learned a lot and enjoyed it
    elif culture_answer == "2":
        p_d("You cover a wide range of subjects, and you never lie.")
        p_d("But you try not to say too much about any one thing.")
        p_d("You have no idea why he wants any of this.")
        p_d("Until you know more, better to hold back.\n")
        p_d("At length, he holds up a hand. “Enough.”")
        p_d("His eyes are full of thoughts.")
    elif culture_answer == "3":
        p_d("You paint a poignant picture of your people.")
        p_d("Joy and sorrow. Heroes and lovers. Sacrifice and triumph.")
        p_d("With every word, you try to show your past is worth remembering.")
        p_d("\nThe longer you continue, the fewer questions Ekkano asks.")
        p_d("At length, he holds up a hand.")
        p_d("“You tell fine stories, Counsellor. There is... beauty to them.")
        p_d("It’s plain that you love your people.”")
        p_d("Strangely, for a Khell, that doesn’t sound like an accusation.")
        p_d("“Yet... realism is a virtue too, is it not?”\n")
        inc_game_value("trust_gov", 1)
        # Gov trust +1, he's moved and a bit sympathetic
        sentimental_story = True
    elif culture_answer == "4":
        p_d("Ekkano has no way of knowing what’s true or false here.")
        p_d("You are quite literally the best source he has.")
        p_d("What he learns from you must not hurt your people.")
        p_d("So you weave a web of implication and deceit,")
        p_d("hiding Adari strengths and vulnerabilities alike.\n")
        p_d("At length, the Governor holds up a hand. “Enough.”")
        p_d("Fatigue is written on his face.")
        p_d("“It’s hard to make sense of all this. Still, I will persist.”")
    story_message = False
    if sentimental_story:
        p_d("How do you answer?")
        sentiment_options = [
            "  1. Stand by your portrayal of the Adari.",
            "  2. Acknowledge some artistic license.",
            "  3. Distinguish between past and present."]
        sentiment_answer = make_choice(sentiment_options)
        if sentiment_answer == "1":
            p_d("“Realism is about acknowledging the truth.” You pause.")
            p_d("“Nothing seems more true to me than what I’ve told you.”")
            p_d("Slowly, he nods, but makes no other reply.\n")
        elif sentiment_answer == "2":
            p_d("You give a small shrug. “Art always has a message.”")
            p_d("He smiles slightly. “And what is your message, Counsellor?”")
            story_message = True
        elif sentiment_answer == "3":
            p_d("“I see no harm in looking back with fond eyes.” You pause.")
            p_d("“At present, the Khell have enough realism for all of us.”")
            p_d("\nThe Governor raises an eyebrow. But he only says:")
            p_d("“The Adari know how to be pragmatic as well.”")
            p_d("To this, you make no reply.\n")
    if story_message:
        message_options = [
            "  1. Tell him.",
            "  2. Let him decide."]
        message_answer = make_choice(message_options)
        if message_answer == "1":
            p_d("You’re walking a dangerous path. Still, you say: “Hope.”")
            p_d("To this, he makes no reply.\n")
        elif message_answer == "2":
            p_d("“I think what matters most is the message you take from it.”")
            p_d("To this, he makes no reply.\n")
    p_d("By now, the sun is low in the sky.")
    p_d("Ekkano stands. “That’s enough for today.")
    p_d("But I may summon you again at any time.")
    p_d("Have them prepare quarters for you in the Palace.")
    p_d("You’ll stay here until your service is done.”\n")
    p_d("You blink. This is both an opportunity and a liability.")
    p_d("How do you answer?")
    home_options = [
        "  1. Accept.",
        "  2. Refuse."]
    home_answer = make_choice(home_options)
    if home_answer == "1":
        p_d("“As you wish, Ekkano.”")
        p_d("He nods, then conjures the door open.")
    elif home_answer == "2":
        p_d("“It would be better if I stay at home.”\n")
        p_d("The Governor shakes his head. “This isn’t a request.")
        p_d("If you need your things, have the Runeguard bring them here.”")
        p_d("\nThe thought of Runeguards in your home chills your blood.")
        p_d("You keep your secret records and equipment well-disguised.")
        p_d("But they might still find something.")
        p_d("You won’t ask them to fetch anything.")
        equip = "You’ll have to make do with what you brought this morning.\n"
        if not game["travel_light"]:
            p_d(equip)  # Stored in string due to line length
        else:
            p_d("Even though you brought no equipment this morning.\n")
        p_d("Ekkano conjures the door open.")
    p_d("It seems you’re meant to see yourself out.")
    leave_options = [
        "  1. Leave.",
        "  2. Linger."]
    leave_answer = make_choice(leave_options)
    if leave_answer == "1":
        p_d("You go, passing two Runeguards stationed outside.")
        p_d("The door closes behind you.")
    elif leave_answer == "2":
        p_d("You walk to the door, then pause and look back.")
        p_d("It seems Ekkano’s already stopped paying attention to you.")
        p_d("Light gathers in his palms as he draws on magic.")
        p_d("In ancient myths, wizards were said to use words of power.")
        p_d("But real magic, the kind the Khell use to conquer,")
        p_d("is utterly silent, known only by its effects.")
        p_d("For a moment, you watch, mentally noting what you see.\n")
        inc_game_value("information", 1)  # Info gain +1
        p_d("[Information has increased by 1.]")
        p_d(f"[The new score is: {game['information']}.]")
        print("")
        p_d("Then the Governor seems to realize you haven’t left.")
        p_d("Meeting your eyes briefly, he gestures for you to go.")
        p_d("What do you do?")
        pry_options = [
            "  1. Leave.",
            "  2. Ask him something."]
        pry_answer = make_choice(pry_options)
        if pry_answer == "1":
            p_d("You go, passing two Runeguards stationed outside.")
            p_d("Facing away from the room, it’s doubtful they saw any magic.")
            p_d("The door closes behind you.")
        elif pry_answer == "2":
            p_d("You begin to form a question, but he shakes his head.")
            p_d("“Not now,” he says. “Remind me later, if it matters.”\n")
            p_d("He seems intent on his sorcery, so you don’t argue.")
            p_d("Leaving, you pass two Runeguards stationed outside.")
            p_d("Facing away from the room, it’s doubtful they saw any magic.")
            p_d("The door closes behind you.")
    p_d("You walk through the Palace, trying to look like you belong here.")
    p_d("In fact, you do belong. More than any of the Khell.\n")
    p_d("Adari built this place, but they do not live here.")
    p_d("Your request for a room thus elicits surprise.")
    p_d("But no one wishes to disobey the Governor.")
    p_d("(Perhaps you can find ways to leverage that.)\n")
    pause()
    p_d("Before long, you are brought to a dusty basement room.")
    p_d("Boxes of old documents have been hastily piled to one side.")
    p_d("For your comfort, there is only a camp bed and a basin.")
    if posture_answer == "1":  # After sitting, you have energy to read a bit
        p_d("Undignified lodgings, yet they suit you well.")
        p_d("You do your best work when you’re beneath notice.")
        p_d("As such, you take a box of records and start reading.")
        p_d("Most of the data is unimportant, obsolete, or both.")
        p_d("Yet some of it provides vital context for old intelligence.")
        inc_game_value("information", 1)  # Info gain +1
        p_d("[Information has increased by 1.]")
        p_d(f"[The new score is: {game['information']}.]")
        inc_game_value("basement_info", 1)   # Got some info from basement docs
        print("")
        p_d("Satisfied, you return everything to its original place.")
        p_d("Then you lie down, and sleep takes you at once.\n")
    elif posture_answer == "2":  # You're exhausted from standing for hours
        p_d("Still, you’re so weary that you lie down at once.")
        p_d("For bedtime reading, you grab the closest document to hand.")
        p_d("Perhaps it could hold useful intelligence.")
        p_d("But, before you can read three sentences, sleep takes you.\n")
    pause()
    inc_game_value("checkpoint", 1)
    save_game()
    second_morning()


def second_morning():
    """
    Story content in which the player seeks intel or makes a report.

    Development postponed until time permits the addition of content.
    """
    name = game["name"]
    p_d("")
    decoration()
    p_d(f"For now, {name}, your mission pauses.")
    p_d(f"The level of information you gained is: {game['information']}.")
    p_d("Await further developments before you continue.\n")
    decoration()
    # This is the end of current game content.


def start_game():
    """
    Begins a new game, called at the end of run.py.

    Prints the game logo.
    Lets the user choose whether to play the game.
    If the user declines: acknowledges this.
    If the user chooses to play: requests a username;
    lets the user choose whether to read establishing text;
    lets the user choose where to read gameplay info;
    and begins the story proper.
    """
    print('''\033[38;2;104;95;143m
██████╗  ██████╗ ██╗   ██╗██████╗ ██╗     ███████╗ \033[38;2;114;117;160m
██╔══██╗██╔═══██╗██║   ██║██╔══██╗██║     ██╔════╝ \033[38;2;124;139;176m
██║  ██║██║   ██║██║   ██║██████╔╝██║     █████╗   \033[38;2;134;154;178m
██║  ██║██║   ██║██║   ██║██╔══██╗██║     ██╔══╝   \033[38;2;144;169;180m
██████╔╝╚██████╔╝╚██████╔╝██████╔╝███████╗███████╗ \033[38;2;194;224;233m
╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝╚══════╝ \033[38;2;194;224;233m
                                                   \033[38;2;170;198;208m
     █████╗  ██████╗ ███████╗███╗   ██╗████████╗   \033[38;2;144;169;180m
    ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝   \033[38;2;134;154;178m
    ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║      \033[38;2;124;139;176m
    ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║      \033[38;2;114;117;160m
    ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║      \033[38;2;104;95;143m
    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝\033[0m\n''')
    # Lets the user choose whether to play the game.
    play_chosen = yes_no("Agent, do you wish to play?")
    if play_chosen:
        p_d("Welcome to a game of swords, sorcery, and spies.")
    else:
        p_d("Acknowledged.")
        p_d("If you cannot say no, then your yes has no meaning.")
        p_d("Farewell, Agent.")
    # Requests a username, applying various checks
    name_chosen = False
    while play_chosen and not name_chosen:
        input_n = get_string("Agent, what is your name?")
        if input_n:
            # If name is all numbers, skip capitalization check
            if input_n.isdecimal():
                game["name"] = input_n
            # If name's first letter(s) not capitalized, confirm
            elif not input_n.istitle():
                cap_n = " ".join(str.capitalize() for str in input_n.split())
                cap_chosen = yes_no(f"Render “{input_n}” as “{cap_n}”?")
                if cap_chosen:
                    game["name"] = cap_n
                else:
                    game["name"] = input_n
            else:
                game["name"] = input_n
        if game["name"]:
            name = game["name"]
            name_chosen = True
    # Chosen username is now in the "game" dictionary, which can now
    # generate a full set of savegame data for the current user.
    # Current username is sought in the name column of the savegame sheet.
    savegame_found = False
    new_game = False
    if name_chosen:
        username = game["name"]
        savegame_found = check_game(username)
    if savegame_found:
        p_d(f"{username}, your file is on record.")
        load_options = [
            "  1. Begin a new mission.",
            "  2. Continue existing mission."
            ]
        load_answer = make_choice(load_options)
        if load_answer == "1":
            save_game()  # Overwrites old save data
            p_d("New mission acknowledged.\n")
        elif load_answer == "2":  # Load savegame to "game"
            load_game()
            p_d(f"Welcome back, {username}...")
    else:
        if play_chosen:
            print("")
            new_game = True
            p_d(f"{name}, you come to the crossroads of your life.")
            p_d("Tread carefully or boldly. See where your steps take you.\n")
    if play_chosen:
        speed_change = yes_no("Do you wish to change text speed?")
        if speed_change:
            change_speed()
        else:
            p_d("Current speed accepted.\n")
    if play_chosen:
        read_brief = yes_no("Do you wish to read a briefing?")
        if read_brief:
            show_briefing()
        else:
            p_d("Briefing declined.\n")
    if play_chosen:
        read_gameplay = yes_no("Do you wish to know how to play?")
        if read_gameplay:
            show_how_to_play()
        else:
            p_d("Information declined.\n")
    if play_chosen and new_game:
        new_savegame()  # Creates a new savegame entry for the user
    if play_chosen:
        current_checkpoint = game["checkpoint"]
        if current_checkpoint == 1:
            first_morning()
        elif current_checkpoint == 2:
            governor_arrives()
        elif current_checkpoint == 3:
            cultural_advice()
        elif current_checkpoint == 4:
            second_morning()
        else:
            print("───MISSION START───\n")
            opening_scene()


start_game()
