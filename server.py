from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.evidence_analyzer import EvidenceAnalyzer
from agents.defense import DefenseAttorney
from agents.prosecutor import Prosecutor
from agents.judge import Judge

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_case():
    """Analyze a case with all 4 agents"""
    try:
        data = request.json
        case = data.get('case')
        defendant = data.get('defendant', '')

        if not case:
            return jsonify({'error': 'Case details required'}), 400

        print('\n' + '='*70)
        print('🚀 ANALYZING CASE WITH ALL AGENTS')
        print('='*70)

        # Run Evidence Analyzer
        print('\n📊 Running Evidence Analyzer...')
        analyzer = EvidenceAnalyzer()
        evidence_result = analyzer.analyze_and_decide(case)

        # Run Defense Attorney
        print('\n🛡️ Running Defense Attorney...')
        defense = DefenseAttorney()
        defense_result = defense.build_defense(case, defendant)

        # Run Prosecutor (WITH defense summary)
        print('\n🔨 Running Prosecutor...')
        prosecutor = Prosecutor()
        prosecution_result = prosecutor.build_case(case, defendant, defense_result['defense'])

        # Run Judge (WITH both sides)
        print('\n⚖️ Running Judge...')
        judge = Judge()
        verdict_result = judge.make_verdict(
            case,
            defendant,
            evidence_result['analysis'],
            defense_result['defense']
        )

        return jsonify({
            'evidence': evidence_result['analysis'],
            'prosecution': prosecution_result['prosecution'],
            'defense': defense_result['defense'],
            'verdict': verdict_result['verdict'],
            'cases_used': evidence_result['cases_used']
        })

    except Exception as error:
        print(f'❌ Error: {str(error)}')
        return jsonify({'error': str(error)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'Backend is running! ✅'})

if __name__ == '__main__':
    print('\n' + '='*70)
    print('🚀 AI COURTROOM BACKEND STARTING')
    print('='*70)
    print('\n✅ Server running on http://localhost:5000\n')
    app.run(debug=True, port=5000)
