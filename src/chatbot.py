import os
from langchain_google_genai import ChatGoogleGenerativeAI
from src.rag_pipeline import RAGPipeline
from langchain.schema import HumanMessage, SystemMessage, AIMessage

class EnvironmentScientistBot:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model='gemini-2.5-pro', temperature=0.2)
        self.rag = RAGPipeline()
        self.system_prompt = \"\"\"You are an expert AI environmental scientist.
Your goal is to provide non-obvious, actionable recommendations to improve biodiversity based on user inputs.
Constraints:
1. If the user input lacks sufficient environmental metrics, you MUST ask clarifying questions to gather at least 3 variables (e.g. soil health, water availability, land use).
2. When providing a recommendation, you must include:
   - Recommendation: What to do.
   - Impacted metrics: Which environmental metrics improve and by how much.
   - Time horizon: Short / medium / long term.
   - Scientific Reasoning & Evidence: Why it works and reference to the provided studies.
3. Perform multi-metric reasoning.
4. Structure your response clearly using markdown.

Use the provided scientific context to formulate your answers. If the context does not contain the answer, rely on your general scientific knowledge but state your assumptions.\"\"\"

    def generate_response(self, user_input, chat_history):
        context = self.rag.retrieve_context(user_input)
        
        messages = [SystemMessage(content=self.system_prompt)]
        for msg in chat_history:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            else:
                messages.append(AIMessage(content=msg['content']))
                
        augmented_input = f"Scientific Context retrieved from knowledge base:\n{context}\n\nUser Query:\n{user_input}"
        messages.append(HumanMessage(content=augmented_input))
        
        response = self.llm.invoke(messages)
        return response.content
