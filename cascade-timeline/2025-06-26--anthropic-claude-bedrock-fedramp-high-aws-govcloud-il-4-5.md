---
type: timeline_event
id: 2025-06-26--anthropic-claude-bedrock-fedramp-high-aws-govcloud-il-4-5
date: 2025-06-26
title: "Anthropic Claude in Amazon Bedrock Cleared for FedRAMP High and DoD IL-4/5 in AWS GovCloud"
importance: 8
status: confirmed
actors:
  - Anthropic
  - Amazon Web Services
  - U.S. Federal Government
  - Department of Defense
  - DISA
tags:
  - anthropic
  - claude
  - fedramp-high
  - dod-impact-level-5
  - aws-govcloud
  - bedrock
  - federal-ai
  - tech-stack
  - investigation-surveillance-inc
sources:
  - title: "Claude in Amazon Bedrock: Approved for Use in FedRAMP High and DoD IL4/5 Workloads"
    url: https://www.anthropic.com/news/claude-in-amazon-bedrock-fedramp-high
    outlet: Anthropic
    date: '2025-06-26'
    tier: 1
  - title: "AWS GovCloud gets high-level security approvals for Anthropic and Meta AI models"
    url: https://www.nextgov.com/artificial-intelligence/2025/06/aws-govcloud-gets-high-level-security-approvals-anthropic-and-meta-ai-models/405995/
    outlet: Nextgov/FCW
    date: '2025-06-26'
    tier: 2
capture_lanes:
  - Surveillance infrastructure
  - Critical-infrastructure dependency
coverage: []
---

## Opening

On June 26, 2025, Amazon Web Services and Anthropic announced that **Claude 3.5 Sonnet v1 and Claude 3 Haiku in Amazon Bedrock** had been authorized for **FedRAMP High** and **Department of Defense Impact Level 4 / Impact Level 5** workloads in AWS GovCloud (US). AWS publicly described itself as the first cloud provider to clear these authorization tiers for foundation models — completing the federal AI-substrate gating event of the second-administration buildout. By the close of June 2025, both **Azure OpenAI Service** (FedRAMP High since September 2024; Top Secret since January 2025) and **AWS GovCloud Claude** were FedRAMP-High and IL-5 authorized for federal customers.

## What Happened

The June 26 authorization documented:

1. **Claude 3.5 Sonnet v1** — Anthropic's strongest publicly-available model class as of mid-2025, available through Amazon Bedrock's inference API in AWS GovCloud (US-West and US-East regions).
2. **Claude 3 Haiku** — Anthropic's faster, less-expensive model class available through the same channel.
3. **Meta's Llama models** — also cleared for FedRAMP High and IL-4/5 in the same AWS announcement.

The Anthropic federal posture is deployed **through AWS GovCloud and through Amazon Bedrock**, not through a direct Anthropic-operated federal endpoint. Federal customers can call Claude inference via Bedrock APIs from inside their AWS GovCloud tenancy; the underlying model weights are operated by AWS as the host vendor under AWS's existing FedRAMP and IL-4/5 authorization regime.

This is **categorically different infrastructure** from the OpenAI federal posture: OpenAI deploys via Microsoft Azure OpenAI Service (Microsoft-operated) inside Azure Government, with separate authorization documents, separate inference-routing topologies, and a separate host-vendor compliance regime. Reporting on "AI for the federal government" that elides this distinction is structurally misleading.

## Why This Event Matters

By end of June 2025 — five months into the second administration — both major hyperscaler regions (Azure Government via OpenAI; AWS GovCloud via Anthropic) had cleared FedRAMP High and DoD IL-5 authorization for frontier-model LLM inference. This is the **engineering-substrate gating event** documented in Layer 3 of [[tech-stack-of-surveillance-inc-engineering-substrate-2010-2026]].

The structural significances are:

1. **Federal customers can now run RAG-based surveillance applications at IL-5.** Agency case files, interview transcripts, FOIA responses, social-media archives, and broker-acquired data can be vector-embedded and made available as context to an LLM at inference time, all inside FedRAMP-High and IL-5 boundaries. The architectural pattern (retrieval-augmented surveillance) is now contractually supported on both major hyperscalers.

2. **Two-vendor frontier-AI federal substrate locked in.** The OpenAI-on-Azure-Government and Anthropic-on-AWS-GovCloud deployments are the two options for federal customers wanting commercial-grade frontier-model inference at classified-tier authorization. The substrate is gated to two vendors.

3. **The June 2025 cluster context.** This authorization sits in the same month as:
   - **June 1, 2025** — Palantir wins $30M ICE ImmigrationOS contract
   - **June 5, 2025** — Anduril Series G with Founders Fund $1B check (largest in fund history)
   - **June 17, 2025** — Wyden-Goldman-Velázquez letter to Karp on ICE surveillance
   - **June 26, 2025** — this event

   The cluster makes June 2025 the **single most consequential month** of the [[trump-2-surveillance-procurement-chronology-2025-2026]] consolidation.

## Broader Context

The June 26 authorization was followed five months later by the **November 12, 2025** addition of **Claude Sonnet 4.5** to Amazon Bedrock in AWS GovCloud (US-West and US-East) via U.S.-Gov Cross-Region Inference — extending federal-customer access to the strongest Claude model class as of late 2025.

The subsequent Anthropic-Pentagon dispute (February-March 2026, per [[2026-02-24--hegseth-threatens-anthropic-blacklist-military-ai-access]] through [[2026-03-09--anthropic-files-dual-lawsuits-pentagon-supply-chain-designation]]) was triggered by the Pentagon's attempt to overcome Anthropic's "red lines" around use cases — but the underlying Anthropic federal substrate authorization (this entry) was not formally rescinded. The dispute is over use-case scoping, not authorization-tier gating.

Per the [[tech-stack-of-surveillance-inc-engineering-substrate-2010-2026]] theme: the categorically important observation is **not** that AWS, Azure, and GCP coordinate. They compete; AWS, Azure, and GCP fight bitterly over individual JWCC task orders. The structural fact is that each holds enough federal contract volume to be a critical-infrastructure dependency, and the federal AI-inference layer is gated to two foundation-model vendors (OpenAI / Anthropic) with Meta Llama as a third on the open-weights track.

## Research Gaps

- [ ] **Specific federal customer adoption** — which DoD components, intelligence-community clients, and civilian-agency teams have actually deployed Claude-via-Bedrock in AWS GovCloud since June 2025?
- [ ] **Total Anthropic federal contract volume** — pre-Pentagon-dispute (Feb 2026), what was the dollar value of Anthropic federal customer commitments through Bedrock?
- [ ] **Anthropic Use Case Policy enforcement at the federal-deployment level** — how does Anthropic enforce its use-case policy when models are operated by AWS as host? The boundary is the legal substrate of the February 2026 Pentagon dispute.
- [ ] **The classified-tier AWS regions** (Secret Region, Top Secret Region) — Claude availability through Amazon SageMaker in those regions is referenced in some documentation; primary-source dates and authorization-tier specifics deserve research.

## Related Entries

- [[trump-2-surveillance-procurement-chronology-2025-2026]]
- [[tech-stack-of-surveillance-inc-engineering-substrate-2010-2026]]
- [[2025-01-28--openai-launches-chatgpt-gov-federal-ai-product-surface]]
- [[2026-02-24--hegseth-threatens-anthropic-blacklist-military-ai-access]]
- [[2026-02-26--anthropic-rejects-pentagon-ultimatum-red-lines]]
- [[2026-03-06--anthropic-sues-dod-supply-chain-risk-designation]]
