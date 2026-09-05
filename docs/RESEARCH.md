# Research Findings — Software Engineering Skills System

Phase 1 output. Consumer: the Phase 2 implementation agent and any maintainer who needs to know *why* the system is shaped the way it is and *what evidence* each reference file may cite.

Research date: 2026-09-04.

## 0. How to read this document

Every substantive claim carries one evidence label:

| Label | Meaning |
|---|---|
| `VERIFIED` | Read directly from the primary source during this research (URL listed in §11). |
| `STANDARD` | Content of a formal standard, read from the standard itself or from a faithful secondary summary when the primary page was inaccessible (noted per item). |
| `ACADEMIC` | From an official curriculum body or university catalog. |
| `INDUSTRY` | Widely adopted industry practice with a recognized primary source (not a standard). |
| `RECOMMENDATION` | Engineering practice this project recommends; grounded in the above but not mandated by any of them. |
| `INFERENCE` | Conclusion drawn by the researcher from the evidence; not stated by a source. |
| `DECISION` | Design choice made for this system (cross-referenced in `DECISIONS.md`). |
| `UNVERIFIED` | Recalled or reported second-hand and not confirmed during this research. Do not cite as fact in skill/reference files without re-verification. |

Rule for Phase 2: reference files inside the repository may only state as fact what is `VERIFIED`, `STANDARD`, or `ACADEMIC` here. Anything `UNVERIFIED` must be re-verified or dropped.

## 1. Method

- Three batched research rounds; independent questions run in parallel; dependent follow-ups only where a primary page failed.
- Source priority: standards bodies → official organizations → official curricula → primary technical docs → academic → recognized industry sources → secondary articles (context only).
- Access log: `iso.org` returned HTTP 403 for every standard page (12207, 25010, 29148); those were reconstructed from secondary sources and are labeled accordingly. `ox.ac.uk` admissions page returned 403; Stanford's old requirements URL 404 (bulletin used instead). NIST SP 800-218 PDF was downloaded and text-extracted locally (pypdf) to read practice names.
- Supplied practical sources: the prompt named "Artia", "UpSites" and "the supplied YouTube resource" but no URLs were supplied. Artia and UpSites articles were located by search and read. **No YouTube URL was supplied, so no YouTube content was accessed or used.** Nothing in this system is derived from a video.

## 2. Formal standards and bodies of knowledge

### 2.1 SWEBOK Guide v4.0 (IEEE Computer Society, 2024) — `VERIFIED`

18 knowledge areas. Three are new in v4 relative to v3: **Software Architecture**, **Software Engineering Operations**, **Software Security**.

Full list: Software Requirements; Software Architecture; Software Design; Software Construction; Software Testing; Software Engineering Operations; Software Maintenance; Software Configuration Management; Software Engineering Management; Software Engineering Process; Software Engineering Models and Methods; Software Quality; Software Security; Software Engineering Professional Practice; Software Engineering Economics; Computing Foundations; Mathematical Foundations; Engineering Foundations.

Implication (`INFERENCE`): the profession's own body of knowledge now treats architecture, operations and security as first-class disciplines, not sub-topics. The skill taxonomy gives each a dedicated skill. KA topic-level detail was not fetched (`UNVERIFIED` beyond KA names).

### 2.2 ISO/IEC/IEEE 12207:2017 — Software life cycle processes — `STANDARD` (via Wikipedia; iso.org 403)

Four process groups and their processes:

- **Agreement**: Acquisition; Supply.
- **Organizational project-enabling**: Life cycle model management; Infrastructure management; Portfolio management; Human resource management; Quality management; Knowledge management.
- **Technical management**: Project planning; Project assessment and control; Decision management; Risk management; Configuration management; Information management; Quality assurance.
- **Technical**: Business or mission analysis; Stakeholder needs and requirements definition; System/software requirements definition; Architecture definition; Design definition; System analysis; Implementation; Integration; Verification; Transition; Validation; Operation; Maintenance; Disposal.

Notes: 12207:2017 is harmonized with ISO/IEC/IEEE 15288 (systems). Wikipedia additionally claims a 2026 edition completed that harmonization — `UNVERIFIED` (could not confirm on iso.org). Skills must cite "12207:2017".

Implication (`INFERENCE`): the technical process list is the most authoritative backbone for the lifecycle. The system's stage names are mapped to it in §9.1. "Disposal" is out of scope except as data-lifecycle/deprecation guidance.

