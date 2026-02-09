# rag/pipeline.py
import json
import os
from datetime import datetime

from rag.loader import load_documents
from rag.chunker import chunk_documents
from rag.vectorstore import build_vectorstore
from rag.retriever import get_retriever
from rag.generator import get_llm, get_prompt
from config import LOG_DIR

from rag.failure_injector import FailureInjector

class RAGPipeline:
    def __init__(self, doc_path, failure_mode=None):
        self.documents = load_documents(doc_path)
        self.chunks = chunk_documents(self.documents)
        self.vectorstore = build_vectorstore(self.chunks)
        self.retriever = get_retriever(self.vectorstore)
        
        self.failure_injector = FailureInjector(failure_mode)

        self.llm = get_llm()
        self.prompt = get_prompt()

    def run(self, query: str):
        retrieved_docs = self.retriever.invoke(query)

        # 💥 FAILURE INJECTION HERE
        retrieved_docs = self.failure_injector.apply(retrieved_docs)


        context = "\n\n".join([d.page_content for d in retrieved_docs])
        prompt_text = self.prompt.format(
            context=context,
            question=query
        )

        answer = self.llm.invoke(prompt_text)

        log = {
            "query": query,
            "retrieved_chunks": [
                {
                    "content": d.page_content,
                    "metadata": d.metadata
                } for d in retrieved_docs
            ],
            "prompt": prompt_text,
            "answer": answer,
            "timestamp": datetime.utcnow().isoformat()
        }

        self._save_log(log)
        return answer, context

    def _save_log(self, log):
        os.makedirs(LOG_DIR, exist_ok=True)
        filename = f"{LOG_DIR}/run_{datetime.utcnow().timestamp()}.json"
        with open(filename, "w") as f:
            json.dump(log, f, indent=2)
