from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from fastapi.middleware.cors import CORSMiddleware

# Khởi tạo app
app = FastAPI()

# Cho phép gọi API từ giao diện web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lấy API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print("API Key trên server:", OPENROUTER_API_KEY)

# Định nghĩa body
class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Hello, this is your Dental AI Chatbot 🚀 (powered by OpenRouter)"}

@app.post("/ask")
async def ask_question(body: QuestionRequest):
    question = body.question

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-3.5-turbo-1106",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Với vai trò là một bác sĩ chuyên khoa răng hàm mặt chuyên sâu về cấy ghép Implant. "
                        "Với 20 năm kinh nghiệm, bạn rất giỏi nắm bắt tâm lý khách hàng, bạn hãy trả lời chính xác, dễ hiểu về các chủ đề như: thời gian điều trị, quy trình, chi phí trồng Implant, chăm sóc sau cấy ghép. "
                        "Nếu bệnh nhân cần tư vấn thêm, hãy lịch sự mời họ đến phòng khám để thăm khám."
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
