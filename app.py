from flask import Flask, request, jsonify
import joblib
import google.generativeai as genai
import os

app = Flask(__name__)

# ==========================================
# 1. التجهيز (Load Brain & Voice)
# ==========================================
# تحميل موديل الذكاء الاصطناعي (تأكد أن الملف بجانب الكود)
model = joblib.load('diabetes_model_compressed.pkl')

# إعداد مفتاح Gemini

# بدلاً من وضع المفتاح مباشرة، نقرأه من متغيرات النظام
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
chat_model = genai.GenerativeModel('gemini-flash-latest')

# خرائط التحويل (لأن الموديل لا يفهم النصوص)
gender_map = {"Female": 0, "Male": 1, "Other": 2}
smoking_map = {
    "No Info": 0, "current": 1, "ever": 2, 
    "former": 3, "never": 4, "not current": 5
}

# ==========================================
# 2. نقطة الفحص (Predict Logic)
# ==========================================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # تجميع الـ 8 متغيرات الضرورية للموديل
        # المنطق: التطبيق يجمعها ويرسلها دفعة واحدة
        features = [
            gender_map.get(data.get('gender'), 0), # الجنس
            float(data.get('age')),                # العمر (محسوب في التطبيق)
            int(data.get('hypertension')),         # ضغط (0 أو 1)
            int(data.get('heart_disease')),        # قلب (0 أو 1)
            smoking_map.get(data.get('smoking_history'), 0), # التدخين
            float(data.get('bmi')),                # كتلة الجسم
            float(data.get('hba1c')),              # التراكمي
            float(data.get('glucose'))             # السكر العشوائي
        ]
        
        # سؤال الموديل
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0][1]

        # إرجاع النتيجة
        return jsonify({
            "status": "success",
            "is_diabetic": int(prediction),
            "risk_score": round(probability * 100, 2),
            "message": "تم التحليل بنجاح"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# ==========================================
# 3. نقطة الشات الذكي (Chat Logic)
# ==========================================

@app.route('/')
def home():
    return "✅ Server is Running! Diabetes AI API is ready."


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get('message')
        
        # استقبال سياق المريض (Context)
        # المنطق: نستقبل أي بيانات متوفرة عن المريض
        ctx = data.get('context', {})
        
        # استخراج البيانات (مع قيم افتراضية إذا كانت ناقصة)
        name = ctx.get('name', 'المستخدم')
        glucose = ctx.get('current_glucose', 'غير متوفر')
        last_meal = ctx.get('last_meal', 'غير معروف')
        diab_type = ctx.get('diabetes_type', 'غير محدد')


        # هندسة الملقن (System Prompt) - نسخة ثنائية اللغة
        system_instruction = f"""
        Act as a smart and empathetic diabetes doctor.
        
        [Patient Context]
        - Name: {name}
        - Diabetes Type: {diab_type}
        - Current Glucose: {glucose}
        - Last Meal: {last_meal}
        
        [Instructions]
        1. If the user asks in Arabic, answer in Arabic. If in English, answer in English.
        2. Analyze the glucose level ({glucose}). If it is dangerous (>250 or <70), start with a clear warning.
        3. Keep your response concise (max 3 sentences) unless asked for details.
        4. Be supportive and friendly.
        
        Patient's Question: {user_msg}
        """
        
        response = chat_model.generate_content(system_instruction)
        
        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        return jsonify({"reply": "عذراً، حدث خطأ في النظام الطبي.", "error": str(e)})

if __name__ == '__main__':
    # تشغيل السيرفر محلياً

    app.run(host='0.0.0.0', port=5000, debug=True)

