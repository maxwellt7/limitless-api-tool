import os
import json
import requests
from datetime import datetime, timedelta, timezone
from _client import get_lifelogs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File to store the last processed conversation timestamp
LAST_PROCESSED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_processed_mem.json")

def get_last_processed():
    """
    Get the last processed conversation timestamp for Mem.ai integration
    """
    if not os.path.exists(LAST_PROCESSED_FILE):
        # If file doesn't exist, create it with default values (1 hour ago)
        default_data = {
            "last_id": "",
            "last_timestamp": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        }
        with open(LAST_PROCESSED_FILE, "w") as f:
            json.dump(default_data, f)
        return default_data
    
    try:
        with open(LAST_PROCESSED_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading last processed file: {e}")
        # Return a default value (1 hour ago)
        return {
            "last_id": "",
            "last_timestamp": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
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
    Get conversations from the last hour
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
        # If no last ID, use all logs from the last hour
        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        for log in lifelogs:
            # Parse the timestamp
            end_time_str = log.get("endTime", "")
            if end_time_str:
                try:
                    # Make sure we have a timezone-aware datetime
                    end_time = datetime.fromisoformat(end_time_str.replace("Z", "+00:00"))
                    if end_time >= one_hour_ago:
                        new_lifelogs.append(log)
                except ValueError:
                    # If we can't parse the timestamp, include the log to be safe
                    new_lifelogs.append(log)
            else:
                # If there's no timestamp, include the log to be safe
                new_lifelogs.append(log)
    
    print(f"Found {len(new_lifelogs)} new conversations")
    return new_lifelogs

def create_mem_note(lifelogs):
    """
    Create a new note in Mem.ai with the provided conversations
    """
    if not lifelogs:
        print("No new conversations to add to Mem.ai")
        return
    
    # Format the conversations as markdown
    current_hour = datetime.now().strftime('%Y-%m-%d %H:00')
    markdown_content = f"# Limitless Conversations: {current_hour}\n\n"
    
    for log in lifelogs:
        title = log.get("title", "Untitled conversation")
        content = log.get("markdown", "")
        start_time = log.get("startTime", "")
        end_time = log.get("endTime", "")
        
        markdown_content += f"## {title}\n\n"
        
        if start_time and end_time:
            # Format timestamps nicely
            try:
                start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                time_str = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
                markdown_content += f"*Time: {time_str}*\n\n"
            except ValueError:
                # If we can't parse the timestamps, use them as-is
                markdown_content += f"*Start: {start_time}*\n*End: {end_time}*\n\n"
        
        # Add the conversation content
        markdown_content += f"{content}\n\n---\n\n"
    
    # Prepare the request to Mem.ai
    mem_api_key = os.getenv("MEM_API_KEY")
    if not mem_api_key:
        print("Error: MEM_API_KEY not found in environment variables")
        return
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mem_api_key}"
    }
    
    data = {
        "content": markdown_content,
        "add_to_collections": ["Limitless Conversations"],
        "created_at": datetime.now().isoformat()
    }
    
    # Make the request
    try:
        response = requests.post(
            "https://api.mem.ai/v1/notes",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            print("Successfully created note in Mem.ai")
            note_data = response.json()
            print(f"Note URL: {note_data.get('url', 'Unknown')}")
            
            # Save the ID of the latest conversation
            if lifelogs:
                save_last_processed(
                    lifelogs[0].get("id", ""),
                    lifelogs[0].get("endTime", datetime.now(timezone.utc).isoformat())
                )
        else:
            print(f"Error creating note in Mem.ai: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"Exception creating note in Mem.ai: {e}")

def main():
    # Check for required environment variables
    required_vars = ["LIMITLESS_API_KEY", "MEM_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your environment or .env file")
        return
    
    # Get recent conversations
    print("Checking for new conversations from Limitless...")
    lifelogs = get_recent_conversations()
    
    # Create a note in Mem.ai
    create_mem_note(lifelogs)
    
    print("Mem.ai sync complete!")

if __name__ == "__main__":
    main() 