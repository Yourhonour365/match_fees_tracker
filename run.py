from datetime import datetime, date
import json, os
DATA_FILE = "data.json"


players = []
matches = []
inactive_players = []


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
        "inactive_players": inactive_players,
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
    global club_name, players, matches, inactive_players
    if not os.path.exists(DATA_FILE):
        return
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        return

    club_name = data.get("club_name", "")
    players[:] = data.get("players", [])
    inactive_players[:] = data.get("inactive_players", [])
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
    Ask for player names and print confirmations.
    Allows adding multiple players.
    """
    print("\n=== Add Players ===")
    print("Enter player names one at a time.")
    print("Press Enter with empty name when finished.\n")

    added_count = 0

    while True:
        name = smart_title(input("Enter player name (or Enter to finish): ").strip())

        if not name:  # Empty input - finish adding
            if added_count == 0:
                print("\nNo players added.")
            else:
                print(f"\nFinished. Added {added_count} player(s).")
            break

        if any(ch.isdigit() for ch in name):
            print("Player name cannot contain numbers. Please try again.")
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
        added_count += 1
        print(f"✓ Added: {name}")

    return  # Returns to player_management menu

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

    while True:  # Loop for filter selection
        # Show filter options
        print("\n=== Team Selection ===")
        print("Show matches:")
        print("1) Recent + upcoming (last 2 weeks + next 2 weeks)")
        print("2) Last month's matches")
        print("3) Next month's matches")
        print("4) All matches")
        print("b) Back to main menu")
        print()

        filter_choice = input("Choose filter: ").strip().lower()
        if filter_choice == 'b':
            return
        if filter_choice not in ['1', '2', '3', '4']:
            print("Please enter 1, 2, 3, 4, or b")
            continue

        filter_choice = int(filter_choice)

        # Filter matches based on selection
        from datetime import timedelta
        today = datetime.now().date()

        if filter_choice == 1:  # Recent + upcoming (4 weeks total)
            start_date = today - timedelta(days=14)
            end_date = today + timedelta(days=14)
            filtered_matches = [m for m in get_matches_sorted() if start_date <= m["date"] <= end_date]
        elif filter_choice == 2:  # Last month
            start_date = today - timedelta(days=30)
            end_date = today
            filtered_matches = [m for m in get_matches_sorted() if start_date <= m["date"] <= end_date]
        elif filter_choice == 3:  # Next month
            start_date = today
            end_date = today + timedelta(days=30)
            filtered_matches = [m for m in get_matches_sorted() if start_date <= m["date"] <= end_date]
        elif filter_choice == 4:  # All matches
            filtered_matches = get_matches_sorted()

        if not filtered_matches:
            print("\nNo matches found for the selected period. Try a different filter.")
            continue  # Go back to filter menu

        break  # Exit loop if we have matches

    # Display filtered matches in table format
    print("\n=== Matches ===")
    print(f"{'No.':<4} {'Date':<10} {'Opponent':<15} {'Selected':<8} {'Available':<9}")
    print("-" * 50)

    for i, match in enumerate(filtered_matches, 1):
        date_fmt = match["date"].strftime("%d %b %y")
        selected_count = len(match["players"])
        active_players = [p for p in players if p not in inactive_players]
        available_count = len([p for p in active_players if p not in match["players"]])

        selected_display = "-" if selected_count == 0 else str(selected_count)
        available_display = "-" if available_count == 0 else str(available_count)

        print(f"{i:<4} {date_fmt:<10} {match['opponent']:<15} {selected_display:<8} {available_display:<9}")

    while True:
        choice = input("\nChoose match number(s) (e.g. 1 or 1,3,5): ").strip()
        if not choice:
            continue

        try:
            # Parse comma-separated numbers
            match_numbers = [int(x.strip()) for x in choice.split(',')]

            # Validate all numbers are in range and limit to 4 matches
            if len(match_numbers) > 4:
                print("Maximum 4 matches can be selected at once")
                continue

            valid_numbers = all(1 <= num <= len(filtered_matches) for num in match_numbers)

            if valid_numbers and match_numbers:
                selected_matches = [filtered_matches[num - 1] for num in match_numbers]
                break
            else:
                print(f"Please enter numbers between 1 and {len(filtered_matches)}, separated by commas")
        except ValueError:
            print("Please enter valid numbers separated by commas (e.g. 1,3,5)")

    # Show team selection table for selected matches
    print("\n=== Team Selection ===")

    # Display matches vertically with available players in columns
    for i, match in enumerate(selected_matches, 1):
        date_fmt = match["date"].strftime("%d %b %y")
        header = f"{i}. {date_fmt} VS {match['opponent']}".upper()

        # Get available players for this match
        active_players = [p for p in players if p not in inactive_players]
        available_players = [p for p in active_players if p not in match["players"]]

        # Split available players into two columns
        half = (len(available_players) + 1) // 2
        col1 = available_players[:half]
        col2 = available_players[half:]

        print(f"\n{header:<30} | Available Players")
        print("-" * 30 + "-|-" + "-" * 40)

        # Show selected players and available players side by side
        max_rows = max(len(match["players"]), len(col1))

        for row in range(max_rows):
            # Selected player column
            if row < len(match["players"]):
                player = match["players"][row]
                status = " (Inac)" if player in inactive_players else ""
                selected_display = f" {row+1}. {player}{status}"
            else:
                selected_display = ""

            # Available players columns
            avail1 = col1[row] if row < len(col1) else ""
            avail2 = col2[row] if row < len(col2) else ""

            print(f"{selected_display:<30} | {avail1:<18} | {avail2}")

        if not match["players"]:
            print(f"{'No players selected':<30} | {col1[0] if col1 else '':<18} | {col2[0] if col2 else ''}")

    print(f"\nSelected {len(selected_matches)} match(es) for team selection.")
    print("Team selection functionality will be enhanced in next update.")

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

def make_player_inactive():
    """Make a player inactive"""
    if not players:
        print("\nNo players to make inactive.")
        return

    active_players = [player for player in players if player not in inactive_players]

    if not active_players:
        print("\nNo active players to make inactive.")
        return

    print("\n=== Make Player Inactive ===")

    # Show active players
    total = len(active_players)
    half = (total + 1) // 2  # Round up for odd numbers

    print("-" * 64)
    left_header = f"{'No.':<3} {'Player':<20} {'Status':<6}"
    right_header = f"{'No.':<3} {'Player':<20} {'Status':<6}"
    print(f"{left_header}  {right_header}")
    print("-" * 64)

    for i in range(half):
        # Left column
        left_no = i + 1
        left_player = active_players[i][:20]  # Truncate if too long
        left_line = f"{left_no:<3} {left_player:<20} {'Actv':<6}"

        # Right column (if exists)
        right_idx = i + half
        if right_idx < total:
            right_no = right_idx + 1
            right_player = active_players[right_idx][:20]  # Truncate if too long
            right_line = f"{right_no:<3} {right_player:<20} {'Actv':<6}"
            print(f"{left_line}  {right_line}")
        else:
            print(left_line)

    print("-" * 64)
    # Get player selection
    made_inactive_count = 0

    while active_players:  # Continue while there are active players
        # Get player selection
        choice = input("\nEnter player number to make inactive (or Enter to finish): ").strip()
        if not choice:  # Empty input - finish
            break

        if choice.isdigit() and 1 <= int(choice) <= len(active_players):
            selected_player = active_players[int(choice) - 1]

            # Make the player inactive
            inactive_players.append(selected_player)
            active_players.remove(selected_player)  # Remove from our working list
            made_inactive_count += 1
            print(f"\n✓ {selected_player.upper()} has been made inactive")

            # Show updated list if there are still active players
            if active_players:
                print(f"\nRemaining active players: {len(active_players)}")
            else:
                print("\nAll players are now inactive.")
                break
        else:
            print(f"Please enter 1-{len(active_players)}")

    if made_inactive_count > 0:
        save_data()
        print(f"\nFinished. Made {made_inactive_count} player(s) inactive.")
    else:
        print("\nNo players were made inactive.")

def make_player_active():
    """Make an inactive player active again"""
    if not players:
        print("\nNo players registered.")
        return

    if not inactive_players:
        print("\nNo inactive players to reactivate.")
        return

    print("\n=== Make Player Active ===")

    # Show inactive players in two columns
    total = len(inactive_players)
    half = (total + 1) // 2

    print("-" * 64)
    left_header = f"{'No.':<3} {'Player':<20} {'Status':<6}"
    right_header = f"{'No.':<3} {'Player':<20} {'Status':<6}"
    print(f"{left_header}  {right_header}")
    print("-" * 64)

    for i in range(half):
        # Left column
        left_no = i + 1
        left_player = inactive_players[i][:20]
        left_line = f"{left_no:<3} {left_player:<20} {'Inac':<6}"

        # Right column (if exists)
        right_idx = i + half
        if right_idx < total:
            right_no = right_idx + 1
            right_player = inactive_players[right_idx][:20]
            right_line = f"{right_no:<3} {right_player:<20} {'Inac':<6}"
            print(f"{left_line}  {right_line}")
        else:
            print(left_line)

    print("-" * 64)

    made_active_count = 0

    while inactive_players:
        choice = input("\nEnter player number to make active (or Enter to finish): ").strip()
        if not choice:
            break

        if choice.isdigit() and 1 <= int(choice) <= len(inactive_players):
            selected_player = inactive_players[int(choice) - 1]

            # Make the player active
            inactive_players.remove(selected_player)
            made_active_count += 1
            print(f"\n✓ {selected_player.upper()} has been made active")

            if inactive_players:
                print(f"\nRemaining inactive players: {len(inactive_players)}")
            else:
                print("\nAll players are now active.")
                break
        else:
            print(f"Please enter 1-{len(inactive_players)}")

    if made_active_count > 0:
        save_data()
        print(f"\nFinished. Made {made_active_count} player(s) active.")
    else:
        print("\nNo players were made active.")

def edit_player_name():
    """Edit an existing player's name"""
    if not players:
        print("\nNo players to edit.")
        return

    sorted_players = sorted(players)

    print("\n=== Edit Player Name ===")
    print("-" * 40)
    print(f"{'No.':<4} {'Player':<30}")
    print("-" * 40)
    for i, player in enumerate(sorted_players, 1):
        print(f"{i:<4} {player:<30}")
    print("-" * 40)

    # Get player selection
    while True:
        choice = input("\nEnter player number to edit (or Enter to cancel): ").strip()
        if not choice:
            print("Edit cancelled.")
            return
        if choice.isdigit() and 1 <= int(choice) <= len(sorted_players):
            player_index = int(choice) - 1
            old_name = sorted_players[player_index]
            break
        print(f"Please enter 1-{len(sorted_players)}")

    # Get new name
    while True:
        new_name = smart_title(input(f"\nEnter new name for {old_name}: ").strip())
        if not new_name:
            print("Name cannot be empty.")
            continue
        if any(ch.isdigit() for ch in new_name):
            print("Player name cannot contain numbers.")
            continue
        if new_name in players and new_name != old_name:
            print(f"{new_name} already exists. Choose a different name.")
            continue
        break

    # Update player name everywhere
    original_index = players.index(old_name)
    players[original_index] = new_name

    # Update in matches too
    for match in matches:
        if old_name in match.get("players", []):
            match["players"] = [new_name if p == old_name else p for p in match["players"]]
        if old_name in match.get("paid", []):
            match["paid"] = [new_name if p == old_name else p for p in match["paid"]]

    save_data()
    print(f"\n✓ Changed '{old_name}' to '{new_name}'")

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
                left_status = 'Inac' if sorted_players[i] in inactive_players else 'Actv'
                left_line = f"{left_no:<3} {left_player:<20} {left_status:<6}"

                # Right column (if exists)
                right_idx = i + half
                if right_idx < total:
                    right_no = right_idx + 1
                    right_player = sorted_players[right_idx][:20]  # Truncate if too long
                    right_status = 'Inac' if sorted_players[right_idx] in inactive_players else 'Actv'
                    right_line = f"{right_no:<3} {right_player:<20} {right_status:<6}"
                    print(f"{left_line}  {right_line}")
                else:
                    print(left_line)

            print("-" * 64)
            print(f"Total: {total} players")

        # Show menu options in two columns
        print("\nOptions:")
        print("1) Add player                4) Make player inactive")
        print("2) Edit player name          5) Make player active")
        print("3) Select players for matches")
        print()
        print("b) Back to main menu")

        choice = input("Choose option from player menu above:").strip().lower()

        if choice == 'b':
            break
        elif choice == '1':
            add_player()
        elif choice == '2':
            edit_player_name()
        elif choice == '3':
            mark_attendance()
        elif choice == '4':
            make_player_inactive()
        elif choice == '5':
            make_player_active()
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
