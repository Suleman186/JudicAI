from utils.llm import call_llm
from utils.semantic_search import SemanticSearch

class Judge:
    """Judge Agent - Makes Fair Verdict"""

    def __init__(self):
        self.name = 'Judge'
        self.search = SemanticSearch()

    def make_verdict(self, case_query, defendant_statement, evidence_summary, defense_summary):
        print('\n⚖️ Judge Examining Evidence...\n')

        relevant_cases = self.search.find_relevant_cases(
            f"{case_query} verdict innocent guilty reasonable doubt constitutional rights",
            num_cases=5
        )

        cases_text = "\n\n".join([
            f"[CASE: {case['name']}]\n{case['content']}"
            for case in relevant_cases
        ])

        prompt = f"""You are a WISE, FAIR JUDGE. You uphold the Constitution and justice. You studied these REAL cases.

RELEVANT CASES YOU'VE STUDIED:
{cases_text}

EXAMINE THIS CASE:
{case_query}

DEFENDANT SAYS: {defendant_statement}

EVIDENCE: {evidence_summary[:300]}...

DEFENSE: {defense_summary[:300]}...

Your task - MAKE A FAIR VERDICT:

1. **EXAMINE EVIDENCE** - Is it reliable?
2. **BEYOND REASONABLE DOUBT** - Guilt proven?
3. **CONSTITUTIONAL RIGHTS** - Fair trial?
4. **APPLY LAW** - Reference precedents
5. **RENDER VERDICT** - GUILTY or NOT GUILTY

TONE: Fair, Judicial, Measured. Base on LAW and EVIDENCE.

Render a FAIR and CONSTITUTIONAL verdict!"""

        try:
            print('📡 Sending to Groq API...\n')
            verdict = call_llm(prompt, timeout=180)

            print('✅ Verdict Rendered\n')
            print('━' * 70)
            print(verdict)
            print('━' * 70 + '\n')

            return {
                'agent': self.name,
                'verdict': verdict,
                'cases_used': len(relevant_cases)
            }
        except Exception as error:
            print(f'❌ Error: {str(error)}')
            raise error
