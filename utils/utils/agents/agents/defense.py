from utils.llm import call_llm
from utils.semantic_search import SemanticSearch

class DefenseAttorney:
    """Defense Attorney Agent - RUDE & AGGRESSIVE"""

    def __init__(self):
        self.name = 'Defense Attorney'
        self.search = SemanticSearch()

    def build_defense(self, case_query, defendant_statement):
        """Build AGGRESSIVE defense using relevant cases"""
        print('\n🛡️ Defense Attorney Building Case...\n')

        relevant_cases = self.search.find_relevant_cases(
            f"{case_query} defense strategy weakness",
            num_cases=5
        )

        cases_text = "\n\n".join([
            f"[CASE: {case['name']}]\n{case['content']}"
            for case in relevant_cases
        ])

        prompt = f"""You are a RUDE, SARCASTIC, AGGRESSIVE defense attorney. You studied these court cases.

CASES YOU'VE STUDIED:
{cases_text}

DEFEND THIS CASE:
{case_query}
Defendant: {defendant_statement}

Be BRUTAL:
1. Mock the evidence - show contempt
2. Attack weaknesses - expose flaws
3. Defend your client - aggressively
4. Build reasonable doubt
5. Close powerfully

Tone: Rude, Sarcastic, Aggressive
Use: "Are you KIDDING me?", "That's ridiculous!", "Seriously?"

Tear apart the prosecution's case!"""

        try:
            print('📡 Sending to Groq API...\n')
            defense = call_llm(prompt, timeout=180)

            print('✅ Defense Strategy Built\n')
            print('━' * 70)
            print(defense)
            print('━' * 70 + '\n')

            return {
                'agent': self.name,
                'defense': defense,
                'cases_used': len(relevant_cases)
            }
        except Exception as error:
            print(f'❌ Error: {str(error)}')
            raise error
