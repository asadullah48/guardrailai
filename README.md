# 🛡️ GuardrailAI: Deterministic Workflow Layer

> **A zero-trust, compliance-critical agentic workflow framework enforcing deterministic guardrails, mathematical bounds, circuit breaker fallbacks, and cryptographic hash-chained audit trails.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Tests Passing](https://img.shields.io/badge/Tests-17%20Passing-brightgreen.svg)]()
[![FastAPI](https://img.shields.io/badge/API-FastAPI%20%3A8003-teal.svg)](http://127.0.0.1:8003/docs)
[![Author](https://img.shields.io/badge/Author-Asadullah%20Shafique-purple.svg)](https://asadullahshafique-devunity.vercel.app)

---

## 🚀 Key Value Propositions

1. **Deterministic Bounded Agents**: Replaces stochastic LLM unreliability with mathematically validated operational bounds.
2. **Pre-Flight & Post-Flight Interceptors**: Validates requests before model execution and reviews results before delivery.
3. **Cryptographic SHA-256 Audit Trail**: Every step is sealed into a tamper-evident blockchain-style hash chain ($H_i = \text{SHA-256}(H_{i-1} + \text{data})$).
4. **Automated Circuit Breakers**: Fails closed gracefully with safe defaults, automated PHI redaction, or human supervisor escalation.
5. **Interactive Glassmorphic Studio**: Live dashboard with multi-domain simulators, circuit breaker testers, and bilingual (English/Arabic) UI.

---

## 🏛️ Specialized Guardrail Modules

```
                    ┌─────────────────────────┐
                    │   Client API / Studio   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Deterministic Engine   │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│ Financial Rules  │   │ Healthcare Rules │   │   Legal Rules    │
│ • AML Threshold  │   │ • HIPAA 18 PHI   │   │ • Liability Cap  │
│ • OFAC Sanctions │   │ • FDA Dosage Cap │   │ • Mutual Indem.  │
│ • AAOIFI Shariah │   │ • 21 CFR Part 11 │   │ • ABA Rule 5.3   │
└──────────────────┘   └──────────────────┘   └──────────────────┘
```

---

## 🛠️ Quick Start

```powershell
# 1. Clone repository
git clone https://github.com/asadullah48/guardrailai.git
cd guardrailai

# 2. Install dependencies
pip install -e .

# 3. Run automated test suite
python -m pytest tests -v

# 4. Start local gateway & frontend dashboard
uvicorn guardrailai.server:app --host 127.0.0.1 --port 8003 --reload
```

- **Interactive Dashboard**: [http://127.0.0.1:8003/](http://127.0.0.1:8003/)
- **Swagger OpenAPI Docs**: [http://127.0.0.1:8003/docs](http://127.0.0.1:8003/docs)

---

## 🧭 Agentic AI Alignment

GuardrailAI exists to make agent behavior boring in the best way:
- **Autonomy** — pre-flight and post-flight interceptors validate a request
  before model execution and review the result before delivery, so the
  system can act without a human reviewing every step.
- **Resilience** — every step is sealed into a tamper-evident SHA-256 hash
  chain, and circuit breakers fail closed to safe defaults (automated PHI
  redaction, human supervisor escalation) instead of failing open.
- **Adaptivity** — domain-specific rule modules (Financial/AML/OFAC,
  Healthcare/HIPAA/FDA, Legal) plug into the same deterministic engine, so
  the guardrail layer extends to new regulatory domains without rewriting
  the core.

## 📈 Roadmap
- [ ] Add further domain rule modules beyond Financial/Healthcare/Legal
- [ ] Expand the circuit-breaker simulators in the Studio dashboard
- [ ] Tighten integration with the sibling agent repos (ContextX,
      MarketAgentHub, WorkforceAI)

---

## 🌐 Connected Ecosystem & Portfolio

- **DevUnity Portfolio**: [https://asadullahshafique-devunity.vercel.app](https://asadullahshafique-devunity.vercel.app)
- **MarketAgentHub**: [https://github.com/asadullah48/marketagenthub](https://github.com/asadullah48/marketagenthub)
- **WorkforceAI**: [https://github.com/asadullah48/workforceai](https://github.com/asadullah48/workforceai)
- **DomainX**: [https://github.com/asadullah48/domainx](https://github.com/asadullah48/domainx)
