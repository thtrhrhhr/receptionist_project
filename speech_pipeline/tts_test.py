import asyncio
import os
import edge_tts
import pygame
import time

# تهيئة مشغل الصوت الداخلي
pygame.mixer.init()

VOICES = {
    "ar": "ar-EG-ShakirNeural",
    "en": "en-US-GuyNeural",
    "ja": "ja-JP-KeitaNeural"
}

async def speak(text: str, lang: str = "ar"):
    voice = VOICES.get(lang, "en-US-GuyNeural")
    output_file = f"tts_output_{lang}.mp3"
    
    print(f"\nجاري توليد الصوت [{lang}]...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    
    print(f"جاري تشغيل الصوت عبر السماعات...")
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    
    # الانتظار حتى ينتهي نطق الجملة بالكامل
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        
    pygame.mixer.music.unload()
    
    if os.path.exists(output_file):
        os.remove(output_file)

async def main():
    print("--- اختبار نطق الردود للغات الثلاث ---")
    
    # 1. العربية
    await speak("أهلاً بك يا يوسف، أنا روبوت الاستقبال وجاهز لمساعدتك اليوم.", "ar")
    
    # 2. الإنجليزية
    await speak("Welcome! I can guide you to the robotics laboratory and offices.", "en")
    
    # 3. اليابانية
    await speak("こんにちは！ご案内いたします。", "ja")
    
    print("\nاكتمل نطق اللغات الثلاث بنجاح!")

if __name__ == "__main__":
    asyncio.run(main())
