import schedule
import time
import subprocess
import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import threading

# Global variables
next_run_time = None
last_run_status = "Not run yet"
app = None

def update_gui():
    """
    Update the GUI with the current status
    """
    if app is None:
        return
        
    global next_run_time, last_run_status
    
    # Update time remaining
    if next_run_time:
        now = datetime.now()
        if next_run_time > now:
            time_diff = next_run_time - now
            minutes = time_diff.seconds // 60
            seconds = time_diff.seconds % 60
            app.time_label.config(text=f"Next run in: {minutes:02d}:{seconds:02d}")
        else:
            app.time_label.config(text="Running now...")
    
    # Update status
    app.status_label.config(text=f"Status: {last_run_status}")
    
    # Schedule the next update
    app.after(1000, update_gui)  # Update every second

def run_sync_job():
    """
    Run the Mem.ai sync job as a subprocess
    """
    global next_run_time, last_run_status
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{current_time}] Running Mem.ai sync job...")
    last_run_status = "Running..."
    
    if app:
        app.status_label.config(text=f"Status: {last_run_status}")
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create the full path to the limitless_to_mem.py script
    sync_script_path = os.path.join(script_dir, "limitless_to_mem.py")
    
    # Run the script as a subprocess
    try:
        result = subprocess.run(["python3", sync_script_path], 
                               capture_output=True, 
                               text=True, 
                               check=True)
        print(result.stdout)
        last_run_status = f"Success at {current_time}"
    except subprocess.CalledProcessError as e:
        print(f"Error running sync job: {e}")
        print(e.stderr)
        last_run_status = f"Failed at {current_time}"
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Mem.ai sync job completed")
    
    # Calculate next run time
    next_run_time = datetime.now() + timedelta(hours=1)

class SchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Limitless to Mem.ai Sync")
        self.geometry("300x150")
        self.resizable(False, False)
        
        # Make window stay on top
        self.attributes("-topmost", True)
        
        # Set window icon (if available)
        try:
            self.iconbitmap("icon.ico")  # You'd need to create this icon file
        except:
            pass  # Ignore if icon not found
        
        # Create frame
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Status label
        self.status_label = ttk.Label(frame, text="Status: Not started")
        self.status_label.pack(pady=5)
        
        # Time until next run
        self.time_label = ttk.Label(frame, text="Next run in: --:--")
        self.time_label.pack(pady=5)
        
        # Manual run button
        self.run_button = ttk.Button(frame, text="Run Now", command=self.run_now)
        self.run_button.pack(pady=5)
        
        # Quit button
        self.quit_button = ttk.Button(frame, text="Quit", command=self.quit_app)
        self.quit_button.pack(pady=5)
    
    def run_now(self):
        """Run the sync job now"""
        threading.Thread(target=run_sync_job).start()
    
    def quit_app(self):
        """Quit the application"""
        self.destroy()
        os._exit(0)  # Force exit all threads

def run_scheduler_thread():
    """
    Thread function for the scheduler
    """
    global next_run_time
    
    # Schedule the job to run every hour
    schedule.every(1).hours.do(run_sync_job)
    
    # Calculate initial next run time
    next_run_time = datetime.now() + timedelta(hours=1)
    
    # Run once immediately on startup
    print("Running initial Mem.ai sync job...")
    run_sync_job()
    
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every second instead of every minute to be more responsive

def main():
    global app
    
    # Create the GUI
    app = SchedulerApp()
    
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler_thread)
    scheduler_thread.daemon = True  # Allow the thread to be terminated when the main program exits
    scheduler_thread.start()
    
    # Start the GUI update
    update_gui()
    
    # Start the main loop
    app.mainloop()

if __name__ == "__main__":
    main() 