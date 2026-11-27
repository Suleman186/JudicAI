from sentence_transformers import SentenceTransformer
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticSearch:
    """Find relevant cases using Hugging Face embeddings"""

    def __init__(self):
        print('📥 Loading Hugging Face model...')
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.case_data_path = Path.cwd() / "case_data"
        print('✅ Model loaded\n')

    def load_all_cases(self):
        """Load all case files"""
        cases = {}
        files = sorted(list(self.case_data_path.glob('*.txt')))

        for file in files:
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    cases[file.name] = content[:1000]  # First 1000 chars
            except:
                pass

        return cases

    def find_relevant_cases(self, query, num_cases=5):
        """
        Find the most relevant cases for a query

        Args:
            query: What to search for (e.g., "murder with evidence")
            num_cases: How many cases to return (default 5)

        Returns:
            List of relevant case contents
        """
        print('🔍 Searching for relevant cases...\n')

        all_cases = self.load_all_cases()

        if not all_cases:
            print('⚠️  No cases found!')
            return []

        query_embedding = self.model.encode(query)

        case_texts = list(all_cases.values())
        case_names = list(all_cases.keys())

        print(f'📊 Encoding {len(case_texts)} cases...')
        case_embeddings = self.model.encode(case_texts)

        similarities = cosine_similarity([query_embedding], case_embeddings)[0]

        top_indices = np.argsort(similarities)[-num_cases:][::-1]

        relevant_cases = []
        for idx in top_indices:
            relevant_cases.append({
                'name': case_names[idx],
                'content': case_texts[idx],
                'similarity': float(similarities[idx])
            })

        print(f'✅ Found {len(relevant_cases)} relevant cases\n')

        return relevant_cases
