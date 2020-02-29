from Poker_app.models import Account, Game
from django.template.defaultfilters import linebreaksbr


# @@@ HELPER METHODS for the CommandHandler: @@@ #

# returns the flag for the html file to display the specific menu
def menu(role):
    if role == "admin":
        return "admin menu"
    if role == "player":
        return "player menu"


# returns true if user is in a game, false otherwise
def is_ingame(user):
    if user:
        return Account.objects.get(username=user.username).in_game


# @@@ COMMANDS: @@@ #

# LOBBY COMMANDS:

# creates player account
# validates input, checks for duplicates. Only the admin can use this
# returns proper message(success or fail)
def create_player(admin, username):
    if admin.role != "admin":
        return "You are not the admin. Try the menu to see your available commands."
    user = Account.objects.filter(username=username)
    if user:
        return f"Player account {username} already exists."
    Account.objects.create(username=username, role="player")
    return f"Player account {username} successfully created."


# displays a list of all existing player accounts with their description
def list_players(admin):
    if admin.role != "admin":
        return "You are not the admin. Try the menu to see your available commands."
    players = Account.objects.all().exclude(role="admin")
    player_str = ""
    for player in players:
        player_str += player.__str__() + "\n"
    return linebreaksbr(player_str)


# starts a new game with the commanding user as the first player in the table
# assumes user already exists in data base
# Gives 100 chips to the user
def new_game(user):
    if is_ingame(user):
        return "You are already in a game. Try a different command or Quit your current game."
    table_id = Game.objects.all().count() + 1
    Game.objects.create(table_id=table_id)
    joined = join_game(user, table_id)
    if "successfully joined" in joined:
        return f"New game at table {table_id} successfully created."
    return joined


# adds the user to the selected game
# assumes user already exists in data base
# if there is a max number of players, check for that
# gives 100 chips to the user
def join_game(user, table_id):
    if is_ingame(user):
        return "You are already in a game. Try a different command or Quit your current game."
    game = Game.objects.filter(table_id=table_id)
    if not game:
        return "This table does not exists. Try joining a different one or open a new table."
    if user.table == game[0]:
        return "You are already in this table."
    # if game.num_players >= max_num_players:
    #     return " Sorry, this table is full."
    Account.objects.filter(username=user.username).update(table=game[0], in_game=True, in_game_chips=100)
    # update number of players in this table
    game[0].num_players += 1
    game[0].save()
    return f"{user.username} has successfully joined Table {table_id}."


# prints out all existing tables that have game_on status off and number of players less than max
def see_available_games(user):
    if is_ingame(user):
        return "You are currently in a game. Try a different command."
    tables = Game.objects.filter(game_on=False).exclude(num_players=8) # assuming max num of players is 8
    if not tables:
        return "No available Tables now."
    tables_str = ""
    for table in tables:
        tables_str += table.__str__() + "\n"
    return linebreaksbr(tables_str)


# prints out a list of the five top high scores from existing players
def top_scores(user):
    if is_ingame(user):
        return "You are in a game. This command is available at the Lobby."
    scores = Account.objects.all().exclude(role="admin").order_by("-score")
    scores_str = ""
    for i in range(5):
        scores_str += scores[i].username + " ---------- highest score: " + str(scores[i].score) + "\n"
    return linebreaksbr(scores_str)


# allows the players to see their profile only if they are in the lobby
def my_profile(user):
    if is_ingame(user):
        "You are in a game. This command is available at the Lobby."
    username = "Username: " + user.username
    role = "Role: " + user.role
    balance = "Total balance: " + str(user.total_balance)
    score = "Highest score: " + str(user.score)
    return linebreaksbr(username + "\n" + role + "\n" + balance + "\n" + score)


# returns this user's current total balance, can be called any time
def total_balance(user):
    return "Total balance: " + str(user.total_balance)


# IN GAME COMMANDS:

# return this user's current number of in game chips
def my_chips(user):
    if not is_ingame(user):
        return "You are currently in the Lobby. This command is not allowed here."
    return "Current chips: " + str(user.in_game_chips)


