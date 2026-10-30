import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import os
import time

SAMPLE_RATE = 16000
DURATION = 15  # مدة التسجيل 15 ثانية
AUDIO_FILE = "test_audio.wav"

print("جاري تحميل النموذج...")
model = WhisperModel("small", device="cpu", compute_type="int8")

print("\nاستعد...")
time.sleep(1)
print(f" تحدث الآن بطلاقة (عربي، English، 日本語 أو كلاهما معاً)... [معك {DURATION} ثانية]")

recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
sd.wait()
write(AUDIO_FILE, SAMPLE_RATE, recording)
print(" انتهى التسجيل! جاري المعالجة وتفريغ اللغات المتعددة...")

# برومبت يدمج اللغات الثلاث لتعليم النموذج كيفية التعامل مع التبديل بينها
multilingual_prompt = "مرحباً بكم. Hello and welcome. こんにちは。 How can I help you? أين يقع المعمل؟"

# تشغيل التفريغ بدون تثبيت لغة محددة (language=None) للسماح بنقل الكلام تلقائياً لكل مقطع
segments, info = model.transcribe(
    AUDIO_FILE,
    beam_size=5,
    initial_prompt=multilingual_prompt,
    vad_filter=True  # فلتر لتجاهل فترات الصمت وتحسين دقة التقاط الكلمات
)

print(f"\n اللغة الأساسية السائدة في البداية: {info.language}")
print(" النص المكتشف عبر المقاطع:")

full_result = []
for segment in segments:
    segment_text = segment.text.strip()
    full_result.append(segment_text)
    print(f"[{segment.start:.1f}s -> {segment.end:.1f}s] {segment_text}")

print("\n النص الكامل المجمع:")
print(f"-> {' '.join(full_result)}")

if os.path.exists(AUDIO_FILE):
    os.remove(AUDIO_FILE)
