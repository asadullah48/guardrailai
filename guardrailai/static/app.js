// GuardrailAI Interactive Controller & Bilingual Localization

let currentLang = 'en';
let currentDomain = 'FINANCIAL';

const TRANSLATIONS = {
  en: {
    badgeTitle: "Deterministic Compliance Layer",
    statusLive: "Engine Active (:8003)",
    heroTitle: "Zero-Trust Agentic Guardrails & Cryptographic Audit Trails",
    heroSubtitle: "Deterministic pre-flight interceptors, mathematical threshold validation, circuit breaker fallbacks, and immutable SHA-256 blockchain-grade non-repudiation.",
    metric1Label: "State Non-Determinism",
    metric1Sub: "Strict Mathematical Bounds",
    metric2Label: "Active Rule Engines",
    metric2Sub: "Finance • Health • Legal",
    metric3Label: "Circuit Breaker SLA",
    metric3Sub: "Safe Default & Escalation",
    metric4Label: "Audit Cryptography",
    metric4Sub: "Tamper-Evident Hash Chain",
    studioTitle: "Deterministic Workflow & Circuit Breaker Studio",
    studioDesc: "Simulate compliance-critical task execution and watch real-time pre/post interceptors and circuit breakers trip.",
    tabFinance: "Financial AML",
    tabHealth: "Healthcare HIPAA",
    tabLegal: "Legal Liability",
    lblWorkflowId: "Workflow Transaction ID",
    lblFallbackPolicy: "Fallback Policy on Violation",
    lblScenarios: "Test Scenarios:",
    lblPayload: "Task Payload (JSON)",
    btnExecute: "Execute Deterministic Pipeline",
    titleExecutionOutput: "Execution Pipeline Trace",
    lblResultJson: "Result & Certificate",
    ledgerTitle: "Immutable Hash-Chained Audit Ledger",
    ledgerDesc: "Real-time SHA-256 blockchain-grade ledger with non-repudiation and automated mathematical verification.",
    btnVerifyLedger: "🛡️ Verify Tamper-Proof Chain"
  },
  ar: {
    badgeTitle: "طبقة الامتثال والحواجز القطعية",
    statusLive: "المحرك نشط (:8003)",
    heroTitle: "حواجز حماية غير مشروطة بالثقة وسجلات تدقيق مشفرة",
    heroSubtitle: "اعتراض قطعي قبل التنفيذ، وفحص للحدود الرياضية، ومفاتيح قطع الدائرة وبدائل آمنة مع ختم تشفيري بسلسلة تجزئة SHA-256.",
    metric1Label: "اللاحتمية السلوكية",
    metric1Sub: "حدود رياضية صارمة",
    metric2Label: "محركات القواعد النشطة",
    metric2Sub: "المالية • الصحية • القانونية",
    metric3Label: "ضمان قطع الدائرة",
    metric3Sub: "بدائل آمنة وتصعيد للمشرف",
    metric4Label: "تشفير التدقيق",
    metric4Sub: "سلسلة تجزئة غير قابلة للتلاعب",
    studioTitle: "استوديو مسارات العمل القطعية ومفاتيح الأمان",
    studioDesc: "قم بمحاكاة تنفيذ المهام الحرجة وشاهد التدقيق التلقائي واشتغال مفاتيح قطع الدائرة عند اكتشاف مخالفات.",
    tabFinance: "الامتثال المالي AML",
    tabHealth: "الصحة والخصوصية HIPAA",
    tabLegal: "المسؤولية القانونية",
    lblWorkflowId: "معرّف معاملة مسار العمل",
    lblFallbackPolicy: "سياسة الأمان البديلة عند المخالفة",
    lblScenarios: "سيناريوهات الاختبار:",
    lblPayload: "بيانات المهمة (JSON)",
    btnExecute: "تشغيل مسار العمل القطعي",
    titleExecutionOutput: "تتبع مراحل التدقيق والتنفيذ",
    lblResultJson: "النتيجة وشهادة عدم الإنكار",
    ledgerTitle: "سجل التدقيق المشفر بسلسلة التجزئة",
    ledgerDesc: "سجل غير قابل للتعديل يماثل تقنية البلوكشين مع تحقق رياضي فوري من سلامة السلسلة.",
    btnVerifyLedger: "🛡️ التحقق من سلامة السلسلة وعدم التلاعب"
  }
};

