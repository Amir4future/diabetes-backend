import joblib
import os

print("⏳ جاري ضغط الموديل...")

# تحميل الموديل الضخم
model = joblib.load('diabetes_model.pkl')

# حفظه مرة ثانية لكن مع ضغط (Compress)
# هذا بيخلي حجمه يصغر جداً
joblib.dump(model, 'diabetes_model_compressed.pkl', compress=3)

# مقارنة الأحجام
old_size = os.path.getsize('diabetes_model.pkl') / (1024 * 1024)
new_size = os.path.getsize('diabetes_model_compressed.pkl') / (1024 * 1024)

print(f"✅ تم! الحجم القديم: {old_size:.2f} MB")
print(f"🎉 الحجم الجديد: {new_size:.2f} MB")