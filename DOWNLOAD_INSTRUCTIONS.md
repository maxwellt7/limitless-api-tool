# 🚀 Download & Setup Instructions for Limitless API Tool

This guide will help you download and set up the comprehensive Limitless API integration toolkit on your computer.

## 📋 Prerequisites

Before starting, make sure you have:
- **Python 3.7+** installed
- **Git** installed
- A **Limitless API key** (get one at [limitless.ai/developers](https://limitless.ai/developers))

## 🔧 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/maxwellt7/limitless-api-tool.git

# Navigate into the project directory
cd limitless-api-tool
```

### Step 2: Set Up Python Environment

```bash
# Navigate to the python directory
cd python

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 3: Install Jupyter (for Chart Dashboard)

```bash
# Install Jupyter notebook
pip install jupyter notebook
```

### Step 4: Configure API Keys

```bash
# Copy the environment example file
cp env.example .env

# Edit the .env file with your API keys
# You can use any text editor like nano, vim, or VS Code
nano .env
```

**Add your API keys to the `.env` file:**

```bash
# Limitless API Key (required)
LIMITLESS_API_KEY=your_limitless_api_key_here

# Notion API Key (optional - for Notion sync)
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_notion_database_id_here

# Mem.ai API Key (optional - for Mem.ai sync)
MEM_API_KEY=your_mem_api_key_here

# OpenAI API Key (optional - for daily summaries)
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 5: Set Up Chart Dashboard

```bash
# Navigate to notebooks directory
cd ../notebooks

# Launch Jupyter notebook
jupyter notebook chart_usage.ipynb
```

**In the notebook:**
1. Open the notebook in your browser
2. In **Cell 1**, replace `< your api key >` with your actual Limitless API key
3. Run all cells to see your data visualization

### Step 6: Set Up Sync Dashboards

#### Option A: Run Both Sync Tools

```bash
# Navigate back to python directory
cd ../python

# Launch both sync dashboards
python run_all_sync.py
```

#### Option B: Run Individual Sync Tools

```bash
# For Notion sync only
python scheduler.py

# For Mem.ai sync only
python mem_smart_scheduler.py
```

## 🔗 Optional Integrations

### Set Up Notion Integration

If you want to sync to Notion:

1. **Create a Notion integration:**
   - Go to [notion.so/my-integrations](https://notion.so/my-integrations)
   - Create a new integration
   - Copy the API key

2. **Create a Notion database:**
   - Create a new page in Notion
   - Add a database with these properties:
     - **Name** (title): Title of the conversation
     - **Content** (rich text): The markdown content
     - **Start Time** (date): When the conversation started
     - **End Time** (date): When the conversation ended
     - **Source** (select): Set to "Limitless"

3. **Get your database ID:**
   - Open the database in Notion
   - Copy the ID from the URL (the part after the last slash)

4. **Update your .env file:**
   ```bash
   NOTION_API_KEY=your_notion_api_key
   NOTION_DATABASE_ID=your_database_id
   ```

### Set Up Mem.ai Integration

If you want to sync to Mem.ai:

1. **Get your Mem.ai API key:**
   - Go to [mem.ai](https://mem.ai)
   - Navigate to Settings → API
   - Generate an API key

2. **Update your .env file:**
   ```bash
   MEM_API_KEY=your_mem_api_key
   ```

## 🎯 What You'll Have After Setup

### 📊 Chart Dashboard
- Visual timeline of your daily recordings
- Usage statistics and patterns
- Interactive data analysis

### 🔄 Sync Dashboards
- Real-time monitoring of sync processes
- Manual trigger buttons
- Status updates and countdown timers

### 📝 Automated Syncs
- Daily Notion sync at 4:00 AM EST
- Hourly Mem.ai smart processing
- Automatic error recovery

## 🔧 Troubleshooting Common Issues

### "Command not found: python3"
```bash
# Try using 'python' instead
python --version
# If that doesn't work, install Python from python.org
```

### "Permission denied" errors
```bash
# Make sure you have write permissions
chmod +x *.py
```

### "Module not found" errors
```bash
# Make sure your virtual environment is activated
source venv/bin/activate
# Reinstall requirements
pip install -r requirements.txt
```

### Jupyter won't start
```bash
# Try installing with pip3
pip3 install jupyter notebook
# Or use conda if you have it
conda install jupyter
```

## ⚡ Quick Start Commands

For someone who just wants to get started quickly:

```bash
# 1. Clone and setup
git clone https://github.com/maxwellt7/limitless-api-tool.git
cd limitless-api-tool/python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt jupyter

# 2. Configure API key
cp env.example .env
# Edit .env with your Limitless API key

# 3. Launch dashboards
python run_all_sync.py
```

## 🎉 Success Indicators

- ✅ Two GUI windows appear (sync dashboards)
- ✅ Chart dashboard shows your recording data
- ✅ No error messages in terminal
- ✅ Sync processes show "Success" status

## 📱 Features Overview

### 🔄 Sync Tools & Dashboards
- `run_all_sync.py` - Launches both Notion and Mem.ai sync dashboards
- `scheduler.py` - Notion sync with GUI monitoring
- `mem_smart_scheduler.py` - AI-powered Mem.ai sync with GUI
- `daily_notion_sync.py` - Automated Notion integration
- `limitless_to_mem_smart.py` - Smart Mem.ai processing

### 📊 Data Visualization
- `notebooks/chart_usage.ipynb` - Interactive usage analytics
- Timeline charts of recording sessions
- Usage statistics and patterns

### 💻 Code Examples
- Python examples with full sync functionality
- TypeScript examples for web integration
- OpenAPI specification for API reference

### 📚 Documentation
- Comprehensive README files
- Setup instructions for each integration
- Environment configuration examples

## 🔒 Security Features

- ✅ API keys removed from code
- ✅ Comprehensive `.gitignore` file
- ✅ Environment variables properly excluded
- ✅ Sensitive data protection

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the individual README files in each directory
3. Check the [Limitless API documentation](https://limitless.ai/developers/docs/api)

---

**Happy syncing! 🚀** 