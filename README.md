# Match Fees Tracker

A Python tool to help amateur sports clubs easily collect and manage match fees. Collecting fees after a game is often an admin headache — some players have already left, some head to the pub, and others go straight home to their families. Match Fees Tracker makes it simple to track payments without the chaos.

## Features

### Player Management
- **Add new players** with validation and duplicate detection
- **Edit player names** with automatic updates across all records
- **Manage active/inactive status** to handle temporary unavailability
- **Two-column display** with status indicators for easy viewing

### Fixture Management
- **Create, edit, and delete** match fixtures
- **Date validation** with flexible input formats (DD/MM/YY or DD/MM/YYYY)
- **Fee tracking** per match with customisable amounts
- **Duplicate detection** and warnings for scheduling conflicts

### Team Selection
- **Multi-match team selection** (up to 4 matches simultaneously)
- **Player availability tracking** across multiple fixtures
- **Bulk operations** with range support (e.g., 1-5, all, 1,3,5)
- **Visual team composition** display with available players

### Financial Management
- **Match fee tracking** and payment recording
- **Player fee balance** reports with outstanding amounts
- **Financial reports** with customisable date filtering
- **Payment validation** (full matches only to avoid confusion)
- **Collection rate** statistics and summaries

### Reporting
- **Player lists** with comprehensive status information
- **Team sheets** in organised two-column format
- **Fixture lists** with multiple filtering options
- **Financial summaries** showing outstanding fees and collection rates

## Installation

### Requirements
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Local Development
```bash
# Clone the repository
git clone https://github.com/Yourhonour365/match_fees_tracker.git
cd match_fees_tracker

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Run the application
python run.py
```

### Heroku Deployment
This application is deployed and running live on Heroku:

**Live Application:** [https://match-fees-tracker-2d395a16f578.herokuapp.com/](https://match-fees-tracker-2d395a16f578.herokuapp.com/)

To deploy your own version:

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Deploy to Heroku
git push heroku main

# View your deployed app
heroku open
```

## Usage

### First Time Setup
1. Run `python run.py` or visit the live Heroku URL
2. The application loads with "Demo Rugby Club" and sample data
3. To set up your own club:
   - Select **m) Club management** from main menu
   - Choose **1) Delete club data**
   - Type `yes` to confirm deletion
   - Enter your club name when prompted
   - Add your own players and fixtures

### Main Menu Navigation
```
MANAGE:
1) Players              3) Fixtures
2) Team selection       4) Match fees

REPORTS:
5) Player list          7) Fixture list
6) Team sheets          8) Match fee balances

