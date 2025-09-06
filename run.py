from datetime import datetime, date
import json, os
DATA_FILE = "data.json"


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

def save_data():
    data = {
        "club_name": club_name,
        "players": players,
        "matches": [
            {
                "opponent": m["opponent"],
                "date": m["date"].isoformat(),  
                "fee": m["fee"],
                "players": m["players"],
                "paid": m["paid"]
            }
            for m in matches
        ]
    }
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass  

def load_data():
    global club_name, players, matches
    if not os.path.exists(DATA_FILE):
        return
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        return  

    club_name = data.get("club_name", "")
    players[:] = data.get("players", [])
    matches[:] = []
    for m in data.get("matches", []):
        try:
            y, mm, dd = map(int, m["date"].split("-"))
            matches.append({
                "opponent": m["opponent"],
                "date": date(y, mm, dd),   
                "fee": float(m["fee"]),
                "players": m.get("players", []),
                "paid": m.get("paid", [])
            })
        except Exception:
            continue  

club_name = ""


def add_player():
    """
    Ask for a player's name and print a confirmation.
    """
    while True:
        name = smart_title(input("\nEnter player name: ").strip())
        if not name:
            print("\nPlayer name cannot be empty. Please try again.")
            continue
        if any(ch.isdigit() for ch in name):
            print("\nPlayer name cannot contain numbers. Please try again.")
            continue
        players.append(name)
        save_data()  
        print(f"\nAdded player: {name}")
        break


def list_players():
    """
    Print all players currently stored in the players list.
    """
    print("\n=== Current Players ===\n")
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
        opponent = smart_title(input("\nEnter match opponent: ").strip())
        if not opponent:
            print("\nOpponent cannot be empty. Please try again.\n")
            continue

        print(f"\nOpponent: {opponent}\n")
        break

    while True:
        date_str = input("Enter match date (DD/MM/YY or DD/MM/YYYY): ").strip()
        if not date_str:
            print("\nDate cannot be empty. Please try again.")
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
                    "\nInvalid date. Please use DD/MM/YY (e.g. 05/09/25) or DD/MM/YYYY (e.g. 05/09/2025)."
                )
                continue

    while True:
        fee_str = input("\nEnter match fee: ").strip()
        if not fee_str:
            print("\nFee cannot be empty. Please try again.")
            continue
        try:
            fee = float(fee_str)
            print(f"\nMatch fee recorded: £{fee:.2f}")
            break
        except ValueError:
            print("\nInvalid fee. Please enter a number.")
            continue

    match = {
        "opponent": opponent,
        "date": parsed_date,
        "fee": fee,
        "players": [],
        "paid": [],
    }
    matches.append(match)
    save_data()  

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
        choice = input("\nChoose match number: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(sorted_matches):
                match = sorted_matches[idx - 1]
                break
        print(f"\nPlease enter 1–{len(sorted_matches)}.")

    list_players_indexed()
    while True:
        player_choice = input("\nChoose player number: ").strip()
        if player_choice.isdigit():
            player_idx = int(player_choice)
            if 1 <= player_idx <= len(players):
                selected_player = players[player_idx - 1]
                break
        print(f"Please enter 1–{len(players)}.")

def list_matches():
    """
    Print all matches currently stored in the matches list.
    Shows date as DD-MMM-YYYY and fee as £x.xx.
    """
    print("\n=== Matches ===")

    for match in matches:
        date_fmt = match["date"].strftime("%d-%b-%Y")
        fee_fmt = f"£{match['fee']:.2f}"
        print(
            f'\n{club_name} vs {match["opponent"]} {date_fmt} Match Fee {fee_fmt}')


def list_matches_indexed():
    """
    Print all matches with an index number so user can select one.
    """
    print("\n=== Matches ===")
    if not matches:
        print("\n(no matches yet)")
        return

    number = 1
    for match in get_matches_sorted():
        date_fmt = match["date"].strftime("%d-%b-%Y")
        fee_fmt = f"£{match['fee']:.2f}"
        print(
            f"\n{number}) {club_name} vs {match['opponent']} {date_fmt} Fee {fee_fmt}")
        number += 1


def list_players_indexed():
    """
    Print all players with an index number so user can select one.
    """
    print("\n=== Players ===")
    if not players:
        print("\n(no players yet)")
        return
    number = 1
    for player in players:
        print(f"\n{number}) {player}")
        number += 1


def main():
    """
    Add club name if not already added.
    Display the main menu for match fees tracker
    """
    global club_name
    while True:
        print("\n=== Match Fees Tracker ===")
        if not club_name:
            club_name = smart_title(
                input("\nEnter the name of your club: ").strip())
            continue
        print(f"\n{'1) Add player':<20} {'5) Mark attendance'}")
        print(f"{'2) List players':<20} {'6) Record payment'}")
        print(f"{'3) Add match':<20} {'7) Show balances'}")
        print(f"{'4) List matches':<20} {'0) Exit'}")
        print()
        if not club_name:
            club_name = smart_title(
                input("Enter the name of your club: ").strip())
            save_data()  
            continue

        choice = input("Choose option from menu above: ").strip()
        if not choice.isdigit():
            print("Please enter a number from the menu.")
            continue

        choice = int(choice)
        if choice == 1:
            add_player()
        elif choice == 2:
            list_players()
        elif choice == 3:
            add_match()
        elif choice == 4:
            list_matches_indexed()
        elif choice == 5:
            mark_attendance()
        elif choice == 6:
            print("Record payment not implemented yet.")  
        elif choice == 7:
            print("Show balances not implemented yet.")   
        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Please choose a valid option.")

if __name__ == "__main__":
    load_data()   
    main()       
