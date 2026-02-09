# ui.py
import streamlit as st

from rag.pipeline import RAGPipeline
from rag.debugger import RAGDebugger

st.set_page_config(
    page_title="RAG Failure Analysis & Hallucination Debugger",
    layout="wide"
)

st.title("🔍 RAG Failure Analysis & Hallucination Debugger")
st.markdown(
    """
    This tool intentionally analyzes **why a RAG system succeeds or fails**.
    It detects hallucinations, conservative refusals, out-of-scope queries,
    and missed answers caused by negation.
    """
)

# ---------------- Sidebar ----------------
st.sidebar.header("⚙️ Configuration")

failure_mode = st.sidebar.selectbox(
    "Failure Injection Mode",
    options=[None, "drop_chunks", "truncate_context"],
    help="Inject failures to test RAG robustness"
)

doc_path = "data/documents.txt"

# Initialize pipeline & debugger
pipeline = RAGPipeline(doc_path, failure_mode=failure_mode)
debugger = RAGDebugger()

# ---------------- Main UI ----------------
st.subheader("📝 Ask a Question")

query = st.text_input(
    "Enter your question",
    placeholder="e.g. Do online shopping platforms manufacture products?"
)

if st.button("Run Debugger") and query.strip():

    with st.spinner("Running RAG pipeline..."):
        answer, context = pipeline.run(query)

        report = debugger.analyze(
            query=query,
            context=context,
            answer=answer,
            failure_mode=failure_mode
        )

    # ---------------- Results ----------------
    st.subheader("🤖 Model Answer")
    st.success(answer)

    # Verdict
    verdict = report.get("verdict", "UNKNOWN")
    hallucination = report.get("hallucination", False)

    if "FAIL" in verdict:
        st.error(f"❌ {verdict}")
    else:
        st.info(f"✅ {verdict}")

    # ---------------- Debugger Report ----------------
    st.subheader("🧠 Debugger Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Context Relevant",
        report.get("context_relevant", False)
    )

    col2.metric(
        "Grounding Score",
        report.get("grounding_score", "N/A")
    )

    col3.metric(
        "Hallucination",
        hallucination
    )

    # Extra flags
    st.markdown("### 🔎 Detailed Flags")
    st.json(report)

    # ---------------- Context Viewer ----------------
    with st.expander("📄 Retrieved Context"):
        if context.strip():
            st.write(context)
        else:
            st.warning("No context retrieved")

else:
    st.info("Enter a question and click **Run Debugger**.")