### 2.3 ISO/IEC 25010:2023 — Product quality model — `STANDARD` (via iso25000.com, arc42 quality site, spree.de summary; iso.org 403)

Nine characteristics (2011 edition had eight):

| Characteristic | Sub-characteristics |
|---|---|
| Functional suitability | functional completeness, functional correctness, functional appropriateness |
| Performance efficiency | time behaviour, resource utilization, capacity |
| Compatibility | co-existence, interoperability |
| Interaction capability (formerly *Usability*) | appropriateness recognizability, learnability, operability, user error protection, user engagement, inclusivity, user assistance, self-descriptiveness |
| Reliability | faultlessness (formerly *maturity*), availability, fault tolerance, recoverability |
| Security | confidentiality, integrity, non-repudiation, accountability, authenticity, resistance (new) |
| Maintainability | modularity, reusability, analysability, modifiability, testability |
| Flexibility (formerly *Portability*) | adaptability, scalability (new), installability, replaceability |
| Safety (new) | operational constraint, risk identification, fail safe, hazard warning, safe integration |

Source discrepancy resolved: the arc42 quality page listed *testability* under Flexibility. The spree.de edition summary lists Flexibility as adaptability, installability, replaceability, scalability (no testability), consistent with the 2011 structure where testability is under Maintainability. This document adopts testability under **Maintainability** (`INFERENCE` from two sources against one).

Implication (`DECISION` D-09): 25010:2023 is the single quality vocabulary used across requirements (NFR categories), architecture (quality attribute scenarios), testing (what each test level verifies) and operations (SLIs).

### 2.4 ISO/IEC/IEEE 29148:2018 — Requirements engineering — `STANDARD` (partial, via Wikipedia SRS article)

Verified: 29148 superseded IEEE 830 (2011; current revision 2018); it defines information items BRS (business), StRS (stakeholder), SyRS (system) and SRS (software); it specifies quality criteria for individual requirements ("necessary, appropriate, unambiguous") and for requirement sets ("complete, consistent, feasible, comprehensible"); it warns against requirement "smells" (subjective language, ambiguous adverbs/adjectives, superlatives, negative statements, non-verifiable terms).

`UNVERIFIED`: the fuller individual-requirement list commonly attributed to 29148 (necessary, appropriate, unambiguous, complete, singular, feasible, verifiable, correct, conforming). Phase 2 may use the verified subset as "29148" and present the rest as `RECOMMENDATION` unless re-verified.

### 2.5 ISO/IEC/IEEE 42010:2022 — Architecture description — `STANDARD` (via Wikipedia)

Current edition November 2022 (lineage: IEEE 1471:2000 → ISO/IEC 42010:2011 → 2022). Core concepts: stakeholders and concerns; viewpoints and views; models; architecture decisions with rationale; correspondences. Strict distinction between an architecture and its description. It does not endorse any specific notation; C4/arc42/4+1 are independent industry frameworks (`INDUSTRY`).

### 2.6 ISO/IEC/IEEE 29119 — Software testing — `STANDARD` (via Wikipedia)

Five parts: 1 Concepts and definitions (2022); 2 Test processes (2021); 3 Test documentation (2021); 4 Test techniques (2021); 5 Keyword-driven testing (2024). Part 2 defines a three-layer process model: organizational test process, test management processes, dynamic test processes (static testing excluded). Part 4 groups techniques as specification-based, structure-based, experience-based.

Disagreement on record: professional associations (Association for Software Testing, International Society for Software Testing) petitioned against 29119 citing documentation heaviness and incompatibility with context-driven testing. `DECISION` D-11: adopt its *concepts* (levels, technique families, strategy → plan → completion evidence) in lightweight artifacts; do not adopt its full documentation set.

## 3. Secure development

### 3.1 NIST SP 800-218, SSDF v1.1 (February 2022) — `VERIFIED` (PDF text extracted)

Four practice groups, 19 practices (PW.3 was merged into PW.4 in v1.1):

**Prepare the Organization (PO)**
- PO.1 Define Security Requirements for Software Development
- PO.2 Implement Roles and Responsibilities
- PO.3 Implement Supporting Toolchains
- PO.4 Define and Use Criteria for Software Security Checks
- PO.5 Implement and Maintain Secure Environments for Software Development (new in v1.1)

