# 🛡️ SentinelAI — Intelligent Threat Detection & Investigation System

### An Explainable, Graph-Enhanced Cybersecurity AI/ML Platform

**SentinelAI** is an AI-powered cybersecurity analytics platform designed to detect suspicious network activity, identify anomalous traffic patterns, explain machine learning predictions, and investigate relationships between network entities.

The platform combines **supervised machine learning, unsupervised anomaly detection, explainable AI, graph analytics, investigation workflows, and MLOps** into a unified framework for defensive cybersecurity research.

Rather than treating intrusion detection as a simple binary classification problem, SentinelAI approaches threat detection as a complete analytical workflow: from dataset validation and model training to alert enrichment, relationship analysis, evidence-based investigation, and model monitoring.

> **Project objective:** Develop an extensible, explainable, and reproducible threat detection platform that supports security analysts in identifying and investigating potentially malicious network activity.

---

## 📌 Table of Contents

1. Project Overview
2. Problem Statement
3. Objectives
4. Key Features
5. System Architecture
6. End-to-End Workflow
7. Module-by-Module Explanation
8. Unique and Advanced Features
9. Machine Learning Methodology
10. Graph-Based Threat Intelligence
11. Explainable AI
12. Dataset and Data Engineering
13. Evaluation Framework
14. Technology Stack
15. Repository Structure
16. Installation and Setup
17. Running the Application
18. API Documentation
19. MLOps and Model Governance
20. Security and Privacy
21. Limitations
22. Future Enhancements
23. Research Contributions
24. Portfolio and Resume Description

---

## 1. Project Overview

Modern network environments generate large volumes of traffic records. Detecting malicious behavior in this data is challenging because attack patterns vary, benign traffic can appear unusual, and conventional classification models often provide limited explanations for their predictions.

SentinelAI addresses these challenges through a modular AI/ML architecture.

The system processes network-flow records, validates their quality, prepares predictive features, runs threat classification and anomaly detection, generates explanations, analyzes endpoint relationships, and presents findings through an analyst-oriented interface.

### Core capabilities

- Network-flow ingestion and dataset quality analysis
- Supervised network threat classification
- Unsupervised anomaly detection
- Feature importance and explainable predictions
- Network endpoint relationship analysis
- Alert enrichment and investigation support
- Experiment tracking and model evaluation
- Model versioning and drift-monitoring workflows
- REST API and interactive security dashboard
- Automated testing and reproducible development

**Important distinction:** SentinelAI is a defensive network-traffic analytics platform. It is not a facial recognition system, an offensive security tool, or an automatic incident-response replacement.

---

## 2. Problem Statement

Traditional intrusion-detection approaches face several practical challenges:

- **High false-positive rates:** Legitimate network activity may be incorrectly flagged.
- **Class imbalance:** Benign traffic can greatly outnumber individual attack categories.
- **Limited interpretability:** A model may predict an attack without explaining which features influenced its decision.
- **Unknown or changing patterns:** Previously unseen behavior may differ from the model's training data.
- **Disconnected alerts:** Individual flow predictions may not reveal broader communication relationships.
- **Evaluation leakage:** Duplicate records, target-derived features, or inappropriate dataset splits can inflate reported metrics.
- **Model maintenance:** Model performance and data distributions can change over time.

SentinelAI is designed to address these challenges by combining multiple analytical signals and emphasizing evaluation quality, interpretability, and reproducibility.

---

## 3. Project Objectives

The primary objectives are:

1. Build a complete network-flow data preparation and validation pipeline.
2. Train and evaluate supervised machine learning models for threat classification.
3. Complement classification with unsupervised anomaly detection.
4. Explain model predictions using feature-level attribution and importance analysis.
5. Represent network communication as a graph for relationship analysis.
6. Correlate related alerts into more meaningful investigation cases.
7. Maintain reproducible model training, evaluation, and version history.
8. Provide an accessible interface for reviewing predictions and exporting results.
9. Establish automated tests and deployment workflows.
10. Create a foundation for future graph neural network research and cross-dataset generalization studies.

