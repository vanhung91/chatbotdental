from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Định nghĩa body nhận question
class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Hello, this is your Dental AI Chatbot 🚀 (powered by OpenAI)"}

@app.post("/ask")
async def ask_question(body: QuestionRequest):
    question = body.question

    if not OPENAI_API_KEY:
        return {"error": "API Key không tồn tại trên server"}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "Bạn là bác sĩ chuyên khoa cấy ghép Implant, với 20 năm kinh nghiệm. "
                    "Trả lời dễ hiểu, chính xác các câu hỏi liên quan đến quy trình, chi phí, chăm sóc sau trồng Implant."
                )},
                {"role": "user", "content": question}
            ]
        )

        answer = response['choices'][0]['message']['content']
        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}
