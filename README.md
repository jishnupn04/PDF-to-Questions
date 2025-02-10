# PDF-Based Question Generator Using g4f

This project is a Django-based web application that allows users to upload a PDF containing study material. The application extracts text from the PDF and generates exam questions based on the content using the **g4f** library, which provides access to GPT-4-like AI models.

## 📌 Features
- Upload a PDF containing study material.
- Extract text from the uploaded PDF.
- Generate questions based on the extracted content using AI.
- Specify the number of marks per question.
- JSON API response with generated questions.

## 🛠 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/pdf-question-generator.git
cd pdf-question-generator
```

### 2. Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install Required Libraries
```bash
pip install django fitz g4f
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Start the Development Server
```bash
python manage.py runserver
```

## 🚀 Usage

### Upload a PDF
You can send a `POST` request to:
```
http://127.0.0.1:8000/api/upload_pdf/
```
with a file field named `pdf` and an optional `marks` field.

#### Example Request (Using cURL)
```bash
curl -X POST -F "pdf=@path/to/your/file.pdf" -F "marks=5" http://127.0.0.1:8000/api/upload_pdf/
```

#### Example JSON Response
```json
{
  "questions": "1. Explain the key concepts of AI.\n2. Define Machine Learning with examples."
}
```

## 📜 Code Structure

### 1. Extract Text from PDF
```python
def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using PyMuPDF (fitz)."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text
```

### 2. Generate Questions Using AI (g4f)
```python
def generate_questions_from_text(text, marks=5):
    """Generates questions using the g4f GPT-4-like AI model."""
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Generate {marks}-mark questions from the following content:\n{text}"}],
        web_search=False
    )
    return response.choices[0].message.content.strip()
```

### 3. Django API Endpoint
```python
@csrf_exempt
def upload_pdf(request):
    """Handles PDF uploads and returns AI-generated questions."""
    if request.method == "POST" and request.FILES.get("pdf"):
        pdf = request.FILES["pdf"]
        marks = int(request.POST.get("marks", 5))

        # Save the PDF file locally
        saved_path = f"uploads/{pdf.name}"
        with open(saved_path, "wb") as f:
            for chunk in pdf.chunks():
                f.write(chunk)

        # Extract text and generate questions
        extracted_text = extract_text_from_pdf(saved_path)
        questions = generate_questions_from_text(extracted_text, marks)

        return JsonResponse({"questions": questions})

    return JsonResponse({"error": "Invalid request"}, status=400)
```

## 🎯 Future Enhancements
- Support for different question types (MCQs, short-answer, etc.).
- Option to save generated questions to a database.

## 📜 License
This project is open-source and available under the MIT License.

## 🤝 Contributing
Feel free to fork this repository and submit a pull request with improvements!