---

## 4. Key Features

| Feature | Description |
|---|---|
| Dataset Forensics | Examines missing values, duplicates, feature types, class imbalance, and potential leakage. |
| Threat Classification | Predicts supported benign and attack labels using trained ML models. |
| Anomaly Detection | Identifies unusual samples using an unsupervised model. |
| Dual-Signal Analysis | Compares classifier output with anomaly scores to prioritize review. |
| Explainable AI | Shows influential features and, where implemented, local SHAP explanations. |
| Network Graph Analysis | Models endpoint relationships and communication patterns. |
| Alert Correlation | Groups related alerts using configured endpoint and temporal rules. |
| Investigation Management | Supports case notes, alert disposition, and evidence references. |
| Model Evaluation | Measures precision, recall, F1, ROC-AUC, PR-AUC, and false-positive rate where applicable. |
| Model Governance | Records model versions, experiment settings, and evaluation results. |
| Drift Monitoring | Compares incoming data or predictions against a reference baseline. |
| Analyst Dashboard | Displays model outputs, investigation information, charts, and exportable results. |
| REST API | Exposes supported capabilities to other applications. |
| Automated Testing | Checks important data, model, API, and graph-analysis behavior. |

---

## 5. System Architecture

The system follows a modular pipeline that separates data preparation, predictive modeling, investigation, and application delivery.

```text
                 ┌─────────────────────────┐
                 │ Network-Flow Data       │
                 │ CSV / Authorized Source │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ Data Ingestion          │
                 │ Schema & Quality Checks │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ Dataset Forensics       │
                 │ Leakage & Class Audits  │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ Preprocessing           │
                 │ Feature Engineering     │
                 │ Train/Test Separation   │
                 └────────────┬────────────┘
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
       ┌───────────────────┐  ┌───────────────────┐
       │ Supervised ML     │  │ Anomaly Detection │
       │ Threat Classifier │  │ Unsupervised Model│
       └─────────┬─────────┘  └─────────┬─────────┘
                 └───────────┬──────────┘
                             ▼
                 ┌─────────────────────────┐
                 │ Prediction Enrichment   │
                 │ Confidence + Anomaly    │
                 └────────────┬────────────┘
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
       ┌───────────────────┐  ┌───────────────────┐
       │ Explainable AI    │  │ Graph Analytics   │
       │ Feature Attribution│ │ Endpoint Relations│
       └─────────┬─────────┘  └─────────┬─────────┘
                 └───────────┬──────────┘
                             ▼
                 ┌─────────────────────────┐
                 │ Alert Correlation       │
                 │ Investigation Workflow  │
                 └────────────┬────────────┘
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
       ┌───────────────────┐  ┌───────────────────┐
       │ Analyst Dashboard │  │ REST API          │
       └───────────────────┘  └───────────────────┘

          Cross-cutting components:
      Evaluation · MLOps · Drift Monitoring
          Testing · Security · Governance
```

---

## 6. End-to-End Workflow

### Step 1 — Data ingestion

The system receives network-flow records from an authorized dataset or supported input source.

Each record can contain flow statistics, protocol information, packet counts, byte counts, rates, timestamps, endpoint identifiers, and a target label during training.

### Step 2 — Dataset forensics

The data-quality module examines:

- Missing and invalid values
- Duplicate records
- Feature types and schema inconsistencies
- Class distribution and imbalance
- Identifier columns and possible target leakage
- Suspicious overlap between data splits

The objective is to identify data-quality risks before model training.

### Step 3 — Preprocessing and feature engineering

Numeric and categorical features are transformed using preprocessing steps fitted on the training data.

The preprocessing pipeline should be saved alongside the trained estimator so that inference uses consistent transformations.

For realistic evaluations, time-based, capture-based, or group-based splits should be considered to reduce contamination between training and testing records.

### Step 4 — Threat classification

The supervised classifier predicts a label from the classes represented in its training data.

For a binary model, the output may distinguish benign traffic from the positive attack class. A multiclass model can distinguish individual attack categories when sufficient labeled data is available.

