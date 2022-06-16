# Double Agent: A Text-Based RPG
## by Siobhán Mooney

### [Click here to view the deployed app.](https://double-agent-rpg.herokuapp.com/)
### [Click here to view the repository.](https://github.com/Estelindis/double-agent-rpg)

# Table of Contents:
1. [About the project](#about-the-project)
    1. [User Goals](#user-goals)
    2. [Owner Goals](#owner-goals)
2. [Narrative and Visual Design](#design-and-visual-design)
    1. [Narrative](#narrative)
    2. [Typography](#typography)
    3. [Colours](#colours)
3. [Code Design](#code-design)
    1. [Text Input and Display](#text-input-and-display)
    2. [Story Functions](#story-functions)
    3. [Savegame System](#savegame-system)
4. [Data Model](#data-model)
5. [Testing, Bugs, and Fixes](#testing-bugs-and-fixes)
    1. [PEP8 Testing](#pep8-testing)
6. [Future Features](#future-features)
7. [Deployment](#deployment)
    1. [Deploying to Heroku](#deploying-to-heroku)
    2. [Forking the Repository on GitHub](#forking-the-repository-on-github)
    3. [Cloning the Repository on GitHub](#cloning-the-repository-on-github)
8. [Used technologies and credits](#used-technologies-and-credits)
    1. [Languages](#languages)
    2. [Python Libraries](#python-libraries)
    3. [Other Technologies](#other-technologies)
    4. [Credits](#credits)


# About the project
Double Agent is a text-based RPG about engaging an oppressive power structure covertly from within.

## User Goals
- Explore espionage tropes, especially those involving trust, loyalty, and hidden agendas.
- Make thematically interesting choices and experience the consequences of these choices. 
- Read story text at a comfortable speed.
- Be able to save game data, so a playthrough can be resumed later.

## Owner Goals
- Present espionage tropes, combining them with fantasy tropes in an engaging manner.
- Provide a range of choices, keeping the user guessing as to what the consequences of these choices might be.
- Give the user options for controlling the speed at which new lines of text are displayed. 
- If the terminal fills up with text, allow the user to read the text at leisure before continuing.
- Provide a savegame system, so returning users don't have to start from the beginning unless they wish.
- Create a range of Python functions that will remain useful if/when the story is expanded in future.

# Narrative and Visual Design
As the project is intended to demonstrate Python principles, only minor edits have been made to the standard visual styling of the terminal's webpage. More time and attention have been dedicated to the principles of narrative design that emerge through the game's story.

## Narrative
- "Double Agent" uses a relatively linear story structure. This reflects the restrictive environment in which the player character operates.
- Aside from the optional background briefing, it is intended that setting information be conveyed in a manner as organic as possible rather than being "info-dumped." When setting information is conveyed as part of the story, further meaning should be imparted by the manner in which it is conveyed. For instance, if a non-player character informs the player character of something, this shows that the non-player character views (or at least presents) themselves as an authoritative source of information. Similarly, if the player character's thoughts provide setting information to the player, this shows what the player character is thinking about (and, perhaps, what the character wishes might be different).
- The restricted use of the username within the story is meant to convey the dehumanizing nature of the setting's imperialistic regime. After giving a username, the user may expect this name to be employed relatively often. In fact, however, the player character is generally addressed by a title. This suggests that the system in which the player character operates has little interest in "people," only in the functions they can carry out. The use of only two named (or "Named") non-player characters (one of them off-screen in the story as currently implemented) reinforces this impression. In planned future story content that was written in a separate document but not added to the current version of the game, the player character would have the option to reveal their name to a member of the Named ruling class. The relative lack of username use up to this point would make this moment emotionally impactful. Additionally, the use of a title for the player character allows the total avoidance of player character pronouns, which lets the user imagine their character as female, male, or non-binary.
- The narrative is designed with the use of a dictionary in mind, so that plot values changed by one function can be accessed from other functions (in addition to the savegame system that the "game" dictionary enables). The player character knows some of their tracked qualities, such as equipment and information. However, other tracked qualities are kept hidden, reflecting the imagined situation of a spy who doesn't fully know if they are trusted. 
- The player character is designed to have a position with a possibly vast yet hidden impact, while remaining vulnerable to the game's outwardly powerful non-player characters. The player character must choose wisely if they are to achieve personally important goals without suffering a grim fate. 
- When writing the player character's actions, thoughts, and dialogue, it is vital to show an internal independence of thought. The player character can choose to treat oppressive structures and individuals with outward respect and obedience. However, this should not have to imply any actual loyalty towards these forms of oppression. This decoupling of the player character's actions from their thoughts and feelings should strengthen the game's portrayal of espionage themes. Additionally, it should provides users with a sense of agency in a situation where the player character's agency is intentionally low.
- The personalities of the two key non-player-characters (the Prefect and the Governor) impact how much the player character's choices increase or decrease the trust of these characters. 
- The Prefect's trust depends on the player character obeying her orders and seeming loyal to the imperial culture and power structure. She will view scorn towards herself as scorn towards the Imperium, and therefore as disloyalty. This reflects the fact that, at present, her sense of self-worth comes from her role as a respected enforcer of the Emperor's will. In future versions of the game with more story content, that might change. The Prefect's trust can never be increased if the player only becomes a double agent under absolute duress. 
- The Governor's trust depends on how helpful and sympathetic the player character appears to him. He will trust a character who helps him achieve a particular goal (as yet unrevealed in the current version of the game), but distrust a character who impedes this goal. Additionally, due to a previous exile and the precariousness of his current position (again unrevealed in the current game), he feels isolated. If the player character appears to offer chances for emotional connection, his trust will be increased.
- The gameplay guide suggests that unfortunate consequences will take place if either form of trust is reduced to zero. Regrettably, however, the story content implemented in the current version of the game did not reach a point where trust could reach zero (which would trigger a range of "game over" functions depending on individual circumstances). The reference in the gameplay guide is left as is, to point towards the intended future state of the game.

## Typography
- The most striking visual element of the game is the starting logo. The ascii art was generated via [http://patorjk.com/](http://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=Double%0A%20Agent). This particular ascii "font" was chosen for its readability and because the shadow effect evokes the "double" aspect of the "Double Agent" title.

![Initial screenshot.](/assets/image-readme/screenshot01.jpg)

## Colours
- A gradient for the logo was generated via patorjk.com's [text colour fader utility](http://patorjk.com/text-color-fader/). As this utility generates HTML gradients, it was converted to Python manually, changing HEX values to RGB and following the guidelines under the heading ["ALL THE COLOURS" on Stack Overflow](https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences). The particular colours of the gradient were chosen to suggest a metallic gleam, lit by purple light.  This combination unifies the cold hardness of the espionage genre with the otherworldly aura of the fantasy genre, as appropriate to a story of "swords, sorcery, and spies."
- The colour of the "run program" button was changed to match the purple part of the game logo gradient.
- The background colour of the webpage was changed to a dark grey to reduce eye strain and complement the other game colours. A pure black background was not used, to ensure that the black terminal does not seem to merge with the background. It is intended the the user's attention should be drawn to the terminal rather than wandering around the page. 
- A background graphic, edited to match the colours of the logo, was tested. This graphic was not retained in the final version, as it was deemed distracting - literally, but also in a broader game design sense, as time could be spent on code than improving the background graphic. In a scenario with more development time, this decision could be revisited.

![Tested background.](/assets/image-readme/background_test.jpg)

# Code Design
Functions are designed with a view to forwards and backwards compatibility. Returning users with savegames from previous versions should be able to continue their story from where they left (or close). Future developers should be able to add further story content without writing new non-story functions.

## Text Input and Display
- The "get_string" function performs the first step in validating user input, screening for empty strings and excessive whitespace.
- The "make_choice" function uses "get_string" while further validating user input. It continues to run until it can return an input number associated with a option. Valid input depends on how many options are offered. See [below](#story-functions) for further comments on this function.
- The "p_d" function (which stands for "print, delay") prints a string followed by a delay. The conventionally suboptimal choice of a very short function name was made to enable longer text strings to be printed, as line lengths in Python (and the dimensions of the terminal) are quite restrictive for a text-based game. The idea to abbreviate the name of the function came from [Star Trek: Time Loop](https://github.com/DeannaCarina/StarTrekTimeLoop) by DeannaCarina. However, DeannaCarina's "P_S" function accepts two parameters: text and delay. Each string to be printed has its own individual delay. "Double Agent" instead controls the delay via a single value: "text_speed" in the "game" dictionary. This value is easily changed, after which all print-delayed strings use the new speed. As well as offering central control, this approach reduces the work that developers need to do when writing print-delayed strings.
- The "change_speed" function allows the user to choose one of four speeds for the print delay implemented by "p_d". The first three speed options are intended for text that is read as it is printed, offering a comfortable experience for users with a variety of reading speeds. The final speed option, for a 0.1 second delay, can be used to speed-run the game for testing purposes. It also offers a different way of reading story text: the text is printed extremely quickly, then read. The "pause" function is crucial to making this setting useful to ordinary users, as it would be irritating to have to scroll back up every time more than a terminal's worth of text is printed between user choices.
- The "pause" function allows the user to decide when to let the text resume scrolling.  As the pause is implemented via the "getpass" library, any input except Enter is not displayed. When Enter is displayed, the pause ends.  The "delete_line" function is then called to remove the pause prompt text, for a cleaner look in the terminal.
- Via the "start_game" function, the input username can be capitalized (if not already capitalized). This is optional, so that any intended unusual capitalization can be preserved, if desired. During the design phase, potential users were asked for their opinions on this feature. Would it be better to auto-implement capitalization to avoid one extra prompt, or check with the user? In response, one potential user commented: "I would prefer not to be corrected - not because I'd particularly want to not capitalize, but because I have grown to be deeply cranky about technology trying to pre-empt and assume what I want when I didn't ask for it. I may also have just had a long afternoon of fighting with Microsoft Word." In this context, a graphic comparing product features with user needs teaches a valuable lesson. Much time can be spent on features that users do not desire - and, indeed, may actively dislike. Designers should always bear user opinions in mind (while acknowledging that users can't offer opinions about features they haven't yet imagined or encountered).

![Features vs. needs.](/assets/image-readme/features_vs_needs.jpg)

## Story Functions
- With a view to narrative cohesion, the "make_choice" function is designed for developers writing and reading user options in the story context in which said options are offered. For a game with a very short plot, story content can usefully be stored in a dictionary. However, "Double Agent" takes a different approach. Significant blocks of story text are written in addition to the choices offered to the user. It would be harder for developers to follow the flow of this story if text blocks and user choices were separated. Rather, story content is (mostly) written in the order in which the user encounters it (situations like equipment choice being the exceptions). Taking this approach, the flow of the story can be followed with ease. 
- Functions that display story text are listed in the order in which they are displayed, again to help developers track the flow of the story. With the array of functions provided, it should be possible for developers to extend the story significantly while only adding functions that display story content (following the examples established by existing story text functions).
- The function "start_game" handles whether the user wants to play the game. If the user chooses to play, the function then offers the chance to change text speed and view setting and/or gameplay info. It then calls the first story function, "opening_scene," which begins the story proper. Each subsequent story function then calls the next. The "start_game" function is called at the end of run.py. This call can easily be commented out to test other code, without starting the game.
- The "inc_game_value" function allows developers to increment (or decrement) the value of any key in the "game" dictionary, where all persistent plot info should be stored. If future versions of the game add extra key-value pairs to the "game" dictionary, developers will still be able to use this function to apply new values to the new keys. 

## Savegame System
- "Double Agent" stores plot information in the "game" dictionary. Its savegame system reads and writes these values to and from a Google Sheet. Comments on the sheet and its structure are provided [below](#data-model).
- In the functions that implement the savegame system, the number of columns to read and write is not a static range. Rather, it is determined dynamically by the number of key-value pairs in the "game" dictionary. If further key-value pairs are later added to the game, the savegame functions will not need to be updated. They will continue to read and write data from the Sheet in accordance with the newly enlarged dictionary.
- Of particular note: when a returning user chooses to load a game, the "game" dictionary is updated with their savegame data. This functionality will not be broken if the dictionary is enlarged later. Imagine a new version of the game with 22 pairs in the dictionary. If the new version loads a save that was created by the present version (which has 18 pairs), it will transfer 18 values to "game" - but the other four will remain, as defined by their default values. They will not be deleted or overwritten. 
- To ensure that version compatibility does not break, any new pairs must always be added to the end of the "game" dictionary, not inserted between existing pairs. 

# Data Model
The Google Sheet "double-agent" was used to store savegame data for "Double Agent." Data from the "game" dictionary was sent to and rewritten from "savegame," this sheet's one worksheet. Each username is assigned one row in the "name" column of the worksheet, with the user's data being stored to the columns corresponding to that row. 

![Data model, showing all columns.](/assets/image-readme/data_model.jpg)

![Data model, cropped for readability.](/assets/image-readme/data_model_cropped.jpg)

# Testing, Bugs, and Fixes
During development, when function bugs were encountered, functions were edited down to a barebones format in which their essential principles could be explored. The functions were then tested in the isolated environment of [Python Tutor](https://pythontutor.com/visualize.html). As Python Tutor does not support all libraries, this form of testing was not possible in all scenarios. However, in most cases, Python Tutor exposed the logic and syntax issues at work, enabling bugs to be fixed there and these principles applied to the more complex versions of the functions in run.py.

## PEP8 Testing
- Run.py passed through [PEP8](http://pep8online.com/) without any issues.

![PEP8 results.](/assets/image-readme/pep8.jpg)

# Future Features
The majority of envisaged future features consist of additional story content. When initially planning this project, a full story was imagined, beginning-to-end, with seven or more days over the course of several in-game months being described. However, as the project developed, it became clear that adding coding functionality was more important than adding story content. This project was intended to develop and show profiency in the Python programming language. The limited development time was therefore best spent on visualizing and implementing complex functions that would allow more story content to be added later without much difficulty. Regrettably, only the first day of planned story content is implemented in the present version of the project. However, with the suite of functions currently offered, the full planned story can be added in a future version of the game, forked from the present repository. A small number of planned non-story-text features additionally did not make the cut due to lack of time. These are outlined below.

## Non-Story-Text Future Features
- Future versions of the game could refactor some of its functions to be more powerful. For instance, the "make_choice" function currently only works with between two and four choices. It could be rewritten to work with a variable number of choices, passed to it via integer argument.
- A future version of the game could implement a custom response to Ctrl+C, [as shown here by Gabor Szabo](https://code-maven.com/catch-control-c-in-python).
- A range of different ending ascii art was planned, but the one such function actually written was removed from the present version, as no endings were reached within the scope of the story as currently presented. See below for the removed content, which represents an ending in which the player character dies.

![Bad ending ascii art.](/assets/image-readme/bad_end.jpg)

# Deployment

## Deploying to Heroku

- Due to a recent data breach, the current deployment method has changed.
- In GitPod, run the command **heroku login -i** and log in when prompted.
- Run the command **heroku create your_app**, replacing *your_app* with the name you want to give your app. (Note: by default, this seems to set the app region to the United States. To set the app region to Europe instead, append **--region=eu**, for a full command of **heroku create your_app --region=eu**.)
- Go to Heroku. On your project page, click the "Settings" tab and scroll to "Config Vars."
- Enter "PORT" in the KEY input field, then enter "8000" in the VALUE input field.
- Click the "Add" button to add the Convig Vars.
-  Add other config vars if needed. For instance, the Double Agent RPG needs CREDS, generated by the Google Drive API. As credentials will be unique to each project, you must generate your own set of credentials and paste them into the VALUE input field beside CREDS.
- On the same page, scroll to the buildpacks section and click "Add Buildpack."
- Add the Python and node.js buildpacks, ensuring that the Python buildpack is listed above the node.js buildpack.
- Return to GitPod. Run the command **git push heroku main** and your app will be deployed to Heroku.

## Forking the Repository on GitHub

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/Estelindis/double-agent) that you want to fork.
2. In the upper right of the repository, click the "Fork" button.
3. A copy of the repository will now be available within your repositories.

Forking the GitHub repository makes a copy of the original repository on our GitHub account to view and/or make changes without affecting the original repository. This copy of the code can be edited without affecting the original code.

## Cloning the Repository on GitHub

1. In the upper section of the repository, click the dropdown named "Code."
2. In the "Clone with HTTPS" section, copy the URL.
3. Open Git Bash in your IDE of choice.
4. Change the current working directory to the location you want for the cloned directory.
5. Type "git clone" and paste the URL copied from GitHub.
6. After pressing Enter, the clone of your repository will be created.

# Used technologies and credits

## Languages
- [HTML5](https://en.wikipedia.org/wiki/HTML)
- [CSS3](https://en.wikipedia.org/wiki/CSS)
- [Python](https://en.wikipedia.org/wiki/Python_(programming_language))

## Python Libraries

- [GSpread](https://pypi.org/project/gspread/) enables the Google Sheets savegame system.
- [Time](https://docs.python.org/3/library/time.html) enables the "p_d" print delay function.
- [Sys](https://docs.python.org/3/library/sys.html) enables the "delete_line" function (and its dependent "pause" function).
- [GetPass](https://docs.python.org/3/library/getpass.html) enables the "pause" function.

## Other Technologies
- [GitHub](https://github.com/)
- [Google Sheets](https://www.google.co.uk/sheets/about/)
- [Python Tutor](https://pythontutor.com/visualize.html)
- [PEP8](http://pep8online.com/)

## Credits
- [Aniket Navlur](https://stackoverflow.com/a/52590238) and [Alper](https://stackoverflow.com/a/70072767) demonstrated how to use "stdout" to delete printed lines.
- [Mike Hordecki](https://stackoverflow.com/a/522578/18794218) demonstrated how to use "enumerate."
- [Pedro Lobito](https://stackoverflow.com/a/42476314/18794218) provided the "next_available_row" function.
- [Star Trek: Time Loop](https://github.com/DeannaCarina/StarTrekTimeLoop) by DeannaCarina provided some code direction, as well as giving an example of an excellent story-based Python project.
- [The Code Institute Slack](https://slack.com/) provided an invaluable database of information and community of support. I am particularly grateful to the msletb-nov-2021 cohort, our facilitator Kasia, and my mentor Darío. From my cohort, special mentions to Rhiannon McNulty and Rachel Rock, who are always ready and willing to provide feedback.
