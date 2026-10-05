# FRAUDPROBE AI
### AI-Powered Credit Card Fraud Detection & Risk Intelligence Platform

FRAUDPROBE AI is a B.Tech major-project prototype for transaction fraud detection, risk prioritization, batch screening and investigation workflows.

## What is included
- ML training pipeline using `HistGradientBoostingClassifier`
- Imbalanced-fraud-aware threshold selection using F1 optimization
- Individual transaction prediction
- Chunked large-CSV batch scoring
- Risk score + transparent risk bands
- Investigation case workflow
- Role/workspace simulation
- Analytics dashboard
- CSV/JSON exports
- Premium green Figma-inspired UI with custom CSS and motion
- Unit tests
- GitHub / Streamlit Community Cloud deployment structure

## Dataset
Do **not** commit a 1 GB dataset to GitHub. Put your dataset locally under:
`data/creditcard.csv`

The classic benchmark schema is:
`Time, V1...V28, Amount, Class`

The app can also use other numeric fraud datasets after adapting the data loader/target mapping.

## Local setup (Windows / VS Code)
```powershell
cd FRAUDPROBE_AI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts\train_model.py --data data/creditcard.csv
streamlit run app.py
```

For a quick demo without downloading a real dataset:
```powershell
python scripts\generate_demo_data.py
python scripts\train_model.py --data data/demo_transactions.csv
streamlit run app.py
```

## Tests
```powershell
pytest -q
```

## GitHub
```powershell
git init
git add .
git commit -m "feat: initial FRAUDPROBE AI prototype"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/fraudprobe-ai.git
git push -u origin main
```

Keep raw datasets and trained model binaries out of Git unless you intentionally use Git LFS/object storage.

## Streamlit deployment
Create the GitHub repo, push the project, connect GitHub to Streamlit Community Cloud, choose the repo/branch and `app.py`, then deploy.

For cloud demos where a trained artifact is too large, train a compact model locally and either:
1. commit a small approved artifact, or
2. add a cloud-safe training/bootstrap strategy.

## Major-project architecture
```text
                    ┌─────────────────────────┐
                    │      Streamlit UI       │
                    │ Dashboard / Probe / CSV │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      Data Adapter        │
                    │ validation / chunking    │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      ML Risk Engine      │
                    │ classifier + probability │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      Risk Layer          │
                    │ score / bands / alerts   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │ Investigation & Export   │
                    └─────────────────────────┘
```

## Important academic limitation
This prototype is suitable for demonstration and academic evaluation. It is not a production banking authorization system. Production deployment would require secure identity, persistent database storage, model monitoring, concept-drift detection, calibration, audit logs, privacy controls, PCI/security review and independent validation.
