

# ⚡ Invarum CLI

The command-line interface for **Invarum**, the Physics-Based Prompt Engineering Framework (PBPEF).

Invarum is a **governance grade** quality engineering platform that provides observability, scoring, constraint tooling, and WORM compatible recording to optimize prompt-response interactions. The CLI allows you to trigger the physics engine directly from your terminal or CI/CD pipeline, offloading the heavy computation to the Invarum Cloud.

> **🌟 Get Started:** You must have an account and an API Key to use this tool.  
> Sign up and generate keys at **[app.invarum.com](https://app.invarum.com)**.

---

## 📦 Features

- **Remote Physics Engine**  
  Submits prompts to the Invarum Cloud, where they are scored against our 4D energy model:  
  - **α** (Task Score)  
  - **β** (Semantic Coherence)  
  - **γ** (Order / Output Uncertainty)  
  - **δ** (Efficiency)

- **Headless Execution**  
  Designed for developers. Run prompt evaluations without opening a browser. Perfect for regression testing and CI/CD pipelines.

- **Policy Gating**  
  Immediate Pass/Fail feedback based on your configured Policy Profile (Governance).

- **Secure Authentication**  
  Supports long-lived API Keys (`inv_sk_...`) for secure, authenticated access to your private workspace.

- **Web Synchronization**  
  Every run triggered via CLI is instantly available in your **[Web Dashboard](https://app.invarum.com)** for deep inspection (Sensitivity Analysis, Evidence Bundles, and Operator Traces).

---

## 🚀 Installation

Install directly via pip (Git method):

```bash
# Install the latest version
pip install git+https://github.com/Invarum/invarum-cli.git

# Verify installation
invarum --help
```

📌 Requires Python 3.9+

---

## 🛠 Getting Started

### 1. Get your API Key
Log in to the **[Invarum Dashboard](https://app.invarum.com/settings)**, navigate to **Settings**, and generate a new **Developer Access Key**.

### 2. Authenticate
Save your key locally. This persists your credentials for future runs.

```bash
invarum login --key inv_sk_your_secret_key_here
```

### 3. Execute a Run
Submit a prompt to the engine. The CLI will poll for completion and display the Energy Scores.

```bash
invarum run "Explain quantum entanglement to a five-year-old."
```

**Output:**
```text
Running physics engine...
Run ID: run_a1b2c3d4

┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Metric             ┃ Score ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Alpha (Task)       │ 0.892 │
│ Beta (Coherence)   │ 0.910 │
│ Gamma (Entropy)    │ 0.450 │
│ Delta (Efficiency) │ 0.780 │
└────────────────────┴───────┘

PASSED POLICY GATES
View details: https://app.invarum.com/runs/run_a1b2c3d4
```

---

##⚙️ Advanced Usage

### Specify Task Type
Help the engine optimize scoring by declaring the task intent (default is auto-detected).

```bash
invarum run "Extract the dates from this contract..." --task extract
```
*Supported tasks: `summarize`, `qa`, `brainstorm`, `fiction`, `extract`, `code`.*

### CI/CD Integration
The CLI supports environment variables for automation. It returns exit code `0` on success and `1` on policy failure, making it ideal for build pipelines.

```bash
# In your GitHub Actions / GitLab CI
export INVARUM_API_KEY="inv_sk_..."
invarum run "Release candidate prompt test"
```

---

## 🧠 Architecture

The Invarum ecosystem is split into two parts:

1.  **The CLI (This Repo):** A lightweight "Thin Client." It handles authentication, input formatting, and result rendering. It contains no proprietary logic.
2.  **The Cloud Engine (API):** The heavy lifting happens on Invarum's secure servers. This is where the **PromptState Pipeline** runs:

```
[CLI Request] → [API Gateway] → [Physics Engine] → [Supabase DB]
                                      ↓
                               [Scores & Evidence]
                                      ↓
[CLI Response] ← [JSON Result] ← [API Gateway]
```

---

## 🔬 Roadmap

- [x] Cloud-based Energy Scoring
- [x] CLI Runner with Polling
- [x] Web Dashboard Synchronization
- [x] API Key Authentication
- [ ] Local Artifact Downloads (PDF Evidence)
- [ ] Batch Processing (CSV/JSONL input)
- [ ] `invarum check` for regression testing files

---

## 🧑‍🔬 Author

**Lucretius Coleman**  
PhD in Physics | Computational Methods | Quantum Systems & Prompt Engineering  
📫 lacolem1@invarum.com

---

## 📄 License

MIT License  
See `LICENSE` for details.