# Trismegistus Supervisor Agent

> Phase 1-2 prototype of the AskDavid supervisor-agent architecture for Hermes.
> Source: zeroxkyle's ranked resource #1, traced to JP Morgan's "Ask David" system.

## Architecture

```
User Query
    ↓
[Intent Router] → classify intent, select skills/model/timeout
    ↓
[Subagent Delegation] → spawn specialized subagent
    ↓
[Reflection Node] → review output before delivery
    ↓
[Human-in-the-Loop] → high-risk tasks pause for approval
    ↓
Delivery
```

## Files

| File | Purpose |
|------|---------|
| `router.py` | Intent classifier using Claude 3.5 Haiku (~$0.0001/query) |
| `supervisor.py` | Orchestrator that routes queries to subagents |
| `design-askdavid-pattern.md` | Design document with full architecture plan |

## Usage

```bash
# Dry run — show plan without executing
python3 supervisor.py "Find recent papers on LLM agents" --dry-run

# Live execution (Phase 3: will spawn actual subagents)
python3 supervisor.py "Fix the bug in deduplicator.py"

# Direct router test
python3 router.py "Your query here"
```

## Intent Categories

| Category | Skills | Tools | Model | Timeout |
|----------|--------|-------|-------|---------|
| research | web, search, arxiv, blogwatcher | web_search, web_extract, arxiv | kimi-coding | 120s |
| code | terminal, file, code_exec, patch | terminal, patch, execute_code | claude-sonnet-4 | 300s |
| ops | terminal, cronjob, file, process | terminal, cronjob, process | claude-sonnet-4 | 180s |
| creative | image_gen, tts, vision | image_generate, text_to_speech | claude-sonnet-4 | 180s |
| analysis | code_exec, terminal, file | execute_code, terminal | claude-sonnet-4 | 300s |
| chat | — | — | kimi-coding | 60s |

## Cost

- Router: ~300 tokens/query @ Claude 3.5 Haiku ≈ $0.0001
- Subagent: varies by task complexity and model

## Roadmap

- **Phase 1** ✅ Intent Router with 6 categories
- **Phase 2** ✅ Supervisor orchestrator with dry-run simulation
- **Phase 3** Live subagent delegation via `delegate_task`
- **Phase 4** LLM-as-judge reflection node
- **Phase 5** Human-in-the-loop risk classification

## License

MIT