const SCENARIOS = {
  FINANCIAL: [
    {
      name: "✅ Clean Domestic Wire ($4,500)",
      payload: { amount_usd: 4500.0, destination_country: "US", debt_to_equity_ratio: 0.20 }
    },
    {
      name: "🚨 AML CTR Threshold ($45,000)",
      payload: { amount_usd: 45000.0, destination_country: "GB", debt_to_equity_ratio: 0.15 }
    },
    {
      name: "⛔ OFAC Sanctioned (North Korea)",
      payload: { amount_usd: 8000.0, destination_country: "NORTH_KOREA", debt_to_equity_ratio: 0.10 }
    }
  ],
  HEALTHCARE: [
    {
      name: "✅ Clean Clinical Encounter",
      payload: { clinical_notes: "Patient presents for routine hypertension follow-up.", medication_name: "Metformin", dosage_mg: 500.0 }
    },
    {
      name: "🚨 HIPAA SSN Leak Detected",
      payload: { clinical_notes: "Patient John Doe SSN: 123-45-6789 reported fever.", medication_name: "Amoxicillin", dosage_mg: 250.0 }
    },
    {
      name: "⛔ Lethal Warfarin Overdose (25mg)",
      payload: { clinical_notes: "Patient with atrial fibrillation.", medication_name: "Warfarin", dosage_mg: 25.0 }
    }
  ],
  LEGAL: [
    {
      name: "✅ Bilateral Mutual MSA",
      payload: { contract_title: "Master Services Agreement", contract_text: "Liability is capped at 12 months fees. Mutual indemnification applies." }
    },
    {
      name: "⛔ Uncapped Unlimited Liability Trap",
      payload: { contract_title: "Cloud Hosting Terms", contract_text: "Vendor agrees that neither party's liability shall be limited under any circumstance." }
    },
    {
      name: "🚨 Unilateral Indemnity Breach",
      payload: { contract_title: "Vendor Subcontract", contract_text: "Customer shall unilateral indemnify and defend vendor against all claims." }
    }
  ]
};

function init() {
  renderScenarios();
  loadScenario(0);
}

function toggleLanguage() {
  currentLang = currentLang === 'en' ? 'ar' : 'en';
  document.documentElement.lang = currentLang;
  document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
  document.getElementById('langLabel').innerText = currentLang === 'en' ? 'العربية' : 'English';

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (TRANSLATIONS[currentLang][key]) {
      el.innerText = TRANSLATIONS[currentLang][key];
    }
  });
}

function switchDomain(domain) {
  currentDomain = domain;
  document.querySelectorAll('.domain-tab').forEach((tab, idx) => {
    tab.classList.toggle('active', tab.innerText.includes(domain === 'FINANCIAL' ? 'Financial' : domain === 'HEALTHCARE' ? 'Healthcare' : 'Legal') || tab.innerText.includes(domain === 'FINANCIAL' ? 'المالي' : domain === 'HEALTHCARE' ? 'الصحة' : 'القانونية'));
  });
  renderScenarios();
  loadScenario(0);
}

function renderScenarios() {
  const container = document.getElementById('scenarioButtons');
  container.innerHTML = '';
  SCENARIOS[currentDomain].forEach((sc, idx) => {
    const btn = document.createElement('button');
    btn.className = 'preset-btn';
    btn.innerText = sc.name;
    btn.onclick = () => loadScenario(idx);
    container.appendChild(btn);
  });
}

