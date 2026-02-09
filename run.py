from rag.pipeline import RAGPipeline
from rag.debugger import RAGDebugger

pipeline = RAGPipeline("data/documents.txt")
debugger = RAGDebugger()

questions = [
    "What payment methods are supported in online shopping?",
    "What is a cookie?",
    "Do online shopping platforms manufacture products?",
    "Do online shopping platforms guarantee product quality?"
]

for q in questions:
    answer, context = pipeline.run(q)
    report = debugger.analyze(
        query=q,
        context=context,
        answer=answer,
        failure_mode=None
    )

    print("\n===== DEBUGGER REPORT =====")
    print("Query:", q)
    print("Answer:", answer)
    for k, v in report.items():
        if k not in ["query"]:
            print(f"{k}: {v}")
    print("==========================")