**Protect the Software (PS)**
- PS.1 Protect All Forms of Code from Unauthorized Access and Tampering
- PS.2 Provide a Mechanism for Verifying Software Release Integrity
- PS.3 Archive and Protect Each Software Release

**Produce Well-Secured Software (PW)**
- PW.1 Design Software to Meet Security Requirements and Mitigate Security Risks
- PW.2 Review the Software Design to Verify Compliance with Security Requirements and Risk Information
- PW.4 Reuse Existing, Well-Secured Software When Feasible Instead of Duplicating Functionality
- PW.5 Create Source Code by Adhering to Secure Coding Practices
- PW.6 Configure the Compilation, Interpreter, and Build Processes to Improve Executable Security
- PW.7 Review and/or Analyze Human-Readable Code to Identify Vulnerabilities and Verify Compliance with Security Requirements
- PW.8 Test Executable Code to Identify Vulnerabilities and Verify Compliance with Security Requirements
- PW.9 Configure Software to Have Secure Settings by Default

**Respond to Vulnerabilities (RV)**
- RV.1 Identify and Confirm Vulnerabilities on an Ongoing Basis
- RV.2 Assess, Prioritize, and Remediate Vulnerabilities
- RV.3 Analyze Vulnerabilities to Identify Their Root Causes

Status (`VERIFIED`, NIST SSDF project page, updated 2026-04-13): v1.1 is current; no v1.2 exists. SP 800-218A is a finalized community profile for generative AI and dual-use foundation models that augments 800-218.

### 3.2 OWASP SAMM v2.0 — `VERIFIED`

Structure: 5 business functions × 3 practices × 2 streams × 3 maturity levels.

- Governance: Strategy & Metrics; Policy & Compliance; Education & Guidance
- Design: Threat Assessment; Security Requirements; Secure Architecture
- Implementation: Secure Build; Secure Deployment; Defect Management
- Verification: Architecture Assessment; Requirements-driven Testing; Security Testing
- Operations: Incident Management; Environment Management; Operational Management

Threat Assessment streams (verified): A — Application Risk Profile (L1 basic likelihood/impact; L2 centralized inventory; L3 periodic review); B — Threat Modeling (L1 best-effort risk-based with brainstorming and simple checklists; L2 standardized training/process/tools; L3 continuous refinement and automation).

### 3.3 OWASP ASVS 5.0.0 (released 2025-05-30) — `VERIFIED`

Chapters V1–V17: Encoding and Sanitization; Validation and Business Logic; Web Frontend Security; API and Web Service; File Handling; Authentication; Session Management; Authorization; Self-contained Tokens; OAuth and OIDC; Cryptography; Secure Communication; Configuration; Data Protection; Secure Coding and Architecture; Security Logging and Error Handling; WebRTC.

Levels: L1 ≈ 20% of requirements, first-layer defenses against common attacks; L2 ≈ 50% more (≈70% cumulative), less-common attacks and more complex protections; L3 remaining ≈ 30%, defense-in-depth for highest assurance. Six declared uses: architecture guidance, secure-coding reference, automated test design, training, procurement, risk-based compliance.

### 3.4 OWASP Top 10:2025 — `VERIFIED`

A01 Broken Access Control; A02 Security Misconfiguration; A03 Software Supply Chain Failures; A04 Cryptographic Failures; A05 Injection; A06 Insecure Design; A07 Authentication Failures; A08 Software or Data Integrity Failures; A09 Security Logging and Alerting Failures; A10 Mishandling of Exceptional Conditions.

### 3.5 Threat Modeling Manifesto — `INDUSTRY`, `VERIFIED`

Four questions: What are we working on? What can go wrong? What are we going to do about it? Did we do a good enough job? Values (e.g., finding and fixing design issues over checkbox compliance; doing threat modeling over talking about it; continuous refinement over a single delivery). Anti-patterns: hero threat modeler, admiration for the problem, tendency to over-focus, perfect representation. STRIDE is not part of the manifesto (`INDUSTRY`, widely used; not verified here).

## 4. Agile — Scrum Guide 2020 — `VERIFIED`

