# Match Fees Tracker

A Python tool to help amateur sports clubs easily collect and manage match fees. Collecting fees after a game is often an admin headache — some players have already left, some head to the pub, and others go straight home to their families. Match Fees Tracker makes it simple to track payments without the chaos.

## Features

- **Simple fee tracking**: Keep track of who played and who has paid for each match
- **Terminal-based interface**: Easy to use command-line tool for quick fee management
- **Match data persistence**: Store match information and payment status
- **Player management**: Track regular players and their payment history

## Roadmap

### Phase 1: Core Python Logic ✅

- 🗸 Basic match and player data structures
- 🗸 Terminal-based fee tracking
- 🗸 Data persistence (JSON/CSV export)
- 🗸 Payment reporting and summaries

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

## Installation

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd match_fees_tracker

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Heroku Deployment

This application is configured for deployment on Heroku for a Code Institute Python project.

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

**Required Heroku files:**
- `requirements.txt` - Python dependencies
- `Procfile` - Tells Heroku how to run the app
- `runtime.txt` - Specifies Python version (optional)

## Usage

### Local Usage
```bash
python main.py
```

### Deployed Version
Visit your Heroku app URL to use the web interface (coming in Phase 2).

## Match Data Structure

Each match is stored as a Python dictionary to keep all details about a match in one place:

```python
match = {
    "id": "unique_match_id",
    "opponent": "ewhurst",
    "date": "2025-09-25",  # ISO format for better sorting
    "venue": "home",       # "home" or "away"
    "fee": 5.0,
    "players": [],         # list of player names/IDs playing in the match
    "paid": [],           # list of player names/IDs who have paid match fees
    "created_at": "2025-09-11T10:30:00",
    "notes": ""           # optional notes about the match
}
```

## Player Data Structure

```python
player = {
    "id": "unique_player_id",
    "name": "John Smith",
    "email": "john@example.com",  # for payment links and reminders
    "phone": "+44123456789",      # optional
    "matches_played": 0,
    "total_fees_owed": 0.0,
    "total_fees_paid": 0.0,
    "payment_history": []         # list of payment records
}
```

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
- **Claude AI** (Anthropic) - Code guidance and project structure
- **ChatGPT** (OpenAI) - Programming assistance
- **Python for Dummies** - Learning resource
- **Python Crash Course** - Educational reference
- **Code Institute** - Learning framework and project requirements

---

*Built with ❤️ for grassroots sports communities*