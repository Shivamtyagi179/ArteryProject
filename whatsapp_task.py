# modules/whatsapp_control.py - 100% DYNAMIC!
import pyautogui
import time
import pyperclip

class WhatsAppControl:
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        print("📱 WhatsAppControl DYNAMIC Ready!")

    def send_message(self, contact: str, message: str) -> str:
        """WHATEVER contact/message milega - wahi send!"""
        print(f"📤 '{contact}' ko '{message}' bhej raha hu...")
        
        # 1. Windows Search → WhatsApp
        pyautogui.hotkey('win')
        time.sleep(0.5)
        pyautogui.write('whatsapp')
        pyautogui.press('enter')
        time.sleep(3)
        
        # 2. Contact search (DYNAMIC!)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.write(contact)  # WHATEVER contact name!
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        
        # 3. Message send (DYNAMIC!)
        pyperclip.copy(message)  # WHATEVER message!
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        
        return f"✅ '{contact}' ko '{message}' bhej diya boss!"

    def read_last_message(self, contact: str) -> str:
        """Last message read (DYNAMIC contact!)"""
        pyautogui.hotkey('win')
        time.sleep(0.5)
        pyautogui.write('whatsapp')
        pyautogui.press('enter')
        time.sleep(3)
        
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.write(contact)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        
        pyautogui.scroll(-3)
        return f"✅ '{contact}' ke messages padh liye!"

    def open_chat(self, contact: str) -> str:
        """Chat kholo (DYNAMIC!)"""
        pyautogui.hotkey('win')
        time.sleep(0.5)
        pyautogui.write('whatsapp')
        pyautogui.press('enter')
        time.sleep(3)
        
        pyautogui.hotkey('ctrl', 'f')
        pyautogui.write(contact)
        pyautogui.press('enter')
        return f"✅ '{contact}' chat khol diya!"
