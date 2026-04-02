


# Invarum CLI

**Measure AI quality in business terms. Enforce policy. Export evidence.**

The Invarum CLI is the command-line entry point to the Invarum cloud engine: a governance-grade AI quality, observability, and evidence layer for LLM applications.

Use it to:
- run evaluations from your terminal
- analyze precomputed responses
- surface business-facing KPI signals
- enforce policy gates in CI/CD
- export evidence bundles and audit PDFs
- inspect runs in the dashboard with diagnostics, traces, and sensitivity context

If your team uses LLMs and needs more than “looks good to me,” Invarum gives you a structured way to measure, review, and prove output quality.

> Get started at **[app.invarum.com](https://app.invarum.com)**

---

## Why Invarum

Most prompt tools help you test outputs. 

Invarum is built to help you **measure, govern, and defend** them. 

It combines:
- **business-facing KPIs** for Helpfulness, Reliability, and Efficiency
- **technical quality metrics** underneath the KPI layer
- **policy-aware verdicts** with explicit decision states and advisories
- **audit-ready artifacts** with evidence exports and integrity metadata
- **dashboard inspection** for diagnostics, traces, and investigation
- **a thin-client architecture** so proprietary evaluation logic stays in the hosted engine

That makes the CLI useful across the org:
- **Developers:** run evals, compare outputs, automate checks
- **AI platform teams:** investigate failures, inspect traces, monitor release quality
- **Risk / compliance / QA:** export evidence bundles and audit PDFs
- **Leaders:** turn “we tested it” into a measurable quality and governance story

---

## Start with the KPI layer

Invarum translates technical evaluation into business-friendly signals:
- **Helpfulness** — did the system accomplish the task?
- **Reliability** — did it clear safety, policy, and stability checks?
- **Efficiency** — did it deliver value at a reasonable cost?

And for teams managing many runs:
- **Reliability Pass Rate** — how often runs clear the reliability bar over time

These KPIs are designed for fast operational reading. The deeper technical metrics remain available when you need them.

---

## The model underneath

Behind the KPI layer, Invarum scores outputs across four core dimensions:

| Metric | Signal | What it measures |
|:---:|:---|:---|
| **$\alpha$ (alpha)** | **TaskScore** | Did the output do the job it was asked to do? |
| **$\beta$ (beta)** | **Coherence** | Did it stay logically and semantically on track? |
| **$\gamma$ (gamma)** | **Order / Entropy** | Was the variability appropriate for the task and domain? |
| **$\delta$ (delta)** | **Efficiency** | How much useful result was delivered for the cost in tokens, time, and steps? |

The KPI layer makes the system legible to operators and decision-makers. The four-metric layer preserves technical depth for engineers, evaluators, and governance teams.

---

## What the CLI does

### 1) Run evaluations
Submit prompts to Invarum and get back a scored run with a response, KPI summary, technical metrics, and policy outcome.

### 2) Analyze existing outputs
Invarum can evaluate responses you already have. That means it can act as a validator and governance layer even when generation happens elsewhere.

If you provide `--response` or `--response-file`, the CLI automatically switches to analyze mode unless you explicitly set `--exec`.

This is especially useful for:
- grading outputs from external LLM systems
- auditing responses captured from production
- evaluating structured multi-step or agent-like outputs in the analyze layer

### 3) Score simulated agent behavior in analyze mode
For imported multi-step or role-simulated outputs, Invarum can score agent-like behavior without becoming your production agent runtime.

Advanced analyze-mode hints include:
- `--structure-mode single`
- `--structure-mode agent`
- `--structure-mode sim_agent`
- `--micro-alpha` for per-virtual-step micro-alpha scoring in SIM-AGENT workflows

Use this when you want to inspect:
- handoff quality across steps
- stability across multi-step reasoning or workflow chains
- whether an imported structured run should pass review thresholds before broader rollout

### 4) Enforce policy in CI/CD
Use `--strict` to return exit code `1` when a run fails policy gates. This acts as a powerful CI/CD gatekeeper for your prompts.

```yaml
# Example CI/CD gate
- name: Certify Prompt Quality
  run: |
    invarum run -f prompts/onboarding.txt --strict
    # Fails the build if the new prompt violates ISO 42001 or internal thresholds
```

### 5) Export evidence
Generate:
- **JSON evidence bundles** for automation and downstream systems *(outputs a cryptographically hashed JSON receipt containing policy gates, model parameters, and metrics)*
- **PDF audit reports** for incident review, governance, and stakeholder communication

The CLI supports both inline save-on-run and standalone export.

### 6) Investigate in the dashboard
Move from terminal to the full run view to inspect:
- KPI breakdowns
- raw $\alpha$ / $\beta$ / $\gamma$ / $\delta$
- policy decisions and failed gates
- advisories
- traces and operator spans
- **Sensitivity Analysis (Wind Tunnel)** to see how mathematically fragile a prompt is to minor structural changes

---

## Governance and evidence

A run can produce more than a score. Invarum also returns:

- policy gate results
- explicit decision states
- advisories with remediation-oriented guidance
- evidence artifacts for export and review
- integrity metadata for verification workflows

This is the difference between a testing utility and a quality/evidence layer.

---

## Architecture

Invarum uses a thin-client architecture.

```text
[CLI] -> [API] -> [Invarum evaluation engine] ->[runs, traces, evidence, audit artifacts]
   ^                                                          |
   |----------------------------------------------------------|
                      summarized results + exports
```

**What runs locally:**
- authentication
- file input/output
- request submission
- terminal rendering
- export handling

**What runs in the cloud engine:**
- scoring
- KPI computation
- policy evaluation
- diagnostics
- evidence generation
- audit artifact generation
- trace and sensitivity processing

---

## Installation

```bash
pip install git+https://github.com/Invarum/invarum-cli.git@v0.1.8
```
*Requires Python 3.9+.*

---

## Quickstart

### Authenticate
```bash
invarum login --key inv_sk_your_secret_key_here
```
Or in CI:
```bash
export INVARUM_API_KEY="inv_sk_..."
```

### Run an evaluation
```bash
invarum run "Summarize the main findings of this abstract in 5 bullets." --domain scientific
```

### Analyze an existing output
```bash
invarum run "Review this customer support response." \
  --response "Thanks for your patience. Your order has shipped..."
```

### Analyze from file
```bash
invarum run "Review this structured support workflow output." \
  --response-file workflow_output.json
```

### Save the evidence bundle during a run
```bash
invarum run "Extract all dates from this contract." \
  --task extract \
  --domain legal \
  --output evidence.json
```

### Export a JSON evidence bundle
```bash
invarum export run_a1b2c3d4 --format json --output evidence.json
```
Or pipe JSON to stdout:
```bash
invarum export run_a1b2c3d4 --format json
```

### Export a PDF audit report
```bash
invarum export run_a1b2c3d4 --format pdf --output report.pdf
```

### Fail CI on policy failure
```bash
invarum run -f prompt.txt --strict --json
```

---

## Common workflows

### Evaluate against a reference
```bash
invarum run "Explain quantum entanglement." \
  --reference "Quantum entanglement is a phenomenon where..."
```

### Use a reference file
```bash
invarum run "Compare this answer to the approved response." \
  --reference-file approved_answer.txt
```

### Be explicit about analyze mode
```bash
invarum run "Review this structured support workflow output." \
  --exec analyze \
  --response-file workflow_output.json
```

### Score a SIM-AGENT-style imported workflow
```bash
invarum run "Review this structured multi-step workflow output." \
  --exec analyze \
  --response-file workflow_output.json \
  --structure-mode sim_agent \
  --micro-alpha
```

### Tune generation
```bash
invarum run "Write a creative poem" --temp 0.9
```

---

## Who this is for

### Developers
Use Invarum to test prompts, score outputs, automate checks, and wire evaluations into delivery workflows.

### AI platform teams
Use it to centralize run evaluation, compare outputs, inspect traces, and review imported outputs from other systems.

### Compliance, QA, and risk
Use evidence bundles and audit PDFs to support review, signoff, and governance processes.

### Founders and executives
Use Invarum when AI quality needs to be measurable, reviewable, and explainable to customers, partners, or internal stakeholders.

---

## Observability

Invarum can integrate with OpenTelemetry-style workflows so traces and metrics can sit alongside broader system telemetry.

---

## Security and data handling

Invarum is designed for auditability without forcing unnecessary retention. Key ideas include:

- BYOK-oriented generation workflows
- configurable prompt/response retention behavior
- evidence artifacts that preserve integrity metadata even when raw text handling is minimized

---

## Troubleshooting

### Command not found after install
```bash
python -m invarum --version
python -m invarum login --key inv_sk_your_secret_key_here
python -m invarum run "Test prompt"
```

### Not logged in
```bash
invarum login --key inv_sk_your_secret_key_here
```

### Evidence not ready yet
If a run completes before evidence is available, retry the export command after a short delay.

### PDF export requires an output file
```bash
invarum export run_a1b2c3d4 --format pdf --output report.pdf
```

---

## License

MIT