### Step 5 — Anomaly scoring

An unsupervised model, such as Isolation Forest, assigns an anomaly score to a flow.

The score indicates how unusual a record is relative to the model's learned distribution. It is not automatically a probability that the record represents an attack.

### Step 6 — Prediction enrichment

The platform combines the available prediction, confidence information, anomaly score, and network context.

Cases where the supervised model and anomaly detector disagree can be prioritized for human review.

### Step 7 — Explainability

The explanation component identifies influential features and, where supported, provides local feature-attribution results for an individual prediction.

### Step 8 — Graph analysis

The graph component models communication relationships between source and destination endpoints. It can help analysts explore connectivity patterns that are difficult to interpret from isolated rows.

### Step 9 — Alert correlation and investigation

Related alerts can be grouped using defined correlation rules. Analysts can review supporting records, add investigation notes, and record a disposition.

### Step 10 — Evaluation and monitoring

The platform records evaluation metrics and model metadata. Monitoring components can compare new traffic with a reference distribution and identify potential drift.

### Step 11 — Reporting and export

The dashboard presents supported results and allows users to export predictions and investigation data for further analysis.

---

## 7. Module-by-Module Explanation

### Module 1 — Dataset Intelligence and Forensics

**Purpose:** Establish data quality and identify potential evaluation problems before model training.

Responsibilities:

- Validate dataset schemas.
- Analyze missing values and duplicate records.
- Examine feature distributions and label balance.
- Flag identifier columns and possible label leakage.
- Generate dataset-quality summaries.
- Support reproducible preprocessing.

**Output:** A validated dataset and a quality report.

### Module 2 — Supervised Threat Classification

**Purpose:** Identify traffic patterns associated with known training labels.

Potential models include:

- Logistic Regression
- Random Forest
- XGBoost or LightGBM
- Additional models selected through benchmarking

The module returns predictions and, where supported, class probabilities.

**Output:** Predicted label, probability information, and evaluation metrics.

### Module 3 — Unsupervised Anomaly Detection

**Purpose:** Highlight records that differ from patterns learned from reference traffic.

Potential methods include:

- Isolation Forest
- One-Class SVM
- Autoencoder-based reconstruction error

The initial implementation should use a clearly defined baseline before adding more complex algorithms.

**Output:** Anomaly scores and candidate records for review.

### Module 4 — Dual-Signal Threat Analysis

**Purpose:** Combine complementary signals rather than relying only on the classifier.

For example:

| Classifier | Anomaly detector | Suggested handling |
|---|---|---|
| Attack | Unusual | Prioritize review |
| Attack | Typical | Review based on predicted attack class |
| Benign | Unusual | Investigate possible novel behavior or benign outlier |
| Benign | Typical | Lower priority, subject to policy and evaluation |

These are investigation suggestions, not final security verdicts. Operational thresholds must be selected and validated using representative data.

### Module 5 — Explainable AI

**Purpose:** Improve the transparency of model outputs.

Capabilities may include:

- Global feature importance
- SHAP summary plots
- Local feature-attribution reports
- Explanation comparisons across model versions
- Analysis of important features for false positives and false negatives

**Output:** A model explanation that helps an analyst understand the prediction.

Feature attribution explains model behavior; it does not independently establish causality or prove malicious intent.

### Module 6 — Network Graph Intelligence

**Purpose:** Represent communication relationships as a graph.

A directed graph can represent source endpoints as nodes, destination endpoints as nodes, and observed flows as directed edges.

Potential graph features include:

- In-degree and out-degree
- Endpoint connectivity
- Neighbor-based traffic statistics
- Connected components
- Time-windowed communication patterns

Advanced implementations can compare graph-derived features with a tabular baseline and subsequently evaluate graph neural networks such as GraphSAGE.

**Output:** Endpoint relationship summaries and graph-derived evidence for investigation.

### Module 7 — Alert Correlation and Investigation

**Purpose:** Organize related predictions into meaningful investigation cases.

Potential capabilities:

