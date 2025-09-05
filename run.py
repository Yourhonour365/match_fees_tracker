players = []
matches = []
#fees = {}

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
    Add a date for each match

    """
    opponent = input("Enter match opponent: ")
    date = input("Enter match date (e.g. 2025-09-04): ")
    fee = float(input("Enter fee amount: "))
    
    # Create a match dictionary to hold match details
    match = {
        "opponent": opponent,
        "date": date,
        "fee": fee,
        "players": [],   # players who are playing in this match
        "paid": []       # players who have paid their match fee
    }
    
    matches.append(match)
    #fees[match] = {"date": date, "fee": fee}
    #print(f"Added match: {match} on {date} (Fee: £{fee:.2f})")


def list_matches():
    """
    Print all matches currently stored in the matches list.
    Also print the fee and date associated with each match.
    """
    print("=== Matches ===")
        #for match in matches:
        #details = fees[match]
        #date = details["date"]
        #fee = details["fee"]
        #print(f"{match} on {date} Match fee = £{fee:.2f}")


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

