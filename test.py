import requests
import json

url = "http://127.0.0.1:5000/chat"

payload = {
    "message": "مرحبا دكتور، أنا أحس بدوخة خفيفة",
    "context": {
        "name": "فيصل",
        "diabetes_type": "Type 1",
        "current_glucose": 85,
        "last_meal": "قبل ساعتين"
    }
}

try:
    print("⏳ جاري الاتصال...")
    response = requests.post(url, json=payload)
    
    data = response.json()
    
    print("\n📩 الرد من السيرفر:")
    print("-" * 30)
    print("الرد للمستخدم:", data.get('reply'))
    
    # هنا السحر: طباعة الخطأ الحقيقي إذا وجد
    if 'error' in data:
        print("\n🚨 تفاصيل الخطأ التقني (المهم):")
        print(data['error'])
    print("-" * 30)

except Exception as e:
    print("خطأ في الاتصال:", e)