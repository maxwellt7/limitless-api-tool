# Limitless to Mem.ai Integration

This tool automatically syncs your Limitless conversations to your Mem.ai knowledge base, providing two different integration approaches:

## Integration Options

### 1. Standard Integration (Create Note API)

The standard integration creates well-formatted notes in Mem.ai containing your Limitless conversations, with each hour's conversations grouped together.

- Uses the Mem.ai Create Note API
- Preserves the original conversation format
- Groups conversations by hour
- Runs every hour automatically

### 2. Smart Integration (Mem It API)

The smart integration uses Mem.ai's intelligent processing to extract key information, action items, and important points from each conversation individually.

- Uses the Mem.ai Mem It API
- AI-powered processing extracts key information
- Each conversation is processed separately
- Automatically organizes content in Mem.ai
- Runs every hour automatically

## Setup

### Prerequisites

- Python 3.7+
- A Limitless API key
- A Mem.ai API key

### Installation

1. Make sure you have the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your `.env` file with your API keys:
   ```
   LIMITLESS_API_KEY=your_limitless_api_key
   MEM_API_KEY=your_mem_api_key
   ```

## Usage

### Standard Integration

To run the standard integration scheduler:

```bash
python3 mem_scheduler.py
```

This will:
- Open a visual interface showing the sync status
- Run immediately on startup
- Continue running every hour
- Allow you to trigger a manual sync with the "Run Now" button

### Smart Integration

To run the smart integration scheduler:

```bash
python3 mem_smart_scheduler.py
```

This provides the same interface and scheduling as the standard integration, but uses Mem.ai's intelligent "Mem It" API to process your conversations.

### Manual Runs

You can also run either integration manually without the scheduler:

```bash
# Standard integration
python3 limitless_to_mem.py

# Smart integration
python3 limitless_to_mem_smart.py
```

## How It Works

### Standard Integration

1. Fetches new Limitless conversations (since the last run)
2. Groups them into a single Markdown-formatted note
3. Creates a note in Mem.ai with proper formatting
4. Keeps track of which conversations have been processed

### Smart Integration

1. Fetches new Limitless conversations (since the last run)
2. Processes each conversation individually with the Mem It API
3. Mem.ai uses AI to extract key information and organize it
4. Keeps track of which conversations have been processed

## Choosing the Right Option

- **Standard Integration**: Best for preserving the original conversation format and getting complete transcripts in your Mem.ai knowledge base.

- **Smart Integration**: Best for extracting important information, action items, and key points from conversations without the extra noise.

You can run both integrations side by side if you want both the complete transcripts and the AI-extracted information.

## Troubleshooting

- Check that your API keys are correct in the `.env` file
- Ensure Python 3.7+ is installed
- Make sure you're running the script from the correct directory
- If you're getting errors, check the console output for details 