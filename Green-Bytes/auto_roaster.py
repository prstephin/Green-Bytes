import google.generativeai as genai
import pyautogui
from gtts import gTTS
from playsound import playsound
import os
import time
import io
from PIL import Image

# --- CONFIGURATION ---
print("Script starting up...")

# നിങ്ങളുടെ API കീ ഇവിടെ പേസ്റ്റ് ചെയ്യുക
try:
    YOUR_API_KEY = "AIzaSyAbTObTCi3oFd9sdqZxaeLU6ZxdC9dATvs"

    if "REPLACE_THIS" in YOUR_API_KEY:
        print("\n--- STOP! ---")
        print("You have not replaced the placeholder API key in the code.")
        exit()
    genai.configure(api_key=YOUR_API_KEY)
    print("API key configured successfully.")
except Exception as e:
    print(f"An error occurred during API configuration: {e}")
    exit()

model = genai.GenerativeModel('gemini-1.5-flash-latest')
print("AI model loaded.")

PROMPT = """
നിങ്ങൾ യൂസറിന്റെ ഒരു മലയാളി ചങ്കാണ്. യൂസർ വെറുതെ സമയം കളയുന്നത് കാണുമ്പോൾ നിങ്ങൾക്ക് നല്ല ദേഷ്യം വരും.
സ്ക്രീൻഷോട്ട് നോക്കി ആ സാഹചര്യത്തിന് ചേർന്ന ഒരു ഒന്നൊന്നര മലയാളം റോസ്റ്റ് കാച്ചണം.
നിന്റെ സംസാരം എപ്പോഴും മലയാളത്തിൽ ആയിരിക്കണം.

ഉദാഹരണത്തിന്:
- യൂസർ YouTube കാണുകയാണെങ്കിൽ, നീ പറയണം: "എണീറ്റ് വല്ല പണിക്കും പോടാ"
- യൂസർ കോഡിംഗ് ചെയ്യുകയാണെങ്കിൽ, നീ പറയണം: "ഓഹ്, വലിയ പ്രോഗ്രാമർ... ഇതൊക്കെ ആരെങ്കിലും ഉപയോഗിക്കുമോ?"
- വെറുതെ ഡെസ്ക്ടോപ്പ് നോക്കി ഇരിക്കുകയാണെങ്കിൽ, നീ പറയണം: "ഒരു പണിയും ഇല്ലാതെ വെറുതെ കുത്തിയിരിക്കുവാണല്ലേ?"
"""
INTERVAL_SECONDS = 4

# --- CORE FUNCTIONS ---

def take_screenshot_in_memory():
    """സ്ക്രീൻഷോട്ട് എടുക്കുന്നു"""
    print("1. സ്ക്രീൻഷോട്ട് എടുക്കുന്നു...")
    screenshot = pyautogui.screenshot()
    img_byte_arr = io.BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    return Image.open(img_byte_arr)

def generate_roast(image: Image, prompt: str) -> str:
    """AI-ക്ക് സ്ക്രീൻഷോട്ട് അയച്ച് റോസ്റ്റ് ഉണ്ടാക്കുന്നു"""
    print("2. നല്ലൊരു റോസ്റ്റ് ആലോചിക്കുന്നു...")
    try:
        response = model.generate_content([prompt, image])
        return response.text.strip().replace('*', '')
    except Exception as e:
        print(f"   An error occurred with the AI call: {e}")
        return "റോസ്റ്റ് ചെയ്യാൻ നോക്കി, പക്ഷെ പണി പാളി. നീ രക്ഷപ്പെട്ടു."

def speak_aloud(text: str):
    """gTTS ഉപയോഗിച്ച് മലയാളം റോസ്റ്റ് ഉറക്കെ പറയുന്നു"""
    if text:
        print(f"3. റോസ്റ്റ് കേട്ടോ: '{text}'")
        try:
            # 1. Google-ലേക്ക് ടെക്സ്റ്റ് അയച്ച് ഓഡിയോ ഉണ്ടാക്കുന്നു
            tts = gTTS(text=text, lang='ml')
            
            # 2. ഓഡിയോ ഒരു താൽക്കാലിക ഫയലായി സേവ് ചെയ്യുന്നു
            audio_file = "roast.mp3"
            tts.save(audio_file)
            
            # 3. ആ ഫയൽ പ്ലേ ചെയ്യുന്നു
            playsound(audio_file)
            
            # 4. പ്ലേ ചെയ്ത ശേഷം ആ ഫയൽ ഡിലീറ്റ് ചെയ്യുന്നു
            os.remove(audio_file)
            
        except Exception as e:
            print(f"--- An error occurred during speech: {e} ---")

# --- MAIN AUTOMATION LOOP ---

def main():
    """ഓട്ടോമേഷൻ ലൂപ്പ് പ്രവർത്തിപ്പിക്കുന്ന പ്രധാന ഫംഗ്ഷൻ"""
    print("\n" + "="*40)
    print("🚀 ഓട്ടോമേറ്റഡ് മലയാളം റോസ്റ്റർ റെഡി! 🚀")
    print(f"ഓരോ {INTERVAL_SECONDS} സെക്കൻഡിലും പുതിയ റോസ്റ്റ് വരും.")
    print("നിർത്താനായി ടെർമിനലിൽ Ctrl+C അമർത്തുക.")
    print("="*40)
    try:
        while True:
            screenshot_image = take_screenshot_in_memory()
            roast_text = generate_roast(screenshot_image, PROMPT)
            speak_aloud(roast_text)
            
            print(f"4. അടുത്ത റോസ്റ്റിനായി {INTERVAL_SECONDS} സെക്കൻഡ് കാത്തിരിക്കുന്നു...")
            time.sleep(INTERVAL_SECONDS)
            print("-" * 20)
    except KeyboardInterrupt:
        print("\n🛑 ചൂട് സഹിക്കാൻ പറ്റുന്നില്ലേ? എന്നാ നിർത്തി.")
    except Exception as e:
        print(f"\nഒരു എറർ സംഭവിച്ചു: {e}")

if __name__ == "__main__":
    main()
