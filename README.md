# Darukaa.Earth: AI Biodiversity Intelligence Chatbot

An AI-powered conversational system that acts as an environmental scientist, providing evidence-backed, multi-metric recommendations to improve biodiversity.

## Architecture

The system is built using a modern RAG (Retrieval-Augmented Generation) pipeline:
- **Frontend / UI:** Streamlit (for both natural language and structured JSON input).
- **LLM Engine:** Google Gemini (gemini-2.5-pro via LangChain) for deep scientific reasoning.
- **Knowledge Base (Vector DB):** FAISS (Facebook AI Similarity Search).
- **Embeddings:** HuggingFace sentence-transformers/all-MiniLM-L6-v2.

The architecture follows a modular design:
- data/: Contains raw scientific text data simulating FAO and IPCC reports.
- src/knowledge_base.py: Ingests documents, chunks them, generates embeddings, and saves to the FAISS index.
- src/rag_pipeline.py: Loads the local FAISS index and handles similarity search based on user queries.
- src/chatbot.py: Orchestrates the LLM, injects the retrieved scientific context, enforces conversational constraints (like asking clarifying questions if metrics are missing), and structures the multi-metric reasoning.
- pp.py: The main Streamlit entry point.

## Database / Schema

We use **FAISS** as a local vector database.
- **Data Source:** Text documents in the data/ directory.
- **Chunking Strategy:** 500 characters with a 50-character overlap (using RecursiveCharacterTextSplitter).
- **Schema:** The vector store retains the original text page_content and metadata (source file). It stores dense vectors representing the semantic meaning of the text.

## Local Setup

### Prerequisites
- Python 3.9+
- A Google Gemini API Key

### Installation

1. Clone the repository:
   `ash
   git clone <your-repo-link>
   cd AI-Biodiversity-Intelligence-Chatbot
   `

2. Create a virtual environment and install dependencies:
   `ash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   `

3. Setup Environment Variables:
   Copy .env.example to .env and add your Gemini API key.
   `
   GEMINI_API_KEY=your_gemini_api_key_here
   `

4. Build the Knowledge Base:
   This step parses the documents and creates the local FAISS vector store.
   `ash
   python src/knowledge_base.py
   `

5. Run the Application:
   `ash
   streamlit run app.py
   `

## CI/CD Details

For continuous integration and deployment, you can use GitHub Actions to deploy to **Streamlit Community Cloud** or **Render**.
1. **CI Pipeline:** A GitHub Action can be set up to run pytest (if tests are added) and lake8 for linting on every push to the main branch.
2. **CD Pipeline:** To deploy to Streamlit Community Cloud:
   - Connect the GitHub repository to your Streamlit account.
   - Set the main file path to pp.py.
   - Add the GEMINI_API_KEY to the Streamlit Advanced Settings (Secrets management).
   - Any push to the main branch will automatically trigger a redeploy of the application.
