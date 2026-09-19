# zilliz_demo

Secure Python + PyMilvus example for a Zilliz/Milvus workflow.

## Flow

1. Load configuration from environment variables.
2. Connect with `MILVUS_URI` + `MILVUS_TOKEN`.
3. Ensure database `demo_db`.
4. Ensure collection `products`.
5. Insert sample products.
6. Run vector search.
7. Extend with filters, query, delete, and teardown as needed.

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Put the real token only in `.env`. Never commit it.

## Verification

```bash
pytest -q
git status
git ls-files .env
git grep -nE "(MILVUS_TOKEN=|sk-[A-Za-z0-9]|ghp_[A-Za-z0-9])" -- .
```

The expected security result is that `.env` is untracked and no real secret appears in repository content.

## Security baseline

- `.env` is ignored.
- `.env.example` contains no secret.
- Python caches and local environments are ignored.
- GitHub branch protection, secret scanning/push protection, Dependabot, and CodeQL should be enabled in repository settings.