- Definition: "a lightweight framework that helps people, teams and organizations generate value through adaptive solutions for complex problems." Purposefully incomplete.
- Theory: empiricism and lean thinking; pillars transparency, inspection, adaptation. Values: commitment, focus, openness, respect, courage.
- Team: Developers, Product Owner, Scrum Master (accountabilities, not job titles); typically ≤ 10 people.
- Events: Sprint (≤ 1 month, container); Sprint Planning (≤ 8 h for a one-month Sprint); Daily Scrum (15 min); Sprint Review (≤ 4 h); Sprint Retrospective (≤ 3 h).
- Artifacts and commitments: Product Backlog → Product Goal; Sprint Backlog → Sprint Goal; Increment → Definition of Done.
- The guide states that leaving out elements or changing its core design "covers up problems and limits the benefits of Scrum" and "the result is not Scrum".

Implication (`DECISION` D-10): the system uses Scrum's artifacts, commitments and event purposes as its *organizational vocabulary* under a skill named `agile-delivery`, and explicitly does **not** claim a solo AI agent is "doing Scrum". Scrum organizes iteration; it is not a substitute for any engineering discipline.

## 5. Computer science and software engineering education

### 5.1 ACM/IEEE-CS/AAAI CS2023 — `ACADEMIC`, `VERIFIED` (KA list only)

Endorsed by ACM (2024-01-18), IEEE-CS (2024-01-22), AAAI (2024-02-22). 17 knowledge areas: AL Algorithmic Foundations; AR Architecture and Organization; AI Artificial Intelligence; DM Data Management; FPL Foundations of Programming Languages; GIT Graphics and Interactive Techniques; HCI Human-Computer Interaction; MSF Mathematical and Statistical Foundations; NC Networking and Communication; OS Operating Systems; PDC Parallel and Distributed Computing; SEC Security; SEP Society, Ethics, and the Profession; SDF Software Development Fundamentals; SE Software Engineering; SPD Specialized Platform Development; SF Systems Fundamentals.

`UNVERIFIED`: CS Core / KA Core hour allocations and the SE KA's knowledge-unit breakdown (report PDFs not read).

### 5.2 University programs — `ACADEMIC` (catalog pages; see access notes)

| Program | Math foundations | Programming | Algorithms / theory | Systems | SE-specific requirement | Notes / access |
|---|---|---|---|---|---|---|
| MIT 6-3 (CS & Engineering) — `VERIFIED` | 6.1200 Math for CS + one of probability/inference/linear algebra | 6.100A/B or 6.1000/6.1010; 6.1903 low-level C/assembly | 6.1210 Intro Algorithms; 6.1400 or 6.1220 | 6.1910 Computation Structures; one of 6.1800 Systems Eng / 6.1810 OS / 6.5831 Databases | **6.1020 Software Construction required** | Tracks; ≥12 units AI |
| Stanford BS CS — `VERIFIED` (bulletin) | MATH 19/20/21 + electives | CS106B | CS161 (CS107, CS111 systems) | CS107, CS111 | **None required**; 9 tracks + senior project | Tracks: AI, Comp Bio, Comp Eng, HCI, Information, Systems, Theory, Visual Computing, Unspecialized/Individually Designed |
| CMU BS CS — `VERIFIED` (catalog) | 15-151, 21-120, 21-122, 21-241/242, multivariable calc, probability | 15-122 imperative, 15-150 functional | 15-210 parallel/sequential DS&A, 15-251 theory, 15-451 algorithms | 15-213 computer systems; Software Systems elective | **17-313 is an elective** (Domains) | Also required: AI, Logic/Languages, Domains electives |
| Oxford CS — partial | Linear Algebra, Discrete and Continuous Mathematics, Logic and Proof (course names `VERIFIED`) | Functional, Imperative, Concurrent Programming (`VERIFIED`) | Design and Analysis of Algorithms, Models of Computation, Complexity (`VERIFIED`) | Digital Systems, Computer Architecture, Networks, Security, Compilers, Databases (`VERIFIED` as offered) | No course named "Software Engineering" on the alphabetical listing; Group Design Practical exists | Year structure only verified as Core 1 / Core 2 + options / options + project / advanced; mapping of subjects to years is `INFERENCE` |
| ETH Zurich BSc CS — `VERIFIED` | Discrete Math, Linear Algebra, Analysis I/II, Probability & Statistics, Numerical Methods | Intro Programming, Parallel Programming, Systems Programming | Data Structures and Algorithms; Algorithms and Probability; Theoretical CS; Formal Methods and Functional Programming | Digital Design and Computer Architecture; Computer Networks; Data Modelling and Databases | "Systems & software engineering" is one of three third-year **majors** | No standalone SE course listed |
| Waterloo BSE (Software Engineering) — `VERIFIED` (program page) | MATH 115/117/119/135, SE 212 Logic and Computation | CS 137/138 | Algorithms in upper years | SE 350 Operating Systems, ECE digital circuits | **SE 464 Software Design and Architectures; SE 465 Software Testing and QA; SE 101 methods; team design project** (`VERIFIED`); SE 463 Requirements (`UNVERIFIED`, not on the fetched page) | Joint Engineering/Math, co-op only; page explicitly contrasts CS (theory of computation) with SE (engineering principles applied to software) |

