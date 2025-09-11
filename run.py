from datetime import datetime, date
import json
import os

DATA_FILE = "data.json"


players = []
matches = []
inactive_players = []


def create_demo_data():
    """Create demo data for Heroku deployment when no data.json exists"""
    global club_name, players, matches, inactive_players

    club_name = "Demo Rugby Club"

    players = [
        "Antoine Dupont",
        "Ardie Savea",
        "Ben Earl",
        "Bundee Aki",
        "Caelan Doris",
        "Dan Sheehan",
        "Duhan van der Merwe",
        "Eben Etzebeth",
        "Faf de Klerk",
        "Finn Russell",
        "Handré Pollard",
        "Hugo Keenan",
        "Jordie Barrett",
        "Malcolm Marx",
        "Owen Farrell",
        "Romain Ntamack",
        "Siya Kolisi",
        "Thomas Ramos",
        "Will Jordan",
        "Will Skelton",
    ]

    inactive_players = ["Owen Farrell"]  # Making one player inactive for demo

    # Create demo matches
    from datetime import date

    matches = [
        {
            "opponent": "Dublin RFC",
            "date": date(2025, 9, 15),
            "fee": 10.0,
            "players": [
                "Antoine Dupont",
                "Ardie Savea",
                "Ben Earl",
                "Bundee Aki",
                "Caelan Doris",
                "Dan Sheehan",
                "Duhan van der Merwe",
            ],
            "paid": ["Antoine Dupont", "Ardie Savea"],
        },
        {
            "opponent": "Edinburgh RFC",
            "date": date(2025, 9, 22),
            "fee": 10.0,
            "players": ["Finn Russell", "Hugo Keenan", "Siya Kolisi"],
            "paid": [],
        },
        {
            "opponent": "London RFC",
            "date": date(2025, 9, 29),
            "fee": 10.0,
            "players": [],
            "paid": [],
        },
        {
            "opponent": "Cape Town RFC",
            "date": date(2025, 10, 6),
            "fee": 10.0,
            "players": [],
            "paid": [],
        },
        {
            "opponent": "Auckland RFC",
            "date": date(2025, 10, 13),
            "fee": 10.0,
            "players": [],
            "paid": [],
        },
    ]


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
        create_demo_data()
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
    print("Press Enter with empty name when finished.")
    print("Type 'b' to go back to player management.\n")

    added_count = 0

    while True:
        name_input = input(
            "Enter player name (or Enter to finish, 'b' to go back): "
        ).strip()

        if not name_input:  # Empty input - finish adding
            if added_count == 0:
                print("\nNo players added.")
            else:
                print(f"\nFinished. Added {added_count} player(s).")
            break

        if name_input.lower() == "b":  # Back option
            if added_count > 0:
                print(
                    f"\nReturning to player management. Added {added_count} player(s)."
                )
            else:
                print("\nReturning to player management.")
            break

        name = smart_title(name_input)

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
    Print all players in two columns with status information.
    """
    print("\n=== Current Players ===")

    if not players:
        print("\nNo players registered yet.")
        return

    sorted_players = sorted(players)
    total = len(sorted_players)
    half = (total + 1) // 2  # Round up for odd numbers

    print("-" * 64)
    left_header = f"{'No.':<3} {'Player':<20} {'Status':<6}"
    right_header = f"{'No.':<3} {'Player':<20} {'Status':<6}"
    print(f"{left_header}  {right_header}")
    print("-" * 64)

    for i in range(half):
        # Left column
        left_no = i + 1
        left_player = sorted_players[i][:20]  # Truncate if too long
        left_status = "Inac" if sorted_players[i] in inactive_players else "Actv"
        left_line = f"{left_no:<3} {left_player:<20} {left_status:<6}"

        # Right column (if exists)
        right_idx = i + half
        if right_idx < total:
            right_no = right_idx + 1
            right_player = sorted_players[right_idx][:20]  # Truncate if too long
            right_status = (
                "Inac" if sorted_players[right_idx] in inactive_players else "Actv"
            )
            right_line = f"{right_no:<3} {right_player:<20} {right_status:<6}"
            print(f"{left_line}  {right_line}")
        else:
            print(left_line)

    print("-" * 64)
    print(
        f"Total: {total} players ({len([p for p in players if p not in inactive_players])} active, {len(inactive_players)} inactive)"
    )

    # Wait for user input before returning to player management
    input("\nPress Enter to return to main menu...")


def add_match():
    """
    Handle fixture operations - add, edit, or delete matches
    """
    while True:
        print("\n=== Fixtures ===")

        if matches:
            # Show existing fixtures
            sorted_matches = get_matches_sorted()
            print(f"\n{'No.':<3} {'Date':<10} {'Opponent':<20} {'Fee':<8}")
            print("-" * 45)

            for i, match in enumerate(sorted_matches, 1):
                date_fmt = match["date"].strftime("%d %b %y")
                fee_fmt = f"£{match['fee']:.2f}"
                print(f"{i:<3} {date_fmt:<10} {match['opponent']:<20} {fee_fmt:<8}")

            print("-" * 45)
            print(f"Total: {len(matches)} fixture(s)")
        else:
            print("\nNo fixtures scheduled yet.")

        print("\nOptions:")
        print("1) Add new fixture")
        if matches:
            print("2) Edit fixture")
            print("3) Delete fixture")
        print("b) Back to main menu")
        print()

        choice = input("Choose option: ").strip().lower()

        if choice == "b":
            break
        elif choice == "1":
            add_new_fixture()
        elif choice == "2" and matches:
            edit_existing_fixture()
        elif choice == "3" and matches:
            delete_existing_fixture()
        else:
            print("Please choose a valid option.")


def add_new_fixture():
    """Add a new fixture"""
    print("\n=== Add New Fixture ===")
    print("Enter fixture details (type 'b' at any prompt to go back)\n")

    # Get opponent
    while True:
        opponent_input = input("Enter match opponent (or 'b' to go back): ").strip()
        if opponent_input.lower() == "b":
            return

        opponent = smart_title(opponent_input)
        if not opponent:
            print("Opponent cannot be empty. Please try again.")
            continue

        print(f"Opponent: {opponent}")
        break

    # Get date
    while True:
        date_input = input(
            "Enter match date (DD/MM/YY or DD/MM/YYYY, or 'b' to go back): "
        ).strip()
        if date_input.lower() == "b":
            return

        if not date_input:
            print("Date cannot be empty. Please try again.")
            continue

        try:
            parsed_date = datetime.strptime(date_input, "%d/%m/%y").date()
            break
        except ValueError:
            try:
                parsed_date = datetime.strptime(date_input, "%d/%m/%Y").date()
                break
            except ValueError:
                print(
                    "Invalid date. Please use DD/MM/YY (e.g. 05/09/25) or DD/MM/YYYY (e.g. 05/09/2025)."
                )
                continue

    # Get fee
    while True:
        fee_input = input("Enter match fee (or 'b' to go back): ").strip()
        if fee_input.lower() == "b":
            return

        if not fee_input:
            print("Fee cannot be empty. Please try again.")
            continue

        try:
            fee = float(fee_input)
            print(f"Match fee recorded: £{fee:.2f}")
            break
        except ValueError:
            print("Invalid fee. Please enter a number.")
            continue

    # Create match object
    match = {
        "opponent": opponent,
        "date": parsed_date,
        "fee": fee,
        "players": [],
        "paid": [],
    }

    # Check for duplicate matches
    for existing_match in matches:
        if (
            existing_match["opponent"] == opponent
            and existing_match["date"] == parsed_date
        ):
            print(
                f"\n⚠ Note: You already have {club_name} vs {opponent} on {parsed_date.strftime('%d/%m/%Y')}"
            )
            while True:
                confirm = (
                    input("Add this match anyway? (y/n/b to go back): ").strip().lower()
                )
                if confirm == "b":
                    return
                elif confirm == "y":
                    break
                elif confirm == "n":
                    print("Match not added.")
                    return
                else:
                    print("Please enter 'y', 'n', or 'b'")
            break

    # Add the match
    matches.append(match)
    save_data()
    print(
        f"\n✓ Fixture added: {club_name} vs {opponent} on {parsed_date.strftime('%d/%m/%Y')} - £{fee:.2f}"
    )


def edit_existing_fixture():
    """Edit an existing fixture"""
    sorted_matches = get_matches_sorted()

    print("\n=== Edit Fixture ===")

    # Select fixture to edit
    while True:
        choice = input("Enter fixture number to edit (or 'b' to go back): ").strip()
        if choice.lower() == "b":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(sorted_matches):
            selected_match = sorted_matches[int(choice) - 1]
            break
        print(f"Please enter 1-{len(sorted_matches)} or 'b'")

    # Show what we're editing
    print(
        f"\nEditing: {selected_match['opponent']} on {selected_match['date'].strftime('%d/%m/%Y')}"
    )

    # Simple edit options
    while True:
        print(f"\nCurrent details:")
        print(f"Date: {selected_match['date'].strftime('%d/%m/%Y')}")
        print(f"Opponent: {selected_match['opponent']}")
        print(f"Fee: £{selected_match['fee']:.2f}")

        print(f"\nWhat to edit?")
        print("1) Date")
        print("2) Opponent")
        print("3) Fee")
        print("b) Back")

        edit_choice = input("\nChoose: ").strip().lower()

        if edit_choice == "b":
            return
        elif edit_choice == "1":
            # Edit date
            new_date = input("New date (DD/MM/YY or DD/MM/YYYY): ").strip()
            try:
                parsed_date = datetime.strptime(new_date, "%d/%m/%y").date()
            except ValueError:
                try:
                    parsed_date = datetime.strptime(new_date, "%d/%m/%Y").date()
                except ValueError:
                    print("Invalid date format.")
                    continue
            selected_match["date"] = parsed_date
            save_data()
            print(f"✓ Date updated to {parsed_date.strftime('%d/%m/%Y')}")

        elif edit_choice == "2":
            # Edit opponent
            new_opponent = smart_title(input("New opponent: ").strip())
            if new_opponent:
                selected_match["opponent"] = new_opponent
                save_data()
                print(f"✓ Opponent updated to {new_opponent}")

        elif edit_choice == "3":
            # Edit fee
            try:
                new_fee = float(input("New fee: ").strip())
                selected_match["fee"] = new_fee
                save_data()
                print(f"✓ Fee updated to £{new_fee:.2f}")
            except ValueError:
                print("Invalid fee.")
        else:
            print("Please choose 1, 2, 3, or b")


def delete_existing_fixture():
    """Delete an existing fixture"""
    sorted_matches = get_matches_sorted()

    print("\n=== Delete Fixture ===")

    # Select fixture to delete
    while True:
        choice = input("Enter fixture number to delete (or 'b' to go back): ").strip()
        if choice.lower() == "b":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(sorted_matches):
            selected_match = sorted_matches[int(choice) - 1]
            break
        print(f"Please enter 1-{len(sorted_matches)} or 'b'")

    # Confirm deletion
    print(
        f"\nDelete: {selected_match['opponent']} on {selected_match['date'].strftime('%d/%m/%Y')}?"
    )
    if selected_match["players"]:
        print(
            f"⚠ WARNING: This fixture has {len(selected_match['players'])} players selected"
        )

    confirm = input("Type 'DELETE' to confirm: ").strip()

    if confirm == "DELETE":
        # Find and remove from original matches list
        for i, match in enumerate(matches):
            if (
                match["date"] == selected_match["date"]
                and match["opponent"] == selected_match["opponent"]
            ):
                matches.pop(i)
                break

        save_data()
        print(f"✓ Fixture deleted")
    else:
        print("Delete cancelled.")


def mark_attendance():
    """
    Mark a player as attended for a match.
    """
    global matches, players, inactive_players

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
        if filter_choice == "b":
            return
        if filter_choice not in ["1", "2", "3", "4"]:
            print("Please enter 1, 2, 3, 4, or b")
            continue

        filter_choice = int(filter_choice)

        # Filter matches based on selection
        from datetime import timedelta

        today = datetime.now().date()

        if filter_choice == 1:  # Recent + upcoming (4 weeks total)
            start_date = today - timedelta(days=14)
            end_date = today + timedelta(days=14)
            filtered_matches = [
                m for m in get_matches_sorted() if start_date <= m["date"] <= end_date
            ]
        elif filter_choice == 2:  # Last month
            start_date = today - timedelta(days=30)
            end_date = today
            filtered_matches = [
                m for m in get_matches_sorted() if start_date <= m["date"] <= end_date
            ]
        elif filter_choice == 3:  # Next month
            start_date = today
            end_date = today + timedelta(days=30)
            filtered_matches = [
                m for m in get_matches_sorted() if start_date <= m["date"] <= end_date
            ]
        elif filter_choice == 4:  # All matches
            filtered_matches = get_matches_sorted()

        if not filtered_matches:
            print("\nNo matches found for the selected period. Try a different filter.")
            continue  # Go back to filter menu

        break  # Exit loop if we have matches

    # Display filtered matches in table format
    print("\n=== Matches ===")
    print(f"{'No.':<4} {'Date':<10} {'Opponent':<25} {'Selected':<8} {'Available':<9}")
    print("-" * 60)

    for i, match in enumerate(filtered_matches, 1):
        date_fmt = match["date"].strftime("%d %b %y")
        selected_count = len(match["players"])
        active_players_list = [p for p in players if p not in inactive_players]
        available_count = len(
            [p for p in active_players_list if p not in match["players"]]
        )

        selected_display = "-" if selected_count == 0 else str(selected_count)
        available_display = "-" if available_count == 0 else str(available_count)

        print(
            f"{i:<4} {date_fmt:<10} {match['opponent']:<25} {selected_display:<8} {available_display:<9}"
        )

    print("\nA maximum of 4 matches can be selected for team selections")

    while True:
        choice = input(
            "\nChoose match number(s) (e.g. 1 or 1,3,5) or 'b' to go back (max 4 matches): "
        ).strip()

        if choice.lower() == "b":
            return  # Go back to main menu

        if not choice:
            continue

        try:
            # Parse comma-separated numbers
            match_numbers = [int(x.strip()) for x in choice.split(",")]

            # Validate all numbers are in range and limit to 4 matches
            if len(match_numbers) > 4:
                print("Maximum 4 matches can be selected at once for team selection")
                continue

            valid_numbers = all(
                1 <= num <= len(filtered_matches) for num in match_numbers
            )

            if valid_numbers and match_numbers:
                selected_matches = [filtered_matches[num - 1] for num in match_numbers]
                break
            else:
                print(
                    f"Please enter numbers between 1 and {len(filtered_matches)}, separated by commas"
                )
        except ValueError:
            print(
                "Please enter valid numbers separated by commas (e.g. 1,3,5) or 'b' to go back"
            )

    # Main team selection loop - regenerate display after each action
    while True:
        # Show team selection table for selected matches
        print("\n=== Team Selection ===")

        # Display matches vertically with available players in columns
        for i, match in enumerate(selected_matches, 1):
            date_fmt = match["date"].strftime("%d %b %y")
            header = f"{i}. {date_fmt} VS {match['opponent']}".upper()

            # Get available players for this match - use safe variable names
            active_players_list = [p for p in players if p not in inactive_players]
            available_players_list = [
                p for p in active_players_list if p not in match["players"]
            ]

            # Split available players into two columns
            half = (len(available_players_list) + 1) // 2
            col1 = available_players_list[:half]
            col2 = available_players_list[half:]

            print(f"\n{header:<30} | Available Players")
            print("-" * 30 + "-|-" + "-" * 40)

            # Show selected players and available players side by side
            max_rows = max(len(match["players"]), len(col1))

            for row in range(max_rows):
                # Selected player column
                if row < len(match["players"]):
                    player = match["players"][row]
                    selected_display = f" {row+1}. {player}"
                else:
                    selected_display = ""

                # Available players columns
                avail1 = col1[row] if row < len(col1) else ""
                avail2 = col2[row] if row < len(col2) else ""

                print(f"{selected_display:<30} | {avail1:<18} | {avail2}")

            # Show "No players selected" only if no players are selected
            if not match["players"]:
                print(
                    f"{'No players selected':<30} | {col1[0] if col1 else '':<18} | {col2[0] if col2 else ''}"
                )

        print(f"\nSelected {len(selected_matches)} match(es) for team selection.")

        print("\nOptions:")
        print("1) Add players to matches")
        print("2) Remove players from matches")
        print("b) Back to main menu")
        main_choice = input("\nChoose option: ").strip().lower()

        if main_choice == "1":
            # Add players functionality
            add_players_to_matches(selected_matches)
        elif main_choice == "2":
            # Remove players functionality
            remove_players_from_matches(selected_matches)
        elif main_choice == "b":
            break  # Return to main menu
        else:
            print("Please enter 1, 2, or b")
            input("Press Enter to continue...")


def add_players_to_matches(selected_matches):
    """Handle adding players to matches in main team selection context"""
    while True:
        # Find players available for matches
        local_active_players = [p for p in players if p not in inactive_players]
        local_player_availability = []

        for local_player in local_active_players:
            local_available_match_nums = []
            local_availability_display = []

            for local_i, local_match in enumerate(selected_matches, 1):
                if local_player not in local_match["players"]:
                    local_available_match_nums.append(str(local_i))
                    local_availability_display.append("-Avail-")
                else:
                    local_availability_display.append("-")

            if local_available_match_nums:
                local_player_availability.append(
                    (
                        local_player,
                        local_availability_display,
                        local_available_match_nums,
                    )
                )

        # Sort players by number of available matches (descending)
        local_player_availability.sort(key=lambda x: len(x[2]), reverse=True)

        print("\n=== Add Players to Matches ===")

        # Show simple match reference list
        print("Selected matches:")
        for local_i, local_match in enumerate(selected_matches, 1):
            local_date_fmt = local_match["date"].strftime("%d %b %y")
            local_team_count = len(local_match["players"])
            print(
                f"{local_i}. {local_date_fmt} vs {local_match['opponent']} ({local_team_count} players)"
            )

        # Show players with their available matches
        print(f"\nPlayer availability:")

        if local_player_availability:
            # Create dynamic header
            local_header = f"{'No.':<3} {'Player':<20}"
            local_base_width = 25

            for local_i, local_match in enumerate(selected_matches, 1):
                local_header += f" {'Available':<9}"
                local_base_width += 10

            local_separator = "-" * local_base_width
            print(local_separator)
            print(local_header)
            print(local_separator)

            for local_i, (
                local_player,
                local_availability,
                local_match_nums,
            ) in enumerate(local_player_availability, 1):
                local_line = f"{local_i:<3} {local_player:<20}"
                for local_avail in local_availability:
                    local_display_avail = local_avail if local_avail != "-" else "-"
                    if local_display_avail != "-":
                        local_display_avail = local_display_avail[:8]
                    local_line += f" {local_display_avail:<9}"
                print(local_line)

            print(local_separator)
            print(f"Total available players: {len(local_player_availability)}")

            # FIXED: Go directly to player selection instead of showing menu
            local_players_input = input(
                f"\nChoose player(s) (e.g. 1 or 1,3,5 or 1-5 or 'all') or 'b' to go back: "
            ).strip()

            if local_players_input.lower() == "b":
                break

            try:
                if local_players_input.lower() == "all":
                    local_player_numbers = list(
                        range(1, len(local_player_availability) + 1)
                    )
                elif "-" in local_players_input and "," not in local_players_input:
                    local_start, local_end = map(int, local_players_input.split("-"))
                    if 1 <= local_start <= local_end <= len(local_player_availability):
                        local_player_numbers = list(range(local_start, local_end + 1))
                    else:
                        print(
                            f"Range must be between 1 and {len(local_player_availability)}"
                        )
                        input("Press Enter to continue...")
                        continue
                else:
                    local_player_numbers = [
                        int(x.strip()) for x in local_players_input.split(",")
                    ]

                if all(
                    1 <= num <= len(local_player_availability)
                    for num in local_player_numbers
                ):
                    local_selected_players_info = [
                        local_player_availability[num - 1]
                        for num in local_player_numbers
                    ]

                    # Show selected players
                    print(f"\n=== Selected Players ===")
                    for local_i, (
                        local_player,
                        local_availability,
                        local_match_nums,
                    ) in enumerate(local_selected_players_info, 1):
                        print(f"{local_i}. {local_player}")

                    # Show matches again for easy reference
                    print(f"\n=== Available Matches ===")
                    for local_i, local_match in enumerate(selected_matches, 1):
                        local_date_fmt = local_match["date"].strftime("%d %b %y")
                        local_team_count = len(local_match["players"])
                        print(
                            f"{local_i}. {local_date_fmt} vs {local_match['opponent']} ({local_team_count} players)"
                        )

                    # Select matches
                    local_matches_input = (
                        input(
                            f"\nAdd selected players to which matches? (e.g. 1 or 1,3,4 or 'all'): "
                        )
                        .strip()
                        .lower()
                    )

                    if local_matches_input == "all":
                        local_target_match_indices = list(range(len(selected_matches)))
                    else:
                        try:
                            local_match_numbers = [
                                int(x.strip()) for x in local_matches_input.split(",")
                            ]
                            if all(
                                1 <= num <= len(selected_matches)
                                for num in local_match_numbers
                            ):
                                local_target_match_indices = [
                                    num - 1 for num in local_match_numbers
                                ]
                            else:
                                print(
                                    f"Please enter numbers between 1 and {len(selected_matches)}"
                                )
                                input("Press Enter to continue...")
                                continue
                        except ValueError:
                            print("Invalid input")
                            input("Press Enter to continue...")
                            continue

                    # Add players to selected matches
                    local_added_count = 0
                    for (
                        local_player,
                        local_availability,
                        local_available_match_nums,
                    ) in local_selected_players_info:
                        local_available_indices = [
                            int(x) - 1 for x in local_available_match_nums
                        ]

                        for local_match_idx in local_target_match_indices:
                            if local_match_idx in local_available_indices:
                                selected_matches[local_match_idx]["players"].append(
                                    local_player
                                )
                                local_added_count += 1

                    save_data()

                    # Show confirmation
                    if local_added_count > 0:
                        print(f"\n✓ Added players successfully!")

                        for local_match_idx in local_target_match_indices:
                            local_match = selected_matches[local_match_idx]
                            local_date_fmt = local_match["date"].strftime("%d %b %y")
                            local_added_to_this_match = []

                            for (
                                local_player,
                                local_availability,
                                local_available_match_nums,
                            ) in local_selected_players_info:
                                local_available_indices = [
                                    int(x) - 1 for x in local_available_match_nums
                                ]
                                if local_match_idx in local_available_indices:
                                    local_added_to_this_match.append(local_player)

                            if local_added_to_this_match:
                                print(
                                    f"\n{local_date_fmt} vs {local_match['opponent']}:"
                                )
                                for local_player in local_added_to_this_match:
                                    print(f"  • {local_player}")
                    else:
                        print(
                            "\nNo players were added (they may already be selected for those matches)"
                        )

                    input("\nPress Enter to continue...")
                    # Continue the loop to refresh the available players list
                else:
                    print(
                        f"Please enter numbers between 1 and {len(local_player_availability)}"
                    )
                    input("Press Enter to continue...")
            except ValueError:
                print("Please enter valid numbers separated by commas")
                input("Press Enter to continue...")
        else:
            print("\nNo players available for any matches.")
            input("Press Enter to continue...")
            break


def remove_players_from_matches(selected_matches):
    """Handle removing players from matches in main team selection context"""
    while True:
        # Find players currently in matches
        local_player_removal_options = []

        for local_player in sorted(players):
            if local_player in inactive_players:
                continue  # Skip inactive players

            local_current_match_nums = []
            local_player_match_display = []

            for local_i, local_match in enumerate(selected_matches, 1):
                if local_player in local_match["players"]:
                    local_current_match_nums.append(str(local_i))
                    local_player_match_display.append("-Avail-")
                else:
                    local_player_match_display.append("-")

            if local_current_match_nums:
                local_player_removal_options.append(
                    (local_player, local_player_match_display, local_current_match_nums)
                )

        # Sort players by number of matches they're in (descending)
        local_player_removal_options.sort(key=lambda x: len(x[2]), reverse=True)

        print("\n=== Remove Players from Matches ===")

        # Show simple match reference list
        print("Selected matches:")
        for local_i, local_match in enumerate(selected_matches, 1):
            local_date_fmt = local_match["date"].strftime("%d %b %y")
            local_team_count = len(local_match["players"])
            print(
                f"{local_i}. {local_date_fmt} vs {local_match['opponent']} ({local_team_count} players)"
            )

        # Show players with their current matches
        print(f"\nPlayers currently in matches:")

        if local_player_removal_options:
            # Create dynamic header
            local_header = f"{'No.':<3} {'Player':<20}"
            local_base_width = 25

            for local_i, local_match in enumerate(selected_matches, 1):
                local_header += f" {'Available':<9}"
                local_base_width += 10

            local_separator = "-" * local_base_width
            print(local_separator)
            print(local_header)
            print(local_separator)

            for local_i, (
                local_player,
                local_player_match_display,
                local_match_nums,
            ) in enumerate(local_player_removal_options, 1):
                local_line = f"{local_i:<3} {local_player:<20}"
                for local_match_status in local_player_match_display:
                    local_display_status = (
                        local_match_status if local_match_status != "-" else "-"
                    )
                    if local_display_status != "-":
                        local_display_status = local_display_status[:8]
                    local_line += f" {local_display_status:<9}"
                print(local_line)

            print(local_separator)
            print(f"Total players in matches: {len(local_player_removal_options)}")

            # FIXED: Go directly to player selection instead of showing menu
            local_players_input = input(
                f"\nChoose player(s) to remove (e.g. 1 or 1,3,5 or 1-5 or 'all') or 'b' to go back: "
            ).strip()

            if local_players_input.lower() == "b":
                break

            try:
                if local_players_input.lower() == "all":
                    local_player_numbers = list(
                        range(1, len(local_player_removal_options) + 1)
                    )
                elif "-" in local_players_input and "," not in local_players_input:
                    local_start, local_end = map(int, local_players_input.split("-"))
                    if (
                        1
                        <= local_start
                        <= local_end
                        <= len(local_player_removal_options)
                    ):
                        local_player_numbers = list(range(local_start, local_end + 1))
                    else:
                        print(
                            f"Range must be between 1 and {len(local_player_removal_options)}"
                        )
                        input("Press Enter to continue...")
                        continue
                else:
                    local_player_numbers = [
                        int(x.strip()) for x in local_players_input.split(",")
                    ]

                if all(
                    1 <= num <= len(local_player_removal_options)
                    for num in local_player_numbers
                ):
                    local_selected_players_info = [
                        local_player_removal_options[num - 1]
                        for num in local_player_numbers
                    ]

                    # Show selected players
                    print(f"\n=== Selected Players to Remove ===")
                    for local_i, (
                        local_player,
                        local_player_match_display,
                        local_current_match_nums,
                    ) in enumerate(local_selected_players_info, 1):
                        print(f"{local_i}. {local_player}")

                    # Show matches again for easy reference
                    print(f"\n=== Available Matches ===")
                    for local_i, local_match in enumerate(selected_matches, 1):
                        local_date_fmt = local_match["date"].strftime("%d %b %y")
                        local_team_count = len(local_match["players"])
                        print(
                            f"{local_i}. {local_date_fmt} vs {local_match['opponent']} ({local_team_count} players)"
                        )

                    # Select matches to remove players from
                    local_matches_input = (
                        input(
                            f"\nRemove selected players from which matches? (e.g. 1 or 1,3,4 or 'all'): "
                        )
                        .strip()
                        .lower()
                    )

                    if local_matches_input == "all":
                        local_target_match_indices = list(range(len(selected_matches)))
                    else:
                        try:
                            local_match_numbers = [
                                int(x.strip()) for x in local_matches_input.split(",")
                            ]
                            if all(
                                1 <= num <= len(selected_matches)
                                for num in local_match_numbers
                            ):
                                local_target_match_indices = [
                                    num - 1 for num in local_match_numbers
                                ]
                            else:
                                print(
                                    f"Please enter numbers between 1 and {len(selected_matches)}"
                                )
                                input("Press Enter to continue...")
                                continue
                        except ValueError:
                            print("Invalid input")
                            input("Press Enter to continue...")
                            continue

                    # Remove players from selected matches
                    local_removed_count = 0
                    for (
                        local_player,
                        local_player_match_display,
                        local_current_match_nums,
                    ) in local_selected_players_info:
                        local_current_indices = [
                            int(x) - 1 for x in local_current_match_nums
                        ]

                        for local_match_idx in local_target_match_indices:
                            if local_match_idx in local_current_indices:
                                if (
                                    local_player
                                    in selected_matches[local_match_idx]["players"]
                                ):
                                    selected_matches[local_match_idx]["players"].remove(
                                        local_player
                                    )
                                    local_removed_count += 1

                    save_data()

                    # Show confirmation
                    if local_removed_count > 0:
                        print(f"\n✓ Removed players successfully!")

                        for local_match_idx in local_target_match_indices:
                            local_match = selected_matches[local_match_idx]
                            local_date_fmt = local_match["date"].strftime("%d %b %y")
                            local_removed_from_this_match = []

                            for (
                                local_player,
                                local_player_match_display,
                                local_current_match_nums,
                            ) in local_selected_players_info:
                                local_current_indices = [
                                    int(x) - 1 for x in local_current_match_nums
                                ]
                                if local_match_idx in local_current_indices:
                                    local_removed_from_this_match.append(local_player)

                            if local_removed_from_this_match:
                                print(
                                    f"\n{local_date_fmt} vs {local_match['opponent']}:"
                                )
                                for local_player in local_removed_from_this_match:
                                    print(f"  • {local_player}")
                    else:
                        print(
                            "\nNo players were removed (they may not be selected for those matches)"
                        )

                    input("\nPress Enter to continue...")
                else:
                    print(
                        f"Please enter numbers between 1 and {len(local_player_removal_options)}"
                    )
                    input("Press Enter to continue...")
            except ValueError:
                print("Please enter valid numbers separated by commas")
                input("Press Enter to continue...")
        else:
            print("\nNo players currently selected for any matches.")
            input("Press Enter to continue...")
            break


def list_matches():
    """
    Display fixture list with match selection functionality
    """
    if not matches:
        print("\nNo matches scheduled yet.")
        return

    while True:  # Loop for filter selection
        # Show filter options
        print("\n=== Fixture List ===")
        print("Show matches:")
        print("1) Recent + upcoming (last 2 weeks + next 2 weeks)")
        print("2) Last month's matches")
        print("3) Next month's matches")
        print("4) All matches")
        print("b) Back to main menu")
        print()

        filter_choice = input("Choose filter: ").strip().lower()
        if filter_choice == "b":
            return
        if filter_choice not in ["1", "2", "3", "4"]:
            print("Please enter 1, 2, 3, 4, or b")
            continue

        filter_choice = int(filter_choice)

        # Filter matches based on selection
        from datetime import timedelta

        today = datetime.now().date()

        if filter_choice == 1:  # Recent + upcoming (4 weeks total)
            start_date = today - timedelta(days=14)
            end_date = today + timedelta(days=14)
            filtered_matches = [
                m for m in get_matches_sorted() if start_date <= m["date"] <= end_date
            ]
        elif filter_choice == 2:  # Last month
            start_date = today - timedelta(days=30)
            end_date = today
            filtered_matches = [
                m for m in get_matches_sorted() if start_date <= m["date"] <= end_date
            ]
        elif filter_choice == 3:  # Next month
            start_date = today
            end_date = today + timedelta(days=30)
            filtered_matches = [
                m for m in get_matches_sorted() if start_date <= m["date"] <= end_date
            ]
        elif filter_choice == 4:  # All matches
            filtered_matches = get_matches_sorted()

        if not filtered_matches:
            print("\nNo matches found for the selected period. Try a different filter.")
            continue  # Go back to filter menu

        break  # Exit loop if we have matches

    # Display fixtures for selection
    print("\n=== Select Fixtures to View ===")
    print(f"{'No.':<4} {'Date':<10} {'Opponent':<25} {'Status':<15}")
    print("-" * 58)

    for i, match in enumerate(filtered_matches, 1):
        date_fmt = match["date"].strftime("%d %b %y")

        if match["players"]:
            status = f"Team set ({len(match['players'])})"
        else:
            status = "Fixture only"

        print(f"{i:<4} {date_fmt:<10} {match['opponent']:<25} {status:<15}")

    print("A maximum of 10 matches can be selected for fixture details")

    while True:
        choice = input(
            "\nChoose match number(s) (e.g. 1 or 1,3,5 or 1-5 or 'all') or 'b' to go back (max 10 matches): "
        ).strip()

        if choice.lower() == "b":
            return

        if not choice:
            continue

        try:
            if choice.lower() == "all":
                # Select all filtered matches (up to 10)
                match_numbers = list(range(1, min(len(filtered_matches) + 1, 11)))
            elif "-" in choice and "," not in choice:
                # Handle range (e.g., 1-5)
                start, end = map(int, choice.split("-"))
                if 1 <= start <= end <= len(filtered_matches):
                    match_numbers = list(range(start, min(end + 1, 11)))
                else:
                    print(f"Range must be between 1 and {len(filtered_matches)}")
                    continue
            else:
                # Handle individual numbers or comma-separated
                match_numbers = [int(x.strip()) for x in choice.split(",")]

            # Validate all numbers are in range and limit to 10 matches
            if len(match_numbers) > 10:
                print("Maximum 10 matches can be selected at once for fixture details")
                continue

            valid_numbers = all(
                1 <= num <= len(filtered_matches) for num in match_numbers
            )

            if valid_numbers and match_numbers:
                selected_matches = [filtered_matches[num - 1] for num in match_numbers]
                break
            else:
                print(
                    f"Please enter numbers between 1 and {len(filtered_matches)}, separated by commas"
                )
        except ValueError:
            print(
                "Please enter valid numbers separated by commas (e.g. 1,3,5) or 'b' to go back"
            )

    # Display selected fixture details
    print("\n=== Fixture Details ===")

    for match in selected_matches:
        date_fmt = match["date"].strftime("%A, %d %B %Y")

        print(f"\n{club_name} vs {match['opponent']}")
        print(f"Date: {date_fmt}")

        if match["players"]:
            print(f"Status: Team selected ({len(match['players'])} players)")
        else:
            print("Status: Fixture scheduled - no team selected yet")

        print("-" * 50)

    # Summary
    if len(selected_matches) > 1:
        print(f"\nSummary for {len(selected_matches)} fixtures:")
        fixtures_with_teams = sum(1 for m in selected_matches if m["players"])
        fixtures_without_teams = len(selected_matches) - fixtures_with_teams

        if fixtures_with_teams > 0:
            print(f"Fixtures with teams selected: {fixtures_with_teams}")
        if fixtures_without_teams > 0:
            print(f"Fixtures needing team selection: {fixtures_without_teams}")

    input("\nPress Enter to continue...")


def show_team_sheets():
    """Display team sheets with match selection and team management options"""
    if not matches:
        print("\nNo matches recorded yet.")
        return

    while True:  # Loop for filter selection
        # Show filter options
        print("\n=== Team Sheets ===")
        print("Show matches:")
        print("1) Recent + upcoming (last 2 weeks + next 2 weeks)")
        print("2) Last month's matches")
        print("3) Next month's matches")
        print("4) All matches")
        print("b) Back to match fees menu")
        print()

        filter_choice = input("Choose filter: ").strip().lower()
        if filter_choice == "b":
            return
        if filter_choice not in ["1", "2", "3", "4"]:
            print("Please enter 1, 2, 3, 4, or b")
            continue

        filter_choice = int(filter_choice)

        # Filter matches based on selection
        from datetime import timedelta

        today = datetime.now().date()

        if filter_choice == 1:  # Recent + upcoming (4 weeks total)
            start_date = today - timedelta(days=14)
            end_date = today + timedelta(days=14)
            filtered_matches = [
                m for m in get_matches_sorted() if start_date <= m["date"] <= end_date
            ]
        elif filter_choice == 2:  # Last month
            start_date = today - timedelta(days=30)
            end_date = today
            filtered_matches = [
                m for m in get_matches_sorted() if start_date <= m["date"] <= end_date
            ]
        elif filter_choice == 3:  # Next month
            start_date = today
            end_date = today + timedelta(days=30)
            filtered_matches = [
                m for m in get_matches_sorted() if start_date <= m["date"] <= end_date
            ]
        elif filter_choice == 4:  # All matches
            filtered_matches = get_matches_sorted()

        if not filtered_matches:
            print("\nNo matches found for the selected period. Try a different filter.")
            continue  # Go back to filter menu

        break  # Exit loop if we have matches

    # Display fixtures for selection
    print("\n=== Select Matches for Team Sheets ===")
    print(f"{'No.':<4} {'Date':<10} {'Opponent':<25} {'Status':<15}")
    print("-" * 58)

    for i, match in enumerate(filtered_matches, 1):
        date_fmt = match["date"].strftime("%d %b %y")

        if match["players"]:
            status = f"Team set ({len(match['players'])})"
        else:
            status = "No team yet"

        print(f"{i:<4} {date_fmt:<10} {match['opponent']:<25} {status:<15}")

    print("A maximum of 8 matches can be selected for team sheets")

    while True:
        choice = input(
            "\nChoose match number(s) (e.g. 1 or 1,3,5 or 1-5 or 'all') or 'b' to go back (max 8 matches): "
        ).strip()

        if choice.lower() == "b":
            return

        if not choice:
            continue

        try:
            if choice.lower() == "all":
                # Select all filtered matches (up to 8)
                match_numbers = list(range(1, min(len(filtered_matches) + 1, 9)))
            elif "-" in choice and "," not in choice:
                # Handle range (e.g., 1-5)
                start, end = map(int, choice.split("-"))
                if 1 <= start <= end <= len(filtered_matches):
                    match_numbers = list(range(start, min(end + 1, 9)))
                else:
                    print(f"Range must be between 1 and {len(filtered_matches)}")
                    continue
            else:
                # Handle individual numbers or comma-separated
                match_numbers = [int(x.strip()) for x in choice.split(",")]

            # Validate all numbers are in range and limit to 8 matches
            if len(match_numbers) > 8:
                print("Maximum 8 matches can be selected at once for team sheets")
                continue

            valid_numbers = all(
                1 <= num <= len(filtered_matches) for num in match_numbers
            )

            if valid_numbers and match_numbers:
                selected_matches = [filtered_matches[num - 1] for num in match_numbers]
                break
            else:
                print(
                    f"Please enter numbers between 1 and {len(filtered_matches)}, separated by commas"
                )
        except ValueError:
            print(
                "Please enter valid numbers separated by commas (e.g. 1,3,5 or 1-5 or 'all') or 'b' to go back"
            )

    # Display selected team sheets in two columns
    print("\n=== Team Sheets ===")

    # Split matches into pairs for two-column display
    for i in range(0, len(selected_matches), 2):
        # Left column match
        left_match = selected_matches[i]
        left_date = left_match["date"].strftime("%d %b %y")
        left_header = f"{i+1}. {left_date} VS {left_match['opponent']}".upper()

        # Right column match (if exists)
        right_match = selected_matches[i + 1] if i + 1 < len(selected_matches) else None
        if right_match:
            right_date = right_match["date"].strftime("%d %b %y")
            right_header = f"{i+2}. {right_date} VS {right_match['opponent']}".upper()

        # Display headers
        if right_match:
            print(f"\n{left_header:<40} | {right_header}")
            print("-" * 40 + "|-" + "-" * 40)
        else:
            print(f"\n{left_header}")
            print("-" * 40)

        # Display team lists side by side
        left_players = (
            left_match["players"]
            if left_match["players"]
            else ["No players selected yet"]
        )
        right_players = (
            right_match["players"]
            if right_match and right_match["players"]
            else (["No players selected yet"] if right_match else [])
        )

        max_players = max(len(left_players), len(right_players))

        # Show team counts
        left_count = (
            f"Team ({len(left_match['players'])} players):"
            if left_match["players"]
            else "No team selected:"
        )
        right_count = (
            f"Team ({len(right_match['players'])} players):"
            if right_match and right_match["players"]
            else ("No team selected:" if right_match else "")
        )

        if right_match:
            print(f"{left_count:<40} | {right_count}")
        else:
            print(left_count)

        # Display players side by side
        for j in range(max_players):
            if j < len(left_players):
                if left_match["players"]:
                    left_display = f"  {j+1:2}. {left_players[j]}"
                else:
                    left_display = f"  {left_players[j]}"
            else:
                left_display = ""

            if right_match and j < len(right_players):
                if right_match["players"]:
                    right_display = f"  {j+1:2}. {right_players[j]}"
                else:
                    right_display = f"  {right_players[j]}"
            else:
                right_display = ""

            if right_match:
                print(f"{left_display:<40} | {right_display}")
            else:
                print(left_display)

    # Summary for multiple matches
    if len(selected_matches) > 1:
        total_matches = len(selected_matches)
        total_all_players = sum(len(m["players"]) for m in selected_matches)
        fixtures_with_teams = sum(1 for m in selected_matches if m["players"])
        fixtures_without_teams = total_matches - fixtures_with_teams

        print(f"\n{'='*50}")
        print(f"SUMMARY FOR {total_matches} MATCHES:")
        print(f"Total players selected: {total_all_players}")
        if fixtures_with_teams > 0:
            print(f"Fixtures with teams selected: {fixtures_with_teams}")
        if fixtures_without_teams > 0:
            print(f"Fixtures needing team selection: {fixtures_without_teams}")

    # Always show team management options after displaying teams
    print(f"\nTeam Management Options:")
    print("1) Update teams for these matches")
    print("b) Back to match fees menu")

    while True:
        team_choice = input("\nChoose option: ").strip().lower()

        if team_choice == "b":
            break
        elif team_choice == "1":
            # Call the team selection system for these matches
            print("\n=== Update Team Selection ===")

            # Display matches vertically with available players in columns
            for i, match in enumerate(selected_matches, 1):
                date_fmt = match["date"].strftime("%d %b %y")
                header = f"{i}. {date_fmt} VS {match['opponent']}".upper()

                # Get available players for this match - use safe variable names
                local_active_players = [p for p in players if p not in inactive_players]
                local_available_players = [
                    p for p in local_active_players if p not in match["players"]
                ]

                # Split available players into two columns
                half = (len(local_available_players) + 1) // 2
                col1 = local_available_players[:half]
                col2 = local_available_players[half:]

                print(f"\n{header:<30} | Available Players")
                print("-" * 30 + "-|-" + "-" * 40)

                # Show selected players and available players side by side
                max_rows = max(len(match["players"]), len(col1))

                for row in range(max_rows):
                    # Selected player column
                    if row < len(match["players"]):
                        player = match["players"][row]
                        selected_display = f" {row+1}. {player}"
                    else:
                        selected_display = ""

                    # Available players columns
                    avail1 = col1[row] if row < len(col1) else ""
                    avail2 = col2[row] if row < len(col2) else ""

                    print(f"{selected_display:<30} | {avail1:<18} | {avail2}")

                # Show "No players selected" only if no players are selected
                if not match["players"]:
                    print(
                        f"{'No players selected':<30} | {col1[0] if col1 else '':<18} | {col2[0] if col2 else ''}"
                    )

            print(f"\nSelected {len(selected_matches)} match(es) for team updates.")

            # Team management loop
            while True:
                print("\nQuick team management:")
                print("1) Add players to matches")
                print("2) Remove players from matches")
                print("b) Back to team sheets")

                quick_choice = input("\nChoose option: ").strip().lower()

                if quick_choice == "1":
                    team_sheets_add_players(selected_matches)
                elif quick_choice == "2":
                    team_sheets_remove_players(selected_matches)
                elif quick_choice == "b":
                    return
                else:
                    print("Please choose a valid option.")
                    input("Press Enter to continue...")


def team_sheets_add_players(selected_matches):
    """Handle adding players in team sheets context"""
    while True:
        # Find players available for matches using safe variable names
        local_active_players = [p for p in players if p not in inactive_players]
        local_player_availability = []

        for local_player in local_active_players:
            local_available_match_nums = []
            local_availability_display = []

            for local_i, local_match in enumerate(selected_matches, 1):
                if local_player not in local_match["players"]:
                    local_available_match_nums.append(str(local_i))
                    local_opponent = local_match["opponent"].split()[0][:8]
                    local_availability_display.append(local_opponent)
                else:
                    local_availability_display.append("-")

            if local_available_match_nums:
                local_player_availability.append(
                    (
                        local_player,
                        local_availability_display,
                        local_available_match_nums,
                    )
                )

        # Sort players by availability
        local_player_availability.sort(key=lambda x: len(x[2]), reverse=True)

        if not local_player_availability:
            print("\nNo players available for any matches.")
            input("Press Enter to continue...")
            break

        print("\n=== Add Players ===")

        # Create dynamic header
        local_header = f"{'No.':<3} {'Player':<20}"
        local_base_width = 25

        for local_i, local_match in enumerate(selected_matches, 1):
            local_opponent = local_match["opponent"].split()[0][:8]
            local_header += f" {local_opponent:<9}"
            local_base_width += 10

        local_separator = "-" * local_base_width
        print(local_separator)
        print(local_header)
        print(local_separator)

        for local_i, (local_player, local_availability, local_match_nums) in enumerate(
            local_player_availability, 1
        ):
            local_line = f"{local_i:<3} {local_player:<20}"
            for local_avail in local_availability:
                local_display_avail = local_avail if local_avail != "-" else "-"
                if local_display_avail != "-":
                    local_display_avail = local_display_avail[:8]
                local_line += f" {local_display_avail:<9}"
            print(local_line)

        print(local_separator)

        # FIXED: Add menu options display
        print("\nOptions:")
        print("1) Add player(s) to matches")
        print("b) Back to team management")

        # FIXED: Get menu choice first
        local_add_choice = input("\nChoose option: ").strip().lower()

        if local_add_choice == "b":
            break
        elif local_add_choice == "1":
            # Now get player selection
            local_players_input = input(
                f"\nChoose player(s) (e.g. 1 or 1,3,5 or 1-5 or 'all') or 'b' to go back: "
            ).strip()

            if local_players_input.lower() == "b":
                continue  # Go back to menu

            try:
                if local_players_input.lower() == "all":
                    local_player_numbers = list(
                        range(1, len(local_player_availability) + 1)
                    )
                elif "-" in local_players_input and "," not in local_players_input:
                    local_start, local_end = map(int, local_players_input.split("-"))
                    if 1 <= local_start <= local_end <= len(local_player_availability):
                        local_player_numbers = list(range(local_start, local_end + 1))
                    else:
                        print(
                            f"Range must be between 1 and {len(local_player_availability)}"
                        )
                        input("Press Enter to continue...")
                        continue
                else:
                    local_player_numbers = [
                        int(x.strip()) for x in local_players_input.split(",")
                    ]

                if all(
                    1 <= num <= len(local_player_availability)
                    for num in local_player_numbers
                ):
                    local_selected_players_info = [
                        local_player_availability[num - 1]
                        for num in local_player_numbers
                    ]

                    # Show selected players
                    print(f"\n=== Selected Players ===")
                    for local_i, (
                        local_player,
                        local_availability,
                        local_match_nums,
                    ) in enumerate(local_selected_players_info, 1):
                        print(f"{local_i}. {local_player}")

                    # Show matches again for easy reference
                    print(f"\n=== Available Matches ===")
                    for local_i, local_match in enumerate(selected_matches, 1):
                        local_date_fmt = local_match["date"].strftime("%d %b %y")
                        local_team_count = len(local_match["players"])
                        print(
                            f"{local_i}. {local_date_fmt} vs {local_match['opponent']} ({local_team_count} players)"
                        )

                    # Select matches
                    local_matches_input = (
                        input(f"\nAdd to which matches? (e.g. 1 or 1,3,4 or 'all'): ")
                        .strip()
                        .lower()
                    )

                    if local_matches_input == "all":
                        local_target_match_indices = list(range(len(selected_matches)))
                    else:
                        try:
                            local_match_numbers = [
                                int(x.strip()) for x in local_matches_input.split(",")
                            ]
                            if all(
                                1 <= num <= len(selected_matches)
                                for num in local_match_numbers
                            ):
                                local_target_match_indices = [
                                    num - 1 for num in local_match_numbers
                                ]
                            else:
                                print(
                                    f"Please enter numbers between 1 and {len(selected_matches)}"
                                )
                                input("Press Enter to continue...")
                                continue
                        except ValueError:
                            print("Invalid input")
                            input("Press Enter to continue...")
                            continue

                    # Add players
                    local_added_count = 0
                    for (
                        local_player,
                        local_availability,
                        local_available_match_nums,
                    ) in local_selected_players_info:
                        local_available_indices = [
                            int(x) - 1 for x in local_available_match_nums
                        ]

                        for local_match_idx in local_target_match_indices:
                            if local_match_idx in local_available_indices:
                                selected_matches[local_match_idx]["players"].append(
                                    local_player
                                )
                                local_added_count += 1

                    save_data()

                    if local_added_count > 0:
                        print(f"\n✓ Players added successfully!")
                    else:
                        print(
                            f"\nNo players were added (they may already be selected for those matches)"
                        )

                    input("Press Enter to continue...")
                    # FIXED: Continue loop instead of break
                    continue
                else:
                    print(
                        f"Please enter numbers between 1 and {len(local_player_availability)}"
                    )
                    input("Press Enter to continue...")
            except ValueError:
                print("Please enter valid numbers")
                input("Press Enter to continue...")
        else:
            print("Please choose a valid option.")
            input("Press Enter to continue...")


def team_sheets_remove_players(selected_matches):
    """Handle removing players in team sheets context"""
    while True:
        # Find players currently in matches
        local_player_removal_options = []

        for local_player in sorted(players):
            if local_player in inactive_players:
                continue

            local_current_match_nums = []
            local_player_match_display = []

            for local_i, local_match in enumerate(selected_matches, 1):
                if local_player in local_match["players"]:
                    local_current_match_nums.append(str(local_i))
                    local_opponent = local_match["opponent"].split()[0][:8]
                    local_player_match_display.append(local_opponent)
                else:
                    local_player_match_display.append("-")

            if local_current_match_nums:
                local_player_removal_options.append(
                    (local_player, local_player_match_display, local_current_match_nums)
                )

        local_player_removal_options.sort(key=lambda x: len(x[2]), reverse=True)

        if not local_player_removal_options:
            print("\nNo players currently in any matches.")
            input("Press Enter to continue...")
            break

        print("\n=== Remove Players ===")

        # Create dynamic header
        local_header = f"{'No.':<3} {'Player':<20}"
        local_base_width = 25

        for local_i, local_match in enumerate(selected_matches, 1):
            local_opponent = local_match["opponent"].split()[0][:8]
            local_header += f" {local_opponent:<9}"
            local_base_width += 10

        local_separator = "-" * local_base_width
        print(local_separator)
        print(local_header)
        print(local_separator)

        for local_i, (
            local_player,
            local_player_match_display,
            local_match_nums,
        ) in enumerate(local_player_removal_options, 1):
            local_line = f"{local_i:<3} {local_player:<20}"
            for local_match_status in local_player_match_display:
                local_display_status = (
                    local_match_status if local_match_status != "-" else "-"
                )
                if local_display_status != "-":
                    local_display_status = local_display_status[:8]
                local_line += f" {local_display_status:<9}"
            print(local_line)

        print(local_separator)

        # Add menu options display
        print("\nOptions:")
        print("1) Remove player(s) from matches")
        print("b) Back to team management")

        # Get menu choice first
        local_remove_choice = input("\nChoose option: ").strip().lower()

        if local_remove_choice == "b":
            break
        elif local_remove_choice == "1":
            # Now get player selection
            local_players_input = input(
                f"\nChoose player(s) to remove (e.g. 1 or 1,3,5 or 1-5 or 'all') or 'b' to go back: "
            ).strip()

            if local_players_input.lower() == "b":
                continue  # Go back to menu

            try:
                if local_players_input.lower() == "all":
                    local_player_numbers = list(
                        range(1, len(local_player_removal_options) + 1)
                    )
                elif "-" in local_players_input and "," not in local_players_input:
                    local_start, local_end = map(int, local_players_input.split("-"))
                    if (
                        1
                        <= local_start
                        <= local_end
                        <= len(local_player_removal_options)
                    ):
                        local_player_numbers = list(range(local_start, local_end + 1))
                    else:
                        print(
                            f"Range must be between 1 and {len(local_player_removal_options)}"
                        )
                        input("Press Enter to continue...")
                        continue
                else:
                    local_player_numbers = [
                        int(x.strip()) for x in local_players_input.split(",")
                    ]

                if all(
                    1 <= num <= len(local_player_removal_options)
                    for num in local_player_numbers
                ):
                    local_selected_players_info = [
                        local_player_removal_options[num - 1]
                        for num in local_player_numbers
                    ]

                    # Show selected players
                    print(f"\n=== Selected Players to Remove ===")
                    for local_i, (
                        local_player,
                        local_player_match_display,
                        local_current_match_nums,
                    ) in enumerate(local_selected_players_info, 1):
                        print(f"{local_i}. {local_player}")

                    # Show matches again for easy reference
                    print(f"\n=== Available Matches ===")
                    for local_i, local_match in enumerate(selected_matches, 1):
                        local_date_fmt = local_match["date"].strftime("%d %b %y")
                        local_team_count = len(local_match["players"])
                        print(
                            f"{local_i}. {local_date_fmt} vs {local_match['opponent']} ({local_team_count} players)"
                        )

                    # Select matches to remove from
                    local_matches_input = (
                        input(
                            f"\nRemove from which matches? (e.g. 1 or 1,3,4 or 'all'): "
                        )
                        .strip()
                        .lower()
                    )

                    if local_matches_input == "all":
                        local_target_match_indices = list(range(len(selected_matches)))
                    else:
                        try:
                            local_match_numbers = [
                                int(x.strip()) for x in local_matches_input.split(",")
                            ]
                            if all(
                                1 <= num <= len(selected_matches)
                                for num in local_match_numbers
                            ):
                                local_target_match_indices = [
                                    num - 1 for num in local_match_numbers
                                ]
                            else:
                                print(
                                    f"Please enter numbers between 1 and {len(selected_matches)}"
                                )
                                input("Press Enter to continue...")
                                continue
                        except ValueError:
                            print("Invalid input")
                            input("Press Enter to continue...")
                            continue

                    # Remove players
                    local_removed_count = 0
                    for (
                        local_player,
                        local_player_match_display,
                        local_current_match_nums,
                    ) in local_selected_players_info:
                        local_current_indices = [
                            int(x) - 1 for x in local_current_match_nums
                        ]

                        for local_match_idx in local_target_match_indices:
                            if local_match_idx in local_current_indices:
                                if (
                                    local_player
                                    in selected_matches[local_match_idx]["players"]
                                ):
                                    selected_matches[local_match_idx]["players"].remove(
                                        local_player
                                    )
                                    local_removed_count += 1

                    save_data()

                    if local_removed_count > 0:
                        print(f"\n✓ Players removed successfully!")
                    else:
                        print(
                            f"\nNo players were removed (they may not be selected for those matches)"
                        )

                    input("Press Enter to continue...")
                    # Continue loop to refresh available players and show menu again
                    continue
                else:
                    print(
                        f"Please enter numbers between 1 and {len(local_player_removal_options)}"
                    )
                    input("Press Enter to continue...")
            except ValueError:
                print("Please enter valid numbers")
                input("Press Enter to continue...")
        else:
            print("Please choose a valid option.")
            input("Press Enter to continue...")


def team_sheets_add_players(selected_matches):
    """Handle adding players in team sheets context"""
    while True:
        # Find players available for matches using safe variable names
        local_active_players = [p for p in players if p not in inactive_players]
        local_player_availability = []

        for local_player in local_active_players:
            local_available_match_nums = []
            local_availability_display = []

            for local_i, local_match in enumerate(selected_matches, 1):
                if local_player not in local_match["players"]:
                    local_available_match_nums.append(str(local_i))
                    local_opponent = local_match["opponent"].split()[0][:8]
                    local_availability_display.append(local_opponent)
                else:
                    local_availability_display.append("-")

            if local_available_match_nums:
                local_player_availability.append(
                    (
                        local_player,
                        local_availability_display,
                        local_available_match_nums,
                    )
                )

        # Sort players by availability
        local_player_availability.sort(key=lambda x: len(x[2]), reverse=True)

        if not local_player_availability:
            print("\nNo players available for any matches.")
            input("Press Enter to continue...")
            break

        print("\n=== Add Players ===")

        # Create dynamic header
        local_header = f"{'No.':<3} {'Player':<20}"
        local_base_width = 25

        for local_i, local_match in enumerate(selected_matches, 1):
            local_opponent = local_match["opponent"].split()[0][:8]
            local_header += f" {local_opponent:<9}"
            local_base_width += 10

        local_separator = "-" * local_base_width
        print(local_separator)
        print(local_header)
        print(local_separator)

        for local_i, (local_player, local_availability, local_match_nums) in enumerate(
            local_player_availability, 1
        ):
            local_line = f"{local_i:<3} {local_player:<20}"
            for local_avail in local_availability:
                local_display_avail = local_avail if local_avail != "-" else "-"
                if local_display_avail != "-":
                    local_display_avail = local_display_avail[:8]
                local_line += f" {local_display_avail:<9}"
            print(local_line)

        print(local_separator)

        # Select players
        local_players_input = input(
            f"\nChoose player(s) (e.g. 1 or 1,3,5 or 1-5 or 'all') or 'b' to go back: "
        ).strip()

        if local_players_input.lower() == "b":
            break

        try:
            if local_players_input.lower() == "all":
                local_player_numbers = list(
                    range(1, len(local_player_availability) + 1)
                )
            elif "-" in local_players_input and "," not in local_players_input:
                local_start, local_end = map(int, local_players_input.split("-"))
                if 1 <= local_start <= local_end <= len(local_player_availability):
                    local_player_numbers = list(range(local_start, local_end + 1))
                else:
                    print(
                        f"Range must be between 1 and {len(local_player_availability)}"
                    )
                    continue
            else:
                local_player_numbers = [
                    int(x.strip()) for x in local_players_input.split(",")
                ]

            if all(
                1 <= num <= len(local_player_availability)
                for num in local_player_numbers
            ):
                local_selected_players_info = [
                    local_player_availability[num - 1] for num in local_player_numbers
                ]

                # Show selected players
                print(f"\n=== Selected Players ===")
                for local_i, (
                    local_player,
                    local_availability,
                    local_match_nums,
                ) in enumerate(local_selected_players_info, 1):
                    print(f"{local_i}. {local_player}")

                # Show matches again for easy reference
                print(f"\n=== Available Matches ===")
                for local_i, local_match in enumerate(selected_matches, 1):
                    local_date_fmt = local_match["date"].strftime("%d %b %y")
                    local_team_count = len(local_match["players"])
                    print(
                        f"{local_i}. {local_date_fmt} vs {local_match['opponent']} ({local_team_count} players)"
                    )

                # Select matches
                local_matches_input = (
                    input(f"\nAdd to which matches? (e.g. 1 or 1,3,4 or 'all'): ")
                    .strip()
                    .lower()
                )

                if local_matches_input == "all":
                    local_target_match_indices = list(range(len(selected_matches)))
                else:
                    try:
                        local_match_numbers = [
                            int(x.strip()) for x in local_matches_input.split(",")
                        ]
                        if all(
                            1 <= num <= len(selected_matches)
                            for num in local_match_numbers
                        ):
                            local_target_match_indices = [
                                num - 1 for num in local_match_numbers
                            ]
                        else:
                            print(
                                f"Please enter numbers between 1 and {len(selected_matches)}"
                            )
                            continue
                    except ValueError:
                        print("Invalid input")
                        continue

                # Add players
                local_added_count = 0
                for (
                    local_player,
                    local_availability,
                    local_available_match_nums,
                ) in local_selected_players_info:
                    local_available_indices = [
                        int(x) - 1 for x in local_available_match_nums
                    ]

                    for local_match_idx in local_target_match_indices:
                        if local_match_idx in local_available_indices:
                            selected_matches[local_match_idx]["players"].append(
                                local_player
                            )
                            local_added_count += 1

                save_data()

                if local_added_count > 0:
                    print(f"\n✓ Players added successfully!")
                    input("Press Enter to continue...")
                break
            else:
                print(
                    f"Please enter numbers between 1 and {len(local_player_availability)}"
                )
        except ValueError:
            print("Please enter valid numbers")


def team_sheets_remove_players(selected_matches):
    """Handle removing players in team sheets context"""
    while True:
        # Find players currently in matches
        local_player_removal_options = []

        for local_player in sorted(players):
            if local_player in inactive_players:
                continue

            local_current_match_nums = []
            local_player_match_display = []

            for local_i, local_match in enumerate(selected_matches, 1):
                if local_player in local_match["players"]:
                    local_current_match_nums.append(str(local_i))
                    local_opponent = local_match["opponent"].split()[0][:8]
                    local_player_match_display.append(local_opponent)
                else:
                    local_player_match_display.append("-")

            if local_current_match_nums:
                local_player_removal_options.append(
                    (local_player, local_player_match_display, local_current_match_nums)
                )

        local_player_removal_options.sort(key=lambda x: len(x[2]), reverse=True)

        if not local_player_removal_options:
            print("\nNo players currently in any matches.")
            input("Press Enter to continue...")
            break

        print("\n=== Remove Players ===")

        # Create dynamic header
        local_header = f"{'No.':<3} {'Player':<20}"
        local_base_width = 25

        for local_i, local_match in enumerate(selected_matches, 1):
            local_opponent = local_match["opponent"].split()[0][:8]
            local_header += f" {local_opponent:<9}"
            local_base_width += 10

        local_separator = "-" * local_base_width
        print(local_separator)
        print(local_header)
        print(local_separator)

        for local_i, (
            local_player,
            local_player_match_display,
            local_match_nums,
        ) in enumerate(local_player_removal_options, 1):
            local_line = f"{local_i:<3} {local_player:<20}"
            for local_match_status in local_player_match_display:
                local_display_status = (
                    local_match_status if local_match_status != "-" else "-"
                )
                if local_display_status != "-":
                    local_display_status = local_display_status[:8]
                local_line += f" {local_display_status:<9}"
            print(local_line)

        print(local_separator)

        # Select players to remove
        local_players_input = input(
            f"\nChoose player(s) to remove (e.g. 1 or 1,3,5 or 1-5 or 'all') or 'b' to go back: "
        ).strip()

        if local_players_input.lower() == "b":
            break

        try:
            if local_players_input.lower() == "all":
                local_player_numbers = list(
                    range(1, len(local_player_removal_options) + 1)
                )
            elif "-" in local_players_input and "," not in local_players_input:
                local_start, local_end = map(int, local_players_input.split("-"))
                if 1 <= local_start <= local_end <= len(local_player_removal_options):
                    local_player_numbers = list(range(local_start, local_end + 1))
                else:
                    print(
                        f"Range must be between 1 and {len(local_player_removal_options)}"
                    )
                    continue
            else:
                local_player_numbers = [
                    int(x.strip()) for x in local_players_input.split(",")
                ]

            if all(
                1 <= num <= len(local_player_removal_options)
                for num in local_player_numbers
            ):
                local_selected_players_info = [
                    local_player_removal_options[num - 1]
                    for num in local_player_numbers
                ]

                # Show selected players
                print(f"\n=== Selected Players to Remove ===")
                for local_i, (
                    local_player,
                    local_player_match_display,
                    local_current_match_nums,
                ) in enumerate(local_selected_players_info, 1):
                    print(f"{local_i}. {local_player}")

                # Show matches again for easy reference
                print(f"\n=== Available Matches ===")
                for local_i, local_match in enumerate(selected_matches, 1):
                    local_date_fmt = local_match["date"].strftime("%d %b %y")
                    local_team_count = len(local_match["players"])
                    print(
                        f"{local_i}. {local_date_fmt} vs {local_match['opponent']} ({local_team_count} players)"
                    )

                # Select matches to remove from
                local_matches_input = (
                    input(f"\nRemove from which matches? (e.g. 1 or 1,3,4 or 'all'): ")
                    .strip()
                    .lower()
                )

                if local_matches_input == "all":
                    local_target_match_indices = list(range(len(selected_matches)))
                else:
                    try:
                        local_match_numbers = [
                            int(x.strip()) for x in local_matches_input.split(",")
                        ]
                        if all(
                            1 <= num <= len(selected_matches)
                            for num in local_match_numbers
                        ):
                            local_target_match_indices = [
                                num - 1 for num in local_match_numbers
                            ]
                        else:
                            print(
                                f"Please enter numbers between 1 and {len(selected_matches)}"
                            )
                            continue
                    except ValueError:
                        print("Invalid input")
                        continue

                # Remove players
                local_removed_count = 0
                for (
                    local_player,
                    local_player_match_display,
                    local_current_match_nums,
                ) in local_selected_players_info:
                    local_current_indices = [
                        int(x) - 1 for x in local_current_match_nums
                    ]

                    for local_match_idx in local_target_match_indices:
                        if local_match_idx in local_current_indices:
                            if (
                                local_player
                                in selected_matches[local_match_idx]["players"]
                            ):
                                selected_matches[local_match_idx]["players"].remove(
                                    local_player
                                )
                                local_removed_count += 1

                save_data()

                if local_removed_count > 0:
                    print(f"\n✓ Players removed successfully!")
                    input("Press Enter to continue...")
                break
            else:
                print(
                    f"Please enter numbers between 1 and {len(local_player_removal_options)}"
                )
        except ValueError:
            print("Please enter valid numbers")


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
        print("1) Delete club data")
        print("b) Back to main menu")
        print()

        choice = input("Choose option: ").strip().lower()

        if choice == "b":
            break
        elif choice == "1":
            confirm = (
                input(
                    "Are you sure you want to delete all club data? This cannot be undone. (yes/no): "
                )
                .strip()
                .lower()
            )
            if confirm == "yes":
                global club_name, players, matches, inactive_players
                club_name = ""
                players.clear()
                matches.clear()
                inactive_players.clear()
                # Delete the data file if it exists
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                print("All club data has been deleted.")
            else:
                print("Delete cancelled.")
        else:
            print("Please choose a valid option.")


def record_payment():
    """Record match fee payments with streamlined player selection"""
    if not matches or not players:
        print("\nYou need at least one match and one player first.")
        return

    # Find players who owe fees
    players_with_fees = []

    for player in sorted(players):
        if player in inactive_players:
            continue  # Skip inactive players

        # Get all unpaid matches for this player (oldest first)
        unpaid_matches = []
        total_due = 0

        for match in get_matches_sorted():  # Already sorted by date
            if player in match.get("players", []) and player not in match.get(
                "paid", []
            ):
                unpaid_matches.append(match)
                total_due += match["fee"]

        if unpaid_matches:
            players_with_fees.append((player, unpaid_matches, total_due))

    if not players_with_fees:
        print("\nNo players have outstanding fees.")
        input("\nPress Enter to continue...")
        return

    while True:
        print("\n=== Record Fee Payment ===")

        # Show players with outstanding fees
        print("Players with outstanding fees:")
        print("-" * 70)
        print(f"{'No.':<3} {'Player':<20} {'Matches Due':<12} {'Total Due':<12}")
        print("-" * 70)

        for i, (player, unpaid_matches, total_due) in enumerate(players_with_fees, 1):
            matches_count = len(unpaid_matches)
            print(f"{i:<3} {player:<20} {matches_count:<12} £{total_due:.2f}")

        print("-" * 70)
        print(f"Total players with fees due: {len(players_with_fees)}")

        print(f"\nSelect player (1-{len(players_with_fees)}) or 'b' to go back:")

        choice = input("\nChoose player: ").strip().lower()

        if choice == "b":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(players_with_fees):
            # Direct player selection
            selected_player, unpaid_matches, total_due = players_with_fees[
                int(choice) - 1
            ]

            # Show player's outstanding fees breakdown
            print(f"\n=== Fee Details for {selected_player} ===")
            print(f"{'Match':<25} {'Date':<12} {'Fee':<10} {'Status':<10}")
            print("-" * 60)

            for match in unpaid_matches:
                date_fmt = match["date"].strftime("%d %b %y")
                opponent = match["opponent"][:24]  # Truncate if too long
                print(f"{opponent:<25} {date_fmt:<12} £{match['fee']:.2f}    Due")

            print("-" * 60)
            print(f"{'TOTAL DUE':<49} £{total_due:.2f}")

            # Show suggested payment amounts
            print(f"\nValid payment amounts (full matches only):")
            running_total = 0
            for i, match in enumerate(unpaid_matches, 1):
                running_total += match["fee"]
                print(f"  £{running_total:.2f} (pays {i} match{'es' if i > 1 else ''})")

            # Get payment amount
            while True:
                amount_input = input(
                    f"\nEnter payment amount or 'b' to go back: £"
                ).strip()

                if amount_input.lower() == "b":
                    break

                try:
                    payment_amount = float(amount_input)

                    if payment_amount <= 0:
                        print("Payment amount must be greater than £0")
                        continue

                    if payment_amount > total_due:
                        print(
                            f"Payment amount cannot exceed total due of £{total_due:.2f}"
                        )
                        continue

                    # Check if payment covers full matches only
                    full_matches_that_can_be_paid = 0
                    running_total = 0

                    for match in unpaid_matches:
                        if running_total + match["fee"] <= payment_amount:
                            running_total += match["fee"]
                            full_matches_that_can_be_paid += 1
                        else:
                            break

                    if running_total == payment_amount:
                        # Perfect match - can pay exact number of full matches
                        payments_made = []

                        for i in range(full_matches_that_can_be_paid):
                            match = unpaid_matches[i]
                            match["paid"].append(selected_player)
                            payments_made.append((match, match["fee"], "Full"))

                        save_data()

                        print(
                            f"\n✓ Payment of £{payment_amount:.2f} recorded for {selected_player}"
                        )
                        print("\nPayment allocated to:")

                        for match, amount, status in payments_made:
                            date_fmt = match["date"].strftime("%d %b %y")
                            print(
                                f"  • {date_fmt} vs {match['opponent']}: £{amount:.2f} ({status})"
                            )

                        print(
                            f"\nNew outstanding balance: £{total_due - payment_amount:.2f}"
                        )

                        # Update the players_with_fees list
                        updated_unpaid = []
                        updated_total = 0
                        for match in unpaid_matches:
                            if selected_player not in match.get("paid", []):
                                updated_unpaid.append(match)
                                updated_total += match["fee"]

                        if updated_unpaid:
                            # Update the entry
                            for i, (player, _, _) in enumerate(players_with_fees):
                                if player == selected_player:
                                    players_with_fees[i] = (
                                        player,
                                        updated_unpaid,
                                        updated_total,
                                    )
                                    break
                        else:
                            # Remove player from list (all fees paid)
                            players_with_fees = [
                                (p, m, t)
                                for p, m, t in players_with_fees
                                if p != selected_player
                            ]

                        input("\nPress Enter to continue...")
                        break
                    else:
                        # Payment amount doesn't match exact matches
                        if running_total > 0:
                            print(
                                f"\n⚠ Payment of £{payment_amount:.2f} doesn't match full match payments"
                            )
                            print(
                                f"This would pay {full_matches_that_can_be_paid} match(es) (£{running_total:.2f}) with £{payment_amount - running_total:.2f} remaining"
                            )
                            print(
                                "Only full match payments are accepted to avoid partial payment confusion."
                            )
                            print(f"\nValid amounts for {selected_player}:")

                            temp_total = 0
                            for i, match in enumerate(unpaid_matches, 1):
                                temp_total += match["fee"]
                                print(
                                    f"  £{temp_total:.2f} (pays {i} match{'es' if i > 1 else ''})"
                                )

                            continue
                        else:
                            print(
                                f"\n⚠ Payment amount £{payment_amount:.2f} is less than the oldest match fee of £{unpaid_matches[0]['fee']:.2f}"
                            )
                            print("Please pay at least one full match fee.")
                            continue

                except ValueError:
                    print("Please enter a valid amount (numbers only, no £ symbol)")

        else:
            print(
                f"Please enter a number between 1 and {len(players_with_fees)} or 'b'"
            )
            input("Press Enter to continue...")


def view_fee_balances():
    """Show fee balance options"""
    while True:
        print("\n=== Match Fee Reports ===")
        print("1) Player fee balances")
        print("2) Match financial report")
        print("b) Back to main menu")
        print()

        choice = input("Choose option: ").strip().lower()

        if choice == "b":
            break
        elif choice == "1":
            # Show player fee balances
            if not players:
                print("\nNo players registered yet.")
                input("\nPress Enter to continue...")
                continue

            print("\n=== Player Fee Balances ===")

            # Calculate balances for all players
            player_balances = []
            total_outstanding = 0

            for player in sorted(players):
                total_owed = 0
                total_paid = 0

                for match in matches:
                    if player in match.get("players", []):
                        total_owed += match["fee"]
                        if player in match.get("paid", []):
                            total_paid += match["fee"]

                balance_due = total_owed - total_paid
                total_outstanding += balance_due

                # Only include players who owe money
                if balance_due > 0:
                    player_balances.append((player, balance_due))

            if not player_balances:
                print("\nNo outstanding fees - all players are up to date!")
                input("\nPress Enter to continue...")
                continue

            # Display in two columns
            total_players = len(player_balances)
            half = (total_players + 1) // 2

            print("-" * 70)
            left_header = f"{'Player':<20} {'Due':<8}"
            right_header = f"{'Player':<20} {'Due':<8}"
            print(f"{left_header}  {right_header}")
            print("-" * 70)

            for i in range(half):
                # Left column
                left_player, left_amount = player_balances[i]
                left_player_display = left_player[:19]  # Truncate if too long
                left_line = f"{left_player_display:<20} £{left_amount:.2f}  "

                # Right column (if exists)
                right_idx = i + half
                if right_idx < total_players:
                    right_player, right_amount = player_balances[right_idx]
                    right_player_display = right_player[:19]
                    right_line = f"{right_player_display:<20} £{right_amount:.2f}"
                    print(f"{left_line} {right_line}")
                else:
                    print(left_line)

            print("-" * 70)
            print(f"TOTAL OUTSTANDING: £{total_outstanding:.2f}")
            print(f"Players with fees due: {len(player_balances)}")

            input("\nPress Enter to continue...")

        elif choice == "2":
            # Match financial report
            if not matches:
                print("\nNo matches recorded yet.")
                input("\nPress Enter to continue...")
                continue

            # Filter selection
            while True:
                print("\n=== Match Financial Report ===")
                print("Show matches:")
                print("1) Recent + upcoming (last 2 weeks + next 2 weeks)")
                print("2) Last month's matches")
                print("3) Next month's matches")
                print("4) All matches")
                print("b) Back to fee reports menu")
                print()

                filter_choice = input("Choose filter: ").strip().lower()
                if filter_choice == "b":
                    break
                if filter_choice not in ["1", "2", "3", "4"]:
                    print("Please enter 1, 2, 3, 4, or b")
                    continue

                filter_choice = int(filter_choice)

                # Filter matches
                from datetime import timedelta

                today = datetime.now().date()

                if filter_choice == 1:
                    start_date = today - timedelta(days=14)
                    end_date = today + timedelta(days=14)
                    filtered_matches = [
                        m
                        for m in get_matches_sorted()
                        if start_date <= m["date"] <= end_date
                    ]
                elif filter_choice == 2:
                    start_date = today - timedelta(days=30)
                    end_date = today
                    filtered_matches = [
                        m
                        for m in get_matches_sorted()
                        if start_date <= m["date"] <= end_date
                    ]
                elif filter_choice == 3:
                    start_date = today
                    end_date = today + timedelta(days=30)
                    filtered_matches = [
                        m
                        for m in get_matches_sorted()
                        if start_date <= m["date"] <= end_date
                    ]
                elif filter_choice == 4:
                    filtered_matches = get_matches_sorted()

                if not filtered_matches:
                    print(
                        "\nNo matches found for the selected period. Try a different filter."
                    )
                    continue

                # Show matches for selection
                print("\n=== Select Matches for Financial Report ===")
                print(
                    f"{'No.':<4} {'Date':<10} {'Opponent':<25} {'Players':<8} {'Fee':<8}"
                )
                print("-" * 60)

                for i, match in enumerate(filtered_matches, 1):
                    date_fmt = match["date"].strftime("%d %b %y")
                    player_count = len(match["players"]) if match["players"] else 0
                    player_display = str(player_count) if player_count > 0 else "-"
                    fee_fmt = f"£{match['fee']:.2f}"

                    print(
                        f"{i:<4} {date_fmt:<10} {match['opponent']:<25} {player_display:<8} {fee_fmt:<8}"
                    )

                print("A maximum of 6 matches can be selected for financial reports")

                # Match selection with enhanced options
                while True:
                    choice_input = input(
                        "\nChoose match number(s) (e.g. 1 or 1,3,5 or 1-6 or 'all') or 'b' to go back (max 6 matches): "
                    ).strip()

                    if choice_input.lower() == "b":
                        break

                    if not choice_input:
                        continue

                    try:
                        if choice_input.lower() == "all":
                            # Select all filtered matches (up to 6)
                            match_numbers = list(
                                range(1, min(len(filtered_matches) + 1, 7))
                            )
                        elif "-" in choice_input and "," not in choice_input:
                            # Handle range (e.g., 1-6)
                            start, end = map(int, choice_input.split("-"))
                            if 1 <= start <= end <= len(filtered_matches):
                                match_numbers = list(range(start, min(end + 1, 7)))
                            else:
                                print(
                                    f"Range must be between 1 and {len(filtered_matches)}"
                                )
                                continue
                        else:
                            # Handle individual numbers or comma-separated
                            match_numbers = [
                                int(x.strip()) for x in choice_input.split(",")
                            ]

                        # Validate all numbers are in range and limit to 6 matches
                        if len(match_numbers) > 6:
                            print(
                                "Maximum 6 matches can be selected at once for financial reports"
                            )
                            continue

                        valid_numbers = all(
                            1 <= num <= len(filtered_matches) for num in match_numbers
                        )

                        if valid_numbers and match_numbers:
                            selected_matches = [
                                filtered_matches[num - 1] for num in match_numbers
                            ]

                            # Generate financial report with compact formatting
                            print("\n=== Match Financial Report ===")
                            print(
                                f"{'Date':<10} {'Opponent':<20} {'Players':<7} {'Total':<8} {'Paid':<8} {'Due':<8}"
                            )
                            print("-" * 65)

                            grand_total_fees = 0
                            grand_total_paid = 0
                            grand_total_due = 0

                            for match in selected_matches:
                                date_fmt = match["date"].strftime("%d %b %y")
                                player_count = len(match["players"])

                                if player_count == 0:
                                    total_fees = 0
                                    total_paid = 0
                                    due = 0
                                    fees_display = "-"
                                    paid_display = "-"
                                    due_display = "-"
                                else:
                                    total_fees = player_count * match["fee"]
                                    paid_count = len(match.get("paid", []))
                                    total_paid = paid_count * match["fee"]
                                    due = total_fees - total_paid

                                    fees_display = f"£{total_fees:.0f}"
                                    paid_display = (
                                        f"£{total_paid:.0f}" if total_paid > 0 else "-"
                                    )
                                    due_display = f"£{due:.0f}" if due > 0 else "-"

                                    grand_total_fees += total_fees
                                    grand_total_paid += total_paid
                                    grand_total_due += due

                                player_display = (
                                    str(player_count) if player_count > 0 else "-"
                                )
                                opponent_short = match["opponent"][
                                    :19
                                ]  # Truncate long names

                                print(
                                    f"{date_fmt:<10} {opponent_short:<20} {player_display:<7} {fees_display:<8} {paid_display:<8} {due_display:<8}"
                                )

                            print("-" * 65)

                            # Summary totals
                            if grand_total_fees > 0:
                                print(
                                    f"{'TOTALS':<37} £{grand_total_fees:.0f}     £{grand_total_paid:.0f}     £{grand_total_due:.0f}"
                                )
                                print(
                                    f"\nSummary for {len(selected_matches)} match(es):"
                                )
                                print(
                                    f"• Total fees generated: £{grand_total_fees:.0f}"
                                )
                                print(f"• Amount collected: £{grand_total_paid:.0f}")
                                print(f"• Still due: £{grand_total_due:.0f}")

                                if grand_total_fees > 0:
                                    collection_rate = (
                                        grand_total_paid / grand_total_fees
                                    ) * 100
                                    print(f"• Collection rate: {collection_rate:.1f}%")
                            else:
                                print(
                                    "No fees generated - no teams selected for these matches"
                                )

                            input("\nPress Enter to continue...")
                            break
                        else:
                            print(
                                f"Please enter numbers between 1 and {len(filtered_matches)}, separated by commas"
                            )
                    except ValueError:
                        print(
                            "Please enter valid numbers separated by commas (e.g. 1,3,5 or 1-6 or 'all') or 'b' to go back"
                        )

                break  # Exit filter loop
        else:
            print("Please choose a valid option.")


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
        choice = input(
            "\nEnter player number to make inactive (or Enter to finish): "
        ).strip()
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
        left_line = f"{left_no:<3} {left_player:<20} {'INAC':<6}"

        # Right column (if exists)
        right_idx = i + half
        if right_idx < total:
            right_no = right_idx + 1
            right_player = inactive_players[right_idx][:20]
            right_line = f"{right_no:<3} {right_player:<20} {'INAC':<6}"
            print(f"{left_line}  {right_line}")
        else:
            print(left_line)

    print("-" * 64)

    made_active_count = 0

    while inactive_players:
        choice = input(
            "\nEnter player number to make active (or Enter to finish): "
        ).strip()
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
            match["players"] = [
                new_name if p == old_name else p for p in match["players"]
            ]
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
                left_status = (
                    "INAC" if sorted_players[i] in inactive_players else "Actv"
                )
                left_line = f"{left_no:<3} {left_player:<20} {left_status:<6}"

                # Right column (if exists)
                right_idx = i + half
                if right_idx < total:
                    right_no = right_idx + 1
                    right_player = sorted_players[right_idx][
                        :20
                    ]  # Truncate if too long
                    right_status = (
                        "INAC"
                        if sorted_players[right_idx] in inactive_players
                        else "Actv"
                    )
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

        choice = input("Choose option: ").strip().lower()

        if choice == "b":
            break
        elif choice == "1":
            add_player()
        elif choice == "2":
            edit_player_name()
        elif choice == "3":
            mark_attendance()
        elif choice == "4":
            make_player_inactive()
        elif choice == "5":
            make_player_active()
        else:
            print("Please choose a valid option.")


def match_fees_menu():
    """Handle match fee operations"""
    while True:
        print("\n=== Match Fees ===")
        print("1) Check match teams")
        print("2) Fees due per match")
        print("3) Record fee payment")
        print("4) Player fee balances")
        print("b) Back to main menu")
        print()

        choice = input("Choose option: ").strip().lower()

        if choice == "b":
            break
        elif choice == "1":
            show_team_sheets()  # Shows team composition for matches
        elif choice == "2":
            # Fees due per match
            if not matches:
                print("\nNo matches recorded yet.")
                input("\nPress Enter to continue...")
                continue

            # Get matches sorted by date
            sorted_matches = get_matches_sorted()

            # Filter options
            while True:
                print("\n=== Fees Due Per Match ===")
                print("Show matches:")
                print("1) Upcoming matches only")
                print("2) Recent + upcoming (last 2 weeks + next 2 weeks)")
                print("3) All matches with outstanding fees")
                print("4) All matches")
                print("b) Back to match fees menu")
                print()

                filter_choice = input("Choose filter: ").strip().lower()
                if filter_choice == "b":
                    break
                if filter_choice not in ["1", "2", "3", "4"]:
                    print("Please enter 1, 2, 3, 4, or b")
                    continue

                # Apply filters
                from datetime import timedelta

                today = datetime.now().date()

                if filter_choice == "1":
                    filtered_matches = [m for m in sorted_matches if m["date"] >= today]
                elif filter_choice == "2":
                    start_date = today - timedelta(days=14)
                    end_date = today + timedelta(days=14)
                    filtered_matches = [
                        m for m in sorted_matches if start_date <= m["date"] <= end_date
                    ]
                elif filter_choice == "3":
                    # Only matches with outstanding fees
                    filtered_matches = []
                    for match in sorted_matches:
                        if match["players"]:
                            paid_count = len(match.get("paid", []))
                            total_players = len(match["players"])
                            if paid_count < total_players:
                                filtered_matches.append(match)
                else:  # choice == '4'
                    filtered_matches = sorted_matches

                if not filtered_matches:
                    print("\nNo matches found for the selected criteria.")
                    input("\nPress Enter to continue...")
                    continue

                # Display fees due per match in two columns (team sheets style)
                print(f"\n=== Fees Due Per Match ({len(filtered_matches)} matches) ===")
                print()

                total_outstanding = 0
                matches_with_fees_due = 0

                # Process matches in pairs for two-column display
                for i in range(0, len(filtered_matches), 2):
                    # Left column match
                    left_match = filtered_matches[i]
                    left_date = left_match["date"].strftime("%d %b %y").upper()
                    left_num = i + 1
                    left_header = (
                        f"{left_num}. {left_date} VS {left_match['opponent'].upper()}"
                    )

                    # Right column match (if exists)
                    right_match = (
                        filtered_matches[i + 1]
                        if i + 1 < len(filtered_matches)
                        else None
                    )
                    if right_match:
                        right_date = right_match["date"].strftime("%d %b %y").upper()
                        right_num = i + 2
                        right_header = f"{right_num}. {right_date} VS {right_match['opponent'].upper()}"

                    # Calculate fees for left match
                    if not left_match["players"]:
                        left_unpaid = []
                        left_fees_due = 0
                    else:
                        left_paid_players = set(left_match.get("paid", []))
                        left_unpaid = [
                            p
                            for p in left_match["players"]
                            if p not in left_paid_players
                        ]
                        left_fees_due = len(left_unpaid) * left_match["fee"]
                        total_outstanding += left_fees_due
                        if left_fees_due > 0:
                            matches_with_fees_due += 1

                    # Calculate fees for right match
                    if right_match:
                        if not right_match["players"]:
                            right_unpaid = []
                            right_fees_due = 0
                        else:
                            right_paid_players = set(right_match.get("paid", []))
                            right_unpaid = [
                                p
                                for p in right_match["players"]
                                if p not in right_paid_players
                            ]
                            right_fees_due = len(right_unpaid) * right_match["fee"]
                            total_outstanding += right_fees_due
                            if right_fees_due > 0:
                                matches_with_fees_due += 1

                    # Display headers
                    if right_match:
                        print(f"{left_header:<40} | {right_header}")
                        print("-" * 40 + " " + "-" * 40)
                    else:
                        print(left_header)
                        print("-" * 40)

                    # Display players who owe fees side by side
                    max_unpaid = max(
                        len(left_unpaid), len(right_unpaid) if right_match else 0
                    )

                    for j in range(max_unpaid):
                        if j < len(left_unpaid):
                            left_player = f"  {j+1:2}. {left_unpaid[j]:<20} £{left_match['fee']:.2f}"
                        else:
                            left_player = ""

                        if right_match and j < len(right_unpaid):
                            right_player = f"  {j+1:2}. {right_unpaid[j]:<20} £{right_match['fee']:.2f}"
                        else:
                            right_player = ""

                        if right_match:
                            print(f"{left_player:<35} | {right_player}")
                        else:
                            print(left_player)

                    # Show "All fees paid" if team selected but no fees due
                    if left_match["players"] and not left_unpaid:
                        left_status = "  ✓ All fees paid"
                    else:
                        left_status = ""

                    if right_match and right_match["players"] and not right_unpaid:
                        right_status = "  ✓ All fees paid"
                    else:
                        right_status = ""

                    if left_status or right_status:
                        if right_match:
                            print(f"{left_status:<35} | {right_status}")
                        else:
                            print(left_status)

                    print()  # Space between match pairs

                # Summary
                print("-" * 40)
                print(f"SUMMARY:")
                print(f"• Total outstanding fees: £{total_outstanding:.2f}")
                print(f"• Matches with fees due: {matches_with_fees_due}")
                print(
                    f"• Matches fully paid: {len(filtered_matches) - matches_with_fees_due}"
                )

                # Add menu options
                print(f"\nOptions:")
                print(f"1) Record fee payment")
                print(f"2) Player fee balances")
                print(f"b) Back to main menu")

                option_choice = input("\nChoose option: ").strip().lower()

                if option_choice == "1":
                    record_payment()
                elif option_choice == "2":
                    # Jump to player fee balances (option 4 from main menu)
                    break  # This will exit the filter loop and go to option 4 handling
                elif option_choice == "b":
                    return  # Go back to main menu
                else:
                    input("\nPress Enter to continue...")
                break
        elif choice == "3":
            record_payment()
        elif choice == "4":
            # Go directly to player fee balances with payment option
            if not players:
                print("\nNo players registered yet.")
                input("\nPress Enter to continue...")
                continue

            while True:
                print("\n=== Player Fee Balances ===")

                # Calculate balances for all players
                player_balances = []
                total_outstanding = 0

                for player in sorted(players):
                    total_owed = 0
                    total_paid = 0

                    for match in matches:
                        if player in match.get("players", []):
                            total_owed += match["fee"]
                            if player in match.get("paid", []):
                                total_paid += match["fee"]

                    balance_due = total_owed - total_paid
                    total_outstanding += balance_due

                    # Only include players who owe money
                    if balance_due > 0:
                        player_balances.append((player, balance_due))

                if not player_balances:
                    print("\nNo outstanding fees - all players are up to date!")
                    input("\nPress Enter to continue...")
                    break

                # Display in two columns
                total_players = len(player_balances)
                half = (total_players + 1) // 2

                print("-" * 70)
                left_header = f"{'Player':<20} {'Due':<8}"
                right_header = f"{'Player':<20} {'Due':<8}"
                print(f"{left_header}  {right_header}")
                print("-" * 70)

                for i in range(half):
                    # Left column
                    left_player, left_amount = player_balances[i]
                    left_player_display = left_player[:19]  # Truncate if too long
                    left_line = f"{left_player_display:<20} £{left_amount:.2f}  "

                    # Right column (if exists)
                    right_idx = i + half
                    if right_idx < total_players:
                        right_player, right_amount = player_balances[right_idx]
                        right_player_display = right_player[:19]
                        right_line = f"{right_player_display:<20} £{right_amount:.2f}"
                        print(f"{left_line} {right_line}")
                    else:
                        print(left_line)

                print("-" * 70)
                print(f"TOTAL OUTSTANDING: £{total_outstanding:.2f}")
                print(f"Players with fees due: {len(player_balances)}")

                # Add payment option
                print("\nOptions:")
                print("1) Record payment for player")
                print("b) Back to match fees menu")

                balance_choice = input("\nChoose option: ").strip().lower()

                if balance_choice == "b":
                    break
                elif balance_choice == "1":
                    record_payment()
                    # After payment, refresh the display to show updated balances
                    continue
                else:
                    print("Please choose a valid option.")
                    input("Press Enter to continue...")
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