# quits the game. The user's ingame status goes off, the user's table is set to none
# the number of players in table is reduced by 1, if number of users goes to 0 then table is deleted
# updates user's balance = balance += chips - 100 if chips are > 100 then sets chips back to 0
# update highest score if new in_game chips > 100 and > old score
# assumes user exists in data base
def quit_game(user):
    if not is_ingame(user):
        return "You are currently in the Lobby."
    user = Account.objects.get(username=user.username)
    table = user.table
    user.in_game = False
    user.table = None
    # update balance and score
    if user.in_game_chips > 100:
        user.total_balance += (user.in_game_chips - 100)
        if user.in_game_chips > user.score:
            user.score = user.in_game_chips
    user.in_game_chips = 0
    user.save()
    table.num_players -= 1
    table.save()
    if table.num_players <= 0:
        Game.objects.get(table_id=table.table_id).delete()
    return "Successfully left the game. You are now in the Lobby."


class CommandHandler:

    def command(self, command_input, username):
        # return "player1 account successfully created."

        # username has priority
        if not username or username == "":
            return "Please give us your username."

        user = Account.objects.filter(username=username)
        if not user:
            return f"Username {username} does not exist or is invalid. Try again."

        # only after checking for username, we check the command input
        # so at this point player[0] is a valid player
        if not command_input or command_input == "":
            return menu(user[0].role)

        # at this point we have valid username and something in the command line
        # # setup variables
        command_list = command_input.split(":")
        if command_list[0] != user[0].username:
            return "Username and pre-pended username do not match! Try again."
        if len(command_list) < 2:
            return "Wrong input format. Try username: command args(if needed)."

        # at this point the command is properly pre-pended, so now we check for every single command
        command_list = command_list[1].split()

        # this condition is for the only 2 keywords command which is: crate_player <username>
        if len(command_list) == 2:
            # only for the admin
            if user[0].role == "admin":
                if command_list[0].lower() == "create_player":
                    # here we will call create_player()
                    return create_player(user[0], command_list[1])
                return "Command not recognized. Refer to the Menu for a list of proper commands."
            # only for the player
            if user[0].role == "player":
                # player calls join_game command
                if command_list[0].lower() == "join_game":
                    return join_game(user[0], command_list[1])
                # player calls raise command
                if command_list[0].lower() == "raise":
                    return "raise"
                return "Command not recognized. Refer to the Menu for a list of proper commands."

        # menu for all users
        if len(command_list) == 1 and command_list[0].lower() == "menu":
            return menu(user[0].role)

        # admin commands:
        if len(command_list) == 1 and user[0].role == "admin":
            # admin calls list_players command
            if command_list[0].lower() == "list_players":
                return list_players(user[0])

        # player commands:
        # each command method call will check for the players playing status
        if len(command_list) == 1 and user[0].role == "player":
            # player calls my_profile command
            if command_list[0].lower() == "my_profile":
                return my_profile(user[0])
            # player calls new_game command
            if command_list[0].lower() == "new_game":
                return new_game(user[0])
            # player calls see_available_games command
            if command_list[0].lower() == "see_available_games":
                return see_available_games(user[0])
            # player calls top_scores command
            if command_list[0].lower() == "top_scores":
                return top_scores(user[0])
            # player calls start command
            if command_list[0].lower() == "start":
                return "game started"
            # player calls quit command
            if command_list[0].lower() == "quit":
                return quit_game(user[0])
            # player calls see_their_cards command
            if command_list[0].lower() == "see_their_cards":
                return "see_their_cards"
            # player calls my_chips command
            if command_list[0].lower() == "my_chips":
                return my_chips(user[0])
            # player calls my_balance command
            if command_list[0].lower() == "my_balance":
                return total_balance(user[0])
            # player calls call_ammount command
            if command_list[0].lower() == "call_amount":
                return "call_amount"
            # player calls see_pot command
            if command_list[0].lower() == "see_pot":
                return "see_pot"
            # player calls call command
            if command_list[0].lower() == "call":
                return "call"
            # player calls check command
            if command_list[0].lower() == "check":
                return "check"
            # player calls fold command
            if command_list[0].lower() == "fold":
                return "fold"
            # player calls see_cards command
            if command_list[0].lower() == "see_cards":
                return "see_cards"
        return "Wrong input format or command. Try username: command args(if needed)."
