players = []
matches = []
fees = {}

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
    Add a match fee that needs to be paid by each player. 
    """
    match = input("Enter match description: ")
    fee = float(input("Enter fee amount: "))
    matches.append(match)
    fees[match] = fee
    print(f"Added match: {match} (Fee: £{fee:.2f})")

def list_matches():
    """
    Print all matches currently stored in the matches list.
    """
    print("=== Matches ===")
    for match in matches:
        print(match)


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
list_matches()

