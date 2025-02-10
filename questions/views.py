import fitz  # PyMuPDF
from g4f.client import Client
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Initialize GPT-4 client (g4f)
client = Client()

def extract_text_from_pdf(pdf_path):
    """Extracts text from the uploaded PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

def generate_questions_from_text(text, marks=5):
    """Generate questions based on extracted text using GPT-4."""
    prompt = f"Generate {marks}-mark questions from the following content:\n{text}"

    # Using g4f's client to call GPT-4 and generate questions
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or any smaller model for faster response like gpt-4-mini
        messages=[{"role": "Teacher", "content": prompt}],
        web_search=False
    )

    # Return the generated questions
    return response.choices[0].message.content.strip()

@csrf_exempt
def upload_pdf(request):
    """Handles PDF upload, extracts text, and generates questions."""
    if request.method == "POST" and request.FILES.get("pdf"):
        pdf = request.FILES["pdf"]
        marks = int(request.POST.get("marks", 5))  # Default to 5 marks

        # Save the PDF file (can use Django's storage system or local storage)
        saved_path = f"uploads/{pdf.name}"
        with open(saved_path, "wb") as f:
            for chunk in pdf.chunks():
                f.write(chunk)

        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(saved_path)

        # Generate questions based on the extracted text
        questions = generate_questions_from_text(extracted_text, marks)

        # Return the generated questions as a response
        return JsonResponse({"questions": questions})

    return JsonResponse({"error": "Invalid request"}, status=400)
