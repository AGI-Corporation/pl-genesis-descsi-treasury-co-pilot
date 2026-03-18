# PL-Genesis DeSci Treasury & Grants Co-Pilot

> **PL Genesis: Frontiers of Collaboration Hackathon** | Track: Flow · Crypto · Funding the Commons · Infrastructure & Digital Rights

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AGI Corporation](https://img.shields.io/badge/org-AGI--Corporation-blue)](https://github.com/AGI-Corporation)
[![Hackathon](https://img.shields.io/badge/hackathon-PL%20Genesis-purple)](https://pl-genesis-frontiers-of-collaboration-hackathon.devspot.app)

## Overview

A **consumer-grade DeSci treasury and grants co-pilot** specifically built for genomics/multi-omics labs, consortia, and public goods contributors. It automates on-chain program design, eligibility checks, payouts, and impact reporting — all governed by CMMC compliance policies and orchestrated via Route.X workflows.

**Core repos integrated:**
- [`CMMC`](https://github.com/AGI-Corporation/CMMC) — compliance engine, RBAC, policy evaluation
- [`Route.X`](https://github.com/AGI-Corporation/Route.X) — workflow orchestration & automation
- [`genomic-go-platform`](https://github.com/AGI-Corporation/genomic-go-platform) — domain schemas (cohorts, assays, projects)
- [`Sapient.x`](https://github.com/AGI-Corporation/Sapient.x) — omics program templates & evaluation rubrics
- [`AGI-Framework`](https://github.com/AGI-Corporation/AGI-Framework) — "Grant Architect" LLM agent

---

## Goals

- Let genomics labs set up on-chain treasuries and grant programs in minutes
- Enforce compliant access control and payout rules via CMMC policy engine
- Link grants and payouts to concrete genomic-go/Sapient.x research projects
- Enable retroactive funding and DAO-style governance via Flow contracts

---

## Hackathon Tracks & Sponsors

| Sponsor / Track | How this project qualifies |
|---|---|
| **Flow** — Future of Finance | Treasury and grant contracts deployed on Flow; walletless onboarding + sponsored gas |
| **Crypto** — Public Goods & Governance | On-chain grant programs with quadratic matching and community governance |
| **Funding the Commons** | Direct payout infrastructure for open science / DeSci contributors |
| **Infrastructure & Digital Rights** | CMMC-enforced data access control, export compliance, KYC for genomics data |
| **Fresh/Existing Code** | Reuses CMMC, Route.X, genomic-go-platform, Sapient.x |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   React Frontend                        │
│  Admin Dashboard │ Researcher Portal │ Compliance View  │
└──────────────────────┬──────────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────────┐
│                Treasury API (FastAPI / NestJS)          │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  CMMC       │  │  Route.X     │  │  genomic-go   │  │
│  │  Auth/RBAC  │  │  Workflows   │  │  + Sapient.x  │  │
│  │  Policies   │  │  Pipelines   │  │  Adapters     │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Flow Blockchain (Cadence)                  │
│   Treasury Contract │ GrantProgram │ Payout Contract     │
└─────────────────────────────────────────────────────────┘
        │
        ▼
  Event Listener → App State Updates
```

**Route.X Pipeline:**
```
CreateProgram → ReviewApplication → PolicyCheck (CMMC) → ApproveAndPayout → ReportImpact
```

---

## Data Schema

```typescript
Organization {
  id: string
  name: string
  onchain_address: string
  compliance_profile: ComplianceProfile
  legal_metadata: object
}

Treasury {
  id: string
  org_id: string
  chain: "flow" | "evm"
  asset_type: string
  balance: number
  risk_flags: string[]
}

GrantProgram {
  id: string
  org_id: string
  title: string
  description: string
  omics_focus: string[]  // e.g. ["biomarker", "genomics", "proteomics"]
  eligibility_rules: PolicyRule[]
  budget: number
  payout_schedule: ScheduleConfig
}

Application {
  id: string
  applicant_org_id: string
  grant_program_id: string
  linked_genomic_go_project_id: string
  rubric_scores: Record<string, number>
  KYC_status: "pending" | "approved" | "rejected"
  status: "submitted" | "in_review" | "approved" | "funded" | "rejected"
}

Payout {
  id: string
  application_id: string
  treasury_id: string
  amount: number
  schedule: ScheduleConfig
  onchain_tx_hash: string
  status: "pending" | "sent" | "confirmed" | "failed"
}

PolicyRule {
  id: string
  expression: string  // Rego / JSONLogic
  attached_entity_type: string
  severity: "info" | "warn" | "block"
}
```

---

## Repo Structure

```
pl-genesis-descsi-treasury-co-pilot/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── schema.md
│   └── demo-script.md
├── backend/                    # FastAPI / NestJS Treasury API
│   ├── app/
│   │   ├── routes/
│   │   │   ├── orgs.py
│   │   │   ├── grant_programs.py
│   │   │   ├── applications.py
│   │   │   └── payouts.py
│   │   ├── services/
│   │   │   ├── cmmc_client.py      # CMMC policy engine integration
│   │   │   ├── routex_client.py    # Route.X workflow integration
│   │   │   ├── genomicgo_client.py # genomic-go-platform adapter
│   │   │   └── flow_client.py      # Flow blockchain client
│   │   └── models/
│   │       ├── organization.py
│   │       ├── treasury.py
│   │       ├── grant_program.py
│   │       ├── application.py
│   │       └── payout.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React dashboard
│   ├── src/
│   │   ├── pages/
│   │   │   ├── AdminDashboard.tsx
│   │   │   ├── ResearcherPortal.tsx
│   │   │   └── ComplianceView.tsx
│   │   └── components/
│   ├── package.json
│   └── Dockerfile
├── contracts/                  # Flow Cadence smart contracts
│   ├── Treasury.cdc
│   ├── GrantProgram.cdc
│   └── Payout.cdc
├── routex/
│   └── workflows/
│       └── grants-lifecycle.yml
├── cmmc/
│   └── policies/
│       ├── grants-access-control.rego
│       └── payout-compliance.rego
└── docker-compose.yml
```

---

## API Endpoints (MVP)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/orgs` | Create organization |
| `POST` | `/grant-programs` | Define grant (title, budget, omics_focus, rules) |
| `GET` | `/grant-programs` | List with filters |
| `POST` | `/grant-programs/{id}/applications` | Submit application (links genomic-go project) |
| `POST` | `/applications/{id}/review` | Record rubric scores + decision |
| `POST` | `/applications/{id}/payouts` | Trigger on-chain payout via Flow |
| `GET` | `/policies` | List active CMMC compliance policies |

---

## User Stories

1. **Lab Admin** — Create a grant program (omics focus, budget, rules) and deploy it on-chain with one click
2. **Researcher** — Apply to a grant by linking my genomic-go project ID and track funding status
3. **Governance Officer** — Define compliance policies (KYC, export limitations) and verify all payouts conform
4. **Donor / DAO** — Audit tamper-evident receipts that link funds to concrete studies

---

## Demo Script

1. Create an org and grant program ("Biomarker Discovery Micro-Grant")
2. Show a genomic-go project, apply using that project ID
3. As admin: review and approve the application — CMMC policy "OK" badge shown
4. Click "Payout" → Flow Explorer transaction shown, UI updates to "Funded"

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Smart Contracts | Flow Cadence |
| Backend | FastAPI (Python) or NestJS |
| Policy Engine | CMMC (OPA/Rego) |
| Workflow Orchestration | Route.X |
| Domain Models | genomic-go-platform + Sapient.x |
| LLM Agent | AGI-Framework (eliza-based) "Grant Architect" |
| Frontend | React + TailwindCSS |
| Infra | Docker, GitHub Actions CI |

---

## Getting Started

```bash
git clone https://github.com/AGI-Corporation/pl-genesis-descsi-treasury-co-pilot
cd pl-genesis-descsi-treasury-co-pilot
cp .env.example .env
docker-compose up
```

Visit `http://localhost:3000` for the frontend and `http://localhost:8000/docs` for the API.

---

## Contributing

PR welcome. Please follow the [AGI Corporation contributing guidelines](https://github.com/AGI-Corporation).

---

## License

MIT — see [LICENSE](LICENSE)

---

*Built for the [PL Genesis: Frontiers of Collaboration Hackathon](https://pl-genesis-frontiers-of-collaboration-hackathon.devspot.app) by AGI Corporation*
