players = []
matches = []

def add_player():
    """
    Ask for a player's name and print a confirmation.
    """
    name = input("Enter player name: ")
    players.append(name)
    print(f"Added player: {name}")

def list_players():
    """
    Print all players currently stored in the players list.
    """
    print("=== Current Players ===")
    for player in players:
        print(player)

def add_match():
    """
    Ask for a match description and store it in the matches list.
    """
    match = input("Enter match description: ")
    matches.append(match)
    print(f"Added match: {match}")


def main():
    """
    Display the main menu for match fees tracker
    """
    print("=== Match Fees Tracker ===")
    print("1) Add player")
    print("2) List players")
    print("0) Exit")

#main()
add_player()
list_players()
add_match()

