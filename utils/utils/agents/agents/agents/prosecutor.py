from utils.llm import call_llm
from utils.semantic_search import SemanticSearch

class Prosecutor:
    """
    Prosecutor Agent - AGGRESSIVE PROSECUTION
    Builds strong case AGAINST defense arguments
    """

    def __init__(self):
        self.name = 'Prosecutor'
        self.search = SemanticSearch()

    def build_case(self, case_query, defendant_statement, defense_summary=None):
        """Build AGGRESSIVE prosecution case AGAINST defense"""
        print('\n🔨 Prosecutor Building Case...\n')

        relevant_cases = self.search.find_relevant_cases(
            f"{case_query} prosecution charges guilty verdict conviction",
            num_cases=5
        )

        cases_text = "\n\n".join([
            f"[CASE: {case['name']}]\n{case['content']}"
            for case in relevant_cases
        ])

        defense_text = f"\n\nDEFENSE CLAIMS:\n{defense_summary[:400]}\n\n" if defense_summary else ""

        prompt = f"""You are a SKILLED, AGGRESSIVE PROSECUTOR. You studied these REAL court cases and learned how prosecutors WIN cases.

RELEVANT CASES YOU'VE STUDIED:
{cases_text}

NOW PROSECUTE THIS CASE:
{case_query}

Defendant Claims: {defendant_statement}

{defense_text}

Your task - BUILD A WINNING CASE THAT DESTROYS THE DEFENSE:

1. **ESTABLISH GUILT** - Present overwhelming evidence
2. **DESTROY ALIBI** - Challenge defendant's lies
3. **ATTACK DEFENSE** - Prove defense arguments are WRONG
4. **MOTIVE & MEANS** - Show why defendant DID IT
5. **PRECEDENT** - Reference cases you studied
6. **CLOSE POWERFULLY** - Demand guilty verdict

TONE: Professional, Authoritative, Compelling, Confident
Be AGGRESSIVE. Tear apart the defense. Show jury defendant is GUILTY.

Based on cases you studied, build an UNDENIABLE prosecution case!"""

        try:
            print('📡 Sending to Groq API...\n')
            prosecution = call_llm(prompt, timeout=180)

            print('✅ Prosecution Case Built\n')
            print('━' * 70)
            print(prosecution)
            print('━' * 70 + '\n')

            return {
                'agent': self.name,
                'prosecution': prosecution,
                'cases_used': len(relevant_cases)
            }
        except Exception as error:
            print(f'❌ Error: {str(error)}')
            raise error