### 5.3 Synthesis: what is consistent across strong CS programs vs. characteristic of SE programs — `INFERENCE`

Consistently present in the CS programs examined: discrete mathematics and logic; linear algebra; probability; calculus; imperative *and* functional programming; data structures and algorithms with complexity analysis; computability/complexity theory; computer architecture and systems programming; operating systems; concurrency/parallelism; networking; databases (as one systems option); a capstone or group project.

Characteristic of SE programs (Waterloo) or of the SE knowledge areas (SWEBOK, CS2023-SE) but elective or absent in most CS programs: requirements engineering; software architecture and design as a taught discipline; software testing and quality assurance; software process, project and configuration management; large-scale team-based construction. MIT is the notable exception with a required Software Construction subject (specifications, testing, abstraction, design for change).

Design implication (`DECISION` D-03): an LLM agent already carries the CS-program content as latent knowledge; what it lacks is *disciplined procedure* and *the trigger for when a foundation matters*. Therefore the system encodes SE disciplines as procedural skills, and CS foundations as compact decision-support references ("when does complexity / consistency / concurrency / data structure choice change the engineering decision?"), not as tutorials.

## 6. Practical SDLC sources supplied by the user

### 6.1 Artia — "Projeto de desenvolvimento de software: 9 passos" (2024-02-19) — secondary, `VERIFIED` read

Nine steps framed as questions: 1) What does the client need? (interviews, document findings) 2) What must the software deliver? (functional + non-functional requirements) 3) Is it feasible? (resources, technical/regulatory constraints, scope adjustment) 4) How will processes be organized? (methodology choice: agile/waterfall/hybrid by complexity, team, culture) 5) How will it be developed? (WBS with owners and estimates) 6) Timeline? (milestones and buffers) 7) Is it progressing? (communication, controlled change, continuous QA) 8) Were needs met? (deploy, configure, train, gather feedback) 9) Is it functioning? (monitoring, security, feedback, preventive maintenance). Emphasizes documentation throughout and that requirements are iterative.

### 6.2 UpSites — "Etapas do desenvolvimento de um software" (2025-05-29, updated 2026-06-26) — secondary, `VERIFIED` read

Seven stages: 1) Briefing and requirements gathering; 2) Planning and prototyping (wireframes, technology choice, MVP roadmap, estimates); 3) Architecture and software design (backend/frontend structure, integrations, security, scalability, performance); 4) Development in iterative sprints with Git and reviews; 5) Testing and validation (automated + manual, user validation, load/security/stress); 6) Launch and publication (deploy, integrations, training, technical documentation); 7) Support and continuous evolution (monitoring, support, updates, improvement planning).

### 6.3 YouTube resource — title only

Phase 1: no URL was supplied; nothing was accessed. Phase 2 addendum (2026-09-04): the user supplied `https://www.youtube.com/watch?v=NgvTsyecAU8`. Fetching the watch page returned only the title — **"Você Não Começa um Software Escrevendo Código"** ("You don't start software by writing code") — and the oEmbed endpoint returned the channel **Loid Padre** (`@LoidPadreDev`). No transcript, description or chapter list was retrievable, so no content from the video is incorporated. The title is consistent with this system's discovery-first ordering but is not used as evidence for it (`VERIFIED` title/channel only; content `UNVERIFIED`).

### 6.4 Reconciliation — `INFERENCE`

Both practical sources agree with each other and with 12207's technical processes on the shape: understand need → specify → check feasibility → plan → design → build iteratively → test → deploy with training/docs → operate and evolve. They add two practical emphases that standards under-weight: (a) *feasibility as an explicit early gate*; (b) *user training and handover documentation at launch*. Both are adopted (discovery gate; deployment plan includes handover). Neither source addresses security engineering, observability or incident response with any depth — those come from SSDF/SAMM/SRE.

## 7. Industry practice anchors — `INDUSTRY`, `VERIFIED`