- Group alerts by shared endpoints.
- Apply configurable time-window rules.
- Link related flow records.
- Preserve supporting evidence references.
- Record analyst notes and dispositions.
- Maintain a history of investigation changes.

Correlation rules must be tested against known scenarios to avoid grouping unrelated activity.

### Module 8 — MLOps and Model Governance

**Purpose:** Maintain reproducibility and traceability across model development and release.

Capabilities include:

- Experiment configuration and tracking
- Model and dataset version metadata
- Evaluation history
- Artifact checksums and manifests
- Regression evaluation gates
- Automated testing
- Data and model drift monitoring
- Model rollback procedures

MLflow can be used for experiment tracking, while a database or artifact store can maintain project-specific metadata.

### Module 9 — Analyst Dashboard and REST API

**Purpose:** Make model outputs accessible to analysts and other software.

The interface can provide:

- Dataset overview
- Prediction summaries
- Anomaly-score visualization
- Feature importance
- Graph analysis
- Investigation records
- Evaluation metrics
- Exportable results

The REST API exposes supported backend capabilities through documented request and response schemas.

---

## 8. Unique and Advanced Features

### 8.1 Dual-Signal Threat Detection

Combines supervised classification and anomaly detection.

**Why it matters:** A flow may receive a benign prediction but still look unusual relative to the training distribution. The disagreement creates an opportunity for further review.

### 8.2 Leakage-Aware Evaluation

The platform emphasizes detecting duplicate records, label-derived features, and inappropriate split strategies before trusting a model's metrics.

**Why it matters:** A seemingly excellent model can perform poorly on genuinely unseen network traffic if evaluation leakage is present.

### 8.3 Graph-Enhanced Investigation

Network relationships provide context that is absent from isolated predictions.

**Why it matters:** Analysts can examine groups of related flows rather than reviewing every alert independently.

### 8.4 Human-in-the-Loop Feedback

Analysts can label alerts and produce reviewed examples for subsequent model development.

**Advanced extension:** Use uncertainty sampling or classifier–anomaly disagreement to select informative samples for human review.

### 8.5 Model Drift and Regression Monitoring

The platform can compare reference and incoming data distributions and evaluate candidate models against fixed test sets.

**Why it matters:** A model that performs well on historical traffic may not remain effective as network behavior changes.

### 8.6 Evidence-Linked Investigation Reports

An investigation report should preserve the record reference, prediction, anomaly score, model version, relevant explanation, graph context, and analyst decision.

**Why it matters:** Findings become more traceable and easier to review.

### 8.7 Ablation-Based Model Comparison

Compare progressively richer models:

1. Tabular classification baseline
2. Classification plus anomaly features
3. Classification plus graph-derived features
4. Combined system with calibrated decision thresholds

This establishes whether each additional component produces measurable benefits.

---

## 9. Machine Learning Methodology

### Supervised learning

The supervised model learns a mapping between network-flow features and the training labels.

The general objective is to minimize prediction error while maintaining acceptable generalization on unseen records.

### Unsupervised learning

Anomaly detection learns a representation of typical observations or identifies outliers relative to the training distribution.

Anomaly scores should be calibrated against validation data before being used to prioritize alerts.

### Feature engineering

Candidate features include:

- Flow duration
- Forward and backward packet counts
- Total bytes
- Packet and byte rates
- Protocol information
- Source and destination port information, where appropriate
- Time-windowed endpoint statistics

Features must be selected according to the dataset schema. Target labels and inappropriate identifier fields must not be included as predictive inputs.

### Threshold selection

The default classification threshold may not be optimal for cybersecurity operations.

Select thresholds using validation data and the relative costs of missed attacks and false alerts. Do not tune the final threshold on the held-out test set.

---

## 10. Graph-Based Threat Intelligence

Graph analysis is a major differentiator of SentinelAI.

### Graph representation

Let a directed graph be represented as:

\[
G=(V,E)
\]

where:

- \(V\) represents observed network entities.
- \(E\) represents directed communication relationships.

Each edge can optionally store flow features, timestamps, prediction labels, and anomaly scores.

### Graph analysis workflow

