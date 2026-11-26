#!/usr/bin/env python3
"""Sync Agent Assist data: canonical source -> embedded fallback + secondary copy.

Canonical source: agentassist.json (root)
Secondary copy:  src/data/agentAssistArticles.json
Embedded fallback: index.html <script id="aaSeedData">

Usage:
  python3 scripts/sync_agentassist.py           # sync + validate
  python3 scripts/sync_agentassist.py --check   # validate only, fail on mismatch
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(ROOT, 'agentassist.json')
SECONDARY = os.path.join(ROOT, 'src', 'data', 'agentAssistArticles.json')
INDEX = os.path.join(ROOT, 'index.html')

def load_canonical():
    with open(CANONICAL, encoding='utf-8') as f:
        data = json.load(f)
    assert isinstance(data, list), 'canonical must be a list'
    assert len(data) > 0, 'canonical is empty'
    # validate schema
    seen = set()
    for i, d in enumerate(data):
        assert isinstance(d, dict), f'entry {i} not object'
        assert 'pg' in d and isinstance(d['pg'], str) and d['pg'].strip(), f'entry {i} missing pg'
        assert 'article' in d and isinstance(d['article'], str) and d['article'].strip(), f'entry {i} missing article'
        assert 'level' in d, f'entry {i} missing level (use "" for unavailable)'
        assert 'cat' in d, f'entry {i} missing cat'
        if d['article'] in seen:
            raise AssertionError(f'duplicate article: {d["article"]}')
        seen.add(d['article'])
    return data

def sync_secondary(data):
    os.makedirs(os.path.dirname(SECONDARY), exist_ok=True)
    with open(SECONDARY, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write('\n')

def sync_embedded(data):
    with open(INDEX, encoding='utf-8') as f:
        html = f.read()
    payload = json.dumps(data, ensure_ascii=False)
    new_tag = '<script type="application/json" id="aaSeedData">' + payload + '</script>'
    pattern = re.compile(r'<script type="application/json" id="aaSeedData">.*?</script>', re.S)
    if not pattern.search(html):
        raise AssertionError('embedded aaSeedData tag not found in index.html')
    html = pattern.sub(new_tag, html, count=1)
    with open(INDEX, 'w', encoding='utf-8') as f:
        f.write(html)

def check_sync(data):
    # secondary
    if os.path.exists(SECONDARY):
        with open(SECONDARY, encoding='utf-8') as f:
            sec = json.load(f)
        if sec != data:
            raise AssertionError('secondary copy out of sync')
    # embedded
    with open(INDEX, encoding='utf-8') as f:
        html = f.read()
    m = re.search(r'<script type="application/json" id="aaSeedData">(.*?)</script>', html, re.S)
    if not m:
        raise AssertionError('embedded tag missing')
    emb = json.loads(m.group(1))
    if emb != data:
        raise AssertionError('embedded data out of sync')

def main():
    check_only = '--check' in sys.argv
    data = load_canonical()
    print(f'canonical entries: {len(data)}')
    print(f'unique articles: {len(set(d["article"] for d in data))}')
    missing = sum(1 for d in data if not d.get('level'))
    print(f'missing SA levels: {missing}')
    if check_only:
        check_sync(data)
        print('OK: all copies in sync')
        return
    sync_secondary(data)
    sync_embedded(data)
    check_sync(data)
    print('synced: secondary + embedded updated and verified')

if __name__ == '__main__':
    main()
