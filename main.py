from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

class LoginData(BaseModel):
    student_id: str
    password: str
    grade: str
    language: str

@app.post("/api/solve")
async def solve_platform(data: LoginData):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    })
    
    # تجربة الدخول على المنصة
    login_url = "https://me-tp.qureo.education/oauth2/password-login"
    payload = {"student_id": data.student_id, "password": data.password}
    
    try:
        res = session.post(login_url, json=payload)
        
        if res.status_code == 401 or res.status_code == 400:
            return {"status": "error", "message": "رقم الطالب أو كلمة المرور غير صحيحة."}

        # هنا بيتم الاتصال بنجاح
        return {
            "status": "success", 
            "message": "تم الاتصال بالمنصة بنجاح!",
            "details": f"السيرفر جاهز لحل التمارين لسنة {data.grade} في لغة {data.language}. (جاري ربط الحل الفعلي)"
        }
    except Exception as e:
        return {"status": "error", "message": f"حدث خطأ: {str(e)}"}
