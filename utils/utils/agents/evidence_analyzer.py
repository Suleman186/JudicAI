from utils.llm import call_llm
from utils.semantic_search import SemanticSearch

class EvidenceAnalyzer:
    """
    Evidence Analyzer Agent
    Finds relevant cases, then analyzes the evidence
    """

    def __init__(self):
        self.name = 'Evidence Analyzer'
        self.search = SemanticSearch()

    def analyze_and_decide(self, case_query):
        print('\n🔍 Evidence Analyzer Starting...\n')

        relevant_cases = self.search.find_relevant_cases(
            f"{case_query} evidence analysis",
            num_cases=5
        )

        cases_text = "\n\n".join([
            f"[CASE: {case['name']} - Relevance: {case['similarity']:.2f}]\n{case['content']}"
            for case in relevant_cases
        ])

        prompt = f"""You are a legal evidence analyst. You have studied the following RELEVANT court cases and learned how to analyze evidence.

RELEVANT CASES YOU'VE STUDIED:
{cases_text}

NOW ANALYZE THIS NEW CASE:
{case_query}

Based on what you learned from these cases, determine:

1. **EVIDENCE ANALYSIS** - What evidence is presented?
2. **STRENGTH RATING** - Rate each as STRONG, MODERATE, or WEAK
3. **RECOMMENDATION** - Should this evidence be PRESENTED or DON'T PRESENT?
4. **REASONING** - Explain using principles from the cases you studied

Be thorough and reference patterns from the cases."""

        try:
            print('📡 Sending to Groq API...\n')
            analysis = call_llm(prompt, timeout=180)

            print('✅ Analysis Complete\n')
            print('━' * 70)
            print(analysis)
            print('━' * 70 + '\n')

            return {
                'agent': self.name,
                'analysis': analysis,
                'cases_used': len(relevant_cases)
            }
        except Exception as error:
            print(f'❌ Error: {str(error)}')
            raise error
