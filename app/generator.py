from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch


class AnswerGenerator:
    def __init__(self, model_name="mrm8488/bert-multi-cased-finetuned-xquadv1"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    def generate_answer(self, question, context):
        # If context is too long, use only the first 512 tokens
        inputs = self.tokenizer(question, context, return_tensors="pt", max_length=512, truncation=True)

        with torch.no_grad():
            outputs = self.model(**inputs)

        # Get answer span
        answer_start = torch.argmax(outputs.start_logits)
        answer_end = torch.argmax(outputs.end_logits) + 1

        # Convert to answer text
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        answer = self.tokenizer.convert_tokens_to_string(tokens[answer_start:answer_end])

        # Clean up answer
        answer = answer.replace("[CLS]", "").replace("[SEP]", "").strip()

        # If no good answer found, provide a simple response
        if not answer or answer == "":
            keywords = question.lower().split()
            sentences = context.split(". ")
            relevant_sentences = []

            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in keywords):
                    relevant_sentences.append(sentence)

            if relevant_sentences:
                answer = ". ".join(relevant_sentences[:2]) + "."
            else:
                answer = "Unfortunately, no clear answer was found for this question."

        return answer