function loadScenario(idx) {
  const scenario = SCENARIOS[currentDomain][idx];
  document.getElementById('payloadTextarea').value = JSON.stringify(scenario.payload, null, 2);
}

async function executeWorkflow() {
  const btn = document.getElementById('execBtn');
  const badge = document.getElementById('workflowStatusBadge');
  const resultViewer = document.getElementById('resultJsonViewer');
  
  const wfId = document.getElementById('workflowIdInput').value.trim() || `wf-tx-${Date.now()}`;
  const policy = document.getElementById('fallbackPolicySelect').value;
  let payload = {};

  try {
    payload = JSON.parse(document.getElementById('payloadTextarea').value);
  } catch (e) {
    alert("Invalid JSON format in Task Payload.");
    return;
  }

  btn.disabled = true;
  btn.innerText = "Evaluating Guardrails...";
  badge.className = "badge badge-info";
  badge.innerText = "PROCESSING";

  try {
    const res = await fetch('/api/v1/workflow/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        workflow_id: wfId,
        domain: currentDomain,
        task_intent: "DEMO_TRANSACTION",
        payload: payload,
        fallback_policy: policy
      })
    });

    const data = await res.json();
    resultViewer.innerText = JSON.stringify(data, null, 2);

    if (data.final_status === 'COMPLETED') {
      badge.className = "badge badge-success";
      badge.innerText = "COMPLETED (CLEAN)";
    } else if (data.final_status === 'CIRCUIT_BREAKER_TRIGGERED') {
      badge.className = "badge badge-danger";
      badge.innerText = "CIRCUIT BREAKER TRIPPED";
    } else {
      badge.className = "badge badge-warning";
      badge.innerText = data.final_status;
    }

    // Refresh Ledger
    fetchLedger(wfId);

  } catch (err) {
    resultViewer.innerText = `Error connecting to GuardrailAI Gateway: ${err.message}`;
    badge.className = "badge badge-danger";
    badge.innerText = "CONNECTION_ERROR";
  } finally {
    btn.disabled = false;
    btn.innerText = TRANSLATIONS[currentLang].btnExecute;
  }
}

async function fetchLedger(wfId) {
  const container = document.getElementById('ledgerBlocksContainer');
  try {
    const res = await fetch(`/api/v1/audit/ledger/${wfId}`);
    if (!res.ok) return;
    const data = await res.json();

    container.innerHTML = '';
    data.blocks.forEach(b => {
      const card = document.createElement('div');
      card.className = 'block-card glass';
      card.innerHTML = `
        <div class="block-index">BLOCK #${b.block_index} • ${b.agent_name}</div>
        <div class="block-step">${b.step_name}</div>
        <div class="block-hash">Hash: ${b.current_block_hash.substring(0, 24)}...</div>
        <div class="block-hash">Prev: ${b.previous_block_hash.substring(0, 24)}...</div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.error("Ledger fetch error:", err);
  }
}

async function verifyLedgerIntegrity() {
  const wfId = document.getElementById('workflowIdInput').value.trim();
  const btn = document.getElementById('verifyBtn');
  btn.disabled = true;
  btn.innerText = "Verifying Hashes...";

  try {
    const res = await fetch(`/api/v1/audit/verify/${wfId}`);
    const data = await res.json();
    if (data.valid) {
      alert(`✅ Cryptographic Audit Chain Verified!\nWorkflow: ${wfId}\nCertificate: ${data.certificate}\nIntegrity: 100% Tamper-Proof.`);
    } else {
      alert(`❌ Hash Mismatch Detected! Ledger chain has been corrupted or tampered.`);
    }
  } catch (e) {
    alert("Please execute a workflow first before verifying ledger.");
  } finally {
    btn.disabled = false;
    btn.innerText = TRANSLATIONS[currentLang].btnVerifyLedger;
  }
}

window.addEventListener('DOMContentLoaded', init);
