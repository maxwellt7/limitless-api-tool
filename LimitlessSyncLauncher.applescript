-- LimitlessSyncLauncher.applescript
-- Launcher for Limitless API Sync tools

tell application "Terminal"
    -- Create a new terminal window
    do script ""
    
    -- Navigate to the correct directory
    do script "cd /Users/maxmayes/limitless-api-examples/python" in front window
    
    -- Run the sync application
    do script "python3 run_all_sync.py" in front window
    
    -- Hide the Terminal window (will still run in background)
    set visible of front window to false
end tell 