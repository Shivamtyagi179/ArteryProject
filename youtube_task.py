# modules/app_control/youtube_task.py - PERFECT WORKING
import webbrowser
import urllib.parse
import time
import pyautogui
import random

class YouTubeTask:
    def __init__(self):
        pass
    
    def execute(self, command, query=None):
        if command == "play":
            return self.play_first_video(query)
        elif command == "next":
            return self.next_video()
        elif command == "previous":
            return self.previous_video()
        elif command == "resume":
            return self.resume_video()
        elif command == "shuffle":
            return self.shuffle_playlist()

    
    def play_first_video(self, song):
        query = urllib.parse.quote(song)
        url = f"https://www.youtube.com/results?search_query={query}"
        
        print(f"🎵 Opening: {url}")
        webbrowser.open(url)
        
        # PERFECT TIMING FOR YOUR SCREEN
        time.sleep(4)  # Wait for load
        
        # EXACT POSITION: Click middle of first video thumbnail (screenshot se dekha)
        pyautogui.click(900, 400)  # Adjust if needed
        time.sleep(1) # Wait for video to start
      #  pyautogui.press("space")   # Play if paused
        
        return f"✅ {song} FIRST VIDEO PLAYING boss! 🎵"
    
    def next_video(self):
        pyautogui.hotkey("shift", "n")
        return "⏭️ Next video boss!"
    def previous_video(self):
        pyautogui.hotkey("shift", "p")
        return "⏮️ Previous video boss!"
    
    def resume_video(self):
        pyautogui.press("space")
        return "▶️ Video resumed boss!"
    
    def shuffle_playlist(self):
        pyautogui.click(1200, 200)  # Shuffle button position (screenshot se dekha)
        return "🔀 Playlist shuffled boss!" \
        " Note: Only works if shuffle button is visible and in the expected position." 
    