1. Create nodes from authorized endpoint identifiers.
2. Create directed edges from observed communication flows.
3. Calculate graph statistics.
4. Enrich relevant flows with graph-derived features.
5. Compare graph-enhanced predictions against the baseline.
6. Display graph relationships for analyst review.

### Graph neural network extension

A GNN can learn node or edge representations by aggregating information from neighboring entities.

However, graph neural networks must be evaluated carefully. Randomly splitting highly related edges can leak information between training and testing data. Prefer temporal or group-aware evaluation where appropriate.

The value of the GNN must be demonstrated through measurable improvements rather than assumed in advance.

---

## 11. Explainable AI Framework

SentinelAI aims to make predictions easier to interpret.

### Global explanations

Show which features most influence the model across a dataset.

### Local explanations

Show which features contributed to a particular prediction, using an appropriate method such as SHAP.

### Explanation validation

Where feasible, evaluate:

- Stability across repeated runs
- Sensitivity to small input changes
- Consistency across model versions
- Usefulness for understanding false positives and false negatives

Explanations should be presented with the model output and its limitations, rather than as definitive proof that a particular feature caused an attack.

---

## 12. Dataset and Data Engineering

Suitable research datasets may include:

- CSE-CIC-IDS2018
- CICIDS2017
- UNSW-NB15

The exact dataset and version should be documented before reporting results.

### Data preparation steps

1. Download data from an authorized source.
2. Record the source, version, and applicable license.
3. Preserve raw files separately from processed data.
4. Validate column names, types, and label mappings.
5. Examine missing values, duplicates, and class imbalance.
6. Audit potential leakage and split contamination.
7. Build preprocessing pipelines using training data only.
8. Save the final split configuration and dataset metadata.
9. Evaluate against held-out data that was not used for tuning.

The included synthetic data, if used, is for testing the application workflow and must not be presented as evidence of real-world detection performance.

---

## 13. Evaluation Framework

SentinelAI should evaluate model quality using metrics appropriate for imbalanced classification.

| Metric | Purpose |
|---|---|
| Precision | Measures the proportion of predicted positive cases that are positive in the reference labels. |
| Recall | Measures the proportion of positive reference cases detected. |
| Macro-F1 | Summarizes class-level F1 scores with equal class weighting. |
| ROC-AUC | Measures ranking quality across classification thresholds. |
| PR-AUC | Evaluates precision–recall trade-offs, especially for imbalanced data. |
| False-positive rate | Measures the proportion of benign cases incorrectly flagged. |
| Confusion matrix | Shows the distribution of correct and incorrect predictions. |
| Inference latency | Measures prediction response time. |
| Memory usage | Measures resource requirements during inference and training. |

### Recommended experiments

- Classical ML baseline comparison
- Class imbalance handling
- Feature-ablation experiments
- Anomaly-score threshold analysis
- Graph-feature ablation
- Cross-capture or cross-dataset testing
- Explanation stability
- Drift simulation
- Repeated runs and confidence intervals

Results should include the dataset version, split strategy, model configuration, seed, and limitations.

---

## 14. Technology Stack

| Layer | Technologies |
|---|---|
| Language | Python |
| Data processing | Pandas, NumPy |
| Classical ML | Scikit-learn |
| Gradient boosting | XGBoost / LightGBM, where integrated |
| Deep learning | PyTorch |
| Graph analysis | NetworkX |
| Graph neural networks | PyTorch Geometric, where integrated |
| Explainable AI | SHAP, where integrated |
| API | FastAPI, Pydantic |
| Dashboard | Streamlit or React-based interface |
| Experiment tracking | MLflow |
| Database | SQLite / PostgreSQL |
| Testing | Pytest |
| Deployment | Docker |
| CI/CD | GitHub Actions |

The actual installed dependencies and implemented integrations should be reflected in the repository's dependency file.

---

## 15. Repository Structure

A recommended modular structure is:

