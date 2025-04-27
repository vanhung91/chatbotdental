from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from fastapi.middleware.cors import CORSMiddleware

# Khởi tạo app
app = FastAPI()

# Cho phép gọi API từ web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lấy API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Định nghĩa body
class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Hello, this is your Dental AI Chatbot 🚀 (powered by OpenRouter)"}

@app.post("/ask")
async def ask_question(body: QuestionRequest):
    question = body.question

    if not OPENROUTER_API_KEY:
        return {"error": "API Key không tồn tại trên server"}

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://yourwebsite.com/",  # Bạn có thể đổi thành website bạn (tạm để vậy cũng được)
            "X-Title": "Dental Chatbot Project"
        }
        payload = {
            "model": "openai/gpt-3.5-turbo-1106",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Bạn là bác sĩ chuyên cấy ghép Implant, hãy trả lời chính xác, dễ hiểu các câu hỏi liên quan đến trồng Implant."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        if 'choices' in response_data:
            answer = response_data['choices'][0]['message']['content']
            return {"answer": answer}
        else:
            error_message = response_data.get('error', {}).get('message', 'Unknown error')
            return {"error": f"Lỗi từ OpenRouter: {error_message}"}

    except Exception as e:
        return {"error": str(e)}