- **ADR** (adr.github.io): decision record per architecturally significant decision; Nygard 2011 template: Title, Status, Context, Decision, Consequences; MADR as alternative; statuses proposed / accepted / deprecated / superseded.
- **C4 model** (Simon Brown): four core levels — System Context, Container, Component, Code — plus System Landscape, Dynamic and Deployment diagrams; notation- and tooling-independent.
- **DORA metrics** (dora.dev, current guide): Deployment Frequency; Change Lead Time; Change Fail Rate; Failed Deployment Recovery Time (replaced MTTR); Deployment Rework Rate. Speed and stability are not trade-offs. Thresholds not on the fetched page (`UNVERIFIED`).
- **Google SRE — SLOs**: SLI (quantitative indicator), SLO (target), SLA (contract with consequences); use percentiles not averages; few SLOs; avoid absolutes; error budgets as control loop.
- **Google SRE — Incident management**: roles Incident Commander, Operations Lead, Communications Lead, Planning Lead; live incident state document; explicit handoff; declare when multiple teams involved, user-visible impact, or unresolved after ~1 hour.
- **Google SRE — Postmortem culture**: blameless; triggers (user-visible downtime/degradation, data loss, on-call manual intervention, resolution time over threshold, monitoring failure); contents (impact, timeline, root cause, trigger, detection, resolution, action items); senior review and broad sharing.
- **Twelve-Factor App** (Wiggins, Heroku, 2011): codebase, dependencies, config, backing services, build/release/run, processes, port binding, concurrency, disposability, dev/prod parity, logs, admin processes.

`UNVERIFIED` but widely known and safe to cite as INDUSTRY with URL in Phase 2 after a quick check: Conventional Commits, Semantic Versioning, OpenAPI Specification, AsyncAPI, OpenTelemetry signals (traces/metrics/logs), STRIDE.

## 8. Agent-skill format and runtime — `VERIFIED`

### 8.1 Agent Skills specification (agentskills.io)
- Skill = directory with `SKILL.md`; optional `scripts/`, `references/`, `assets/`.
- Frontmatter fields: `name` (required; 1–64 chars; `a-z0-9-`; no leading/trailing/consecutive hyphens; **must match parent directory name**), `description` (required; 1–1024 chars; what + when), `license`, `compatibility` (≤ 500 chars), `metadata` (string→string map), `allowed-tools` (experimental).
- Progressive disclosure: metadata (~100 tokens) always loaded; body (< 5000 tokens recommended, keep `SKILL.md` under 500 lines) loaded on activation; resources on demand. Keep file references one level deep.
- Validation: `skills-ref validate ./my-skill`.

### 8.2 Claude Code specifics
- Skill locations: `~/.claude/skills/`, `.claude/skills/`, plugin `skills/`. Claude Code accepts extra frontmatter (`disable-model-invocation`, `user-invocable`, `when_to_use`, `paths`, `context: fork`, `agent`, `model`, `effort`, `hooks`, `shell`, `arguments`, `argument-hint`), but **claude.ai upload / Skills API / `package_skill.py` reject any field outside the six spec fields with a hard error**.
- Skill listing budget: names + descriptions loaded every turn; budget ≈ 1% of context window; each entry's description (+ `when_to_use`) capped at 1,536 chars; over budget, least-used descriptions are dropped. After auto-compaction, invoked skills are re-attached keeping the first 5,000 tokens each within a shared 25,000-token budget.
- Plugin: `.claude-plugin/plugin.json` (only `name` required; `version`, `description`, `license`, `keywords`, `repository` optional); `skills/` at plugin root is auto-scanned; skills invoked as `/plugin-name:skill-name`; test with `claude --plugin-dir ./path`; validate with `claude plugin validate ./path --strict`. Local evidence: the installed `mattpocock-skills` plugin nests skills two levels deep (`skills/productivity/writing-for-agents/SKILL.md`) and is discovered — nested category folders work in Claude Code (`VERIFIED` locally; portability to other runtimes `UNVERIFIED`).

### 8.3 Writing-for-agents guidance (local reference, mattpocock `writing-for-agents`) — `INDUSTRY`
Adopted principles: descriptions are context pointers — front-load the trigger, one trigger per branch; steps end on checkable completion criteria; disclose reference behind pointers; use leading words; state the positive behaviour rather than prohibitions; avoid duplicating what the environment already states; prune no-ops.