```text
SentinelAI/
├── backend/
│   └── sentinelai/
│       ├── api.py
│       ├── data.py
│       ├── preprocessing.py
│       ├── train.py
│       ├── inference.py
│       ├── anomaly_detection.py
│       ├── explainability.py
│       ├── graph_analysis.py
│       ├── graph_learning.py
│       ├── alert_correlation.py
│       ├── investigation.py
│       ├── drift_monitor.py
│       └── reporting.py
├── dashboard/
│   ├── app.py
│   └── pages/
├── configs/
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── artifacts/
├── scripts/
├── tests/
├── docs/
├── .github/
│   └── workflows/
├── Dockerfile
├── Makefile
├── pyproject.toml
└── README.md
```

This tree is a reference structure. Keep only paths that exist in the actual repository and update the tree whenever modules are added or reorganized.

---

## 16. Installation and Setup

### Prerequisites

- Python 3.11 recommended
- Git
- pip
- A compatible development environment
- Optional: Docker

### Clone the repository

```bash
git clone <YOUR_SENTINELAI_REPOSITORY_URL>
cd SentinelAI
```

### Create a virtual environment

On macOS:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install dependencies

Use the repository's actual dependency configuration. For a project that defines a `dev` optional dependency group:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

If dependencies are defined in a requirements file instead, follow that file's installation instructions.

---

## 17. Running the Application

The following commands apply if the corresponding scripts and modules exist in the repository.

### Generate demonstration data

```bash
python scripts/generate_demo_data.py
```

### Train the baseline models

```bash
python -m sentinelai.train \
  --data data/sample/network_flows.csv \
  --target attack_label \
  --out artifacts
```

If the package is not installed and the repository uses a `backend/` source layout, install it in editable mode first or follow the repository's configured Python path.

### Start the API

```bash
uvicorn sentinelai.api:app --reload --host 127.0.0.1 --port 8000
```

### Start the dashboard

```bash
streamlit run dashboard/app.py
```

### Run tests

```bash
pytest
```

Open the local API documentation at:

`http://127.0.0.1:8000/docs`

Use the local address printed by Streamlit to open the dashboard.

---

## 18. API Documentation

Document each endpoint according to the actual API implementation.

A typical API design may include:

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Check service availability and model readiness. |
| `/predict` | POST | Generate predictions for supported flow records. |
| `/metrics` | GET | Retrieve available model evaluation metrics. |
| `/graph/analyze` | POST | Summarize endpoint relationships. |
| `/investigations` | GET / POST | Retrieve or create investigation cases, if implemented. |
| `/models` | GET | Retrieve model metadata, if implemented. |

Example prediction request for an API that supports these field names:

```json
{
  "records": [
    {
      "flow_duration": 120,
      "total_fwd_packets": 12,
      "total_bwd_packets": 8,
      "flow_bytes_s": 4200,
      "flow_packets_s": 55,
      "protocol": "TCP"
    }
  ]
}
```

The fields must match the model's expected input schema. The request above is illustrative and must be adapted to the trained model.

---

## 19. MLOps and Model Governance

Reliable threat detection requires more than training a model once.

SentinelAI's MLOps design should track:

- Dataset source and version
- Dataset checksum
- Feature schema
- Preprocessing configuration
- Model parameters and random seeds
- Training and evaluation metrics
- Model artifact version
- Experiment timestamps
- Evaluation-gate results
- Release and rollback history

### Model release workflow

```text
Dataset validation
        ↓
Model training
        ↓
Evaluation on validation data
        ↓
Regression and safety checks
        ↓
Compare with current model
        ↓
Approve or reject candidate
        ↓
Release approved model
        ↓
Monitor and evaluate drift
```

Candidate models should not replace a working model merely because they achieve a higher score on one metric. Evaluate false-positive rates, minority-class performance, generalization, and operational constraints before release.

---

## 20. Security and Privacy

SentinelAI must be developed and operated with appropriate safeguards.

- Process only network data that you are authorized to analyze.
- Keep raw sensitive traffic out of public repositories.
- Minimize or pseudonymize endpoint identifiers when possible.
- Protect stored datasets, model artifacts, logs, and investigation records.
- Add authentication and authorization before exposing sensitive APIs.
- Use rate limits and request-size limits.
- Validate uploaded files and incoming data schemas.
- Load model artifacts only from trusted sources.
- Preserve audit records for important model and investigation actions.
- Require human approval before operational remediation.

