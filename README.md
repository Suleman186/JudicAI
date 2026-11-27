# AI Courtroom Backend

Multi-agent AI courtroom backend built with Flask. Four AI agents (Evidence Analyzer, Defense Attorney, Prosecutor and Judge) analyze a case using Groq (Llama 3.3 70B) and semantic search over real court cases, then deliver a verdict.

> Educational project. Output is AI-generated and is not legal advice.

## How it works

1. You send a case description and the defendant's statement to the API.
2. Each agent uses sentence-transformer embeddings (`all-MiniLM-L6-v2`) to find the most relevant court cases from `case_data/`.
3. The agents run in this order:
   - **Evidence Analyzer** rates the evidence as strong, moderate or weak and recommends whether to present it.
   - **Defense Attorney** builds an aggressive defense.
   - **Prosecutor** builds the case and rebuts the defense.
   - **Judge** weighs the evidence and defense against precedent and the Constitution, then renders a verdict.
4. The API returns all four outputs as JSON.

## Tech stack

- Python, Flask, Flask-CORS
- Groq API (`llama-3.3-70b-versatile`)
- sentence-transformers, scikit-learn, NumPy

## Project structure

```
ai-courtroom-backend/
├── server.py                  # Flask API
├── requirements.txt
├── .env.example
├── agents/
│   ├── evidence_analyzer.py
│   ├── defense.py
│   ├── prosecutor.py
│   └── judge.py
├── utils/
│   ├── llm.py                 # Groq client
│   └── semantic_search.py     # embedding-based case search
├── tests/
│   └── test_agents.py
└── case_data/                 # .txt court cases and legal documents
```

## Setup

1. Clone the repo and create a virtual environment:

   ```bash
   git clone https://github.com/<your-username>/ai-courtroom-backend.git
   cd ai-courtroom-backend
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add your Groq API key. Get one at https://console.groq.com.

   ```bash
   cp .env.example .env
   ```

   Then edit `.env`:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Make sure `case_data/` contains your `.txt` case files, then start the server from the repo root:

   ```bash
   python server.py
   ```

The server runs on `http://localhost:5000`. The first request is slow because the embedding model downloads on first use.

## API

### `POST /analyze`

Request body:

```json
{
  "case": "Murder case. Fingerprints on weapon, security footage, phone location data.",
  "defendant": "I was home that night with my family."
}
```

Response:

```json
{
  "evidence": "...",
  "prosecution": "...",
  "defense": "...",
  "verdict": "...",
  "cases_used": 5
}
```

`case` is required. Without it the API returns `400`.

### `GET /health`

Returns `{"status": "Backend is running! ✅"}`.

## Example

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"case": "Burglary with CCTV footage and a stolen item found at the suspect home", "defendant": "I bought it from a stranger."}'
```

## Frontend

This repo contains the backend only. CORS is enabled, so any frontend can call the API from any port.

## Tests

```bash
python tests/test_agents.py
```

This calls the real Groq API, so it needs a valid key in `.env`.

## Notes

- Run commands from the repo root. `case_data/` is looked up relative to the current working directory.
- Never commit your `.env` file. It is listed in `.gitignore`.
- Only the first 1,000 characters of each case file are used for search and prompts.

## License

Add a license of your choice (for example MIT).
