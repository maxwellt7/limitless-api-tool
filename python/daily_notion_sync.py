import os
import requests
import datetime
import json
from datetime import datetime, timedelta
from _client import get_lifelogs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File to store the last processed conversation timestamp
LAST_PROCESSED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_processed.json")

def format_for_notion(lifelogs):
    """
    Format lifelogs for insertion into a Notion database
    """
    formatted_entries = []
    
    for lifelog in lifelogs:
        # Extract relevant information
        title = lifelog.get("title", "Untitled conversation")
        content = lifelog.get("markdown", "")
        start_time = lifelog.get("startTime", "")
        end_time = lifelog.get("endTime", "")
        id = lifelog.get("id", "")
        
        # Create Notion-formatted entry
        entry = {
            "id": id,
            "title": title,
            "content": content,
            "start_time": start_time,
            "end_time": end_time
        }
        
        formatted_entries.append(entry)
    
    return formatted_entries

def send_to_notion(entries, notion_api_key, database_id):
    """
    Send formatted entries to a Notion database
    """
    if not entries:
        print("No new entries to add to Notion")
        return
        
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    for entry in entries:
        # Construct Notion page properties based on your database schema
        # Adjust property names and types to match your Notion database
        properties = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": entry["title"]
                        }
                    }
                ]
            },
            "Content": {
                "rich_text": [
                    {
                        "text": {
                            "content": entry["content"][:2000] if len(entry["content"]) > 2000 else entry["content"]
                        }
                    }
                ]
            },
            "Start Time": {
                "date": {
                    "start": entry["start_time"]
                }
            },
            "End Time": {
                "date": {
                    "start": entry["end_time"]
                }
            },
            "Source": {
                "select": {
                    "name": "Limitless"
                }
            }
        }
        
        # Create the page in Notion
        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        
        response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
        
        if response.status_code != 200:
            print(f"Error creating Notion page: {response.status_code}")
            print(response.json())
        else:
            print(f"Successfully added entry: {entry['title']}")
            # Update last processed timestamp
            save_last_processed(entry["id"], entry["end_time"])

def get_last_processed():
    """
    Get the last processed conversation timestamp
    """
    if not os.path.exists(LAST_PROCESSED_FILE):
        # If file doesn't exist, create it with default values
        default_data = {
            "last_id": "",
            "last_timestamp": (datetime.now() - timedelta(days=7)).isoformat()
        }
        with open(LAST_PROCESSED_FILE, "w") as f:
            json.dump(default_data, f)
        return default_data
    
    try:
        with open(LAST_PROCESSED_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading last processed file: {e}")
        # Return a default value (1 week ago)
        return {
            "last_id": "",
            "last_timestamp": (datetime.now() - timedelta(days=7)).isoformat()
        }

def save_last_processed(conversation_id, timestamp):
    """
    Save the last processed conversation timestamp
    """
    data = {
        "last_id": conversation_id,
        "last_timestamp": timestamp
    }
    
    with open(LAST_PROCESSED_FILE, "w") as f:
        json.dump(data, f)

def get_recent_conversations():
    """
    Get recent conversations (since last processed)
    """
    # Get the current date for logging
    current_date = datetime.now()
    current_date_str = current_date.strftime('%Y-%m-%d')
    print(f"Current date: {current_date_str}")
    
    # Use today's date for the API call
    today_str = current_date.strftime('%Y-%m-%d')
    
    # Get the last processed timestamp
    last_processed = get_last_processed()
    print(f"Last processed timestamp: {last_processed['last_timestamp']}")
    print(f"Last processed ID: {last_processed['last_id']}")
    
    # Get recent lifelogs
    print(f"Fetching conversations from Limitless for date: {today_str}")
    lifelogs = get_lifelogs(
        api_key=os.getenv("LIMITLESS_API_KEY"),
        date=today_str,
        limit=None,  # Get all available logs
        timezone="America/New_York",  # Use EST timezone
        direction="desc"  # Get most recent first
    )
    
    # If no conversations found for today, try yesterday
    if not lifelogs:
        yesterday = current_date - timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        print(f"No conversations found for today, trying yesterday: {yesterday_str}")
        lifelogs = get_lifelogs(
            api_key=os.getenv("LIMITLESS_API_KEY"),
            date=yesterday_str,
            limit=None,
            timezone="America/New_York",
            direction="desc"
        )
    
    # Filter out already processed conversations
    last_id = last_processed["last_id"]
    new_lifelogs = []
    
    if last_id:
        # If we have a last ID, filter by it
        for log in lifelogs:
            if log.get("id") == last_id:
                # We've reached the last processed conversation
                break
            new_lifelogs.append(log)
    else:
        # If no last ID, use all logs
        new_lifelogs = lifelogs
    
    print(f"Found {len(new_lifelogs)} new conversations")
    return new_lifelogs

def main():
    # Check for required environment variables
    required_vars = ["LIMITLESS_API_KEY", "NOTION_API_KEY", "NOTION_DATABASE_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your environment or .env file")
        return
    
    # Get recent conversations
    print("Checking for new conversations from Limitless...")
    lifelogs = get_recent_conversations()
    
    if not lifelogs:
        print("No new conversations found")
        return
    
    # Format for Notion
    entries = format_for_notion(lifelogs)
    
    # Send to Notion
    print("Sending to Notion database...")
    send_to_notion(
        entries,
        os.getenv("NOTION_API_KEY"),
        os.getenv("NOTION_DATABASE_ID")
    )
    
    print("Sync complete!")

if __name__ == "__main__":
    main() 