# Educational Chatbot

A simple backend service that can answer educational questions based on provided content using natural language processing techniques.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![Transformers](https://img.shields.io/badge/Transformers-4.34.1-orange)

## 📋 Table of Contents

- [Installation](#installation)
  - [Local Installation](#local-installation)
  - [Docker Installation](#docker-installation)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
- [Adding Educational Content](#adding-educational-content)
- [How It Works](#how-it-works)


## 🚀 Installation

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/educational-chatbot.git
   cd educational-chatbot
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API**
   - The API will be available at http://localhost:8000
   - Interactive documentation is available at http://localhost:8000/docs

### Docker Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/amir-esmaeili/educational-chatbot.git
   cd educational-chatbot
   ```

2. **Build the Docker image**
   ```bash
   docker build -t educational-chatbot .
   ```

3. **Run the Docker container**
   ```bash
   # On Linux/macOS
   docker run -p 8000:8000 -v $(pwd)/data:/app/data educational-chatbot
   
   # On Windows Command Prompt
   docker run -p 8000:8000 -v %cd%/data:/app/data educational-chatbot
   
   # On Windows PowerShell
   docker run -p 8000:8000 -v ${PWD}/data:/app/data educational-chatbot
   ```

4. **Access the API**
   - The API will be available at http://localhost:8000
   - Interactive documentation is available at http://localhost:8000/docs

## 📝 Usage

### API Endpoints

| Endpoint  | Method | Description |
|-----------|--------|-------------|
| `/ask`    | POST | Submit a question and get an answer |
| `/splash` | GET | Check if the service is running |


## 📚 Adding Educational Content

Educational content is stored in the `data/content.json` file in the following format:

```json
[
  {
    "id": 1,
    "title": "سلول‌های گیاهی",
    "content": "سلول‌های گیاهی واحدهای ساختاری و عملکردی گیاهان هستند. این سلول‌ها دارای دیواره سلولی، کلروپلاست و واکوئل مرکزی هستند که آنها را از سلول‌های جانوری متمایز می‌کند. دیواره سلولی به سلول استحکام می‌دهد و کلروپلاست‌ها محل انجام فتوسنتز هستند. فتوسنتز فرآیندی است که در آن گیاهان با استفاده از انرژی نور خورشید، آب و دی‌اکسید کربن را به قند و اکسیژن تبدیل می‌کنند."
  },
  {
    "id": 2,
    "title": "فتوسنتز",
    "content": "فتوسنتز فرآیندی بیوشیمیایی است که طی آن گیاهان، جلبک‌ها و برخی باکتری‌ها انرژی نور خورشید را به انرژی شیمیایی تبدیل می‌کنند. این فرآیند در کلروپلاست‌ها انجام می‌شود و شامل دو مرحله اصلی است: واکنش‌های نوری و چرخه کالوین. در واکنش‌های نوری، انرژی نور خورشید جذب و به ATP و NADPH تبدیل می‌شود. در چرخه کالوین، از این انرژی برای تثبیت کربن و تولید قندها استفاده می‌شود."
  }
]
```

To add more content:

1. Open `data/content.json`
2. Add new entries following the same format
3. Make sure the file is saved with UTF-8 encoding
4. Restart the application to load the new content

## ⚙️ How It Works

The chatbot works in three main steps:

1. **Content Embedding**: Educational content is split into chunks and converted into vector embeddings using a multilingual sentence transformer model.

2. **Retrieval**: When a question is received, it is also converted to a vector embedding and compared with the content embeddings to find the most relevant passages.

3. **Answer Generation**: The relevant passages are used as context to generate an appropriate answer to the question using a transformer-based model.

### Component Details

- **ContentEmbedder**: Handles loading content and creating vector embeddings
- **ContentRetriever**: Finds relevant content for a given query
- **AnswerGenerator**: Generates answers based on the question and relevant content
- **FastAPI Application**: Provides the HTTP interface for the chatbot

### Logs

To see detailed logs:

```bash
# When running with uvicorn
uvicorn app.main:app --reload --log-level debug

# When running with Docker
docker run -p 8000:8000 educational-chatbot uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level debug
```