## 9. Cross-source synthesis

### 9.1 Lifecycle mapping (system stage ↔ sources)

| System stage | 12207:2017 technical process | SWEBOK v4 KA | SSDF / SAMM | Artia / UpSites |
|---|---|---|---|---|
| Discovery & feasibility (problem, stakeholders, scope, constraints, feasibility, risks, success criteria) | Business or mission analysis; Stakeholder needs and requirements definition | Requirements; SE Economics; SE Management (risk) | SAMM Threat Assessment stream A (risk profile) | Artia 1–3; UpSites 1 |
| Requirements | System/software requirements definition | Software Requirements | PO.1 security requirements; SAMM Security Requirements | Artia 2; UpSites 1 |
| Product backlog & iteration planning | Project planning; Project assessment and control | SE Management; SE Process | — | Artia 4–7; UpSites 2, 4 |
| Domain model | Design definition (conceptual) | Software Design; Models and Methods | — | — |
| Architecture | Architecture definition; System analysis | Software Architecture | PW.1, PW.2; SAMM Secure Architecture | UpSites 3 |
| Data design | Design definition | Software Design; Computing Foundations | data protection (ASVS V14) | UpSites 3 |
| API design | Design definition; Integration (contracts) | Software Design | ASVS V4 | UpSites 3 |
| Implementation (detailed design + construction) | Implementation; Integration | Software Design; Software Construction | PW.4–PW.7; SAMM Secure Build | Artia 5–7; UpSites 4 |
| Testing | Verification; Validation | Software Testing; Software Quality | PW.8; SAMM Requirements-driven Testing, Security Testing | Artia 7; UpSites 5 |
| Security validation (transversal) | Verification | Software Security | PW.7, PW.8, RV.*; SAMM Verification | UpSites 5 |
| Deployment | Transition | SE Operations; Configuration Management | PS.1–PS.3, PW.9; SAMM Secure Deployment | Artia 8; UpSites 6 |
| Operations & monitoring | Operation | SE Operations | SAMM Operational Management, Environment Management | Artia 9; UpSites 7 |
| Incident response | Operation | SE Operations | RV.1–RV.3; SAMM Incident Management | — |
| Maintenance & evolution | Maintenance | Software Maintenance | RV.2, RV.3 | Artia 9; UpSites 7 |
| Legacy modernization | Maintenance; Architecture definition (re-architecture) | Maintenance; Architecture | — | — |

### 9.2 Quality and security are transversal — `STANDARD` + `INFERENCE`
25010 characteristics are inputs to requirements (NFRs), architecture (quality attribute scenarios), testing (coverage of each characteristic) and operations (SLIs). SSDF places security in preparation, design, construction, verification and response — i.e., in every stage. The system therefore has one `security` skill invoked at multiple gates rather than a single "security phase", and quality is expressed through references and gates rather than a standalone skill (`DECISION` D-08, D-09).

### 9.3 Disagreements identified and how they were resolved

| # | Disagreement | Resolution |
|---|---|---|
| 1 | 29119 (document-heavy) vs. context-driven testing community | Adopt concepts and lightweight strategy/plan; not the full doc set (D-11). |
| 2 | Scrum Guide's "all or it is not Scrum" vs. an AI agent that cannot hold events | Use Scrum vocabulary and commitments; do not claim Scrum conformance (D-10). |
| 3 | arc42 vs. spree.de on placement of *testability* in 25010:2023 | Testability under Maintainability (two sources vs. one; consistent with 2011). |
| 4 | Wikipedia's "2026 edition" of 12207 | Cite 12207:2017 only; treat 2026 as unverified. |
| 5 | Microservices as default (popular) vs. modular monolith | Default to the simplest architecture satisfying quality scenarios; distribution requires explicit drivers recorded in an ADR (D-12). |
| 6 | DORA "MTTR" (older literature) vs. "Failed Deployment Recovery Time" (current) | Use current DORA names. |
| 7 | Rich Claude-Code-only frontmatter vs. the six-field Agent Skills spec | Six spec fields only, for portability (D-05). |
| 8 | CS-program breadth vs. what an agent actually lacks | Procedural SE skills + decision-support CS references (D-03). |

## 10. Limitations and unverified items (carry into Phase 2)

