# Myntra CC SOP Knowledge Base

A static, searchable knowledge base of Myntra Customer Care SOPs for **Delivery**, **Return**, and **Refund** concerns, plus an **Agent Assist Finder**.

## Use locally
Open `index.html` in any browser. No build step required.

Or serve it:
```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Data files
- `agentassist.json` — dedicated Agent Assist dataset (338 articles).
- `src/data/agentAssistArticles.json` — same dataset, following `src/data/` convention.
- `source.txt` — verbatim original SOP notes.

Each article has: `pg` (process group), `article` (exact Agent Assist article name), `level` (SA Level, or "" if missing in source), `cat` (category).

## Deploy
Deployed on Vercel. To redeploy:
```sh
vercel --prod
```

## Features
- 38 SOP topics across 3 categories (Delivery / Return / Refund)
- Agent Assist Finder: search by complaint/process/article, synonyms, category & SA Level filters, favorites, recently viewed, import/export
- Live search with highlighting, sidebar nav, copy-on-click incident codes
- Complete verbatim source notes (lazy-loaded)
- Dark/light theme, responsive, reduced-motion support
- Fully self-contained (no external CDN dependencies)
