from datetime import datetime


players = []
matches = []


def smart_title(text: str) -> str:
    """
    Capitalise words (title case) but keep common club acronyms in uppercase.
    Example:
      "tigers cc"   -> "Tigers CC"
      "ewhurst rfc" -> "Ewhurst RFC"
      "jed smith"   -> "Jed Smith"
    """
    acronyms = {"cc", "fc", "rfc", "afc"}
    result = []
    for w in text.split():
        if w.lower() in acronyms:
            result.append(w.upper())
        else:
            result.append(w.capitalize())
    return " ".join(result)


def get_matches_sorted():
    return sorted(matches, key=lambda m: m["date"])


club_name = smart_title(input("Enter the name of your club: ").strip())


def add_player():
    """
    Ask for a player's name and print a confirmation.
    """
    while True:
        name = smart_title(input("Enter player name: ").strip())
        if not name:
            print("Player name cannot be empty. Please try again.")
            continue
        if any(ch.isdigit() for ch in name):
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
    Validates:
      - opponent: non-empty, smart title-cased
      - date: DD/MM/YY or DD/MM/YYYY, stored as datetime.date
      - fee: numeric, echoed as £x.xx
    """

    while True:
        opponent = smart_title(input("Enter match opponent: ").strip())
        if not opponent:
            print("Opponent cannot be empty. Please try again.")
            continue

        print(f"Opponent: {opponent}")
        break

    while True:
        date_str = input("Enter match date (DD/MM/YY or DD/MM/YYYY): ").strip()
        if not date_str:
            print("Date cannot be empty. Please try again.")
            continue
        try:
            parsed_date = datetime.strptime(date_str, "%d/%m/%y").date()
            break
        except ValueError:
            try:
                parsed_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                break
            except ValueError:
                print(
                    "Invalid date. Please use DD/MM/YY (e.g. 05/09/25) or DD/MM/YYYY (e.g. 05/09/2025)."
                )
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
        "paid": [],
    }
    matches.append(match)


def mark_attendance():
    """
    Mark a player as attended for a match.
    """
    if not matches or not players:
        print("You need at least one match and one player first.")
        return

    sorted_matches = get_matches_sorted()

    list_matches_indexed()
    while True:
        choice = input("Choose match number: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(sorted_matches):
                match = sorted_matches[idx - 1]
                break
        print(f"Please enter 1–{len(sorted_matches)}.")


def list_matches():
    """
    Print all matches currently stored in the matches list.
    Shows date as DD-MMM-YYYY and fee as £x.xx.
    """
    print("=== Matches ===")

    for match in matches:
        date_fmt = match["date"].strftime("%d-%b-%Y")
        fee_fmt = f"£{match['fee']:.2f}"
        print(
            f'{club_name} vs {match["opponent"]} {date_fmt} Match Fee {fee_fmt}')


def list_matches_indexed():
    """
    Print all matches with an index number so user can select one.
    """
    print("=== Matches ===")
    if not matches:
        print("(no matches yet)")
        return

    number = 1
    for match in get_matches_sorted():
        date_fmt = match["date"].strftime("%d-%b-%Y")
        fee_fmt = f"£{match['fee']:.2f}"
        print(
            f"{number}) {club_name} vs {match['opponent']} {date_fmt} Fee {fee_fmt}")
        number += 1


def list_players_indexed():
    """
    Print all players with an index number so user can select one.
    """
    print("=== Players ===")
    if not players:
        print("(no players yet)")
        return
    number = 1
    for player in players:
        print(f"{number}) {player}")
        number += 1


def main():
    """
    Display the main menu for match fees tracker
    """
    print("\n=== Match Fees Tracker ===")
    print("1) Add player")
    print("2) List players")
    print("3) Add match")
    print("4) List matches")
    print("5) Mark attendance")
    print("6) Record payment")
    print("7) Show balances")
    print("0) Exit")


main()
