import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from dotenv import load_dotenv
from _client import get_lifelogs

# Load environment variables from .env file
load_dotenv()

class ConfigurationDialog:
    def __init__(self, parent=None):
        self.result = None
        self.setup_dialog(parent)
    
    def setup_dialog(self, parent):
        """Create the configuration dialog window"""
        self.dialog = tk.Toplevel(parent) if parent else tk.Tk()
        self.dialog.title("Limitless API Configuration")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        # Make dialog modal and stay on top
        if parent:
            self.dialog.transient(parent)
            self.dialog.grab_set()
        self.dialog.attributes("-topmost", True)
        
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔧 API Configuration Setup", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_text = ("Welcome to the Limitless Sync Monitor!\n\n"
                    "Please enter your API credentials below. These will be securely "
                    "saved to your .env file for future use.")
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.CENTER, wraplength=450)
        desc_label.pack(pady=(0, 20))
        
        # API Key entries frame
        entries_frame = ttk.LabelFrame(main_frame, text="API Credentials", padding="15")
        entries_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Limitless API Key (Required)
        ttk.Label(entries_frame, text="Limitless API Key (Required):", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.limitless_key_var = tk.StringVar()
        limitless_entry = ttk.Entry(entries_frame, textvariable=self.limitless_key_var, 
                                   width=60, show="*")
        limitless_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Show/Hide button for Limitless key
        show_limitless_var = tk.BooleanVar()
        def toggle_limitless_visibility():
            limitless_entry.config(show="" if show_limitless_var.get() else "*")
        ttk.Checkbutton(entries_frame, text="Show Limitless API Key", 
                       variable=show_limitless_var, 
                       command=toggle_limitless_visibility).pack(anchor=tk.W, pady=(0, 15))
        
        # Optional APIs separator
        ttk.Separator(entries_frame, orient='horizontal').pack(fill=tk.X, pady=(0, 10))
        ttk.Label(entries_frame, text="Optional API Keys (for additional integrations):", 
                 font=("Arial", 9)).pack(anchor=tk.W, pady=(0, 10))
        
        # Notion API Key (Optional)
        ttk.Label(entries_frame, text="Notion API Key (Optional):").pack(anchor=tk.W, pady=(0, 5))
        self.notion_key_var = tk.StringVar()
        ttk.Entry(entries_frame, textvariable=self.notion_key_var, width=60).pack(fill=tk.X, pady=(0, 5))
        
        # Notion Database ID (Optional)
        ttk.Label(entries_frame, text="Notion Database ID (Optional):").pack(anchor=tk.W, pady=(0, 5))
        self.notion_db_var = tk.StringVar()
        ttk.Entry(entries_frame, textvariable=self.notion_db_var, width=60).pack(fill=tk.X, pady=(0, 5))
        
        # Mem.ai API Key (Optional)
        ttk.Label(entries_frame, text="Mem.ai API Key (Optional):").pack(anchor=tk.W, pady=(0, 5))
        self.mem_key_var = tk.StringVar()
        ttk.Entry(entries_frame, textvariable=self.mem_key_var, width=60).pack(fill=tk.X, pady=(0, 5))
        
        # OpenAI API Key (Optional)
        ttk.Label(entries_frame, text="OpenAI API Key (Optional):").pack(anchor=tk.W, pady=(0, 5))
        self.openai_key_var = tk.StringVar()
        ttk.Entry(entries_frame, textvariable=self.openai_key_var, width=60).pack(fill=tk.X, pady=(0, 10))
        
        # Load existing values if .env file exists
        self.load_existing_values()
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Save button
        save_btn = ttk.Button(buttons_frame, text="Save Configuration", 
                             command=self.save_configuration, style="Accent.TButton")
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Cancel button
        cancel_btn = ttk.Button(buttons_frame, text="Cancel", command=self.cancel)
        cancel_btn.pack(side=tk.RIGHT)
        
        # Help button
        help_btn = ttk.Button(buttons_frame, text="Help", command=self.show_help)
        help_btn.pack(side=tk.LEFT)
        
        # Focus on the Limitless API key entry
        limitless_entry.focus()
        
    def load_existing_values(self):
        """Load existing values from .env file if it exists"""
        env_path = ".env"
        if os.path.exists(env_path):
            load_dotenv(env_path)
            self.limitless_key_var.set(os.getenv("LIMITLESS_API_KEY", ""))
            self.notion_key_var.set(os.getenv("NOTION_API_KEY", ""))
            self.notion_db_var.set(os.getenv("NOTION_DATABASE_ID", ""))
            self.mem_key_var.set(os.getenv("MEM_API_KEY", ""))
            self.openai_key_var.set(os.getenv("OPENAI_API_KEY", ""))
    
    def save_configuration(self):
        """Save the configuration to .env file"""
        limitless_key = self.limitless_key_var.get().strip()
        
        # Validate required field
        if not limitless_key:
            messagebox.showerror("Error", "Limitless API Key is required!")
            return
        
        # Prepare .env content
        env_content = f"""# Limitless API credentials
LIMITLESS_API_KEY="{limitless_key}"

# Notion API credentials
NOTION_API_KEY="{self.notion_key_var.get().strip()}"
NOTION_DATABASE_ID="{self.notion_db_var.get().strip()}"

# Mem.ai API credentials  
MEM_API_KEY="{self.mem_key_var.get().strip()}"

# OpenAI API credentials
OPENAI_API_KEY="{self.openai_key_var.get().strip()}"

# Optional settings
# LIMITLESS_API_URL=https://api.limitless.ai  # Only needed if using a custom API URL
"""
        
        try:
            # Write to .env file
            with open(".env", "w") as f:
                f.write(env_content)
            
            # Reload environment variables
            load_dotenv(override=True)
            
            self.result = "saved"
            messagebox.showinfo("Success", "Configuration saved successfully!")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")
    
    def cancel(self):
        """Cancel the configuration"""
        self.result = "cancelled"
        self.dialog.destroy()
    
    def show_help(self):
        """Show help information"""
        help_text = """🔗 Where to get your API keys:

🔸 Limitless API Key (Required):
   Visit: https://limitless.ai/developers
   Sign up/login and generate an API key

🔸 Notion API Key (Optional):
   Visit: https://notion.so/my-integrations
   Create a new integration and copy the API key

🔸 Mem.ai API Key (Optional):
   Visit: https://mem.ai (Settings → API)
   Generate an API key

🔸 OpenAI API Key (Optional):
   Visit: https://platform.openai.com/api-keys
   Create and copy an API key

💡 Tip: Only the Limitless API key is required.
The others are optional for additional sync features."""
        
        messagebox.showinfo("API Key Help", help_text)
    
    def run(self):
        """Run the dialog and return the result"""
        self.dialog.mainloop()
        return self.result

def check_configuration():
    """Check if the required configuration exists"""
    load_dotenv()
    limitless_key = os.getenv("LIMITLESS_API_KEY")
    return bool(limitless_key and limitless_key.strip())

class SyncMonitor:
    def __init__(self):
        self.api_key = os.getenv("LIMITLESS_API_KEY")
        self.sync_data = {}
        self.load_sync_history()
        
    def load_sync_history(self):
        """Load existing sync history from JSON files"""
        files = [
            "last_processed.json",
            "last_processed_mem.json", 
            "last_processed_mem_smart.json"
        ]
        
        for file in files:
            if os.path.exists(file):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        self.sync_data[file] = data
                except:
                    self.sync_data[file] = {"last_processed": None, "count": 0}
            else:
                self.sync_data[file] = {"last_processed": None, "count": 0}
    
    def get_daily_imports(self, days_back=30):
        """Get daily import counts from Limitless API"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        daily_counts = {}
        
        # Get data for each day
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            
            try:
                lifelogs = get_lifelogs(
                    api_key=self.api_key,
                    date=date_str,
                    limit=100,
                    direction="desc"
                )
                
                daily_counts[date_str] = len(lifelogs)
                
            except Exception as e:
                print(f"Error fetching data for {date_str}: {e}")
                daily_counts[date_str] = 0
            
            current_date += timedelta(days=1)
        
        return daily_counts
    
    def get_sync_status(self):
        """Get current sync status for all integrations"""
        status = {}
        
        # Check Notion sync
        if "last_processed.json" in self.sync_data:
            last_notion = self.sync_data["last_processed.json"].get("last_processed")
            if last_notion:
                last_notion_date = datetime.fromisoformat(last_notion.replace('Z', '+00:00'))
                hours_since_notion = (datetime.now() - last_notion_date).total_seconds() / 3600
                status["Notion"] = {
                    "last_sync": last_notion_date.strftime('%Y-%m-%d %H:%M'),
                    "hours_ago": round(hours_since_notion, 1),
                    "status": "Up to date" if hours_since_notion < 24 else "Behind",
                    "count": self.sync_data["last_processed.json"].get("count", 0)
                }
            else:
                status["Notion"] = {"last_sync": "Never", "hours_ago": "N/A", "status": "Not configured", "count": 0}
        
        # Check Mem.ai sync
        if "last_processed_mem.json" in self.sync_data:
            last_mem = self.sync_data["last_processed_mem.json"].get("last_processed")
            if last_mem:
                last_mem_date = datetime.fromisoformat(last_mem.replace('Z', '+00:00'))
                hours_since_mem = (datetime.now() - last_mem_date).total_seconds() / 3600
                status["Mem.ai"] = {
                    "last_sync": last_mem_date.strftime('%Y-%m-%d %H:%M'),
                    "hours_ago": round(hours_since_mem, 1),
                    "status": "Up to date" if hours_since_mem < 24 else "Behind",
                    "count": self.sync_data["last_processed_mem.json"].get("count", 0)
                }
            else:
                status["Mem.ai"] = {"last_sync": "Never", "hours_ago": "N/A", "status": "Not configured", "count": 0}
        
        # Check Mem.ai Smart sync
        if "last_processed_mem_smart.json" in self.sync_data:
            last_mem_smart = self.sync_data["last_processed_mem_smart.json"].get("last_processed")
            if last_mem_smart:
                last_mem_smart_date = datetime.fromisoformat(last_mem_smart.replace('Z', '+00:00'))
                hours_since_mem_smart = (datetime.now() - last_mem_smart_date).total_seconds() / 3600
                status["Mem.ai Smart"] = {
                    "last_sync": last_mem_smart_date.strftime('%Y-%m-%d %H:%M'),
                    "hours_ago": round(hours_since_mem_smart, 1),
                    "status": "Up to date" if hours_since_mem_smart < 24 else "Behind",
                    "count": self.sync_data["last_processed_mem_smart.json"].get("count", 0)
                }
            else:
                status["Mem.ai Smart"] = {"last_sync": "Never", "hours_ago": "N/A", "status": "Not configured", "count": 0}
        
        return status
    
    def create_sync_chart(self):
        """Create a comprehensive sync monitoring chart"""
        daily_imports = self.get_daily_imports(30)
        sync_status = self.get_sync_status()
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Chart 1: Daily imports
        dates = list(daily_imports.keys())
        counts = list(daily_imports.values())
        
        ax1.bar(dates, counts, color='skyblue', alpha=0.7)
        ax1.set_title('Daily Limitless Imports (Last 30 Days)', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Number of Imports')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add average line
        avg_count = sum(counts) / len(counts) if counts else 0
        ax1.axhline(y=avg_count, color='red', linestyle='--', alpha=0.7, label=f'Average: {avg_count:.1f}')
        ax1.legend()
        
        # Chart 2: Sync status
        services = list(sync_status.keys())
        hours_ago = []
        colors = []
        
        for service in services:
            hours = sync_status[service]["hours_ago"]
            if hours == "N/A":
                hours_ago.append(0)
                colors.append('gray')
            else:
                hours_ago.append(hours)
                colors.append('green' if hours < 24 else 'orange' if hours < 48 else 'red')
        
        bars = ax2.bar(services, hours_ago, color=colors, alpha=0.7)
        ax2.set_title('Sync Status - Hours Since Last Sync', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Hours Ago')
        ax2.set_ylim(0, max(hours_ago) * 1.2 if hours_ago else 24)
        
        # Add value labels on bars
        for bar, hours in zip(bars, hours_ago):
            if hours > 0:
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                        f'{hours}h', ha='center', va='bottom', fontweight='bold')
        
        # Add status text
        status_text = "Sync Status Summary:\n"
        for service, info in sync_status.items():
            status_text += f"• {service}: {info['status']} (Last: {info['last_sync']}, Count: {info['count']})\n"
        
        plt.figtext(0.02, 0.02, status_text, fontsize=10, 
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        return daily_imports, sync_status

class SyncMonitorGUI:
    def __init__(self):
        self.monitor = SyncMonitor()
        self.setup_gui()
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Limitless Sync Monitor")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Make window stay on top
        self.root.attributes("-topmost", True)
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Limitless Sync Monitor", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Current Sync Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_labels = {}
        self.update_status_display(status_frame)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create chart button
        self.chart_button = ttk.Button(button_frame, text="Generate Sync Chart", 
                                      command=self.generate_chart)
        self.chart_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh button
        self.refresh_button = ttk.Button(button_frame, text="Refresh Status", 
                                        command=self.refresh_status)
        self.refresh_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Configuration button
        self.config_button = ttk.Button(button_frame, text="⚙️ Configure API Keys", 
                                       command=self.open_configuration)
        self.config_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Auto-refresh checkbox
        self.auto_refresh_var = tk.BooleanVar()
        self.auto_refresh_check = ttk.Checkbutton(button_frame, text="Auto-refresh every 30s", 
                                                 variable=self.auto_refresh_var, 
                                                 command=self.toggle_auto_refresh)
        self.auto_refresh_check.pack(side=tk.RIGHT)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(main_frame, text="Summary", padding="10")
        summary_frame.pack(fill=tk.BOTH, expand=True)
        
        self.summary_text = tk.Text(summary_frame, height=8, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for summary
        scrollbar = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL, command=self.summary_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.summary_text.configure(yscrollcommand=scrollbar.set)
        
        # Start auto-refresh if enabled
        self.auto_refresh_enabled = False
        self.update_summary()
        
    def open_configuration(self):
        """Open the configuration dialog"""
        config_dialog = ConfigurationDialog(self.root)
        result = config_dialog.run()
        
        if result == "saved":
            # Reload the monitor with new configuration
            load_dotenv(override=True)
            self.monitor = SyncMonitor()
            self.refresh_status()
            messagebox.showinfo("Success", "Configuration updated! The monitor has been refreshed with your new settings.")
        
    def update_status_display(self, parent):
        """Update the status display in the GUI"""
        # Clear existing labels
        for widget in parent.winfo_children():
            widget.destroy()
        
        sync_status = self.monitor.get_sync_status()
        
        for i, (service, info) in enumerate(sync_status.items()):
            # Service name
            service_label = ttk.Label(parent, text=f"{service}:", font=("Arial", 10, "bold"))
            service_label.grid(row=i, column=0, sticky=tk.W, padx=(0, 10), pady=2)
            
            # Status with color
            status_color = "green" if info["status"] == "Up to date" else "orange" if info["status"] == "Behind" else "gray"
            status_label = ttk.Label(parent, text=info["status"], foreground=status_color)
            status_label.grid(row=i, column=1, sticky=tk.W, padx=(0, 20), pady=2)
            
            # Last sync time
            time_label = ttk.Label(parent, text=f"Last: {info['last_sync']}")
            time_label.grid(row=i, column=2, sticky=tk.W, padx=(0, 20), pady=2)
            
            # Count
            count_label = ttk.Label(parent, text=f"Count: {info['count']}")
            count_label.grid(row=i, column=3, sticky=tk.W, pady=2)
            
            self.status_labels[service] = {
                "status": status_label,
                "time": time_label,
                "count": count_label
            }
    
    def update_summary(self):
        """Update the summary text"""
        self.monitor.load_sync_history()  # Reload data
        sync_status = self.monitor.get_sync_status()
        
        summary = "Sync Status Summary:\n\n"
        
        total_synced = 0
        up_to_date_count = 0
        
        for service, info in sync_status.items():
            summary += f"📊 {service}:\n"
            summary += f"   Status: {info['status']}\n"
            summary += f"   Last Sync: {info['last_sync']}\n"
            summary += f"   Total Synced: {info['count']} items\n"
            summary += f"   Hours Ago: {info['hours_ago']}\n\n"
            
            total_synced += info['count']
            if info['status'] == "Up to date":
                up_to_date_count += 1
        
        summary += f"📈 Overall:\n"
        summary += f"   Total Items Synced: {total_synced}\n"
        summary += f"   Services Up to Date: {up_to_date_count}/{len(sync_status)}\n"
        summary += f"   Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(1.0, summary)
        
        # Schedule next update if auto-refresh is enabled
        if self.auto_refresh_enabled:
            self.root.after(30000, self.update_summary)  # 30 seconds
    
    def generate_chart(self):
        """Generate and display the sync chart"""
        try:
            self.chart_button.config(state='disabled')
            self.chart_button.config(text="Generating...")
            
            # Run chart generation in a separate thread
            def generate():
                try:
                    daily_imports, sync_status = self.monitor.create_sync_chart()
                    self.root.after(0, lambda: self.chart_button.config(text="Generate Sync Chart", state='normal'))
                except Exception as e:
                    print(f"Error generating chart: {e}")
                    self.root.after(0, lambda: self.chart_button.config(text="Generate Sync Chart", state='normal'))
            
            threading.Thread(target=generate, daemon=True).start()
            
        except Exception as e:
            print(f"Error: {e}")
            self.chart_button.config(text="Generate Sync Chart", state='normal')
    
    def refresh_status(self):
        """Refresh the status display"""
        self.update_summary()
        
        # Update status display
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.LabelFrame) and "Current Sync Status" in child.cget("text"):
                        self.update_status_display(child)
                        break
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh functionality"""
        self.auto_refresh_enabled = self.auto_refresh_var.get()
        if self.auto_refresh_enabled:
            self.update_summary()
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

def main():
    """Main function to run the sync monitor"""
    print("Starting Limitless Sync Monitor...")
    print("This will show you sync status and generate charts of your imports")
    
    # Check if configuration is complete
    if not check_configuration():
        print("No valid configuration found. Opening setup dialog...")
        
        # Create a temporary root window for the configuration dialog
        temp_root = tk.Tk()
        temp_root.withdraw()  # Hide the temporary window
        
        config_dialog = ConfigurationDialog()
        result = config_dialog.run()
        
        temp_root.destroy()
        
        if result != "saved":
            print("Configuration cancelled. Exiting...")
            return
    
    # Reload environment variables after potential configuration
    load_dotenv(override=True)
    
    # Verify we have the required API key
    if not os.getenv("LIMITLESS_API_KEY"):
        print("Error: LIMITLESS_API_KEY environment variable not set")
        print("Please run the configuration dialog to set up your API keys")
        return
    
    # Create and run the GUI
    monitor_gui = SyncMonitorGUI()
    monitor_gui.run()

if __name__ == "__main__":
    main() 