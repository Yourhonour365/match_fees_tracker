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
                "paid": m["paid"],
            }
            for m in matches
        ],
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
            matches.append(
                {
                    "opponent": m["opponent"],
                    "date": date(y, mm, dd),
                    "fee": float(m["fee"]),
                    "players": m.get("players", []),
                    "paid": m.get("paid", []),
                }
            )
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
        if name in players:
            print(f"\n{name} already exists in the player list.")
            print("\nTo differentiate players with the same name, consider adding:")
            print("  • Junior/Senior (e.g., John Smith Jr, John Smith Sr)")
            print("  • Age group (e.g., John Smith U15, John Smith Adult)")
            print("  • Nickname (e.g., John 'Smudge' Smith)")
            print("  • Middle initial (e.g., John A Smith, John B Smith)")
            print("  • Team/role (e.g., John Smith (Captain), John Smith (Keeper))")
            print("\nPlease enter a unique identifier for this player.")
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
    for existing_match in matches:
        if existing_match["opponent"] == opponent and existing_match["date"] == parsed_date:
            print(f"\n⚠ Note: You already have {club_name} vs {opponent} on {parsed_date.strftime('%d/%m/%Y')}")
            confirm = input("Add this match anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                print("\nMatch not added.")
                return
            break
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

    available_players = [player for player in players if player not in match["players"]]

    if not available_players:
        print(f"\nAll players are already marked as attended for this match.")
        return

    print("\n=== Available Players ===")
    for i, player in enumerate(available_players, 1):
        print(f"\n{i}) {player}")
    while True:
        player_choice = input("\nChoose player number: ").strip()
        if player_choice.isdigit():
            player_idx = int(player_choice)
            if 1 <= player_idx <= len(available_players):
                selected_player = available_players[player_idx - 1]
                break
        print(f"Please enter 1–{len(available_players)}.")

    match["players"].append(selected_player)
    save_data()

    opponent = match["opponent"]
    date_fmt = match["date"].strftime("%d-%b-%Y")
    print(
        f"\n✓ {selected_player} marked as attended for {club_name} vs {opponent} on {date_fmt}"
    )

    if len(match["players"]) > 1:
        print(
            f"\nCurrent attendance ({len(match['players'])} players): {', '.join(match['players'])}"
        )


def list_matches():
    """
    Print all matches currently stored in the matches list.
    Shows date as DD-MMM-YYYY and fee as £x.xx.
    """
    print("\n=== Matches ===")

    for match in matches:
        date_fmt = match["date"].strftime("%d-%b-%Y")
        fee_fmt = f"£{match['fee']:.2f}"
        print(f'\n{club_name} vs {match["opponent"]} {date_fmt} Match Fee {fee_fmt}')

def show_team_sheets():
    """Display team sheets for all matches"""
    if not matches:
        print("\nNo matches recorded yet.")
        return

    sorted_matches = get_matches_sorted()

    print("\n=== Team Sheets ===")
    for match in sorted_matches:
        date_fmt = match["date"].strftime("%d/%m/%Y")
        fee_fmt = f"£{match['fee']:.2f}"

        # Determine if played or fixture
        if match["players"]:
            status = f" (Played - {len(match['players'])} players)"
        else:
            status = " (Fixture - no team selected yet)"

        print(f"\n{club_name} vs {match['opponent']} - {date_fmt}{status}")
        print(f"Match Fee: {fee_fmt}")

        if match["players"]:
            print("Team:")
            for player in match["players"]:
                paid_status = " ✓ Paid" if player in match.get("paid", []) else " - Fee due"
                print(f"  • {player}{paid_status}")
        else:
            print("No players selected yet")

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
            f"\n{number}) {club_name} vs {match['opponent']} {date_fmt} Fee {fee_fmt}"
        )
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


def club_management():
    """
    Handle club management options
    """
    while True:
        print("\n=== Club Management ===")
        print("{'1) Switch club'}")
        print("{'2) Delete club data'}")
        print("{'b) Back to main menu'}")
        print()

        choice = input("Choose option: ").strip().lower()

        if choice == "b":
            break
        elif choice == "e":
            print("Goodbye!")
            exit()
        elif not choice.isdigit():
            print("Please enter a valid option.")
            continue

        choice = int(choice)

        if choice == 1:
            print("Switch club not implemented yet.")
        elif choice == 2:
            print("Delete club data not implemented yet.")
        else:
            print("Please choose a valid option.")

