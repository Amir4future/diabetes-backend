import google.generativeai as genai

# ==========================================
# ⚠️ انسخ مفتاحك من ملف app.py وضعه هنا
# ==========================================
MY_API_KEY = "AIzaSyBLtcrmMJhA4uC7rVsDrr1iGlvmNcFevko"

genai.configure(api_key=MY_API_KEY)

print("🔍 جاري الاتصال بجوجل لجلب قائمة الموديلات المتاحة لك...\n")

try:
    # طلب القائمة من السيرفر
    count = 0
    for model in genai.list_models():
        # نفلتر فقط الموديلات اللي تدعم الشات (توليد النصوص)
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ متاح: {model.name}")
            print(f"   الوصف: {model.description}")
            print("-" * 30)
            count += 1

    if count == 0:
        print("⚠️ لم يتم العثور على موديلات! تأكد من صحة المفتاح.")

except Exception as e:
    print(f"❌ حدث خطأ أثناء الاتصال: {e}")