import os
import requests
import tzlocal
import time

def get_lifelogs(api_key, api_url=os.getenv("LIMITLESS_API_URL") or "https://api.limitless.ai", endpoint="v1/lifelogs", limit=50, batch_size=10, includeMarkdown=True, includeHeadings=False, date=None, timezone=None, direction="asc", max_retries=3, retry_delay=5):
    all_lifelogs = []
    cursor = None
    
    # If limit is None, fetch all available lifelogs
    # Otherwise, set a batch size (e.g., 10) and fetch until we reach the limit
    if limit is not None:
        batch_size = min(batch_size, limit)
    
    while True:
        params = {  
            "limit": batch_size,
            "includeMarkdown": "true" if includeMarkdown else "false",
            "includeHeadings": "false" if includeHeadings else "true",
            "date": date,
            "direction": direction,
            "timezone": timezone if timezone else str(tzlocal.get_localzone())
        }
        
        # Add cursor for pagination if we have one
        if cursor:
            params["cursor"] = cursor
            
        # Add retry logic
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(
                    f"{api_url}/{endpoint}",
                    headers={"X-API-Key": api_key},
                    params=params,
                    timeout=30  # Add a timeout to prevent hanging requests
                )
                
                if response.ok:
                    break  # Success, exit retry loop
                elif response.status_code == 504:  # Gateway Timeout
                    retries += 1
                    print(f"Received 504 Gateway Timeout. Retry {retries}/{max_retries}...")
                    if retries < max_retries:
                        time.sleep(retry_delay)  # Wait before retrying
                    else:
                        raise Exception(f"HTTP error after {max_retries} retries! Status: {response.status_code}")
                else:
                    # For other errors, don't retry
                    raise Exception(f"HTTP error! Status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                retries += 1
                print(f"Request exception: {e}. Retry {retries}/{max_retries}...")
                if retries < max_retries:
                    time.sleep(retry_delay)  # Wait before retrying
                else:
                    raise Exception(f"Request failed after {max_retries} retries: {e}")
        
        if not response.ok:
            raise Exception(f"HTTP error! Status: {response.status_code}")

        data = response.json()
        lifelogs = data.get("data", {}).get("lifelogs", [])
        
        # Add transcripts from this batch
        for lifelog in lifelogs:
            all_lifelogs.append(lifelog)
        
        # Check if we've reached the requested limit
        if limit is not None and len(all_lifelogs) >= limit:
            return all_lifelogs[:limit]
        
        # Get the next cursor from the response
        next_cursor = data.get("meta", {}).get("lifelogs", {}).get("nextCursor")
        
        # If there's no next cursor or we got fewer results than requested, we're done
        if not next_cursor or len(lifelogs) < batch_size:
            break
            
        print(f"Fetched {len(lifelogs)} lifelogs, next cursor: {next_cursor}")
        cursor = next_cursor
    
    return all_lifelogs
