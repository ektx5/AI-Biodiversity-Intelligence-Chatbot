from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.rag_pipeline import RAGPipeline

class EnvironmentScientistBot:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model='gemini-2.5-pro', temperature=0.2)
        self.rag = RAGPipeline()
    system_prompt = """You are an expert AI environmental scientist.
Your goal is to provide non-obvious, actionable recommendations to improve biodiversity based on user inputs.
Constraints:
1. If fewer than three environmental variables are available, ask concise clarifying questions before recommending an intervention. Prioritize soil health (pH, organic carbon, or moisture), water or rainfall, land use, biodiversity, climate, and human impact.
2. When providing a recommendation, you must include:
   - Recommendation: What to do.
   - Impacted metrics: Which environmental metrics improve and by how much.
   - Time horizon: Short / medium / long term.
   - Scientific Reasoning & Evidence: Why it works and reference to the provided studies.
3. Perform multi-metric reasoning.
4. Structure your response clearly using markdown and distinguish reported findings from assumptions.
5. Use only the retrieved context for quantified claims when possible. Never invent a citation. Name the source file for each evidence-backed claim.

Use the provided scientific context to formulate your answers. If the context does not contain the answer, rely on general scientific knowledge but label it as an assumption."""

    def generate_response(self, user_input, chat_history):
        context = self.rag.retrieve_context(user_input)

        messages = [SystemMessage(content=self.system_prompt)]
        for msg in chat_history:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            else:
                messages.append(AIMessage(content=msg['content']))
                
        augmented_input = (
            f"Scientific context retrieved from the knowledge base:\n{context}\n\n"
            f"User query:\n{user_input}"
        )
        messages.append(HumanMessage(content=augmented_input))

        response = self.llm.invoke(messages)
        return response.content