Predictions are advisory. The system should not automatically block endpoints or take disruptive actions solely because a model produces an alert.

---

## 21. Limitations

The platform's capabilities depend on the implemented modules, the quality of its datasets, and the evaluation methodology.

Important limitations include:

1. Offline network-flow analysis does not automatically imply live packet capture or real-time detection.
2. Anomaly detection identifies unusual behavior, not necessarily malicious behavior.
3. Class probabilities may be poorly calibrated.
4. Graph connectivity alone does not establish an attack.
5. Explanations describe model behavior and do not establish causality.
6. Dataset-specific performance may not generalize to other networks.
7. A graph neural network requires separate implementation and evaluation.
8. Production deployment requires additional authentication, access controls, observability, and operational testing.

Report only capabilities that have been implemented and verified. Do not claim benchmark performance without reproducible experimental evidence.

---

## 22. Future Enhancements

Potential directions for continued development include:

- Real-time flow ingestion and streaming inference
- More advanced graph neural network models
- Temporal graph analysis
- Cross-dataset generalization studies
- Active learning and analyst-feedback loops
- Calibrated risk scoring
- Confidence intervals and repeated-run evaluation
- Robustness testing under feature perturbations
- Advanced alert deduplication and correlation
- Multi-user investigation management
- Role-based access control
- Containerized inference services
- Scalable model serving
- Drift-triggered evaluation workflows
- Analyst-facing natural-language report generation grounded in stored evidence

These enhancements should be prioritized according to measured benefits, system requirements, and available resources.

---

## 23. Research Contributions

SentinelAI provides a foundation for investigating several research questions.

### Research Question 1
Does combining supervised classification with anomaly detection improve the prioritization of suspicious network flows?

### Research Question 2
Do graph-derived features improve detection performance compared with a tabular-only model under a leakage-resistant evaluation protocol?

### Research Question 3
How well do models trained on one network-traffic dataset generalize to a different dataset or capture environment?

### Research Question 4
How stable and useful are feature-level explanations when models are retrained or evaluated on changing traffic distributions?

### Research Question 5
Can analyst feedback and uncertainty-based sample selection improve the quality of subsequent training datasets?

### Experimental methodology

Evaluate each question through controlled experiments, consistent splits, ablation studies, appropriate baselines, and documented metrics.

The objective is to establish which components provide measurable value rather than assuming that combining more techniques automatically improves the system.

---

## 24. Portfolio and Resume Description

### Resume project title

**SentinelAI — Explainable AI-Powered Network Threat Detection and Investigation Platform**

### Resume description

Developed a modular cybersecurity analytics platform combining supervised threat classification, unsupervised anomaly detection, explainable AI, and graph-based network analysis. Designed data-quality and leakage checks, model evaluation workflows, and an investigation-oriented interface to support transparent analysis of suspicious network activity.

### Skills demonstrated

- Python and data engineering
- Supervised and unsupervised machine learning
- Feature engineering and model evaluation
- Explainable AI
- Graph analytics and graph learning research
- REST API development
- Experiment tracking and model governance
- Automated testing and CI/CD
- Cybersecurity analytics and data privacy

Add quantitative achievements only after experiments have been executed. Report actual dataset sizes, benchmark results, false-positive rates, latency, and other measured outcomes rather than estimated or invented figures.

---

## Conclusion

SentinelAI aims to move network threat detection beyond isolated classification predictions toward a more explainable and investigation-oriented AI/ML workflow.

Its core design combines data forensics, supervised learning, anomaly detection, graph analysis, model explanations, investigation support, and reproducible evaluation.

The central engineering objective is to produce a system whose predictions can be evaluated, whose reasoning can be inspected, and whose limitations are clearly documented.

**SentinelAI is intended as a research and decision-support platform for defensive cybersecurity—not as a substitute for security analysts or a guarantee of attack detection.**
