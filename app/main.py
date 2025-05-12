from fastapi import FastAPI, HTTPException, Body
from app.models import QuestionRequest, AnswerResponse
from app.retriever import ContentRetriever
from app.generator import AnswerGenerator
import os

app = FastAPI(title="Educational Chatbot API")

# Initialize components
content_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "content.json")
retriever = ContentRetriever(content_path)
generator = AnswerGenerator()


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest = Body(
        example={"question": "فتوسنتز چه نوع فرآیندی است"}
    )
):
    content_data = retriever.get_relevant_content(request.question)

    if not content_data:
        raise HTTPException(status_code=404, detail="No relevant content found")

    answer = generator.generate_answer(request.question, content_data["text"])

    return AnswerResponse(
        question=request.question,
        answer=answer,
        source_passage=content_data["text"]
    )


@app.get("/splash")
async def health_check():
    return {"status": "healthy"}
