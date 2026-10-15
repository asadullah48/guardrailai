# GuardrailAI code-first review

Repository: asadullah48/guardrailai. Baseline commit: `1c7c04d4900fc25812d9c62d00c17d0680d46821`.

## Verified findings and fixes

Baseline locations below refer to that commit; fixed locations refer to this branch.

| Finding | Baseline evidence | Change and regression evidence |
|---|---|---|
| Audit digests omitted timestamps, metadata, index and workflow identity; genesis contents were not checked | `guardrailai/core/audit_ledger.py:26`, `:41`, `:63-71` | Hash every stored field except its own digest, including genesis; validate sequence and identity. `guardrailai/core/audit_ledger.py:60-77`; field mutation tests in `tests/test_regressions.py:17-28`. |
| Empty ledgers verified successfully and certificate generation indexed an empty list | `guardrailai/core/audit_ledger.py:63-75` | Reject empty chains and return a false audit seal without indexing them. `tests/test_regressions.py:31-36`. |
| Nested caller metadata remained aliased after append | `guardrailai/core/audit_ledger.py:54` | Deep-copy metadata before storing/hashing. `tests/test_regressions.py:39-45`. |
| Python hash randomization and payload insertion order changed references | `guardrailai/agents/process_agent.py:17`; `guardrailai/orchestration/workflow.py:131` | Sorted JSON SHA-256 transaction reference and SHA-256 workflow reference. `tests/test_regressions.py:48-71` compares independent processes and reordered keys. |
| Post-flight BLOCKING violations returned COMPLETED | `guardrailai/orchestration/workflow.py:82` | Route BLOCKING and CRITICAL to fallback, matching pre-flight. `guardrailai/orchestration/workflow.py:84`; injected-policy regression `tests/test_regressions.py:74-86`. |
| SAFE_DEFAULT claimed clamping but returned only descriptive data | `guardrailai/orchestration/workflow.py:119-139` | Correct response and Studio labels to say the operation is withheld; describe actual fallback behavior in README. |
| Regulatory and immutable/non-repudiation claims exceeded implementation | `guardrailai/guardrails/financial.py:7-51`, `healthcare.py:13-44`, `legal.py:12-48`; `guardrailai/core/audit_ledger.py:79-82`; `guardrailai/orchestration/workflow.py:23-27`, `:121-142` | Keep deterministic workflow and SHA-256 headlines. Replace unsupported safety percentages and immutable/signed certificate language in English/Arabic docs and Studio. Consolidate scope in README Limits / non-goals. Mark SPEC as historical design; package maturity as Beta. |

## Exact test summary output

Tests were run before implementation changes. The sandboxed first attempt stalled at the FastAPI dashboard test; running outside the sandbox completed. This is an environment distinction, not an application fix.

Baseline command: `python -m pytest tests -v -o faulthandler_timeout=30`

```text
============================= 17 passed in 9.21s ==============================
```

New regressions against unchanged implementation: `python -m pytest tests/test_regressions.py -q`

```text
18 failed, 7 passed in 12.44s
```

The passing cases already covered fields protected by the original chain. Failing cases demonstrated previously undetected field edits, an empty ledger, metadata aliasing, inconsistent references and post-flight blocking bypass.

After implementation fixes: `python -m pytest tests -v -o faulthandler_timeout=30`

```text
============================= 42 passed in 16.26s =============================
```

Each run also emitted this installed-plugin startup warning before pytest collection:

```text
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
  from pydantic.v1 import (
```

It originated from `langsmith/schemas.py:23` in the environment, not from this repository. Pytest's own summaries above did not include a warning count. Runtime: Python 3.14.7, pytest 9.0.2. No warning filters were added.

Final verification after documentation and Studio edits: `python -m pytest tests -v -o faulthandler_timeout=30` (captured with PowerShell Tee-Object).

```text
============================= 42 passed in 4.43s ==============================
```

[Full final test output](validation-after.txt). The README example returned `COMPLETED` and `True`; `node --check guardrailai/static/app.js` and `git diff --check` exited successfully.

## Diffs and compatibility

- `guardrailai/core/audit_ledger.py`: field-complete hashing, genesis verification, identity/sequence checks, metadata snapshot and empty-chain handling.
- `guardrailai/agents/process_agent.py`, `guardrailai/orchestration/workflow.py`: stable references; post-flight blocking routing; accurate fallback message.
- `tests/test_regressions.py`: executable regressions and existing-protection checks, all exercised before and after fixes.
- `README.md`, `README.ar.md`, Studio HTML/JS, `SPEC.md`, `pyproject.toml`, audit-agent docstring: implementation-aligned presentation.

Reference strings and block digests change. The ledger is in memory, so there is no persistence migration. Run `git diff 1c7c04d4900fc25812d9c62d00c17d0680d46821 --` for the full diff. Production, regulatory certification and external integrations were not validated; see README Limits / non-goals for scope.

## Portfolio card changes needed:

Before text comes from the user-supplied card snapshot. Apply after the code changes merge. Title and Status remain unchanged.

- **Tagline**
  - Before: Zero-Trust Agentic Guardrails, Circuit Breakers & Cryptographic SHA-256 Audit Trails
  - After: Deterministic Agentic Guardrails, Circuit Breakers & Tamper-Evident SHA-256 Audit Trails

- **Description**
  - Before: Compliance-critical multi-agent framework enforcing deterministic guardrails, mathematical bounds, circuit breaker fallbacks, and cryptographic hash-chained audit trails.
  - After: Typed agentic workflow engine with deterministic processing, pre/post policy checks, explicit fallback routing, and field-complete SHA-256 hash-chained audit trails.

- **Problem**
  - Before: Probabilistic LLM agents cannot be deployed in high-consequence finance, healthcare, and legal workflows due to non-deterministic hallucinations, lack of hard safety ceilings, and failure to meet evidentiary audit standards (SOC-2, SEC 17a-4, HIPAA).
  - After: Agentic workflows need inspectable policy decisions, explicit failure paths, and verifiable execution records before their behavior can be evaluated for higher-stakes applications.

- **Solution**
  - Before: A zero-trust multi-agent state machine where compliance is structural: pre-flight statutory interceptors, ProcessAgent bounded executions, ComplianceAgent post-flight threshold enforcement, automated circuit breakers with safe fallbacks, and an immutable SHA-256 blockchain-style audit ledger.
  - After: A typed pre-flight, deterministic processing, post-flight and audit pipeline, with blocking/critical fallback routing and SHA-256 verification of every stored block field.

- **Impact**
  - Before: 0.00% state non-determinism, 100% automated enforcement across AML, OFAC, HIPAA Safe Harbor, and liability caps, cryptographic non-repudiation certificates, and 17/17 passing automated tests.
  - After: 42 passing tests covering domain policy examples, API execution, audit-field tampering, metadata snapshots, stable references across Python processes, and post-flight blocking fallback.

- **Metrics**
  - Before: Tests: 17, Audit Ledger: SHA-256
  - After: Tests: 42, Audit Ledger: SHA-256
