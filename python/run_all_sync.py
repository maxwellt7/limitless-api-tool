import subprocess
import sys
import os
import time

def main():
    """
    Run both the Limitless-to-Notion and Limitless-to-Mem.ai sync jobs
    """
    print("Starting Limitless integrations...")
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create full paths to the script files
    notion_script_path = os.path.join(script_dir, "scheduler.py")
    mem_script_path = os.path.join(script_dir, "mem_smart_scheduler.py")
    
    # Command to run the Notion scheduler
    notion_cmd = [sys.executable, notion_script_path]
    
    # Command to run the Mem.ai scheduler
    mem_cmd = [sys.executable, mem_script_path]
    
    try:
        # Start the Notion scheduler in a separate process
        print("Starting Limitless-to-Notion sync...")
        notion_process = subprocess.Popen(notion_cmd)
        
        # Wait a bit to avoid any potential conflicts
        time.sleep(2)
        
        # Start the Mem.ai scheduler in a separate process
        print("Starting Limitless-to-Mem.ai sync...")
        mem_process = subprocess.Popen(mem_cmd)
        
        print("\nBoth sync processes are now running!")
        print("You should see two separate GUI windows.")
        print("Press Ctrl+C to stop both processes.\n")
        
        # Keep the script running to manage the subprocesses
        while True:
            # Check if processes are still running
            if notion_process.poll() is not None:
                print("Notion sync process has stopped. Restarting...")
                notion_process = subprocess.Popen(notion_cmd)
            
            if mem_process.poll() is not None:
                print("Mem.ai sync process has stopped. Restarting...")
                mem_process = subprocess.Popen(mem_cmd)
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nStopping all sync processes...")
        # Terminate the processes on Ctrl+C
        if 'notion_process' in locals():
            notion_process.terminate()
        if 'mem_process' in locals():
            mem_process.terminate()
        print("All sync processes stopped.")

if __name__ == "__main__":
    main() 