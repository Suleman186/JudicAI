import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.evidence_analyzer import EvidenceAnalyzer
from agents.defense import DefenseAttorney

def test_both_agents():
    """Test Evidence Analyzer AND Defense Attorney"""
    case = "Murder investigation with fingerprints on weapon, witness testimony, and phone location data"
    defendant_says = "I was at home that night, I wasn't there"

    analyzer = EvidenceAnalyzer()
    result1 = analyzer.analyze_and_decide(case)

    defense = DefenseAttorney()
    result2 = defense.build_defense(case, defendant_says)

    print(f'Evidence Analyzer used: {result1["cases_used"]} cases')
    print(f'Defense Attorney used: {result2["cases_used"]} cases')

if __name__ == '__main__':
    test_both_agents()
