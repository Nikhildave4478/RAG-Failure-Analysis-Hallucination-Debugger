# rag/generator.py
#pip install langchain-ollama langchain-community

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from config import TEMPERATURE

def get_llm():
    return Ollama(
        model="llama3",
        temperature=TEMPERATURE
    )

def get_prompt():
    return PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a strict QA system.\n"
            "Answer ONLY using the context below.\n"
            "If the answer is not in the context, say: "
            "'I do not know.'\n\n"
            "Context:\n{context}\n\n"
            "Question:\n{question}\n\n"
            "Answer:"
        )
    )
