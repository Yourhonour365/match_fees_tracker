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
git clone <repository-url>
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