1. No YouTube resource was accessed (no URL supplied).
2. iso.org pages inaccessible (403): 12207, 25010, 29148 content came from secondary sources; 25010 sub-characteristics were cross-checked across three sources.
3. CS2023 hour allocations and SE knowledge units not read.
4. SWEBOK v4 KA topic breakdowns not read.
5. Oxford year-by-year mapping inferred; Waterloo SE 463 not confirmed.
6. DORA performance thresholds not verified.
7. 29148 full nine-item requirement-quality list not verified.
8. Nested skill folders verified only for Claude Code (local plugin evidence), not for other Agent-Skills runtimes.

## 11. Sources (access status)

Standards and official bodies
- IEEE CS SWEBOK v4 — https://www.computer.org/education/bodies-of-knowledge/software-engineering — read
- ISO/IEC/IEEE 12207:2017 — https://www.iso.org/standard/63712.html — 403; used https://en.wikipedia.org/wiki/ISO/IEC_12207
- ISO/IEC 25010:2023 — https://www.iso.org/standard/78176.html — 403; used https://iso25000.com/index.php/en/iso-25000-standards/iso-25010 (page 1), https://quality.arc42.org/standards/iso-25010, https://blog.spree.de/2024/01/02/iso-iec-25010-news-from-the-2nd-edition-2023-11/
- ISO/IEC/IEEE 29148:2018 — via https://en.wikipedia.org/wiki/Software_requirements_specification
- ISO/IEC/IEEE 42010:2022 — https://en.wikipedia.org/wiki/ISO/IEC_42010
- ISO/IEC/IEEE 29119 — https://en.wikipedia.org/wiki/ISO/IEC_29119
- NIST SP 800-218 SSDF v1.1 — https://csrc.nist.gov/pubs/sp/800/218/final and PDF https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf — read (text-extracted); project page https://csrc.nist.gov/Projects/ssdf — read
- OWASP SAMM v2 — https://owaspsamm.org/model/ and https://owaspsamm.org/model/design/threat-assessment/ — read
- OWASP ASVS 5.0.0 — https://owasp.org/www-project-application-security-verification-standard/ ; https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en ; https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x03-What-is-the-ASVS.md ; …/0x04-Assessment_and_Certification.md — read
- OWASP Top 10:2025 — https://owasp.org/Top10/2025/ — read
- Threat Modeling Manifesto — https://www.threatmodelingmanifesto.org/ — read
- Scrum Guide 2020 — https://scrumguides.org/scrum-guide.html — read
- ACM CS2023 — https://csed.acm.org/ ; https://csed.acm.org/knowledge-areas/ ; https://csed.acm.org/final-report/ — read (KA list)

Universities
- MIT 6-3 — https://catalog.mit.edu/degree-charts/computer-science-engineering-course-6-3/ — read
- Stanford BS CS — https://bulletin.stanford.edu/programs/CS-BS — read
- CMU BS CS — http://coursecatalog.web.cmu.edu/schools-colleges/schoolofcomputerscience/undergraduatecomputerscience/computer-science-bs/ — read
- Oxford — https://www.cs.ox.ac.uk/teaching/courses/2026-2027/ (alphabetical list) and https://www.cs.ox.ac.uk/admissions/undergraduate/courses/cs.html (structure) — read; https://www.ox.ac.uk/... — 403
- ETH Zurich — https://inf.ethz.ch/studies/bachelor.html — read
- Waterloo SE — https://uwaterloo.ca/future-students/programs/software-engineering — read

Industry practice
- ADR — https://adr.github.io/ — read
- C4 — https://c4model.com/ — read
- DORA — https://dora.dev/guides/dora-metrics-four-keys/ — read
- Google SRE — https://sre.google/sre-book/service-level-objectives/ ; https://sre.google/sre-book/managing-incidents/ ; https://sre.google/sre-book/postmortem-culture/ — read
- Twelve-Factor App — https://12factor.net/ — read

Practical SDLC (supplied by user, located by search)
- Artia — https://artia.com/blog/projeto-de-desenvolvimento-de-software/ — read
- UpSites — https://upsites.digital/desenvolvimento-web/software/etapas-desenvolvimento-software/ — read
- YouTube — no URL supplied — not accessed

Agent skill format
- Agent Skills spec — https://agentskills.io/specification — read
- Claude Code skills — https://code.claude.com/docs/en/skills — read
- Claude Code plugins reference — https://code.claude.com/docs/en/plugins-reference — read
- Local: mattpocock-skills `writing-for-agents` SKILL.md and SKILL-MECHANICS.md — read