def record_payment():
    """Record a match fee payment from a player"""
    if not matches or not players:
        print("\nYou need at least one match and one player first.")
        return

    matches_with_players = [m for m in matches if m["players"]]
    if not matches_with_players:
        print("\nNo matches have been played yet (no players marked).")
        return


    print("\n=== Select Match ===")
    for i, match in enumerate(matches_with_players, 1):
        date_fmt = match["date"].strftime("%d/%m/%Y")
        print(f"{i}) {club_name} vs {match['opponent']} on {date_fmt}")


    while True:
        choice = input("\nChoose match number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(matches_with_players):
            selected_match = matches_with_players[int(choice) - 1]
            break
        print(f"Please enter 1-{len(matches_with_players)}")


    unpaid = [p for p in selected_match["players"] if p not in selected_match["paid"]]
    if not unpaid:
        print("\nAll players have paid for this match!")
        return

    print("\n=== Unpaid Players ===")
    for i, player in enumerate(unpaid, 1):
        print(f"{i}) {player} - owes £{selected_match['fee']:.2f}")


    while True:
        choice = input("\nWho has paid? Choose number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(unpaid):
            player_who_paid = unpaid[int(choice) - 1]
            break
        print(f"Please enter 1-{len(unpaid)}")


    selected_match["paid"].append(player_who_paid)
    save_data()
    print(f"\n✓ Payment recorded: {player_who_paid} paid £{selected_match['fee']:.2f}")

def view_fee_balances():
    """Show fee balances for all players"""
    if not players:
        print("\nNo players registered yet.")
        return

    print("\n=== Match Fee Balances ===")
    print("-" * 60)
    print(f"{'Player':<25} {'Matches':<10} {'Paid':<10} {'Due':<10}")
    print("-" * 60)

    total_outstanding = 0

    for player in sorted(players):  # Added sorted() here
        total_owed = 0
        total_paid = 0
        matches_played = 0

        for match in matches:
            if player in match.get("players", []):
                matches_played += 1
                total_owed += match["fee"]
                if player in match.get("paid", []):
                    total_paid += match["fee"]

        balance_due = total_owed - total_paid
        total_outstanding += balance_due

        # Format the amounts - keeping consistent width
        paid_str = f"£{total_paid:.2f}" if total_paid > 0 else "-"
        due_str = f"£{balance_due:.2f}" if balance_due > 0 else "-"
        matches_str = str(matches_played) if matches_played > 0 else "-"

        print(f"{player:<25} {matches_str:<10} {paid_str:<10} {due_str:<10}")

    print("-" * 60)
    if total_outstanding > 0:
        print(f"{'TOTAL':<25} {'':<10} {'':<10} £{total_outstanding:.2f}")
    else:
        print(f"{'TOTAL':<25} {'':<10} {'':<10} -")

def player_management():
    """Handle player management operations"""
    while True:
        # Show player table
        print("\n=== Player Management ===")
        if not players:
            print("\nNo players registered yet.")
        else:
            sorted_players = sorted(players)
            total = len(sorted_players)
            half = (total + 1) // 2  # Round up for odd numbers

            print("-" * 64)
            # Fixed spacing in header
            left_header = f"{'No.':<3} {'Player':<20} {'Status':<6}"
            right_header = f"{'No.':<3} {'Player':<20} {'Status':<6}"
            print(f"{left_header}  {right_header}")
            print("-" * 64)

            for i in range(half):
                # Left column
                left_no = i + 1
                left_player = sorted_players[i][:20]  # Truncate if too long
                left_line = f"{left_no:<3} {left_player:<20} {'Actv':<6}"

                # Right column (if exists)
                right_idx = i + half
                if right_idx < total:
                    right_no = right_idx + 1
                    right_player = sorted_players[right_idx][:20]  # Truncate if too long
                    right_line = f"{right_no:<3} {right_player:<20} {'Actv':<6}"
                    print(f"{left_line}  {right_line}")
                else:
                    print(left_line)

            print("-" * 64)
            print(f"Total: {total} players")

        # Show menu options in two columns
        print("\nOptions:")
        print("1) Add player                3) Make player inactive")
        print("2) Edit player name          4) Select players for matches")
        print()
        print("b) Back to main menu")
        print()

        choice = input("Choose option: ").strip().lower()

        if choice == 'b':
            break
        elif choice == '1':
            add_player()
        elif choice == '2':
            print("Edit player not implemented yet.")
        elif choice == '3':
            print("Make inactive not implemented yet.")
        elif choice == '4':
            print("Select for matches not implemented yet.")
        else:
            print("Please choose a valid option.")

def match_fees_menu():
    """Handle match fee operations"""
    while True:
        print("\n=== Match Fees ===")
        print("1) Mark who played (creates fee obligation)")
        print("2) Record fee payment")
        print("3) View fee balances")
        print("b) Back to main menu")
        print()

        choice = input("Choose option: ").strip().lower()

        if choice == 'b':
            break
        elif choice == '1':
            mark_attendance()  # Your existing function
        elif choice == '2':
            record_payment()
        elif choice == '3':
            print("View balances not implemented yet.")
        else:
            print("Please choose a valid option.")

def main():
    """
    Add club name if not already added.
    Display the main menu for match fees tracker
    """
    global club_name
    while True:
        if club_name:
            print(f"\n=== Match Fees Tracker - {club_name} ===")
        else:
            print("\n=== Match Fees Tracker - [Club Name Not Set] ===")

        if not club_name:
            club_name = smart_title(input("\nEnter the name of your club: ").strip())
            continue

        print("\nMANAGE:")
        print(f"{'1) Players':<20} {'3) Fixtures'}")
        print(f"{'2) Team selection':<20} {'4) Match fees'}")
        print()
        print("REPORTS:")
        print(f"{'5) Player list':<20} {'7) Fixture list'}")
        print(f"{'6) Team sheets':<20} {'8) Match fee balances'}")
        print()
        print(f"{'m) Club management':<20} {'e) Exit'}")
        print()

        if not club_name:
            club_name = smart_title(input("Enter the name of your club: ").strip())
            save_data()
            continue

        choice = input("Choose option from menu above: ").strip()
        if choice == "m":
            club_management()
            continue
        elif choice == "e":
            print("Goodbye!")
            break

        if not choice.isdigit():
            print("Please enter a number from the menu.")
            continue

        choice = int(choice)
        if choice == 1:
            player_management()
        elif choice == 2:
            mark_attendance()
        elif choice == 3:
            add_match()
        elif choice == 4:
            match_fees_menu()
        elif choice == 5:
            list_players()
        elif choice == 6:
            show_team_sheets()
        elif choice == 7:
            list_matches()
        elif choice == 8:
            view_fee_balances()
        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    load_data()
    main()
