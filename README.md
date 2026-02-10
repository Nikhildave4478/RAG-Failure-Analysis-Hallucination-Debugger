<h1>🔍 RAG Failure Analysis & Hallucination Debugger</h1>

<p>
An <strong>explainable debugging tool for Retrieval-Augmented Generation (RAG) systems</strong>
that analyzes <em>why</em> answers fail instead of only checking <em>whether</em> they are correct.
</p>

<p>
This project focuses on <strong>hallucinations, conservative refusals, missing context, and injected failures</strong>,
with clear diagnostics and an interactive UI.
</p>

<hr>

<h2>🚀 What This Project Does</h2>

<p>
Unlike typical RAG demos, this tool answers deeper questions:
</p>

<ul>
    <li>Did the model hallucinate?</li>
    <li>Was the retrieved context irrelevant?</li>
    <li>Did the model refuse despite sufficient evidence?</li>
    <li>Was the failure caused by retrieval, context loss, or LLM behavior?</li>
</ul>

<p>
The system <strong>classifies and explains RAG behavior</strong>, not just outputs answers.
</p>

<hr>

<h2>🧠 Key Features</h2>

<ul>
    <li><strong>Modular RAG Pipeline:</strong> Document loading, chunking, vector retrieval, and context-grounded answer generation</li>
    <li><strong>Failure Injection:</strong> Dropping retrieved chunks and truncating context to simulate degraded retrieval</li>
    <li><strong>Grounding-Based Hallucination Detection:</strong> Flags answer sentences unsupported by retrieved context</li>
    <li><strong>Query–Context Relevance Detection:</strong> Distinguishes out-of-scope queries from conservative refusals</li>
    <li><strong>Negation / Contradiction Detection:</strong> Identifies missed answers caused by explicit negative evidence</li>
    <li><strong>Explainable Debugger Output:</strong> Clear PASS / FAIL verdicts with reasons</li>
    <li><strong>Interactive Streamlit UI:</strong> Real-time inspection of answers, context, grounding scores, and failure modes</li>
</ul>

<hr>

<h2>🧪 Example Debugger Outcomes</h2>

<table border="1" cellpadding="8" cellspacing="0">
    <tr>
        <th>Scenario</th>
        <th>Debugger Verdict</th>
    </tr>
    <tr>
        <td>Fully supported answer</td>
        <td>PASS (fully grounded)</td>
    </tr>
    <tr>
        <td>Out-of-scope query</td>
        <td>PASS (correct refusal)</td>
    </tr>
    <tr>
        <td>Missing information</td>
        <td>PASS (conservative refusal)</td>
    </tr>
    <tr>
        <td>Missed negative answer</td>
        <td>PASS (negative evidence present)</td>
    </tr>
    <tr>
        <td>Unsupported claim</td>
        <td>FAIL (hallucination detected)</td>
    </tr>
</table>

<hr>

<h2>🏗️ System Architecture</h2>

<pre>
User Query
   ↓
Document Loader
   ↓
Text Chunking
   ↓
Embedding + Vector Store
   ↓
Retriever
   ↓
(Optional Failure Injection)
   ↓
Context Assembly
   ↓
LLM Answer Generation
   ↓
Debugger Analysis Layer
   ↓
UI + Logs
</pre>

<hr>

<h2>🖥️ UI Preview (What Reviewers See)</h2>

<ul>
    <li>Question input</li>
    <li>Model answer</li>
    <li>Debugger verdict (PASS / FAIL)</li>
    <li>Hallucination flag</li>
    <li>Context relevance and grounding scores</li>
    <li>Retrieved context inspection</li>
    <li>Failure injection controls</li>
</ul>

<hr>

<h2>⚙️ Tech Stack</h2>

<ul>
    <li>Python</li>
    <li>LangChain</li>
    <li>FAISS (Vector Store)</li>
    <li>Local LLM via Ollama</li>
    <li>Streamlit (UI)</li>
</ul>