m) Club management      e) Exit
```

### Player Management
- **Add players**: Enter names one at a time with automatic formatting
- **Edit names**: Update player names with system-wide updates
- **Status management**: Mark players as active/inactive
- **Smart formatting**: Handles club acronyms (RFC, FC, CC) correctly

### Team Selection Workflow
1. **Select matches** (up to 4 for efficient management)
2. **View availability** in dynamic tables showing player/match combinations
3. **Bulk operations** using flexible input:
   - Single: `1`
   - Multiple: `1,3,5`
   - Range: `1-5`
   - All: `all`

### Fee Management
- **Payment recording** with validation for full matches only
- **Outstanding balances** displayed in organised tables
- **Financial reports** with date filtering options
- **Collection tracking** with percentage rates

## Data Structure

### Match Object
```python
{
    "opponent": "Dublin RFC",
    "date": date(2025, 9, 15),
    "fee": 10.0,
    "players": ["Player 1", "Player 2"],
    "paid": ["Player 1"]
}
```

### Application State
- **Players**: List of all registered players
- **Inactive Players**: Separate tracking for unavailable players
- **Matches**: Complete match records with teams and payments
- **Data Persistence**: JSON file storage with automatic backup

Testing
Manual Testing Procedures
The application has been thoroughly tested using manual testing procedures to ensure all functionality works as intended.
Test Environment

Local Environment: Python 3.8+ on Ubuntu/Windows
Deployment Environment: Heroku cloud platform
Data Storage: JSON file persistence

Core Functionality Tests
Test CaseDescriptionExpected ResultActual ResultStatusPlayer ManagementTC01Add new player with valid namePlayer added to roster, confirmation shownPlayer added successfully✅ PassTC02Add player with duplicate nameError message with suggestions for differentiationError displayed with helpful suggestions✅ PassTC03Add player with numbers in nameValidation error, name rejectedError: "Player name cannot contain numbers"✅ PassTC04Edit existing player nameName updated across all matches and recordsAll records updated correctly✅ PassTC05Make player inactive/activeStatus updated, affects team selection availabilityStatus changed, excluded from team selection✅ PassFixture ManagementTC06Add fixture with valid date (DD/MM/YY)Fixture created with correct date parsingDate parsed correctly, fixture saved✅ PassTC07Add fixture with invalid date formatValidation error with format guidanceError with clear format instructions✅ PassTC08Add duplicate fixtureWarning shown, option to proceedWarning displayed, user choice respected✅ PassTC09Edit fixture detailsSelected fixture updated correctlyAll changes saved and displayed✅ PassTC10Delete fixture with playersWarning about selected players shownWarning displayed, confirmation required✅ PassTeam SelectionTC11Select single player for matchPlayer added to match rosterPlayer appears in team list✅ PassTC12Bulk select players (1,3,5)Multiple players added efficientlyAll specified players added✅ PassTC13Select player range (1-5)Range of players added to matchesCorrect range processed and added✅ PassTC14Select "all" available playersAll eligible players added to matchesAll available players selected✅ PassTC15Remove players from matchesPlayers removed from team rosterPlayers successfully removed✅ PassFinancial ManagementTC16Record valid payment amountPayment recorded for correct number of matchesPayment allocated to oldest matches first✅ PassTC17Attempt partial paymentValidation error, full matches onlyError: "Only full match payments accepted"✅ PassTC18Payment exceeding amount dueValidation error preventing overpaymentError: "Cannot exceed total due"✅ PassTC19Generate financial reportAccurate calculations and displayTotals, percentages calculated correctly✅ PassTC20View player balancesOutstanding amounts displayed correctlyAll balances accurate and up-to-date✅ Pass
Data Validation Tests
Input TypeInvalid InputExpected BehaviorResultPlayer Name"John123"Reject with error message✅ Error displayedPlayer Name"" (empty)Require non-empty name✅ Validation enforcedDate"32/13/25"Invalid date error✅ Error with format helpDate"abc"Format validation error✅ Clear error messageFee Amount"abc"Numeric validation error✅ "Please enter a number"Fee Amount"-5"Positive number required✅ Validation enforcedMatch Selection"99"Range validation✅ "Please enter 1-X"Payment Amount"0"Positive amount required✅ "Amount must be > £0"
User Interface Tests
FeatureTestExpected ResultStatusMenu NavigationPress 'b' from any submenuReturn to previous menu✅ PassMenu NavigationEnter invalid menu optionClear error message✅ PassTable DisplayView player listTwo-column format, status indicators✅ PassTable DisplayView team sheetsSide-by-side match comparison✅ PassInput HandlingEnter empty input where requiredAppropriate validation message✅ PassInput HandlingUse 'all' keywordProcess all available items✅ Pass
Edge Cases and Error Handling
ScenarioExpected BehaviorResultEmpty player rosterGraceful handling with helpful message✅ "No players registered yet"No matches scheduledClear messaging and guidance✅ "No matches scheduled yet"All players inactiveTeam selection shows no available players✅ Handled correctlyLarge player namesText truncation in tables✅ Names truncated to fit displayFuture/past date filteringCorrect date range calculations✅ Filters work accurately
Code Quality Testing
PEP8 Compliance

Tool Used: flake8 and black formatter
Status: Code formatted to PEP8 standards
Remaining Issues: None significant
Line Length: Maintained under 88 characters (black default)

Performance Testing

Large Dataset: Tested with 50+ players, 20+ matches
Response Time: All operations complete within acceptable time
Memory Usage: Efficient data structures, no memory leaks observed

Known Issues
IssueSeverityStatusWorkaroundVery long opponent namesMinorOpenNames truncated in displaysTimezone handlingLowDocumentedUses local system time
Testing Conclusion
All critical functionality has been tested and verified to work correctly. The application handles user input validation effectively, provides clear error messages, and maintains data integrity throughout all operations. Edge cases are handled gracefully with appropriate user feedback.
The testing process revealed no critical bugs, and all identified minor issues have been documented with appropriate workarounds where necessary.

## Roadmap

### Phase 1: Core Python Logic ✅
- ✓ Basic match and player data structures
- ✓ Terminal-based fee tracking
- ✓ Data persistence (JSON storage)
- ✓ Payment reporting and summaries
- ✓ Team selection and management

### Phase 2: Payment Integration
- [ ] Generate secure payment links for easy sharing
- [ ] WhatsApp-friendly link format for team groups
- [ ] Real-time payment status tracking
- [ ] Outstanding payment highlighting

### Phase 3: Automation
- [ ] Automatic payment reminders
- [ ] Email/SMS integration
- [ ] Team admin dashboard
- [ ] Payment history and analytics

## Target Sports

This tool is especially relevant for grassroots sports where players typically pay small match fees per game:

- **Cricket**: Teas, match balls, ground fees
- **Hockey**: Astroturf costs, lighting, equipment
- **Football**: Referee fees, pitch hire, equipment
- **Rugby**: Ground maintenance, match officials, kit

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have suggestions for improvements, please open an issue on GitHub or contact the development team.

## Acknowledgments

This project was developed with assistance from:
- **Claude AI** (Anthropic) - Code refactoring, structure guidance, and problem-solving assistance
- **ChatGPT** (OpenAI) - Programming support and debugging help
- **Python for Dummies** by Stef Maruch and Aahz Maruch - Learning resource for Python fundamentals
- **Python Crash Course** by Eric Matthes - Educational reference for Python programming concepts
- **Code Institute** - Learning framework and project requirements

---

*Built with ❤️ for grassroots sports communities*