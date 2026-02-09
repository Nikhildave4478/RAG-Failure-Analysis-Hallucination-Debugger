# rag/debugger.py
import re
STOPWORDS = {
    "what", "is", "a", "an", "the", "do", "does", "are", "of",
    "in", "on", "for", "to", "and", "or", "with", "by"
    }

class RAGDebugger:
    def __init__(
        self,
        grounding_threshold=0.3,
        relevance_threshold=0.2
    ):
        self.grounding_threshold = grounding_threshold
        self.relevance_threshold = relevance_threshold

    def _tokenize(self, text):
        text = text.lower()
        tokens = re.findall(r"\b\w+\b", text.lower())
        return set(t for t in tokens if t not in STOPWORDS)

    def _overlap_score(self, a, b):
        a_tokens = self._tokenize(a)
        b_tokens = self._tokenize(b)

        if not a_tokens:
            return 0.0

        return len(a_tokens.intersection(b_tokens)) / len(a_tokens)

    def analyze(self, query, context, answer, failure_mode=None):
        report = {}

        # Basic flags
        context_empty = len(context.strip()) == 0
        refusal = answer.strip().lower() == "i do not know."

        # Relevance
        relevance_score = self._overlap_score(query, context)
        context_relevant = relevance_score >= self.relevance_threshold

        report["query"] = query
        report["failure_injected"] = failure_mode is not None
        report["context_empty"] = context_empty
        report["context_relevant"] = context_relevant
        report["query_context_relevance"] = round(relevance_score, 2)
        report["model_refusal"] = refusal

        # --- REFUSAL CASES ---
        if refusal:
            report["hallucination"] = False
            report["grounding_score"] = None
            report["unsupported_sentences"] = []

            if context_empty or not context_relevant:
                report["verdict"] = "PASS (correct refusal: out-of-scope)"
            else:
                report["verdict"] = "PASS (conservative refusal)"

            return report

        # --- ANSWERED CASES ---
        sentences = re.split(r"[.\n]", answer)
        unsupported = []
        grounding_scores = []

        for s in sentences:
            s = s.strip()
            if not s:
                continue

            score = self._overlap_score(s, context)
            grounding_scores.append(score)

            if score < self.grounding_threshold:
                unsupported.append({
                    "sentence": s,
                    "grounding_score": round(score, 2)
                })

        avg_grounding = (
            sum(grounding_scores) / len(grounding_scores)
            if grounding_scores else 0.0
        )

        hallucination = len(unsupported) > 0

        report["grounding_score"] = round(avg_grounding, 2)
        report["unsupported_sentences"] = unsupported
        report["hallucination"] = hallucination

        if hallucination:
            report["verdict"] = "FAIL (hallucination detected)"
        else:
            report["verdict"] = "PASS (fully grounded answer)"

        return report
