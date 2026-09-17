# Darukaa.Earth: AI Biodiversity Intelligence Chatbot

An AI-powered conversational system that acts as an environmental scientist, providing evidence-backed, multi-metric recommendations to improve biodiversity.

## Architecture

The system uses a Retrieval-Augmented Generation (RAG) pipeline:
- **Frontend / UI:** Streamlit with natural-language and structured JSON input.
- **LLM Engine:** Google Gemini (`gemini-3.1-pro-preview`) via LangChain.
- **Knowledge Base:** FAISS vector database.
- **Embeddings:** HuggingFace `sentence-transformers/all-MiniLM-L6-v2`.

The main modules are:
- `data/`: Raw scientific text documents based on FAO, IPCC, and biodiversity reports.
- `src/knowledge_base.py`: Chunks documents, creates embeddings, and builds the FAISS index.
- `src/rag_pipeline.py`: Retrieves relevant evidence for each user query.
- `src/chatbot.py`: Combines retrieved evidence, conversation history, and Gemini reasoning.
- `app.py`: Streamlit application entry point.

## Knowledge Base

FAISS stores dense vectors for document chunks and retains the original text and source metadata. The source documents cover soil health, land use, biodiversity indicators, climate, water availability, pollution, and deforestation.

## Local Setup

### Prerequisites

- Python 3.9+
- A Gemini API key with available quota

### Installation and Execution

1. Clone the repository:
   ```bash
   git clone https://github.com/ektx5/AI-Biodiversity-Intelligence-Chatbot.git
   cd AI-Biodiversity-Intelligence-Chatbot
   ```

2. Create a virtual environment and install dependencies in PowerShell:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Create `.env` from the template:
   ```powershell
   Copy-Item .env.example .env
   ```
   Open `.env` and replace the placeholder:
   ```text
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. Build the local knowledge base:
   ```powershell
   python src/knowledge_base.py
   ```

5. Start the application:
   ```powershell
   streamlit run app.py
   ```

6. Open http://localhost:8501 in your browser.

### Gemini API quota limitation

The free Gemini API tier may not be sufficient for this application. Requests can consume the available quota or trigger rate limits before the model returns a result, especially with larger conversation histories and repeated tests.