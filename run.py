players = []
matches = []

club_name = input("Enter the name of your club: ").strip().title()


def add_player():
    """
    Ask for a player's name and print a confirmation.
    """
    while True:
        name = input("Enter player name: ").strip().title()
        if not name:
            print("Player name cannot be empty. Please try again.")
            continue
        if any(char.isdigit() for char in name):
            print("Player name cannot contain numbers. Please try again.")
            continue
        players.append(name)
        print(f"Added player: {name}")
        break


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
    while True:
        opponent = input("Enter match opponent: ").strip().title()
        if not opponent:
            print("Opponent cannot be empty. Please try again.")
            continue
        print(f"Opponent: {opponent}")
        break

    from datetime import datetime

    while True:
        date_str = input("Enter match date (DD/MM/YY): ").strip()
        if not date_str:
            print("Date cannot be empty. Please try again.")
            continue
        try:
            # if 2 digit year
            parsed_date = datetime.strptime(date_str, "%d/%m/%y").date()
            break
        except ValueError:
            try:
                # if 4 digit year
                parsed_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                break
            except ValueError:
                print(
                    "Invalid date. Please use DD/MM/YY (05/09/25)")
                continue

    while True:
        fee_str = input("Enter match fee: ").strip()
        if not fee_str:
            print("Fee cannot be empty. Please try again.")
            continue
        try:
            fee = float(fee_str)
            print(f"Match fee recorded: £{fee:.2f}")
            break
        except ValueError:
            print("Invalid fee. Please enter a number.")
            continue

    match = {
        "opponent": opponent,
        "date": parsed_date,
        "fee": fee,
        "players": [],
        "paid": []
    }

    matches.append(match)


def list_matches():
    """
    Print all matches currently stored in the matches list.
    Also print the fee and date associated with each match.
    """
    print("=== Matches ===")
    for match in matches:
        date_fmt = match["date"].strftime("%d-%b-%Y")  # e.g. 11-Nov-2025
        print(
            f'{club_name} vs {match["opponent"]} {date_fmt} Match Fee £{match["fee"]:.2f}')


def main():
    """
    Display the main menu for match fees tracker
    """
    print("=== Match Fees Tracker ===")
    print("1) Add player")
    print("2) List players")
    print("3) Add match")
    print("4) List matches")
    print("0) Exit")


# main()
add_player()
list_players()
add_match()
list_matches()
