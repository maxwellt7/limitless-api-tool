# Limitless to Notion Daily Sync

This tool automatically syncs your Limitless conversations to a Notion database every day at 4:00 AM EST.

## Features

- Fetches all Limitless conversations from the previous day
- Formats them for Notion with proper timestamps
- Creates a new page in your Notion database for each conversation
- Runs automatically at 4:00 AM EST daily

## Setup

### Prerequisites

- Python 3.7+
- A Limitless API key
- A Notion API key
- A Notion database set up with the appropriate properties

### Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   cd python
   pip install -r requirements.txt
   ```
3. Copy the env.example file to .env:
   ```bash
   cp env.example .env
   ```
4. Edit the .env file with your API keys and database ID

### Notion Database Setup

Your Notion database should have the following properties:
- Name (title): Title of the conversation
- Content (rich text): The markdown content of the conversation
- Start Time (date): When the conversation started
- End Time (date): When the conversation ended
- Source (select): Set to "Limitless"

## Usage

### Manual Run

To run the sync manually:

```bash
python daily_notion_sync.py
```

### Automated Schedule

To start the scheduler that runs daily at 4:00 AM EST:

```bash
python scheduler.py
```

The scheduler will run continuously. To keep it running in the background, you can use tools like `nohup` on Linux/Mac or run it as a service.

#### Example for Linux/Mac:

```bash
nohup python scheduler.py > notion_sync.log 2>&1 &
```

#### Setting up as a Service

For production use, consider setting up the script as a proper service using systemd (Linux) or launchd (macOS).

## Troubleshooting

- Check the logs for errors
- Verify that your API keys are correct
- Ensure your Notion database has the correct properties
- Make sure your computer is on at 4:00 AM EST for the scheduled job to run

## License

This tool is released under the same license as the limitless-api-examples repository. 