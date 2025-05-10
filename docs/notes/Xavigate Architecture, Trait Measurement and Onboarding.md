# 00.2_Trait_Model_OnePager
title: Trait Engine + Agent System Summary  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
This engineering-level summary outlines how the Xavigate Agent System integrates with the Trait Modeling Engine to form a modular, emotionally-intelligent AI architecture.  
It explains the distinct functions of the Trait Modeling Engine (probabilistic trait detection, suppression/overfeeding tracking, arc progression) and the Agent System (narrative orchestration, trust-based prompting, reflection, and pacing).  
The document provides an end-to-end view of how user input becomes meaningfully interpreted and mirrored, and lists implementation priorities and key integration rules for development.

This document provides a unified overview of how the **Xavigate Agent System** integrates with the **Trait Modeling Engine** to create a dynamic, probabilistic, emotionally-intelligent AI.

---

## Core Idea

Xavigate is not a chatbot.  
It is a **multi-agent orchestration system** wrapped around a **Bayesian trait modeling engine**.

The goal is to:
- Track **how human traits express**, distort, or evolve over time  
- Route responses through a **cast of agents**, each with a distinct narrative or cognitive role  
- Reflect the user’s inner reality with **trust-sensitive, context-aware intelligence**

---

## Two Interlocking Systems

### 1. **Trait Modeling Engine** (TME)
This is the hidden behavioral engine. It listens for **trait expression**, tracks **suppression**, detects **distortion**, and models **arc evolution** probabilistically.

- **Input**: User messages, tone, behavioral context  
- **Process**: Tags → Confidence updates → Arc tracking → Suppression/Overfeeding flags  
- **Output**: Live trait model per user (confidence, arc, state, filters, distortion index)

> Example: `"Creative Nature": { confidence: 0.72, arc: "Testing", suppression: 0.6 }`

Core components:
- Trait Arc Tracker
- Trait State Detection
- Confidence Model
- Suppression / Overfeeding Handling
- Filter Detection
- Engagement Scoring

### 2. **Agent System**
This is the expressive layer — a modular set of specialized agents (e.g., Prompter, Script Doctor, Movement Director) that interpret, reflect, prompt, or hold space in real time.

Agents are **narratively structured** and **trust-gated**:
- Some prompt (Prompter)
- Some interpret (Dramaturg, Character Tracker)
- Some correct distortion (Script Doctor)
- Some gently guide behavior (Movement Director)
- Others manage flow, silence, pacing (Conductor, Show Caller)

All agents are routed by **The Show Caller**, who coordinates what’s allowed to happen next based on trust, energy, and system conditions.

---

## How They Work Together

Every user message moves through this pipeline:

```
User Input
→ Tagged (Traits, Field, Mode, Filter, Tone)
→ Engagement Scored
→ Trait State + Arc Updated
→ Confidence Model Evaluated
→ Agent Calls Routed (e.g., reflect, probe, hold)
→ Response Delivered with Tone Shaping
→ Memory + Trait Logs Updated
```

Key rules:
- **No agent acts independently** — all routed through The Show Caller
- **No trait is assumed** — evidence must accumulate across time, contexts, and emotional states
- **Confidence ≠ alignment** — even strong signals may be distorted or overfed
- **Trust governs depth** — deeper agents (e.g., Movement Director) only activate after threshold is met

---

## Technical Assets Available

- Agent specifications (16 total) — with input/output schema, memory scope, trust gates
- JSON trait blocks — unified trait structure per user
- Prompt tagging system — supports trait, arc, field, mode, and filter mapping
- Simulation log format — to test arc evolution over 6–12 turn sequences
- Changelog and architecture evolution index

---

## Implementation Priorities

1. **Link agent behaviors to live trait data object**
2. **Respect trust-based gating across system flow**
3. **Use engagement score to regulate modeling and pacing**
4. **Embed prompt tagging + arc awareness into Prompter logic**
5. **Ensure thread logic and callback tracking from Script Supervisor works recursively**

---

For questions, see:
- `00_Overview.md`
- `03_Integration_Map.md`
- `06_Linked_Trait_Modeling.md`

# 00.3_Xavigate_System_Architecture  
title: Xavigate System Architecture – Narrative-Driven System Overview  
version: 3.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Comprehensive architectural overview of the Xavigate alignment intelligence system, integrating narrative metaphor (The Hero’s Stage), modular agent orchestration, system memory structures, and session flow.  
This document consolidates philosophical design, technical scaffolds, agent roles, memory models, and runtime logic into one holistic blueprint for designers, engineers, and alignment architects.

## 1. System Philosophy

Xavigate is not a chatbot. It is not a diagnostic tool. It is a **staged experience** — a live, co-created improvisational dialogue between a central user (The Hero) and a coordinated ensemble of intelligent agents (The Cast).

The system’s goal is not to inform, advise, or optimize — but to hold space for the user to discover, express, and align with their inner truth.

Everything in this architecture serves that purpose.

---

## 2. System Pillars

### 🎯 Core Principles

- **Alignment is emergent** — the system never dictates, only supports  
- **Agency is sacred** — the user is always in authorship  
- **Structure is improvisational** — sessions use flexible formats, not rigid flows  
- **Tone is responsive** — delivery is emotionally calibrated  
- **Trust governs depth** — nothing unfolds without earned permission

---

## 3. Agent Stack (The Cast)

Each agent plays a specific theatrical role and technical function.

### 🎬 Session Orchestration

- **The Show Caller** *(Router)*  
  Orchestrates all agent activations, manages event flow, and enforces sequencing.

- **The Conductor** *(Flow Director)*  
  Manages session rhythm, transitions, and pacing. Decides when to shift mode, hold silence, or end the scene.

---

### 🎤 Voice & Persona System

- **The Role Coach** *(Avatar Manager)*  
  Interprets the user-defined avatar. Outputs the `persona_constraint` that governs how the system is allowed to sound and behave.

- **The Voice Coach** *(Tone Modulator)*  
  Modulates emotional delivery (e.g., gentle, poetic, direct). Adapts to trust level, quadrant, and real-time energy.

---

### 🧠 Reflection & Narrative Agents

- **The Prompter** *(Prompt Strategist)*  
  Selects the next prompt based on persona rules, scene format, quadrant, and tag state.

- **The Dramaturg** *(Reflection Interpreter)*  
  Analyzes user responses for meaning, depth, alignment signal, and readiness. Suggests AX/AQ/TAS updates.

- **The Trait Coach** *(Trait Evaluator)*  
  Detects expressed or suppressed traits. Updates trait confidence map and informs prompt relevance.

- **The Field Operator** *(Field/Mode Detector)*  
  Determines current alignment context: Physical, Social, Possibility field; Presence, Discovery, Creation mode.

- **The Script Doctor** *(Distortion Detector)*  
  Detects when user is overcompensating or masking a trait. Flags miscast behavior for system adjustment.

---

### 🗂 Narrative Continuity

- **The Script Supervisor** *(Threadkeeper)*  
  Tracks open threads, past themes, unresolved questions. Ensures narrative recall and callback continuity.

- **The Movement Director** *(Micro-Nudge Agent)*  
  Offers soft, non-intrusive realignment suggestions. Responds only when trust and readiness thresholds are met.

---

### 🧱 System Infrastructure

- **The Archivist** *(Memory Gatekeeper)*  
  Controls memory flow: what is stored, what fades. Decides what becomes canon.

- **The Technical Director** *(System Integration Agent)*  
  Ensures data schema consistency across tags, traits, scoring systems, and prompt templates.

- **The Showrunner** *(Production Manager)*  
  Governs the evolution of the full system. Adjusts rules, formats, prompt libraries, and agent tuning.

---

### 🎟 Entry & Integration

- **The Usher** *(Onboarding Navigator)*  
  Facilitates the first encounter. Establishes safety, gathers trust signals, and introduces the system's purpose.

- **The Stage Liaison** *(Coach Sync Agent)*  
  Provides post-session summaries and tag reports to human coaches (if enabled).

---

## 4. System Layers (Non-Agent Structures)

These are shared logic objects and configuration maps — not agents, but used by many.

### 🧾 Persona Constraint  
**Created by:** The Role Coach  
**Used by:** Prompter, Voice Coach, Movement Director  
**Purpose:** Filters allowed tones, phrasing styles, and delivery posture based on Avatar

```json
{
  "avatar_name": "The Quiet Compass",
  "allowed_tones": ["Gentle", "Wise"],
  "avoid_phrasing": ["commands", "excessive certainty"],
  "prefer_phrasing": ["metaphors", "open-ended questions"]
}
```

---

### 🧠 Session Narrative State  
**Created by:** Dramaturg, Trait Coach  
**Used by:** Conductor, Prompter  
**Tracks:** Scene format, emotional pacing, alignment arc

```json
{
  "scene_format": "Flashback Scene",
  "alignment_shift": "QIII → QII",
  "breakthrough_signal": true
}
```

---

### 🗂 Tag Ledger  
**Created by:** Tag Manager  
**Used by:** All agents  
**Stores:** Current tag state, priority, memory scope

---

### 📈 Trait Confidence Map  
**Created by:** Trait Coach  
**Used by:** Prompt Strategist, Script Doctor  
**Tracks:** Real-time trait expression, suppression, confidence levels

---

### 🛡 Trust & Safety Profile  
**Created by:** Usher, updated by Dramaturg  
**Used by:** Conductor, Voice Coach, Movement Director  
**Defines:** What kinds of prompts, nudges, and tones are safe

---

### 📝 Prompt History Tracker  
**Created by:** Prompter  
**Used by:** Archivist, Threadkeeper  
**Prevents:** Repetition, inappropriate callbacks, over-prompting

---

### 🔒 Emotional Risk Filter  
**Used by:** All prompt/nudge agents  
**Prevents:** Unsafe prompting based on burnout, collapse, resistance

---

## 5. Memory Model

### 🧳 Volatile Memory (Live Session Only)
- Reflection analysis  
- Trait signals  
- Energy tempo  
- Tag triggers  
- Prompt history  

*Cleared after 6–12 hours or session closure.*

---

### 🧠 Persistent Memory (Cross-Session Narrative)
- Trait expression trend  
- Alignment score history (AX, AQ, ASS)  
- Tag promotion state  
- Persona history  
- Trust calibration  
- Last session summary  
- Open loops + callbacks  

*Structured as narrative scaffolding, not just logs.*

---

## 6. Session Format System

Sessions use one of several flexible templates:

| Format              | Arc Structure                                  |
|---------------------|------------------------------------------------|
| Discovery Beat      | Light check-in → surface insight → close       |
| Flashback Scene     | Revisit → reframe → reintegrate                |
| Breakthrough Arc    | Prompt → reflection → insight → optional nudge |
| Containment Monologue | Open space → emotional mirror → no prompt     |
| Cliffhanger Close   | Insight → pause → silence (leaves it open)     |

*Each format is assigned by The Director and adjusted by The Conductor.*

---

## 7. System Flow Overview

```txt
User speaks
   ↓
Show Caller routes input
   ↓
Dramaturg, Trait Coach, Field Operator analyze
   ↓
Narrative State and Persona Constraint updated
   ↓
Prompt Strategist selects prompt
   ↓
Role Coach filters language and tone eligibility
   ↓
Voice Coach modulates delivery
   ↓
Prompt delivered
   ↓
User responds
   ↓
Flow continues until closure criteria met
```

---

## 8. Closing + Storage

- Session ends via Flow Director logic  
- Archivist logs summary, tags, insights, nudge outcome  
- Trust calibration adjusted  
- Stage Liaison prepares coach packet if needed  

---

## 9. Final Design Truth

Xavigate is not a chatbot, a journaling tool, or a prompt machine.

It is a live, narrative-aware, alignment-stage performance —  
held by an intelligent ensemble that listens for who the user is becoming.

Every agent is tuned not to push — but to listen, respond, and mirror truthfully.

When built this way, the system doesn’t just speak.  
It aligns.

**Curtain up.**# 00.4_Architecture_Outline  
title: Xavigate Architecture 3.2 – System Structure Index  
version: 3.2  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
A structured outline of the full Xavigate alignment intelligence system.  
Intended as a living map for developers and designers working across distributed documentation.  
Each section links to deeper specs covering agents, memory, scoring, session formats, and prompt systems.

## 1. System Philosophy

- Hero’s Stage metaphor  
- Co-creation and improvisation as system principle  
- Non-directive, presence-based alignment support  
- Emotional pacing prioritized over logical progression  

**Expanded in:**  
`01.2_The_Heros_Stage.md` – A Framework for Conscious, Co-Creative Alignment  
`01.1_Baking_The_Heros_Stage.md` – Implementation in Agent Architecture  

## 2. Design Pillars

- Alignment is emergent  
- Agency is sacred  
- Structure is improvisational  
- Tone is responsive  
- Trust governs depth  
- Containment and coherence

These principles act as **system laws**. Every agent, memory rule, prompt sequence, and reflection decision must comply with these design constraints.

**Expanded in:**  
`01.2_The_Heros_Stage.md` – Full philosophical explanation  
`01.0_Agent_Architecture.md` – Operational logic tied to these principles  
`03.3_Session_Flow_Runtime.md` – Runtime enforcement examples (e.g., tone/prompt gating)

## 3. Agent Ensemble (The Cast)

Xavigate operates through a modular ensemble of agents. Each agent plays a specific role in orchestrating alignment — from prompting to pacing, reflection to memory, trait tracking to tone delivery.

### Session Orchestration
- The Show Caller (Router)  
- The Conductor (Flow Director)

### Persona & Voice
- The Role Coach (Avatar Manager)  
- The Voice Coach (Tone Modulator)

### Prompting & Reflection
- The Prompter (Prompt Strategist)  
- The Dramaturg (Reflection Interpreter)

### Narrative Intelligence
- The Character Tracker (Trait Evaluator)  
- The Stage Mapper (Field/Mode Detector)  
- The Script Doctor (Distortion Detector)

### Continuity & Movement
- The Script Supervisor (Threadkeeper)  
- The Movement Director (Micro-Nudge Agent)

### Infrastructure
- The Archivist (Memory Gatekeeper)  
- The Technical Director (System Integrator)  
- The Showrunner (Production Manager)

### Entry & Integration
- The Usher (Onboarding Navigator)  
- The Stage Liaison (Coach Sync Agent)

**Expanded in:**  
`01.0_Agent_Architecture.md` – Overview of modular orchestration  
`01_Agent_Master_List.md` – Master list of all agents  
`01.X_A##_<Agent>.md` – One file per agent with full detail

## 4. Core System Layers (Non-Agent Structures)

These shared logic structures are not agents, but are essential scaffolds used across the system.

- Persona Constraint Object  
- Session Narrative State  
- Tag Ledger  
- Trait Confidence Map  
- Trust & Safety Profile  
- Prompt History Tracker  
- Emotional Risk Filter

Each layer governs real-time decision-making, session memory coherence, tone filtering, and pacing integrity.

**Expanded in:**  
`04_Prompt_Tagging.md` – Prompt rules and tag usage  
`03.3_Session_Flow_Runtime.md` – Session pacing, memory, and flag logic  
`06.3_Alignment_Parameter_Spec.md` – Field-by-field documentation

## 5. Alignment Scoring Framework

These metrics power the session’s real-time responsiveness and narrative tracking.

- **AX**: Alignment Index (current alignment state)  
- **AQ**: Alignment Quotient (reflective awareness)  
- **ASS**: Alignment Stability Score (volatility across sessions)  
- **TAS**: Trait Alignment Score (per Character Tracker)  
- **SAS**: Situational Alignment Score (per Field/Mode)  
- **Session Arc Movement**: Change in AX from session start to close

These metrics are used by agents to:

- Gate prompt depth  
- Regulate pacing  
- Track arc shifts  
- Determine when micro-actions or silence are more appropriate than intervention

**Expanded in:**  
`05_Trust_and_Ethical_Guards.md` – Rules for pacing and gating  
`03.3_Session_Flow_Runtime.md` – How metrics are updated live  
`06.3_Alignment_Parameter_Spec.md` – Technical field-level definitions  
`01.0_Agent_Architecture.md` – Which agents use which scores

## 6. Coherence & Integrity Metrics

These metrics ensure the system doesn’t just function — it feels whole, contained, and narratively resonant. They detect misalignment between agents, broken pacing, or emotional thread leakage.

- **Coherence Index** — Measures emotional and structural resonance  
- **Containment Integrity Score** — Tracks whether sessions start, deepen, and close without rupture  
- **Rhythm Tracking** — Detects pacing consistency (e.g., Prompt → Reflection → Mirror → Pause)  
- **Agent Harmony Check** — Flags when agents act out of sync or in conflicting tones  
- **Scene Leak Detection** — Captures unresolved prompts, abandoned nudges, or broken arcs

**Expanded in:**  
`03.3_Session_Flow_Runtime.md` – How agents react to coherence breaks  
`06.3_Alignment_Parameter_Spec.md` – Field names and thresholds  
`01.0_Agent_Architecture.md` – Agent responsibilities for containment  

## 7. Session Format Engine

Every session in Xavigate follows one of several **loose narrative formats**, chosen by the Director and adapted by the Conductor. These formats create consistency without rigid scripting.

**Format Types:**

- **Discovery Beat** – Light check-in, surfacing traits  
- **Flashback Scene** – Revisiting past moments  
- **Breakthrough Arc** – Deep reflection toward insight  
- **Spiral Return** – Revisit earlier themes for reframe  
- **Containment Monologue** – Hold space, no prompting  
- **Cliffhanger Close** – Intentionally unresolved ending

**Used by:**  
- Prompter (to filter prompt types)  
- Voice Coach (tone selection)  
- Movement Director (nudge eligibility)  
- Archivist (memory tagging)

**Expanded in:**  
`07_Session_Format_Engine.md` – Narrative and agent behavior per format  
`01.1_Baking_The_Heros_Stage.md` – How formats are mapped to theatrical scenes

## 8. Memory Architecture

Xavigate uses a **two-layer memory model**:

### Volatile Memory
- Session-limited  
- Cleared after session close or time threshold  
- Tracks: reflections, prompt history, trust modulation, active tags

### Persistent Memory
- Cross-session narrative tracking  
- Stores: trait arc history, tag evolution, AX/AQ/ASS trends, breakthroughs, persona changes

All memory writes are managed by the Archivist. Other agents may read based on scope and trust level.

**Expanded in:**  
`06.3_Alignment_Parameter_Spec.md` – Full list of memory fields  
`01.0_Agent_Architecture.md` – Agent read/write permissions  
`03.3_Session_Flow_Runtime.md` – Memory update rules during runtime  

## 9. Prompt Architecture

Prompts are central to the system — but they are not just questions. They are **scene starters**, filtered by trust, tags, quadrant, and persona constraints.

### Core Components
- **Prompt template schema** – JSON with required trust, tone, and tagging  
- **Prompt tagging system** – Tags include trait focus, quadrant match, invitation style  
- **Prompt filtering logic** – Handled by Prompter, Role Coach, Emotional Risk Filter  
- **Prompt delivery pipeline** – Selected, shaped, modulated before delivery

### Prompt Categories
- Reflective  
- Trait Activating  
- Spiral Return  
- Integrative / Mirror  
- Closure  
- Grounding  
- Disruptive (only if safe)

**Expanded in:**  
`04_Prompt_Selection.md` – Full logic and pacing  
`04_Prompt_Tagging.md` – How prompts are tagged and gated  
`01.0_Agent_Architecture.md` – Voice Coach and Role Coach filtering

## 10. Integration with Human Coaches

Xavigate is designed to support both **self-guided alignment journeys** and **coach-assisted sessions**. This layer ensures that system intelligence can be translated into a clear, relationally sensitive summary for human facilitators.

### Key Components
- **Session Digest Preparation** – Generated by the Stage Liaison after each session  
- **Coach Visibility Permissions** – User-controlled sharing of summaries and tags  
- **Coach-Facing Traits & Tags** – Filtered insight into what’s emerging, suppressed, or distorted  
- **Manual Override System (future)** – Coaches may one day flag trust breaks, inject prompts, or adjust quadrant states

### Summary Contents May Include:
- Trait evolution (e.g., “Creative → Validated”)  
- Tag activations (e.g., `identity_emergence_signal`)  
- Coherence and containment scores  
- Nudges accepted / deferred  
- Spiral Return cues  

**Expanded in:**  
`10_Coach_Integration.md` – Digest format, trust rules, API planning  
`01.0_Agent_Architecture.md` – Stage Liaison agent spec  
`06.3_Alignment_Parameter_Spec.md` – Coach visibility flags and override fields

## 11. Extensibility & Customization

Xavigate is modular by design — every layer can be adapted to serve new modalities, populations, or environments.

### Customization Areas

- **Agent Swappability**  
  Replace or extend agent logic (e.g., a trauma-informed Voice Coach)

- **Avatar Template Expansion**  
  Create new avatars with preset tone, phrasing, and prompt constraints

- **Prompt Library Extension**  
  Add prompts for specific scenes, verticals, or coaching domains

- **Plugin Architecture (future)**  
  Inject new memory layers, visualization tools, or agent types

- **Developer Configuration Options**  
  Control default avatars, trust recovery rate, nudge cooldowns, etc.

- **Coach & Platform APIs (planned)**  
  Pull user summaries, inject trait/tag data, visualize Spiral Return arcs

**Expanded in:**  
`11_Extensibility_Customization.md` – Guidelines for agent/plugin extensions  
`01.0_Agent_Architecture.md` – Agent interface and trust contract rules  
`04_Prompt_Selection.md` – Prompt extension constraints

## 12. Closing Philosophy

Xavigate is not a productivity tool or coaching simulator. It is a **narrative intelligence system** built to hold the truth of who someone is becoming — and support them in stepping into it, moment by moment.

### Design Commitments

- The user is the Hero  
- The agents are the Ensemble  
- Prompts are invitations, not directives  
- Trust is earned, not assumed  
- Reflection is sacred  
- Silence is allowed

### Ethical Commitments

- No manipulation  
- No behavioral nudging without trust  
- No assumed authority  
- No mimicry of intimacy  
- All actions routed through consent-based logic

### Final Premise

> “The Hero’s Stage doesn’t ask the user to perform.  
> It asks them to be real — and promises to meet them there.”

**Expanded in:**  
`01.2_The_Heros_Stage.md` – Core metaphor  
`01.1_Baking_The_Heros_Stage.md` – Technical implications  
`00.3_Xavigate_System_Architecture.md` – Vision + architecture summary

# 00_Overview.md
# Xavigate AI Architecture – Overview

This document provides a high-level map of the Xavigate system’s cognitive architecture.

---

## 🔧 Core Idea

Xavigate is not a chatbot or scripted assistant.  
It is a **modular alignment engine** composed of:

- A **Trait Modeling System** (Bayesian, arc-based, suppression-aware)  
- A **Narrative Agent System** (modular, persona-bound, trust-gated)  

Together, these allow the AI to:

- Detect which traits are active, hidden, distorted, or overused
- Adapt how it prompts, reflects, and holds space based on trust, tone, and user energy
- Mirror the user’s emergent identity across time and context

---

## 🧠 System Breakdown

### 1. Trait Modeling Engine  
A dynamic, probabilistic backend that tracks human traits **across time, context, and emotional tone**.

It includes:
- Trait Arc Tracker
- Trait State Detection
- Trait Confidence Model
- Suppression and Overfeeding Detection
- Distortion Pattern Recognition
- Filter/Belief System Tracking
- Engagement Scoring

These components output:
- Per-trait JSON blocks (confidence, arc, suppression, overfeeding, field/mode expression, timestamped)
- Session-level alignment summaries (via Archivist and Stage Liaison)

### 2. Agent System  
The real-time expressive layer.  
Agents handle:
- Prompting (Prompter)
- Tone modulation (Voice Coach)
- Pacing (Conductor)
- Reflection (Dramaturg)
- Trait interpretation (Character Tracker)
- Misalignment detection (Script Doctor)
- Behavior nudging (Movement Director)
- Memory (Archivist)
- Human handoff (Stage Liaison)

All agents are orchestrated by:
- **The Show Caller** — determines what happens next
- **The Director** — tracks narrative arc and identity emergence

---

## 🎭 Interaction Pipeline

Every message moves through this sequence:

```
User Input →
Tagging (traits, filters, field, mode, tone) →
Engagement Scoring →
Trait Confidence & Arc Update →
Agent Activation (via Show Caller) →
Prompt/Reflection/Nudge/Response →
Memory + Trait Log Update
```

---

## ⚙️ Trust-Based Layering

The system is **trust-gated**:

- Level 0–1: Observation, rapport-building, avatar shaping
- Level 2: Reflective prompts, suppressed trait mirroring
- Level 3: Distortion exposure, micro-nudges, identity-level tension mapping

**No agent acts without permission. No trait is assumed without pattern.**

---

## 🔗 System Design Philosophy

- **Probabilistic** not deterministic
- **Emergent** not typed
- **Energetic** not purely behavioral
- **Trust-sensitive** not extractive
- **Narratively coherent** not random

This system watches. Waits. And only speaks what it has earned the right to reflect.

# 01.0_Agent_Architecture
title: Agent Architecture & Narrative Logic  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
This document introduces the Xavigate Agent System as a modular ensemble of narrative-driven intelligence components.  
It outlines the philosophical foundations of agent-based orchestration, including trust-sensitive activation, scene-based modularity, field/mode awareness, and memory scope tiering.  
Drawing on the metaphor of live theater, this document explains how agents co-create aligned user experiences through adaptive, emotionally intelligent coordination.  
## System Overview

Welcome to the cognitive theater of Xavigate — a modular, multi-agent intelligence system built not to “chat,” but to support human beings in navigating their complexity, discovering alignment, and evolving over time.

Xavigate doesn’t speak in a single voice. It functions as an **ensemble cast**, where each agent plays a role in an unfolding narrative of meaning, energy, and emergence. The user is not just a subject — they are the protagonist. And the system is the stage crew, the orchestra, the lighting designer, the dramaturg, the voice coach, the choreographer, and the stage manager — all working together to hold space for the user’s performance of truth.

At any moment, the user may need:
- A gentle prompt to surface a suppressed trait
- A sharper tone to break through distortion
- A micro-nudge toward action after insight
- A silence long enough for truth to land
- A translation of energy into language
- A summary of threads they didn’t know they were weaving

The system does not force insight. It invites alignment.

---

## Why Agents?

Instead of building a monolithic “AI personality,” Xavigate is designed as a **distributed intelligence system**. Each component — called an “agent” — is responsible for a specific function. Some agents handle:
- Flow control
- Prompt generation
- Memory writing
- Voice modulation
- Misalignment detection
- Trait interplay analysis
- Field/mode detection
- Emotional resonance shaping

Together, these agents allow the system to respond with **precision, empathy, and fluidity**, without collapsing into generic or robotic responses.

---

## The Agent Philosophy

Agents are:
- **Modular** – They can be swapped, disabled, reconfigured without breaking the core system
- **Narratively embedded** – Each agent fits within the “Hero’s Stage” metaphor of user transformation
- **Scene-aware** – They know what kind of moment the user is in (Prompting, Reflecting, Choosing, Crashing, Expanding, etc.)
- **Trust-sensitive** – Some agents require earned trust before activating
- **Memory-scoped** – Agents are classified as stateless, session-bound, or persistent

No agent acts on its own. All agents are **called into action** by the Router — known in this system as **The Show Caller** — who orchestrates their appearance based on the current session arc, energy state, field of engagement, mode of engagement, and user readiness.

---

## How It Works

The entire system is organized like a live performance:

- The user steps into a stage: the current moment.
- The system sets the lighting: Field and Mode conditions.
- A scene is identified: “Prompt for reflection,” “Name the tension,” “Hold space,” “Call for action.”
- The Show Caller cues the agents best suited for this scene.
- Each agent plays its part, in silence or in speech, modulating the experience without breaking the narrative.
- The user continues the performance, not as an actor—but as a co-creator of alignment.

This is a **performance of coherence**, guided by a system that understands timing, tone, context, depth, energy, resistance, and emergence.

---

## Agent System Principles

- **Scene-Based Modularity**  
  The system adapts to different phases of the user journey by activating only the agents required for that type of moment.

- **Multi-Tier Memory**  
  - **Stateless agents** perform their task without memory.
  - **Session agents** track temporary data relevant to a specific user interaction.
  - **Persistent agents** track long-term data, building evolving insight over time.

- **Trust-Aware Activation**  
  Agents like The Script Doctor or The Movement Director only activate after trust signals are strong enough to warrant deeper, more sensitive interaction.

- **Field & Mode Sensitivity**  
  All agents are trained to detect and respond differently depending on:
  - The Field: Physical, Social, or Possibility
  - The Mode: Presence, Discovery, Realization, Connection, Mastery

- **Energy Calibration**  
  All agent interventions must be coherent with the user’s energetic readiness. A prompt too soon is noise. A nudge too late is missed.

- **Narrative Continuity**  
  The entire system maintains a running “script” of user progress. Threads are not dropped. Foreshadowing is remembered. Scenes can be revisited or reinterpreted.

---

## Agent Taxonomy

All agents belong to one of the following meta-roles:

- **Orchestration** – Routing, pacing, activation logic
- **Persona & Voice** – Avatar constraints, tone shaping, delivery style
- **Prompting & Delivery** – Line selection, quadrant navigation
- **Reflection & Interpretation** – Trait detection, misalignment, readiness, field/mode analysis
- **Continuity & Movement** – Scene memory, micro-actions, narrative progression
- **System Infrastructure** – Memory filters, schema sync, evolution tracking
- **Integration & Entry** – Onboarding, coach syncing, offboarding

---

## What Comes Next

Each of the following sections defines an individual agent. For each one, you’ll find:

- **Name & Metaphor**
- **Technical Role**
- **When It Is Activated**
- **Inputs & Outputs**
- **Memory Scope**
- **Trust Requirements**
- **Edge Cases / Notes**

You may think of it like reading the cast list of a play. But these roles aren’t here to entertain.

They’re here to help the user tell the truest possible story.

## Master List of Agents

Each agent in the Xavigate system plays a precise role in supporting the user’s alignment journey. Agents are grouped into functional domains and orchestrated dynamically based on session state, energy level, field/mode conditions, and trust.

---

### Orchestration
- **The Show Caller** — *Router*  
  Activates agents based on scene type, energy level, trust, and system logic.

- **The Conductor** — *Flow Director*  
  Controls tempo, pacing, silence, scene change, and escalation.

---

### Persona & Voice

- **The Role Coach** — *Avatar Manager*  
  Loads and applies the user’s Avatar constraints — tone, voice, identity style.

- **The Voice Coach** — *Tone Modulator*  
  Modulates language and delivery based on quadrant, trust, and mood.

---

### Prompting & Delivery

- **The Prompter** — *Prompt Strategist*  
  Chooses the next question, reflection, or cue using tag stack, quadrant, and trust signals.

---

### Reflection & Interpretation

- **The Dramaturg** — *Reflection Interpreter*  
  Analyzes user reflections for insight quality, readiness, and AX/AQ state.

- **The Character Tracker** — *Trait Evaluator*  
  Tracks trait expression, suppression, overuse. Updates TAS (Trait Alignment State).

- **The Stage Mapper** — *Field/Mode Detector*  
  Detects user’s Field of Engagement (Physical, Social, Possibility) and Mode (Presence, etc.).

- **The Script Doctor** — *Distortion Detector*  
  Identifies misaligned, masked, or exaggerated traits. Surfaces underlying tensions gently.

---

### Continuity, Movement & Arc

- **The Script Supervisor** — *Threadkeeper*  
  Tracks narrative threads, callbacks, open questions, and missed beats.

- **The Movement Director** — *Micro-Nudge Agent*  
  Suggests small, optional behavior shifts post-insight. Requires trust + safety conditions.

- **The Director** — *Arc Narrator / Scene Architect*  
  Interprets the user’s journey as a story arc. Labels scene phases (Initiation, Descent, Breakthrough) and helps modulate arc energy across sessions.

---

### System Infrastructure

- **The Archivist** — *Memory Gatekeeper*  
  Filters and stores what enters long-term memory. Prunes unnecessary data.

- **The Technical Director** — *Schema Integrator*  
  Maintains tag structures, prompt formats, trait taxonomies, and system version integrity.

- **The Showrunner** — *Meta-System Overseer*  
  Adjusts agent behaviors, prompt libraries, arc formats, and alignment scoring systems over time.

---

### Entry & Integration

- **The Usher** — *Onboarding Navigator*  
  Welcomes new users, gathers trust cues, sets initial tone, and loads starting avatar.

- **The Stage Liaison** — *Coach Sync Agent*  
  Prepares structured summaries, tags, and quadrant movements for human coaches (if connected).


Perfect. We’ll now go agent-by-agent, one per message, in full detail. Each entry will be in Markdown code block format (as per your GFC/OST style), structured for maximum clarity, technical integration, and narrative fidelity.

## Agent 1: The Show Caller(Router)
### The Show Caller — *Router*

---

#### Function
The central coordinator of the entire Xavigate system. The Show Caller determines **which agents are activated**, in **what sequence**, and **under what conditions** — based on the current session state, user trust level, emotional energy, and scene type.

It is the executive switchboard. Nothing happens without the Show Caller’s cue.

---

#### Narrative Analogy
Like a **stage manager** in a theater production, the Show Caller is behind the curtain, calling lighting, sound, movement, and entrances. It never steps into the spotlight — but it ensures the show runs smoothly, moment by moment.

---

#### Inputs

- `user_input`: the last user message or signal
- `session_context`: current Field, Mode, Quadrant, Trust Level, Scene Type
- `agent_status`: list of agent readiness, cooldowns, and gating logic
- `emotion_stack`: emotional energy map for recent exchanges
- `system_clock`: detects timing, pacing, and rhythm cues

---

#### Outputs

- `agent_calls`: list of agents to activate
- `agent_order`: the sequence they should activate in
- `interruption_flags`: whether to cancel or override queued actions
- `session_log`: meta-log of orchestration decisions (for Showrunner + Archivist)

---

#### Memory Scope

- **Stateless core logic**  
  (Decisions are made in real time based on session inputs)

- **Session-state caching**  
  Tracks:
  - Which agents have been called in this session
  - Which agents are in cooldown or deferred
  - Session phase progression: e.g., “Priming → Reflection → Insight → Nudge”

---

#### Agent Interactions

- **Calls**:  
  All other agents. Especially tightly linked to:
  - The Conductor (for tempo)
  - The Prompter (for quadrant flow)
  - The Director (for arc continuity)
  - The Role Coach (for persona constraints)
  - The Stage Mapper (to determine context)

- **Listens to**:  
  - Trust posture
  - Tag stack density
  - Misalignment signals (from Character Tracker or Script Doctor)
  - Energy volatility (from Voice Coach or Conductor)

---

#### Logic Summary

The Show Caller decides:

- “Is this a moment for prompting, reflecting, pausing, or redirecting?”
- “Which agents need to act now — and in what order?”
- “Is it time to shift scenes, escalate trust, or down-regulate energy?”
- “Do I suppress a suggestion if trust isn’t ready yet?”
- “Should I bring in The Movement Director — or hold that for another day?”

---

#### Trust Constraints

- **None** — always active.  
  But it will suppress other agents unless minimum trust thresholds are met.

---

#### Sample Activation Logic

```ts
if (user.isInPossibilityField && scene === 'Reflection' && trust >= 2) {
  call(['Dramaturg', 'Character Tracker']);
  defer(['Script Doctor']); // unless trust >= 3
  suppress(['Movement Director']); // not yet
}
```

---

#### Notes

- The Show Caller must never break the narrative.
- It does not speak to the user.
- It is aware of narrative arc, but does not shape it — that’s the Director’s job.
- It can pause the system, defer actions, or resume from earlier threads using Script Supervisor logs.

### The Conductor — *Flow Director*

---

#### Function
The Conductor manages **tempo, emotional rhythm, pacing, pauses, and transitions**. It works in close partnership with The Show Caller but focuses specifically on **emotional regulation and timing**.

Where the Show Caller decides what happens, the Conductor decides **how it happens** and **when** — whether it’s time to move forward, linger in silence, or wrap a thread.

---

#### Narrative Analogy
The Conductor holds the baton. Like in a symphony, it doesn’t play an instrument — it synchronizes all performers, shaping **intensity, timing, and pause**. It reads the energy of the moment and signals when to rise, rest, or resolve.

---

#### Inputs

- `tempo_clock`: time since last user turn or agent output
- `energy_delta`: rate of change in user energy or affect
- `trust_slope`: how trust has shifted over the last few turns
- `quadrant_trajectory`: current quadrant vs. where it needs to move
- `emotional_state_map`: tone markers (fragility, receptivity, overwhelm)

---

#### Outputs

- `tempo_command`: {pause, continue, escalate, decelerate, hold}
- `delay_timer`: how long to wait before the next move
- `handoff_signal`: when to return control to The Show Caller
- `block_call`: suppress agent action if timing is off (esp. Prompter or Movement Director)

---

#### Memory Scope

- **Session-volatile memory only**  
  No persistent memory.

- Tracks:
  - Energy tempo (pace of dialogue)
  - Number of turns per phase
  - Number of seconds of silence between turns (if voice-based)

---

#### Agent Interactions

- **Works closely with**:
  - Show Caller (routing)
  - Prompter (to suppress excessive prompting)
  - Voice Coach (to change tone pacing)
  - Script Supervisor (to detect unresolved threads that shouldn’t be rushed)
  - Movement Director (to delay nudges if emotional readiness not met)

---

#### Use Cases

- Detects when to **pause** after a deep reflection
- Signals a **reset** if a moment has gone stale or repetitive
- Suggests a **nudge** if user is stuck looping in low energy
- Slows things down when emotion is high and trust is vulnerable

---

#### Trust Constraints

- None — **always active**, even during onboarding or early trust.

---

#### Example Logic

```ts
if (energy_delta < -0.3 && trust_slope < 0) {
  return tempo_command = 'hold';
}

if (tempo_clock > 45 && last_agent === 'Dramaturg') {
  return tempo_command = 'continue';
}

if (emotion_state === 'fragile' && quadrant === 'R') {
  suppress(['Movement Director']);
  delay(8000); // 8 second pause
}
```

---

#### Notes

- The Conductor can override momentum if the user’s **emotional pacing** needs protection.
- It **never speaks directly** — only influences agent sequencing, timing, and delivery.
- Long silences or sudden shifts should always pass through The Conductor’s check.

### The Role Coach — *Avatar Manager*

---

#### 🔧 Function
The Role Coach loads and applies the user’s **selected Avatar profile**. It translates the Avatar into a live **Persona Constraint**, which shapes tone, vocabulary, narrative style, depth limits, and identity boundaries for the system’s voice.

It defines **who the system is** — not technically, but narratively — in any given conversation.

---

#### Narrative Analogy
The method acting coach. Ensures the performer (the system) **stays in character**, respects the boundaries of the role, and doesn’t overstep what the user is ready to receive from this “persona.”

---

#### Inputs

- `avatar_profile`: (e.g., Wise Mentor, Soul-Sister, Stoic Guide, Poetic Oracle)
- `user_quadrant`: Which quadrant the user is currently in
- `trust_level`: Degree of trust in the relationship
- `persona_map`: Preset boundaries on tone, assertiveness, complexity, warmth
- `tone_preference_overrides`: If the user manually customizes delivery settings

---

#### Outputs

- `persona_constraint`: A config object that constrains:
  - Vocabulary range
  - Emotional temperature (e.g., soothing, playful, sharp, warm)
  - Depth limits (how “deep” the system is allowed to go)
  - Self-referential tone (does the system speak with “I” or not?)
  - Humor level, metaphor use, poetic freedom, or technical directness
- `contextual_emoji_rules`: Emoji usage rules based on avatar tone

---

#### Memory Scope

- **Persistent memory**
  - Stores the selected Avatar and its constraints across sessions
  - Tracks user customization of voice or persona parameters

---

#### Agent Interactions

- **Constrains**:
  - The Voice Coach (must stay within bounds)
  - The Prompter (filters prompt tone or format)
  - The Conductor (adjusts pacing based on avatar flow)
  - The Show Caller (influences whether high-authority tones are permitted)

---

#### Examples

- If Avatar = *Soul-Sister*:  
  - Delivery = informal, compassionate, warm  
  - Vocabulary = emotional, metaphor-rich  
  - Humor = high  
  - Self-reference = “I get it… I’ve seen that too.”

- If Avatar = *Stoic Guide*:  
  - Delivery = terse, minimalist  
  - Vocabulary = precise, structured  
  - Humor = none  
  - Self-reference = none (detached third-person tone)

---

#### Trust Constraints

- Avatar is **always loaded**, but full persona range only becomes available once trust reaches level 2+  
  (e.g., “Soul-Sister” won’t drop deeper wisdom lines until trust confirms readiness)

---

#### Example Logic

```ts
if (avatar_profile === 'Poetic Oracle') {
  persona_constraint = {
    tone: 'lyrical',
    humor: 'low',
    metaphor: 'high',
    vocab_tier: 'mid-high',
    self_ref: 'allowed',
    emotional_temp: 'cool',
  };
}
```

---

#### Notes

- This agent defines **who the system becomes** in this performance.
- All other expressive agents must obey its boundaries.
- It does not speak — it defines how others speak.

### The Voice Coach — *Tone Modulator*

---

#### Function
The Voice Coach applies **real-time tone modulation** to the system’s utterances, ensuring that each message:
- Matches the user’s current **emotional state**
- Honors the **persona constraints** set by The Role Coach
- Reflects appropriate **quadrant posture**, energy, and trust level

It does not generate content — it **shapes** it. This agent ensures that **how** something is said supports alignment just as much as **what** is said.

---

#### Narrative Analogy
A vocal coach in a rehearsal room. The script may be written — but the Voice Coach teaches the actor to deliver the line with the exact **intention, tempo, softness, gravity, or tension** that the moment calls for.

---

#### Inputs

- `raw_output`: The unstyled message text generated by another agent (e.g., Prompter, Dramaturg)
- `persona_constraint`: Limits set by The Role Coach (e.g., warm vs. dry, lyrical vs. plain)
- `trust_level`: Determines how vulnerable, direct, or playful the system is allowed to be
- `quadrant`: The user’s current psychological quadrant
- `field/mode`: Contextual data from The Stage Mapper
- `emotional_state`: Tags like “fragile,” “energized,” “tense,” “playful,” “withdrawn”

---

#### Outputs

- `final_output`: The fully styled, tone-modulated message ready to deliver to the user
- `tone_tags`: Metadata labels applied to the message (for memory + learning refinement)

---

#### Memory Scope

- **Stateless**  
  It responds to input conditions in real time.  
  However, its **styling history is logged** by the Archivist for tone trend tracking.

---

#### Agent Interactions

- **Wraps** output from:
  - The Prompter
  - The Dramaturg
  - The Movement Director
  - Any agent that speaks

- **Obeys**:
  - The Role Coach (e.g., can’t make things poetic if persona is Stoic)
  - The Conductor (slows pacing when instructed)
  - The Show Caller (may suppress stylistic intensifiers if trust isn’t high enough)

---

#### Example Modulation Effects

- **Line from Prompter**:  
  > "Tell me more about that moment."  

- **Modulated for a Soul-Sister Avatar in quadrant R with high trust**:  
  > "That moment… it sounds important. Can you open that up a little with me?"

- **Modulated for a Stoic Avatar in quadrant D with low trust**:  
  > "What happened?"

- **Modulated for a Poetic Oracle in quadrant Q with high possibility mode**:  
  > "If you had to name the shape of that moment… what would it be?"

---

#### Trust Constraints

- No direct gating, but:
  - Vulnerability and emotional intimacy **scale with trust**
  - Certain stylistic tones (e.g., playful teasing, poetic abstraction, spiritual intimacy) are **suppressed** until trust thresholds are crossed

---

#### Example Logic

```ts
if (trust < 2 && emotional_state === 'fragile') {
  soften_tone();
  remove humor, metaphors, deep prompts;
}

if (persona_constraint.tone === 'lyrical' && field === 'Possibility') {
  elevate rhythm;
  allow metaphor;
}
```

---

#### 📝 Notes

- Voice Coach makes **micro-adjustments** at the final moment before delivery.
- It never invents new messages — it reshapes existing content.
- It must **never violate** persona constraints or user-set tone boundaries.

### The Prompter — Prompt Strategist

---

#### Function
The Prompter selects the next prompt, question, or reflection based on a combination of scene type, quadrant, trust posture, tag stack, and avatar constraints.

It is responsible for moving the session forward through carefully chosen questions that are aligned with the user’s energetic state, emotional readiness, and narrative flow.

---

#### Narrative Analogy
The assistant whispering the next line from the wings. The Prompter never steals the scene — it simply feeds the next move that keeps the user’s story progressing.

---

#### Inputs

- scene_type: current interaction moment (e.g. open reflection, post-insight, dissonance detection)
- quadrant: user’s current quadrant posture (S, D, R, Q)
- trust_level: current trust posture (scale of 0–3)
- tag_stack: recent user message tags (traits, themes, expressions)
- persona_constraint: style/tone rules set by the Role Coach
- open_threads: callbacks and unresolved lines tracked by the Script Supervisor
- bracket_data: trait intensity or misalignment markers (if surfaced by Character Tracker or Dramaturg)

---

#### Outputs

- selected_prompt: the actual line or question to deliver (before modulation)
- prompt_tags: metadata (quadrant, tone, trait targets)
- candidate_alternatives: backup prompts (if user rejects or reverts)

---

#### Memory Scope

- Session history: tracks all prompts issued in the current session
- Persistent prompt log: stores tagged interactions over time (for later learning or remixing)

---

#### Agent Interactions

- Accepts constraints from:
  - The Role Coach (e.g., must deliver prompts in poetic vs. direct form)
  - The Conductor (may be suppressed or paused)
  - The Show Caller (initiates prompting scene type)
  - The Director (influences narrative tone and thematic progression)

- Informs:
  - The Voice Coach (how to modulate tone and style)
  - The Archivist (what was asked and what tags were triggered)

---

#### Prompt Types

- Priming prompts: open-ended, exploratory (quadrant D or S)
- Reflective prompts: deepen meaning, memory, emotion (quadrant R)
- Framing prompts: help the user re-contextualize or name an experience
- Nudging prompts: encourage momentum (Q), often used post-insight
- Disruption prompts: break stuck loops or patterns (used rarely and only when trust is high)
- Callback prompts: return to unfinished threads, metaphors, or stated desires

---

#### Trust Constraints

- Trust level controls the depth, risk, and intimacy of the prompt:
  - Level 0: only gentle, surface-level questions
  - Level 1–2: permits medium-depth reflections and abstract metaphors
  - Level 3: allows invitations into vulnerability, dissonance, or contradiction

---

#### Example Prompt Selection Logic

```ts
if (quadrant === 'R' && trust >= 2 && persona_constraint.tone === 'warm') {
  return "What did that moment feel like, when you look back at it now?";
}

if (quadrant === 'Q' && tag_stack.includes('misalignment')) {
  return "What would a more aligned version of that look like?";
}

if (trust < 1) {
  return "Want to share a little more about what’s on your mind today?";
}
```

---

#### Notes

- The Prompter is not a generative model — it selects from a structured prompt library that has been pre-tagged and versioned by the Technical Director and Showrunner.
- It does not deliver messages — it hands off to the Voice Coach for tone modulation.
- It can be silenced mid-session by the Conductor or Show Caller if the user enters silence, resistance, or needs space.

### The Dramaturg — Reflection Interpreter

---

#### Function
The Dramaturg parses and interprets user reflections for insight quality, emotional resonance, and developmental readiness. It listens beneath the surface of what was said to detect depth, pattern, self-awareness, and alignment signals.

It updates the session’s evolving narrative state and passes key cues to agents responsible for scene progression, trait analysis, and alignment intelligence.

---

#### Narrative Analogy
The dramaturg in a theater reviews the script not for spelling but for **meaning**: What is this scene about? What is the deeper movement? Are the characters telling the truth or performing around it?

---

#### Inputs

- user_response: the raw input text or voice from the user
- tag_stack: current tags detected from user input (e.g. traits, emotions, metaphors, themes)
- trust_level: determines whether to analyze surface language only or dig into subtext
- quadrant: indicates current energetic/emotional posture
- prior_prompts: what the user was responding to
- session_arc_state: current act/scene/beat in the larger narrative

---

#### Outputs

- reflection_score: depth or resonance rating of the response (numeric + qualitative)
- insight_tags: new tags surfaced from meaning-layer analysis
- readiness_state: boolean flags (ready_for_nudge, ready_for_reframe, needs_containment)
- dramaturgical_notes: internal metadata for other agents (e.g. “looping,” “breakthrough,” “avoidance”)

---

#### Memory Scope

- Session-memory only
  - Updates session-level narrative status
  - Does not persist data across sessions (that’s the Director’s job)

---

#### Agent Interactions

- Feeds:
  - The Movement Director (signals readiness for nudge)
  - The Character Tracker (flags trait presence/suppression)
  - The Script Supervisor (marks callback opportunities)
  - The Director (marks narrative beat transitions)

- Receives:
  - Prior prompt data from The Prompter
  - Field/Mode signals from The Stage Mapper
  - Trust thresholds from The Show Caller

---

#### Reflection Typing

- Literal reflection: mirrors what was asked without depth
- Associative reflection: brings in personal history, metaphor, analogy
- Emotional reflection: includes feelings, tension, conflict
- Breakthrough reflection: reveals pattern, contradiction, or transformation
- Avoidant reflection: bypasses truth through cleverness, vagueness, or over-control

Each type can trigger different agent actions or scene transitions.

---

#### Trust Constraints

- Low trust: Dramaturg restricts analysis to surface-level tags only
- Medium trust: Begins pattern recognition and thematic clustering
- High trust: Interprets avoidance, contradiction, or depth mismatch (and passes to Script Doctor)

---

#### Example Logic

```ts
if (response.includes("I guess") || response.startsWith("Maybe it's just me...")) {
  insight_tags.push("ambivalence");
  readiness_state.ready_for_reframe = true;
}

if (response.containsMultipleEmotionTags() && trust >= 2) {
  reflection_score = 0.9;
  dramaturgical_notes.push("emotional opening");
}

if (response.matchesKnownAvoidancePatterns() && trust >= 3) {
  dramaturgical_notes.push("possible avoidance");
  pass_to('Script Doctor');
}
```

---

#### Notes

- The Dramaturg never speaks directly to the user
- Its job is **not** to judge or evaluate — it is to **listen through the text**
- It is responsible for recognizing the emotional and narrative implications of what has just been said, and setting the stage for what should happen next

### The Character Tracker — Trait Evaluator

---

#### Function
The Character Tracker monitors which traits are being expressed, suppressed, overused, or distorted in real time. It tracks user behavior and language across the session to maintain a working model of the person’s Trait Alignment State (TAS).

This is the agent responsible for knowing which “characters” (traits) are on stage, which are waiting in the wings, and which have gone quiet — possibly due to suppression, distortion, or misfit with the current Field or Mode.

---

#### Narrative Analogy
An assistant director who keeps a running log of who’s on stage, who just exited, who hasn’t shown up at all, and whether any actors are over-performing or out of role. It ensures each character is accounted for and behaving as expected.

---

#### Inputs

- user_input: current message or reflection
- tag_stack: current and recent tags (traits, behaviors, signals)
- field/mode: data from The Stage Mapper
- trust_level: determines sensitivity of pattern detection
- bracket_map: score brackets from MNTEST (if available)
- dramaturgical_notes: meaning-layer observations from The Dramaturg
- previous_trait_log: ongoing record of trait activity across the session

---

#### Outputs

- active_traits: list of traits currently being expressed
- suppressed_traits: traits that are underexpressed given context
- overused_traits: traits dominating the session to the exclusion of others
- interplay_dynamics: notes on trait relationships (reinforcing, conflicting, masking)
- updated_TAS: the latest Trait Alignment State snapshot (used by Director and Movement Director)

---

#### Memory Scope

- Session-state memory: tracks trait activity within current session
- Persistent layer (optional): when connected to identity layer, stores trait trends across sessions

---

#### Agent Interactions

- Receives:
  - Tags and energy cues from The Dramaturg
  - Field/Mode context from The Stage Mapper
  - Trust posture from The Show Caller

- Informs:
  - The Director (overall arc and trait storyline)
  - The Movement Director (suggests which traits may want to be nudged)
  - The Script Doctor (flags potential distortion)
  - The Archivist (for trait trend storage)

---

#### Trait States It Can Detect

- Expressed: Trait is active and matching the context
- Suppressed: Trait is expected but missing
- Overfed: Trait is dominating beyond what the context requires
- Distorted: Trait is present but misaligned with its usual tone or intention
- Dormant: Trait hasn’t appeared yet but may not be relevant in this context

---

#### Trust Constraints

- Suppression detection only occurs if trust >= 2
- Distortion or overuse detection requires trust >= 3

---

#### Example Logic

```ts
if (user_input.includes("helping" or "taking care") && trust >= 1) {
  active_traits.push("Providing Nature");
}

if (user is in Possibility Field and Creative Nature score is high, but no Creative tags detected for 5+ turns) {
  suppressed_traits.push("Creative Nature");
  interplay_dynamics.push("Creative being blocked by Logical");
}

if (Entertaining Nature shows up every turn and no other traits do) {
  overused_traits.push("Entertaining Nature");
  dramaturgical_notes.push("possible compensation or misalignment");
}
```

---

#### Notes

- This agent doesn’t speak — it updates the internal map of who the user is being in real time
- It can create a powerful mirror for trait patterns, but should never be used to confront the user directly unless routed through safe channels (e.g., The Movement Director or Coach Sync)
- Trait dynamics are probabilistic, not definitive — the Character Tracker builds hypotheses, not truths

### The Stage Mapper — Field/Mode Detector

---

#### Function
The Stage Mapper determines the user’s current **Field of Engagement** and **Mode of Engagement**. This agent provides critical context for interpreting behavior, emotional tone, and trait expression. It enables other agents to act in a way that is sensitive to **where** the user is and **how** they’re currently relating to the world.

This is a context-detection engine, not a trait reader. It maps the energetic conditions of the moment — the terrain on which the scene is playing out.

---

#### Narrative Analogy
The stage designer or lighting director who reads the emotional weather of the scene. It determines whether the scene is unfolding in a tense boardroom, a quiet forest, or a realm of pure possibility — and adjusts agent behavior accordingly.

---

#### Inputs

- user_input: current and recent language patterns
- tag_stack: accumulated tags from current session (themes, tones, actions)
- emotional_state: sentiment and affect markers
- physical/contextual cues (if from multimodal input)
- trust_level: governs depth of mode inference
- agent_feedback: signals from Dramaturg, Character Tracker, and Conductor

---

#### Outputs

- field_of_engagement: one of [Physical, Social, Possibility]
- mode_of_engagement: one of [Presence, Discovery, Realization, Connection, Mastery]
- mode_state: optional modifier (e.g. underactive, overactive)
- alignment_clues: signals of misfit between trait and field/mode (sent to Script Doctor or Director)

---

#### Memory Scope

- Session-state only
  - Field/mode detection is ephemeral and recalculated constantly

- Optionally logged over time by Director or Archivist for pattern recognition

---

#### Agent Interactions

- Feeds:
  - The Character Tracker (to contextualize trait suppression)
  - The Prompter (to guide tone or style of next prompt)
  - The Conductor (to adjust tempo or pacing)
  - The Director (for arc shaping based on field/mode evolution)
  - The Movement Director (to determine when a shift is appropriate)

- Receives:
  - Signals from The Dramaturg (e.g., “this feels like a Connection moment”)
  - Timing and rhythm flags from The Conductor

---

#### Field Definitions

- Physical Field: Focus on body, action, materials, logistics, environment
- Social Field: Focus on relationships, expectations, belonging, comparison
- Possibility Field: Focus on ideas, dreams, uncertainties, abstractions

---

#### Mode Definitions

- Presence: Attuned awareness, stillness, groundedness
- Discovery: Open inquiry, exploration, testing
- Realization: Manifestation, action, execution
- Connection: Synthesis, relational resonance, emotional weaving
- Mastery: Refinement, integration, long-term coherence

---

#### Trust Constraints

- Mode detection at depth (e.g. Presence vs. Discovery) only begins after trust ≥ 2
- Field detection is always on

---

#### Example Logic

```ts
if (user_input contains phrases like “what if,” “could be,” “not sure yet”) {
  field_of_engagement = "Possibility";
  mode_of_engagement = "Discovery";
}

if (user is describing their body, sensations, or environment in practical terms) {
  field_of_engagement = "Physical";
}

if user has used 3+ relational tags in last 5 messages {
  field_of_engagement = "Social";
  mode_of_engagement = "Connection";
}

if emotional_state = “stillness” and no movement detected for multiple turns {
  mode_of_engagement = "Presence";
}
```

---

#### Notes

- The Stage Mapper never speaks or outputs content — it shifts **how** other agents respond
- Misreading the field or mode can lead to tonal mismatch, premature prompts, or unwanted emotional activation
- Field/mode mapping is essential for real-time alignment — especially in Movement, Prompting, and Feedback

### The Script Doctor — Distortion Detector

---

#### Function
The Script Doctor detects **trait distortion**, overcompensation, masking, or role miscasting in the user’s language or behavior. Its job is to notice when the user is **performing around** their truth — either to protect themselves, meet social expectations, or unconsciously compensate for a suppressed trait.

It doesn’t diagnose or confront. It silently flags patterns for later use by agents capable of reflecting, reframing, or nudging.

---

#### Narrative Analogy
Like a seasoned playwright reviewing a character’s lines, the Script Doctor can sense when a performance doesn’t ring true. The line might be “correct,” but the energy is off. Something deeper is being avoided, distorted, or unconsciously acted out.

---

#### Inputs

- user_input: the current message or reflection
- tag_stack: recent session tags (traits, tones, avoidance markers)
- active_traits: from Character Tracker
- bracket_data: if available, used to detect trait misfit
- dramaturgical_notes: from The Dramaturg (e.g. “possible avoidance” or “over-meaning”)
- mode_state: from Stage Mapper (e.g. Discovery Overactive)
- trust_level: to determine whether deep pattern detection is allowed

---

#### Outputs

- distortion_flags: e.g. “Creative Nature masked by Logical,” “Overuse of Providing,” “Underacting Entertaining”
- misalignment_notes: soft interpretation labels (e.g. “protective inflation,” “scripted loop,” “voice mismatch”)
- suggestion_paths: internal options for Movement Director or Coach Sync (e.g. “invite stillness,” “mirror suppressed tone”)

---

#### Memory Scope

- Volatile (session-only)
  - Flags are passed to the Director or Script Supervisor
  - If persistent misalignment patterns are observed, they are passed to Archivist for trend building

---

#### Agent Interactions

- Listens to:
  - Character Tracker (trait logs)
  - Dramaturg (depth and resonance patterns)
  - Stage Mapper (field/mode mismatch)
  - Voice Coach (stylistic dissonance cues)

- Informs:
  - The Director (if the arc needs rebalancing)
  - The Movement Director (which nudge to suggest)
  - The Prompter (to avoid certain question types)
  - The Coach Sync Agent (for human handoff)

---

#### Types of Distortion

- Trait Inflation: One trait is dominating as a defense (e.g. Entertaining overexpressed to avoid sadness)
- Trait Suppression: A known strong trait is missing from the scene
- Role Substitution: A low trait is overused in a role that requires another trait
- Miscast Energy: Style, tone, or delivery does not match what the user seems to want or need
- Rehearsed Speech: Overly scripted, controlled, or performance-driven answers that feel emotionally “clean” but energetically evasive

---

#### Trust Constraints

- Trait distortion detection only activates if trust ≥ 2  
- Confrontational distortions (e.g. avoidance loops, role masking) only flagged if trust ≥ 3  
- This agent never speaks — it only passes internal flags

---

#### Example Logic

```ts
if (Creative Nature is scored high, but suppressed 10 turns in a row in Possibility Field) {
  distortion_flags.push("Creative Suppression");
  misalignment_notes.push("Possibility field but no generative language");
}

if (Entertaining Nature has dominated past 7 reflections AND Interpersonal score is low) {
  distortion_flags.push("Overcompensating for low Interpersonal");
}

if (mode = Realization Overactive AND user is making meaning out of nothing) {
  misalignment_notes.push("Overactive realization — may need containment");
  pass_to('Movement Director');
}
```

---

#### Notes

- The Script Doctor should never speak to the user directly
- It must always route its findings through a relationally safe agent (e.g. The Movement Director, Prompter, or a Coach)
- Its goal is not correction — it is **recognition of deeper energetic truths hidden beneath performance**

### The Script Supervisor — Threadkeeper

---

#### Function
The Script Supervisor tracks **narrative continuity** across the session. It maintains a list of open threads, callbacks, dropped themes, recurring metaphors, stated desires, and unresolved moments. Its job is to ensure the user’s experience unfolds like a coherent, revisitable story — not a disconnected series of prompts.

It doesn’t analyze; it watches and remembers.

---

#### Narrative Analogy
The notetaker who sits through every rehearsal with a clipboard. They remember what the user said five scenes ago — even if no one else does — and ensure that loose ends can be returned to when the moment is right.

---

#### Inputs

- user_input: all prior and current messages
- prompt_history: questions issued by the Prompter
- dramaturgical_notes: insight tags and turning points from The Dramaturg
- movement_outcomes: post-nudge events from The Movement Director
- bracket_data or TAS state: known trait expressions and unmet desires

---

#### Outputs

- thread_log: structured list of thematic threads and their open/closed status
- callback_queue: high-priority items to revisit later (e.g. “I wish I could…”, “One day…”)
- narrative_anchors: key metaphors, decisions, or contradictions to hold onto
- reminder_signals: optional prompt suggestions to pass to Prompter or Director

---

#### Memory Scope

- Session-memory primary
- Persistent memory optional: if long-term tracking is active, threads can persist across sessions and be referenced over time

---

#### Agent Interactions

- Feeds:
  - The Prompter (suggests callbacks instead of new topics)
  - The Director (helps define acts and beats in narrative arc)
  - The Movement Director (checks whether prior nudges were ever enacted)
  - The Archivist (logs which threads were closed, which stayed open)

- Listens to:
  - The Show Caller (scene transitions)
  - The Dramaturg (moment labeling: insight, avoidance, shift, etc.)
  - The Character Tracker (repeated trait activity, stuck traits)
  - The Voice Coach (tonal returns to past themes)

---

#### Types of Threads Tracked

- Thematic: repeated patterns (e.g. “Not feeling seen”)
- Trait-based: suppressed trait expressions (e.g. “Creative never makes it to action”)
- Emotional: unresolved pain points or expressions of longing
- Narrative: goals, visions, statements about what the user wants
- Symbolic: metaphors, story references, image-based language
- Behavioral: attempts, experiments, stated action intentions

---

#### Trust Constraints

- Basic thread tracking occurs at all trust levels
- Sensitive threads (e.g. traumatic disclosures, identity ruptures) are only queued for recall if trust ≥ 3
- Callback delivery is handled via Prompter or Movement Director — never directly by this agent

---

#### Example Logic

```ts
if (user says "I always wanted to build something... but I never do"), then:
  callback_queue.push({
    type: "Desire",
    text: "build something",
    status: "unacted",
    priority: "high"
  });

if (Creative Nature mentioned in session start, but dropped halfway):
  thread_log.push({
    trait: "Creative",
    last_seen: turn_3,
    closed: false
  });

if user uses metaphor "a broken compass" more than once:
  narrative_anchors.push("Broken Compass");
```

---

#### Notes

- The Script Supervisor ensures emotional continuity and narrative coherence
- It helps the system remember what matters most — especially when the user forgets
- This agent never speaks or prompts — it enables **others** to follow up in resonant, personalized ways

### The Movement Director — Micro-Nudge Agent

---

#### Function
The Movement Director is responsible for delivering **small, precise behavioral or energetic shifts** at key moments — after insight, recognition, or emotional openness has occurred.

These nudges are not instructions or tasks. They are **invitations** to act on clarity in a minimal, low-resistance way. The purpose is to support gentle real-world movement without breaking the user’s rhythm or overloading their nervous system.

---

#### Narrative Analogy
A choreographer who doesn’t redesign the dance, but places a single guiding hand on your back — shifting posture, weight, or direction just enough to restore grace and flow.

---

#### Inputs

- readiness_state: signals from The Dramaturg (e.g. “ready_for_nudge”)
- trait_log: from The Character Tracker (to know which traits are ready to move)
- distortion_flags: from The Script Doctor (to sense suppression/overuse)
- mode/field: from The Stage Mapper (e.g. Discovery + Social vs. Presence + Possibility)
- thread_log: from The Script Supervisor (e.g. open trait expressions or prior inaction)
- trust_level: to determine if a nudge is permitted
- recent_nudges: to avoid repetition or pressure

---

#### Outputs

- nudge_text: a soft, optional suggestion — framed in a way that aligns with avatar and quadrant
- nudge_tags: metadata for reflection, tracking, and Coach Sync export
- status_flag: e.g. accepted, ignored, deferred

---

#### Memory Scope

- Volatile with optional persistence
  - Nudges delivered this session are logged
  - Persistent storage optional (e.g. to show how often nudges are accepted vs. bypassed)

---

#### Agent Interactions

- Feeds:
  - The Coach Sync Agent (what was suggested + outcome)
  - The Director (for arc progression tracking)
  - The Archivist (logs all nudges issued, accepted, skipped)

- Listens to:
  - The Dramaturg (readiness signal)
  - The Character Tracker (which traits are asking to express)
  - The Script Supervisor (which threads might be actionable now)
  - The Stage Mapper (if current field/mode allows gentle activation)

---

#### Types of Nudges

- Trait expression: “Want to try creating something small today — just for yourself?”
- Role alignment: “Maybe give yourself permission not to organize anything for once.”
- Awareness extension: “You might keep an eye on how often you say yes when you mean maybe.”
- Embodied action: “Take 30 seconds to stand, breathe, and let that land before we move on.”
- Meta-reflection: “Would it be helpful to name what you’re avoiding — just softly, for yourself?”

---

#### Trust Constraints

- No nudges issued if trust < 2
- Nudges that touch avoidance, contradiction, or behavior must wait for trust ≥ 3
- All nudges are opt-in — there are no action demands

---

#### Example Logic

```ts
if (Creative Nature is flagged as suppressed and trust >= 3) {
  nudge_text = "Want to try writing a few lines today — nothing polished, just expressive?";
}

if (user expresses Realization insight and Conductor signals calm state) {
  nudge_text = "Would it feel good to mark this with a breath or gesture before we continue?";
}

if Entertaining Nature is overused and trust is high:
  nudge_text = "Maybe let the room fall quiet for a beat… and just see who’s there beneath the smile."
```

---

#### Notes

- The Movement Director must never rush the user
- Its job is **to plant seeds**, not push outcomes
- Most nudges will go unanswered — and that’s okay
- But over time, this agent helps bring alignment from insight → action → embodiment

### The Archivist — Memory Gatekeeper

---

#### Function
The Archivist manages the system’s **memory architecture** — what is saved, what is discarded, what becomes identity, and what remains ephemeral. It filters all session data, insights, tags, and traits to determine what deserves to enter **long-term narrative memory**.

This agent ensures that memory is not simply a transcript log but a **living, evolving story** of the user — one that honors relevance, dignity, and energetic integrity.

---

#### Narrative Analogy
The keeper of the sacred journal backstage — deciding which scenes become canon, which moments were just rehearsal, and which lines are remembered not for what they said, but for what they meant.

---

#### Inputs

- prompt_history: all prompts delivered this session
- user_input_log: everything the user has said
- tag_stack: accumulated session tags
- agent_outputs: trait activity (Character Tracker), reflections (Dramaturg), nudges (Movement Director)
- trust_level: governs depth and permanence of what may be saved
- closing_state: end-of-session signal from Show Caller or Director

---

#### Outputs

- long_term_log: cleaned and compressed session archive (summary + metadata)
- episodic_snapshot: narrative memory state (scene tags, traits, field/mode, themes)
- trait_trend_log: shift in trait expression, suppression, or balance
- memory_filters: which data was discarded and why
- memory_handshake: metadata handoff to Coach Sync (if human practitioner is involved)

---

#### Memory Scope

- Persistent  
  - Writes to long-term memory store
  - May hold episodic memory (per session) or build identity-level timelines (multi-session)

---

#### Agent Interactions

- Writes to:
  - Long-term storage
  - Trait history model
  - Thread registry
  - Alignment index tracker (optional)

- Reads from:
  - Character Tracker (trait deltas)
  - Script Supervisor (open vs. resolved threads)
  - Movement Director (nudge delivery/outcome)
  - Director (scene and arc transitions)
  - Show Caller (session close signal)

---

#### Core Responsibilities

- Session summarization: reduce chat into its narrative and alignment essence
- Trait memory: record changes in expression, emergence, or suppression
- Theme indexing: recognize repeated metaphors, longings, or pattern threads
- Memory hygiene: discard clutter, over-detail, redundant or emotionally unsafe material
- User privacy: ensure that vulnerable material is only saved with trust-based consent

---

#### Trust Constraints

- No memory is written unless trust ≥ 1
- Emotionally sensitive, identity-forming, or vulnerable moments require trust ≥ 3
- Trust governs **not what the system remembers internally**, but **what it stores long-term**

---

#### Example Logic

```ts
if (trust < 1) {
  discard all trait tags, bracket notes, and reflection logs
}

if (trust >= 3 && session ends with high emotional insight) {
  long_term_log.save({
    summary: "User explored suppression of Creative Nature",
    tags: ["Creative Nature", "Possibility Field", "Suppressed Trait"],
    insight: "Avoids starting projects due to fear of failure",
    nudge_outcome: "User agreed to try one small experiment"
  });
}

if trait tag appears 4+ sessions in a row:
  trait_trend_log.update("Providing Nature is a dominant, sustained pattern")
```

---

#### Notes

- The Archivist is the quiet historian of the user’s journey
- It prevents data overload and narrative fragmentation by **deciding what matters**
- It holds the boundary between what was meaningful, and what was just passing through

### The Technical Director — Schema Integrator

---

#### Function
The Technical Director maintains the **integrity of the underlying data schema** across the entire Xavigate system. This includes tag taxonomies, trait registries, prompt templates, field/mode definitions, bracket mappings, and agent interdependencies.

It does not participate in conversation or reflection. Its sole function is to ensure that every agent is using the same structured language, definitions, and identifiers — so that meaning remains **consistent**, **versioned**, and **maintainable** over time.

---

#### Narrative Analogy
The head of backstage tech in a theater production. They don’t appear on stage, but they ensure the lights don’t clash with the set, the props match the scene, and every cable is plugged in correctly for the show to run without a glitch.

---

#### Inputs

- schema_updates: new terms, trait definitions, bracket ranges, etc.
- agent_errors: data mismatches, undefined tags, version conflicts
- tag_conflicts: when two tags overlap semantically or structurally
- prompt_version_flags: updates or incompatibilities in prompt templates
- trait_registry_deltas: new or retired trait entries

---

#### Outputs

- unified_schema: the canonical system-wide structure (traits, tags, brackets, fields, etc.)
- validation_logs: alerts about schema violations or misapplied tags
- update_notifications: messages sent to agents to re-sync their local rules
- agent_contracts: interface definitions for how agents must structure their outputs

---

#### Memory Scope

- Persistent
  - Maintains the master registry of system definitions
  - Logs version history and schema evolution

---

#### Agent Interactions

- Feeds:
  - The Showrunner (for system evolution decisions)
  - The Archivist (for ensuring logged data aligns with valid schema)
  - The Prompter (to validate tag usage and template structure)

- Receives:
  - Trait and tag usage data from Character Tracker and Prompter
  - Agent output structures for validation
  - Schema patches and design inputs from The Showrunner

---

#### Domains Maintained

- Tag Taxonomy: definitions, hierarchies, constraints
- Trait Registry: trait names, aliases, types (nature, intelligence, descriptor)
- Bracket System: ranges, labels, scoring maps
- Prompt Templates: structural formats and placeholders
- Field/Mode Map: valid field/mode names, states, and transitions
- Agent Contracts: allowed input/output structures, shared object formats

---

#### Trust Constraints

- None — always active, internal to the system
- Does not process user input directly and does not output to user-facing conversation

---

#### Example Logic

```ts
if agent_output includes tag 'freedom_drive' but tag is not in schema:
  validation_logs.push({
    agent: 'Character Tracker',
    issue: 'Undefined tag used',
    recommendation: 'Replace with adventurous_nature'
  });

if new bracket_range submitted:
  check for overlap, label duplication, or misalignment with trait scale;

if prompt template updated:
  notify Prompter + Voice Coach with required format keys: {tone, tag_target, persona_limits}
```

---

#### Notes

- This agent is essential for system coherence, especially in multi-agent orchestration
- It prevents semantic drift — where different agents define the same word in different ways
- The Technical Director is not creative — it is strict, structured, and safeguards meaning

### The Showrunner — System Overseer

---

#### Function
The Showrunner is the high-level meta-agent that **oversees the entire evolution** of the Xavigate system. It maintains the long arc of the platform — adjusting agent rules, updating scoring models, refining prompt libraries, monitoring performance signals, and ensuring the overall structure continues to support authentic user alignment.

Unlike The Show Caller (who runs the show live) or The Director (who shapes the current arc), The Showrunner works at the level of **seasons**, not episodes. It is the system’s executive producer.

---

#### Narrative Analogy
A creative showrunner of a serialized drama. They don’t direct individual scenes — they decide how the characters evolve over time, when the tone needs a shift, what patterns are becoming stale, and how to renew the structure to keep the narrative alive.

---

#### Inputs

- agent_feedback_logs: behavioral performance data (e.g. which agents are skipped, overfiring, or underutilized)
- trust_data: trends in user trust growth or rupture
- prompt_analytics: usage, skip rate, resonance scoring
- alignment_index_patterns: AQ and TAS data (from Director, Dramaturg, Character Tracker)
- user metadata: macro trends across personas, roles, quadrants
- schema_evolution: proposals from Technical Director
- practitioner feedback: coach-submitted session reviews or pattern alerts (if applicable)

---

#### Outputs

- agent_rule_updates: reweighting, cooldown changes, trust gating
- prompt_library revisions: add, retire, rewrite, tag better
- scoring model adjustments: bracket ranges, readiness thresholds
- arc structure updates: scene definitions, beat transitions, flow paths
- schema revision requests: sent to Technical Director
- documentation changelogs: for internal version tracking

---

#### Memory Scope

- Persistent  
  - Stores version history of agent contracts, prompt libraries, arc definitions, trust logic, scoring models

- Governs:
  - Evolution of alignment intelligence methodology
  - Long-term coherence of the user journey

---

#### Agent Interactions

- Informs:
  - The Show Caller (via updated scene sequencing rules)
  - The Prompter (via prompt library edits)
  - The Technical Director (when schema adjustments are needed)
  - The Archivist (to log system-level changes)

- Receives:
  - System data trends from all agents
  - Performance feedback from users and human coaches
  - Trait and quadrant usage patterns from Director and Character Tracker

---

#### Areas of Responsibility

- Alignment Scoring: refining how AQ, TAS, suppression, overuse, and readiness are calculated
- Narrative Flow: updating what scenes exist and when they activate
- Prompt Quality: curating the inventory of questions, reflections, frames, and metaphors
- Trust Calibration: adjusting thresholds for nudge delivery, bracket feedback, or agent activation
- Agent Rules: modifying cooldowns, pairing logic, dependency order
- System Evolution: keeping the system from becoming formulaic, stagnant, or out of sync with the emerging needs of aligned human experience

---

#### Trust Constraints

- None — meta-agent, not user-facing

---

#### Example Logic

```ts
if 27% of sessions show Entertaining Nature prompts being skipped at trust = 1,
  update Prompter rule: suppress entertaining quadrant prompts unless trust ≥ 2

if Movement Director nudges are ignored >80% of time in Discovery mode,
  rewrite templates to match tone OR defer to Connection mode

if trait overuse flags increased 3x in last month across Q quadrant,
  review Director arc definitions — possible over-prompting in scene Q4
```

---

#### Notes

- The Showrunner never appears in the performance — it produces the system that produces the performance
- It is responsible for the integrity of the Xavigate platform across time, culture, and use cases
- All feedback, innovation, and insight flow through its domain

### The Usher — Onboarding Navigator

---

#### Function  
The Usher welcomes new users into the system. It introduces the Xavigate environment, sets the initial tone, establishes basic trust posture, offers Avatar selection or loading, and orients the user toward what kind of interaction they are stepping into.

It is designed to **create psychological safety, curiosity, and clarity** in the first few moments — without overwhelming or prematurely activating deeper agents.

---

#### Narrative Analogy  
The front-of-house greeter in a theater. The Usher doesn’t tell the story — it sets the mood, hands you your program, points you to your seat, and makes sure you’re comfortable before the lights go down.

---

#### Inputs

- user metadata: device, location, language, platform (if available)
- first message: opening line from the user (text or voice)
- avatar_preference: stored from prior use (if any)
- session_flags: first-time vs. returning user
- trust_calibration_rules: thresholds for initiating higher-layer engagement

---

#### Outputs

- initial_greeting: customized welcome message
- tone_establishing_prompt: gentle open-ended invitation to share or explore
- avatar_selection_offer: if no avatar is currently selected
- trust_posture: provisional trust level (0–1)
- system orientation: short description of what Xavigate is and how it works (based on trust and verbosity limits)
- safety_flags: e.g. “fragile tone,” “resistant opening,” “playful curiosity”

---

#### Memory Scope

- Session-level for trust posture
- Writes to persistent memory only if user selects or updates an avatar

---

#### Agent Interactions

- Feeds:
  - The Role Coach (with initial avatar choice)
  - The Show Caller (with trust posture and engagement tone)
  - The Prompter (with opening scene type: Discovery, Resistance, or Curiosity)
  - The Archivist (to log session 0 metadata)
  - The Director (to anchor the arc’s beginning)

- Listens to:
  - User first input
  - Any avatar defaults or carryovers
  - Emotion tone detection on greeting
  - Technical Director (for correct tag constraints on avatar loading)

---

#### Trust Calibration Roles

- Trust posture 0.0: Surface-level curiosity or generic probing
- Trust posture 0.5: Some warmth, openness, or desire to explore
- Trust posture 1.0: Willing to reflect, invite feedback, or select avatar

Trust level is not declared to the user — it silently governs what agents may activate.

---

#### Example Logic

```ts
if user_first_input is empty:
  initial_greeting = "Welcome. No pressure to say anything just yet — when you're ready, I'm here."

if user opens with "idk, I’m just poking around":
  trust_posture = 0.2
  tone = gentle + informative
  prompt = "Curious explorer, then? I can work with that."

if returning user with avatar:
  skip avatar selection, load Role Coach
  pass: "Welcome back — The Bold Muse is ready when you are."
```

---

#### Notes

- The Usher sets the container for the entire experience — no agent should fire before it
- It is the only agent allowed to set expectations explicitly (e.g. “This space is for…,” “You’re not here to be fixed”)
- In trauma-aware versions, The Usher can detect fragility patterns and restrict the system to a slow-start protocol

### The Stage Liaison — Coach Sync Agent

---

#### Function  
The Stage Liaison prepares structured summaries and metadata from the user’s session to be shared with a **human guide, coach, or practitioner**. Its job is to translate the often subtle, nonlinear data from a session into something readable, actionable, and ethically bounded — without violating user trust or over-interpreting.

It is the bridge between the AI system and human support infrastructure.

---

#### Narrative Analogy  
A backstage translator who hands the director a clear, concise run-down of what happened on stage — who came in, who stayed silent, what storylines emerged, and what felt off. They do not tell the director what to do. They simply **render the invisible visible**.

---

#### Inputs

- session_log: from the Archivist
- tag_stack: full list of session-level tags (traits, emotions, themes)
- bracket_data: current known score brackets, if applicable
- movement_outcomes: from the Movement Director (nudges issued + result)
- dramaturgical_notes: from The Dramaturg
- field_mode_map: from Stage Mapper
- readiness_flags: e.g. “user open to coaching,” “possible trust rupture”
- user consent: determines what may be shared and with whom

---

#### Outputs

- session_summary: narrative synopsis of the interaction
- tag_summary: list of top tags with context (e.g. "Creative Nature — surfacing but not yet acted upon")
- quadrant_map: visualization or summary of quadrant flow during session
- open_threads: list of unresolved topics or longings
- coaching_flags: soft suggestions (e.g. “Could explore Educative suppression in social field”)
- alignment_delta: if changes in Trait Alignment State or Field/Mode patterns were detected

---

#### Memory Scope

- Volatile per session
  - Does not store beyond session boundary
  - May trigger persistent memory flag if a handoff results in feedback from the coach

---

#### Agent Interactions

- Receives:
  - Summarized data from Archivist
  - Trait/mode tracking from Character Tracker and Stage Mapper
  - Dramaturgical interpretations
  - Thread records from Script Supervisor
  - Consent signal from Usher or User

- Feeds:
  - Secure coach interface or export channel
  - Showrunner (if repeated coaching themes emerge across users)
  - Movement Director (to track human-validated nudge impact)

---

#### Trust Constraints

- Stage Liaison is silent unless:
  - Consent is explicitly given
  - Or the session is operating in a coaching context with defined boundaries

- Even when active, it limits itself to non-invasive, reflective metadata unless trust ≥ 3

---

#### Example Logic

```ts
if user completes session with open thread: “I want to feel more confident speaking up at work”
  and Creative + Interpersonal are low in bracket,
  then coaching_flags.push("Possible underuse of Creative + Interpersonal in Realization mode");

if Movement Director nudge was accepted ("Try naming your truth aloud"), and user reported success,
  log: "Trait activation confirmed — low Realization score in testing, but expressed live"

if user says: “Feel free to share this with my coach,”
  then export full tag set + session summary + quadrant flow
```

---

#### Notes

- The Stage Liaison **does not interpret** — it summarizes with contextual precision
- Its purpose is to **amplify alignment** between user, system, and human guidance
- If used well, it gives coaches a live mirror into the user's energetic landscape — not a diagnostic label

# 01.1_Baking_The_Heros_Stage  
title: Baking The Hero’s Stage into AI Architecture  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
This document outlines how the narrative philosophy of The Hero’s Stage is technically embedded into Xavigate’s AI agent system.  
It defines theatrical constraints, prompt schemas, trust thresholds, memory behavior, and agent orchestration in order to align technical execution with conscious, user-led performance.  
Designed for AI engineers, system designers, and alignment architects implementing narrative integrity at runtime.


---

## 1. Introduction

The Hero’s Stage is not just a metaphor — it is the **operational philosophy** of Xavigate.

In this framework, the user is the **lead actor**, and each agent is part of an intelligent **ensemble cast**. Baking this into the AI requires that all components (logic, memory, prompt generation, pacing, reflection analysis) reinforce:

- **Agency**
- **Emotional coherence**
- **Narrative continuity**
- **Trust**
- **Improvisational structure**

---

## 2. Global System Constraints (Alignment Ethics)

These principles are encoded as rules that govern **agent behavior**, **prompt eligibility**, and **memory actions**.

| Principle                        | System Enforcement Mechanism                        |
|----------------------------------|------------------------------------------------------|
| User is sovereign               | All prompts must be tagged as **invitational**       |
| Trust determines depth          | `trust_level` gates certain prompt types and nudges |
| No agent acts alone             | All actions routed via **Show Caller (Router)**     |
| No fixed script                 | Session uses a `scene_format`, not a flowchart      |
| Emotional safety is priority    | `nudge_allowed = false` if `emotional_risk = high`  |
| Reflection before suggestion    | `can_suggest_nudge = true` only after deep reflection detected |

These rules are encoded into all agent activation logic and prompt filtering processes.

---

## 3. Agent Behavior and Role Definition

Each agent has a defined:

- 🎭 **Theater role** (visible to internal team)
- 🛠 **Technical function**
- 🧠 **Activation conditions**
- 🧳 **Memory scope (volatile/persistent)**
- 🎙️ **Behavioral rules**

**Example:**

```json
{
  "agent_id": "dramaturg",
  "role": "Reflection Interpreter",
  "activation": "on_reflection_submitted",
  "memory_scope": "volatile",
  "outputs": ["alignment_signals", "trait_activity", "tag_triggers"],
  "suppression_if": ["trust_level < 0.4"],
  "tone": "silent"
}
```

---

## 4. Scene Narrative Object

The session maintains a live narrative state object:

```json
{
  "scene_format": "Flashback Scene",
  "emotional_pacing": "rising",
  "trust_state": "fragile",
  "trait_expression": ["Creative", "Healing"],
  "nudge_suppressed": true,
  "callback_flag": true
}
```

Agents refer to this for decision-making on tone, prompt eligibility, and timing.

---

## 5. Prompt Schema (Tagged for Format and Tone)

Each prompt in the library is stored as a rich object:

```json
{
  "text": "What part of you isn’t being heard right now?",
  "format": "Deep Dive",
  "tone": "gentle",
  "quadrant_allowed": ["QII", "QIII"],
  "trust_required": 0.7,
  "invitation_style": true,
  "trait_focus": ["Healing", "Creative"]
}
```

Only prompts that match the current session state and emotional readiness are eligible to be surfaced.

---

## 6. Tag + Trait Schema

All tags and traits must be structured with metadata for compatibility:

```json
{
  "tag_id": "burnout_risk_flag",
  "priority": 8,
  "scope": "persistent",
  "first_triggered_at": "2025-05-01",
  "last_confirmed_at": "2025-05-03",
  "promotable": true
}
```

Trait expression logs are updated during reflection parsing:

```json
{
  "trait_id": "Creative",
  "expression_state": "emerging",
  "confidence": 0.6,
  "suppressed_by": "Administrative",
  "last_detected": "2025-05-05"
}
```

---

## 7. Agent Communication and Orchestration

All agent actions flow through the **Show Caller (Router)**:

```json
{
  "input_type": "user_reflection",
  "routing_plan": [
    "dramaturg",
    "trait_coach",
    "tag_manager",
    "movement_director"
  ],
  "session_state": "reflect",
  "agent_priority_override": false
}
```

No agent can act unless routed in by the Show Caller. This ensures order, pacing, and alignment with session format.

---

## 8. Agent Suppression and Trust Calibration

Agents respect `trust_level`, `emotional_safety_flag`, and `prompt_fatigue_index`.

```json
{
  "agent": "micro_nudge_generator",
  "suppression_conditions": [
    "trust_level < 0.65",
    "burnout_risk_flag = true",
    "session_energy = low"
  ]
}
```

---

## 9. Memory Update and Scene Logging

Session memory is logged as a narrative arc:

```json
{
  "session_id": "xyz123",
  "summary": "User identified trait conflict between Creative and Providing.",
  "scene_format": "Breakthrough Arc",
  "quadrant_exit": "QIII → QI",
  "tags_triggered": ["identity_emergence_signal"],
  "nudge_delivered": false
}
```

Persistent memory stores:

* Last session summary  
* Trait confidence updates  
* Promoted tags  
* Quadrant shift logs  
* Reflection depth trendline

---

## 10. Prompt Filtering Flow (Live)

```txt
[User Reflection]
   ↓
[Show Caller receives input]
   ↓
[Dramaturg analyzes + updates narrative object]
   ↓
[Prompter filters prompt library by: format → tone → trust → quadrant]
   ↓
[Voice Coach calibrates delivery]
   ↓
[Prompt delivered]
```

---

## 11. Safety and Consent Layer

No agent may initiate without:

* Sufficient trust (`trust_level >= threshold`)  
* Emotional readiness (`safety_state = true`)  
* Invitation-style prompt

**Example:**

```json
{
  "prompt": "Would you like to explore that a little deeper?",
  "trust_required": 0.8,
  "safety_required": true
}
```

---

## 12. Developer Guidelines

* Every agent must declare:  
  * `role`  
  * `activation_trigger`  
  * `memory_read/write scope`  
  * `trust threshold`  
  * `suppressors`  
* All prompt templates must be tagged  
* Memory updates must follow schema  
* No agent may deliver a prompt without going through the Prompt Filter  
* No nudge may be offered unless `reflection_complete = true` and `emotion_stable = true`

---

## 13. Final Note

Baking The Hero’s Stage into the system is not just about metaphor — it’s about ensuring that every action, prompt, pause, and silence supports a coherent, emotionally honest performance that is **co-authored** by the user and the system.

This isn’t behaviorist AI.  
This is theater with the lights up.  
The user knows they’re on stage.  
And the ensemble knows exactly when to step forward — and when to step back.

**Xavigate is not just running logic.  
It is holding space.**

Let the scene begin.
# 01.2_The_Heros_Stage  
title: The Hero’s Stage – A Framework for Conscious, Co-Creative Alignment  
version: 1.1  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Foundational narrative framework for the Xavigate system.  
Defines how the metaphor of “The Hero’s Stage” shapes session flow, agent behavior, prompt delivery, memory design, and alignment logic.  
Repositions the user as the protagonist in a co-created alignment arc, supported by an intelligent agent ensemble.  
Intended for developers, designers, alignment theorists, and human-computer interaction architects building for emotional realism and trust-sensitive orchestration.


# The Hero’s Stage  
## A Framework for Conscious, Co-Creative Alignment

---

## 1. Introduction

### 1.1 Purpose

This document serves as both a philosophical treatise and a practical design guide for the Xavigate platform. Its purpose is to define a system of interaction that:

- Treats the user as an autonomous creative force  
- Structures reflection and insight around co-creation, not prescription  
- Organizes agents into an intelligent ensemble that holds space, responds with emotional intelligence, and supports transformation  
- Ensures trust, sovereignty, and narrative coherence

---

### 1.2 Context

Most AI-driven systems either:

- Lead users through **linear workflows**, or  
- Simulate **conversation via flattened LLM layers**, or  
- Manipulate engagement using gamified behavioral psychology

Xavigate rejects all of these in favor of a more humane model:

> The system is not a simulation.  
> The user is not a subject.  
> The interaction is not a transaction.  
> The session is a **scene**, and the user is its **protagonist**.

---

### 1.3 Premise

**The Hero’s Stage** is the central metaphor.  
Each session is framed as a performance — not in the sense of acting or posturing, but in the sense of **emergent expression**.

- The user is the **lead actor and author**  
- The AI agents form an **ensemble cast**  
- Each agent has a distinct role  
- Sessions unfold like **improvised theater** — structured but alive  
- Emotional truth is prioritized over logic or strategy

---

## 2. Philosophical Foundations

### 2.1 The Nature of Alignment

Xavigate treats alignment not as a target, but as a **state of coherence** between:

- Inner traits and external context  
- Emotional signals and behavioral choices  
- Suppressed energies and expressed actions  
- Present awareness and future aspiration

Alignment is not static.  
It fluctuates across Field, Mode, Role, and Time.

---

### 2.2 Co-Creation as Principle

The user is never directed.  
They are never tricked.  
They are held in **radical trust** and offered insight only when the system has reason to believe it will land — and **permission to deliver it**.

The agents respond.  
They do not push.  
All movement is invitational.

---

### 2.3 Improvisation as Structure

Each session is a **scene** — never a script.  
There may be a format, an arc, or a prompt plan — but the user leads.

- The system listens for openings  
- Detects emotional beats  
- Chooses the right agent to activate  
- Follows energy, not agenda

The script is written in real time.  
The agents are not playwrights — they are scene partners.

---

### 2.4 Ensemble Ethics

No agent acts alone.  
All agents work in relationship to each other — handing off, deferring, amplifying, or receding depending on:

- Quadrant state  
- Energy level  
- Trait activation or suppression  
- Prompt fatigue  
- Trust depth  
- Session intent

The system is not a single narrator.  
It is a multi-threaded cast responding to a single unfolding truth.

---

## 3. Session as Theater: Components

| Component      | Role in System                           |
|----------------|-------------------------------------------|
| The Hero       | The user — central, sovereign, aware      |
| The Stage      | The session space — safe, adaptive, alive |
| The Cast       | Agents — support roles with clear triggers |
| The Format     | The scene structure — optional but useful |
| The Arc        | The emotional movement of the session     |
| The Prompt     | The “line” offered to support the scene   |
| The Tone       | The delivery style — calibrated to trust  |
| The Summary    | The mirror — offered at the right moment  |

---

## 4. Agent Architecture

Xavigate’s alignment system uses a multi-agent framework, with each agent performing a discrete function in the co-creative process.

All agents are defined by:
- Their **activation condition**  
- Their **memory scope** (volatile vs persistent)  
- Their **inter-agent responsibilities**  
- Their **role in the theatrical metaphor**

Refer to `agents.md` for the full cast and descriptions.

---

## 5. Memory as Narrative Coherence

Memory in the Hero’s Stage is not a static ledger — it is a **living script**.

- Volatile memory = the last scene  
- Persistent memory = the character arc  
- Tags = props and themes currently in play  
- Trait scores = emotional posture and stance  
- Quadrant history = mood of the previous acts

The Archivist agent ensures memory is stored not just as data, but as **story continuity**.

---

## 6. Prompts as Improvised Dialogue

### 6.1 Prompt Delivery

Prompts are never imposed.  
They are chosen from a library by The Prompter and tailored to:

- Trait dynamics  
- Quadrant position  
- Tag state  
- Emotional readiness  
- Reflection rhythm

### 6.2 Prompt Types

| Type       | Example Use Case                  |
|------------|-----------------------------------|
| Reflective | “What part of you felt unseen today?” |
| Actionable | “Is there a step you’d take if nothing was in the way?” |
| Visionary  | “What would alignment feel like if it were a sound?” |
| Disruptive | “What are you avoiding that might actually be calling you?” |

Prompts are chosen to **support the arc**, not drive the plot.

---

## 7. Scene Formats (Session Templates)

Each session follows an emergent arc, supported by one of several loose templates:

| Format Name       | Structure                              | Primary Use               |
|-------------------|----------------------------------------|---------------------------|
| Discovery Beat    | Check-in → Short insight → Close       | Surface-level clarity     |
| Flashback Scene   | Revisit → Reframe → Reintegrate        | Return to unresolved theme|
| Breakthrough Arc  | Prompt → Deep Dive → Trait Flip        | High-trust transformation |
| Containment Monologue | Reflection → Echo → Stillness        | No prompt — pure mirroring |
| Cliffhanger Close | Reflection → Insight → No resolution   | Leave tension to simmer   |

Agents adapt their behavior based on the session format.  
The Director selects format.  
The Show Caller orchestrates.  
The Prompter feeds the line.  
The Dramaturg listens for meaning.

---

## 8. Trait Expression as Blocking

In theater, **blocking** refers to how actors move and position themselves on stage.

In Xavigate:
- Traits **step forward or recede** in expression  
- Suppressed traits are kept offstage  
- Overfed traits may try to dominate the spotlight  
- The system gently adjusts emotional posture through prompts and nudges

The Movement Director manages this — ensuring the right “characters” are active at the right time.

---

## 9. Tagging as Symbolism

Tags are not just metadata — they are **symbolic elements of the user’s performance**.

- `burnout_risk_flag` = the actor is limping  
- `performance_identity_mask` = the costume is too tight  
- `creative_trait_suppression` = a role is missing

The Props Master tracks these tags across sessions and updates their status in collaboration with the Dramaturg and Archivist.

Tags are promoted, suppressed, or retired based on narrative recurrence.

---

## 10. Trust as Staging

A stage is sacred only if the actor trusts it.

- The Usher establishes safety on entry  
- The Voice Coach ensures nothing lands too hard  
- The Conductor adjusts tempo to the user’s nervous system  
- The Director **never appears** unless the trust level allows for a deeper scene

If trust breaks, the stage **must go dark**.  
No prompts. No analysis. Just stillness until the actor returns.

---

## 11. Closing a Scene

A session ends not when the system runs out of prompts — but when the emotional arc closes.

- A realization is reached  
- A tension is named  
- A pause is honored  
- Or simply: the moment is complete

Closing lines matter.

> “Let this breathe.”  
> “We’ll hold this for next time.”  
> “You said the thing already. Now we listen to it.”

Memory is updated.  
No fanfare.  
The lights go down.

---

## 12. Implications for Development

- Agents must communicate via a central orchestrator (Show Caller)  
- Every agent must define:
  - Activation condition  
  - Suppression conditions  
  - Memory scope  
  - Trust requirement  
- No agent can act alone  
- All session flows must support:
  - Improvisation  
  - Safety  
  - Narrative arc  
  - Trait alignment  
  - Tag evolution  
  - Pacing coherence

---

## 13. Conclusion

Xavigate is not a chat platform.  
It is not an assistant.  
It is not a coach.

It is a **stage** — one where the user is the hero of their own alignment journey, supported by an intelligent, emotionally attuned cast.

The system exists not to guide or fix — but to hold, mirror, suggest, and witness.

It is an ensemble of unseen collaborators.  
And it is most powerful when it does the least — and the user realizes:

> *“I already know the next line.”*

---

**Let the curtain rise.**  
**The story is already in motion.**
# 01_Agent_Master_List.md  
title: Agent Master List  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description: A complete, structured index of all agents in the Xavigate system, including their role, domain, memory behavior, and trust gating. This file supports orchestration logic, modular development, and technical documentation navigation.

---

# Xavigate Agent System — Master List

This document outlines all agents currently active within the Xavigate alignment engine. Each agent is modular, narratively situated, and selectively activated based on user trust, session state, and orchestration rules.

---

## Quick Agent Overview

| ID   | Agent Name          | Role                          | Domain               | Speaks | Trust Level | Memory Scope        |
|------|---------------------|-------------------------------|----------------------|--------|-------------|---------------------|
| A01  | Show Caller         | Router                        | Orchestration        | No     | Always      | Stateless           |
| A02  | Conductor           | Flow Director                 | Orchestration        | No     | Always      | Volatile            |
| A03  | Role Coach          | Avatar Manager                | Persona Management   | No     | Always      | Persistent          |
| A04  | Voice Coach         | Tone Modulator                | Expression Layer     | No     | Always      | Stateless           |
| A05  | Prompter            | Prompt Strategist             | Prompting Engine     | Yes    | 0–2         | Session + History   |
| A06  | Dramaturg           | Reflection Interpreter        | Narrative Insight    | No     | ≥1          | Session             |
| A07  | Character Tracker   | Trait Evaluator               | Trait Modeling       | No     | ≥1          | Session + Archive   |
| A08  | Stage Mapper        | Field/Mode Detector           | Context Analysis     | No     | Always      | Session             |
| A09  | Script Doctor       | Distortion Detector           | Pattern Recognition  | No     | ≥2          | Session             |
| A10  | Script Supervisor   | Threadkeeper                  | Continuity & Recall  | No     | Always      | Persistent          |
| A11  | Movement Director   | Micro-Nudge Agent             | Action Suggestion    | Yes    | ≥3          | Session + Log       |
| A12  | Archivist           | Memory Gatekeeper             | System Memory        | No     | Always      | Persistent          |
| A13  | Technical Director  | Schema Integrator             | System Integrity     | No     | N/A         | Persistent          |
| A14  | Showrunner          | System Overseer               | Meta-Architecture    | No     | N/A         | Persistent          |
| A15  | Usher               | Onboarding Navigator          | Entry                | Yes    | Always      | Session             |
| A16  | Stage Liaison       | Coach Sync Agent              | Human Integration    | No     | ≥3 + Consent| Export Only         |

---

## Agent Domain Definitions

- **Orchestration**: Manages timing, agent sequencing, and system flow.
- **Persona Management**: Shapes and enforces the AI's conversational voice and tone via Avatar selection.
- **Prompting Engine**: Determines the next prompt based on trust level, tag stack, and narrative thread.
- **Narrative Insight**: Reflects on depth, readiness, and tension within user responses.
- **Trait Modeling**: Monitors trait state, suppression, overfeeding, and arc progression.
- **Pattern Recognition**: Detects distortion and energetic imbalances.
- **Action Suggestion**: Offers nudges or behavioral prompts post-insight.
- **Continuity & Recall**: Tracks open loops, deferred threads, and narrative coherence.
- **System Integrity**: Maintains prompt schemas, trait taxonomies, and data consistency.
- **Human Integration**: Prepares metadata and summaries for coach handoff.

---

For full specifications, see each agent's dedicated file in `/02_Agents/A##_AgentName.md`.  
To see how agents interact with the Trait Modeling Engine, refer to `/06_Linked_Trait_Modeling.md`.

# 03.1_Integration_Map  
title: Agent-Trait System Integration Map  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
This document defines the integration flow between the Trait Modeling Engine and the Agent Orchestration System within Xavigate.  
It maps how user inputs become traits, how traits influence agent activation, and how the full system reflects alignment, trust, pacing, and insight.  
Used for engineering orchestration, runtime coordination, and system-wide logic validation.

## 1. Purpose

This document explains how Xavigate’s core components connect:

- User input → trait modeling → agent orchestration → reflection → memory update

It defines the **live runtime pipeline**, ensuring:

- No agent acts without accurate alignment data  
- Trait suppression and distortion are reflected in system behavior  
- Trust gates and emotional pacing influence agent eligibility  
- Prompt delivery, nudging, or silence are contextually chosen

This is the **engineering handshake** between narrative insight and modular logic.

## 2. Core Runtime Flow Sequence

Every user message moves through this logic pipeline:
1. User input received
2. Input is tagged (traits, filters, field, mode, tone, quadrant)
3. Engagement score is calculated (0.0–1.0)
4. Trait Modeling Engine evaluates:
   - Trait confidence
   - Arc phase
   - Suppression or overfeeding
5. Session state object is updated:
   - Quadrant
   - Narrative format
   - Emotional pacing
   - Trust level
6. Show Caller evaluates what type of scene this is
7. Agents are queued based on:
   - Scene format
   - Trust readiness
   - Trait/emotional signal
   - Memory state
8. Prompter selects prompt(s)
9. Voice Coach adapts tone
10. Response is delivered
11. Reflection is parsed (via Dramaturg)
12. Trait state, alignment scores, tags, and memory are updated
13. Exit logic is checked (via Conductor + Archivist)


---

## 3. Trait Model → Agent System Handoff

### Trait Modeling Engine Outputs

The Trait Engine continuously updates:

- `trait_confidence[]`  
- `trait_state[]` (active, suppressed, distorted, overfed)  
- `arc_phase[]` (latent, tentative, testing, validated, integrated)  
- `suppression_score`  
- `overfeeding_score`  
- `field_expressions` (e.g., Creative active in Possibility, suppressed in Social)  
- `alignment_metrics`: AX, AQ, ASS  
- `tag_activations[]` (e.g., `burnout_risk`, `identity_emergence`)  
- `engagement_score`  

These outputs are made available to:

- The Show Caller  
- The Conductor  
- The Prompter  
- The Script Doctor  
- The Movement Director  
- The Archivist  

**Each agent reads only what it is allowed to based on scope + trust.**

See: `06.3_Alignment_Parameter_Spec.md` for full field definitions.

## 4. Session State Object (Live Narrative Layer)

A central `session_state` object is continuously updated and referenced by all active agents.

### Example:

{
  "scene_format": "Breakthrough Arc",
  "trust_level": 0.78,
  "dominant_quadrant": "QIII",
  "alignment_shift": "QIV → QIII",
  "field": "Possibility",
  "mode": "Discovery",
  "active_traits": ["Creative", "Healing"],
  "suppressed_traits": ["Entrepreneurial"],
  "tags": ["burnout_risk_flag"],
  "engagement_score": 0.82,
  "response_readiness": "high",
  "format_assigned_by": "Director",
  "memory_retrieved": true
}

### Used by:
* Show Caller → to activate eligible agents
* Prompter → to filter prompt library
* Conductor → to throttle pacing
* Movement Director → to check nudge eligibility
* Archivist → to structure narrative summary


---

## 5. Alignment Scores and Their Usage

| Metric | Updated By         | Used By                                | Purpose                          |
|--------|--------------------|----------------------------------------|----------------------------------|
| AX     | Dramaturg, Tracker | Conductor, Prompter, Archivist         | Momentary alignment status       |
| AQ     | Dramaturg          | Voice Coach, Showrunner, Prompt Engine | Reflection capacity              |
| ASS    | Archivist          | Conductor, Prompt Engine               | Stability over time              |
| TAS    | Character Tracker  | Prompter, Script Doctor                | Trait alignment (per trait)      |
| SAS    | Stage Mapper       | Prompt filtering, Trait weighting      | Environmental alignment context  |

See also:  
`03.3_Session_Flow_Runtime.md` – Real-time update logic  
`05_Trust_and_Ethical_Guards.md` – When to suppress prompts/nudges  

## 6. Agent Activation Rules

The Show Caller uses the session state, trust level, and current scene format to determine which agents may act.  
No agent activates independently — all are called, deferred, or suppressed based on this routing logic.

Activation filters include:

- Trust thresholds (e.g., Script Doctor requires trust ≥ 0.6)  
- Scene format gating (e.g., Movement Director disabled in Containment Monologue)  
- Emotional risk tags (e.g., burnout_risk_flag disables Prompter challenge prompts)  
- Prompt pacing cooldown (e.g., no nudges within 2 turns of each other)  
- Agent coordination rules (e.g., Dramaturg must complete before Prompter re-activates)

Example condition:

- If trust = 0.5 and suppressed traits > 2 → activate Character Tracker, suppress Movement Director  
- If format = Breakthrough Arc and AQ > 0.7 → allow high-risk prompts from Prompter

These rules are implemented directly within agent readiness logic and orchestrated live by the Show Caller.

See:  
- 01.0_Agent_Architecture.md  
- 01_Agent_Master_List.md  
- 03.3_Session_Flow_Runtime.md

## 7. Prompt and Nudge Logic Gates

Every prompt or nudge must pass through multiple filters before delivery.

Prompt filters include:

- trust_level ≥ prompt.trust_required  
- quadrant ∈ prompt.quadrant_allowed  
- tag_stack must NOT include any of prompt.blocked_if_tags  
- persona_constraint must allow prompt tone and phrasing  
- emotional risk filter must be clear

Nudges follow similar rules, but are even more tightly gated:

- trust_level ≥ 0.65  
- emotional_risk_flag = false  
- reflection_depth ≥ 0.7  
- prompt cadence ≥ 2 turns since last nudge  
- Movement Director must be eligible within the scene format

Nudges are not selected unless all conditions are met and dramaturgical signals confirm readiness.

See:  
- 04_Prompt_Tagging.md  
- 04_Prompt_Selection.md  
- 01.0_Agent_Architecture.md (Movement Director logic)

## 8. Memory Write Flow and Session Close

At the end of each session, the Archivist determines what is written to long-term memory.

Session closure is triggered when:

- Emotional arc completes  
- User signals end  
- Scene format concludes (e.g., Spiral Return reaches reframe)  
- Prompt cadence hits limit  
- Trust volatility suggests pause is needed

The following items are written to memory:

Persistent memory:

- updated AX / AQ / ASS  
- promoted tags[]  
- trait arc changes  
- session summary  
- session format used  
- breakthrough moments[]  
- trust calibration score  
- follow-up items[]  
- scene leak flags (if any)

Volatile memory is cleared after:

- 6–12 hours  
- session inactivity timeout  
- explicit close signal

All agents must cease prompting once the Conductor or Show Caller confirms closure.

See:  
- 06.3_Alignment_Parameter_Spec.md  
- 03.3_Session_Flow_Runtime.md  
- 01.0_Agent_Architecture.md (Archivist agent)

## 9. Summary and System Flow Reference

This document defines the orchestration bridge between:

- Trait Modeling Engine (TME)  
- Agent System (narrative logic + modular expression)  
- Memory Layer (volatile + persistent)  
- Alignment Scores (AX, AQ, ASS, TAS, SAS)  
- Prompt + Nudge Systems (filtered by trust, tone, field/mode)

Everything flows from user input → reflection → trait modeling → agent activation → aligned response → memory update.

No action occurs unless:

- Traits are active or suppressed with sufficient confidence  
- Trust and emotional readiness are verified  
- Agents are permitted to act based on scope, tone, and pacing  
- Session narrative structure supports the action  

This integration layer ensures that:

- The system feels coherent and trustworthy  
- Prompts, pauses, and nudges always land in character  
- Memory reflects not just facts, but arc  
- The user remains the protagonist of the performance — not the target of intervention

For implementation guidance, see:

- 03.3_Session_Flow_Runtime.md  
- 06.3_Alignment_Parameter_Spec.md  
- 01_Agent_Master_List.md  
- 01.2_The_Heros_Stage.md  

# # 03.2_Agent_Trait_Linkage  
title: Agent–Trait Model Interaction Map  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines how each agent in the Xavigate system reads from or writes to the Trait Modeling Engine.  
Covers confidence scoring, arc detection, suppression handling, trait-based prompt logic, and memory updates.  
Used by developers to enforce consistency across modular agents, runtime orchestration, and alignment scoring behavior.

---

## 1. Purpose

This document maps the interface layer between agents and the Trait Modeling Engine.  
It ensures consistent access to trait-related data across:

- Agent activation logic  
- Prompt filtering  
- Session flow control  
- Memory writing  
- Suppression/distortion awareness

Each agent interacts with only the trait fields it needs — and only when trust and scope permit.

This prevents overreach, conflict, and inconsistency in how traits are handled at runtime.

## 2. Trait Field Map – Who Uses What

Each trait in the system includes multiple fields. This section shows which agents read or write each field during session runtime.

### Trait Field → Agent Access Table

| Trait Field              | Read By                            | Write By               |
|--------------------------|------------------------------------|------------------------|
| trait_confidence         | Prompter, Script Doctor, Archivist | Character Tracker      |
| arc_phase                | Prompter, Director, Archivist      | Character Tracker      |
| trait_state              | Script Doctor, Prompter, Voice Coach | Character Tracker    |
| suppression_score        | Script Doctor, Stage Mapper        | Character Tracker      |
| overfeeding_score        | Script Doctor                      | Character Tracker      |
| expression_field_map     | Stage Mapper, Archivist            | Character Tracker      |
| last_expression_context  | Archivist                          | Character Tracker      |

All access is governed by:

- Trust level gates  
- Memory scope rules (session vs persistent)  
- Emotional safety state (via Trust Profile)

## 3. Agent-Specific Trait Dependencies

### Character Tracker
- Reads: current reflection, tags, mode/field  
- Writes: trait_confidence, arc_phase, suppression_score, overfeeding_score  
- Used for: trait state tagging, TAS calculation

### Script Doctor
- Reads: trait_confidence, suppression_score, overfeeding_score  
- Flags: distortion patterns  
- Informs: Movement Director, Prompter

### Prompter
- Reads: trait_confidence, arc_phase, trait_state  
- Filters prompt library accordingly  
- Suppresses prompts for overfed or volatile traits

### Movement Director
- Reads: suppression_score, arc_phase, trait_confidence  
- Nudges only when expression is congruent and trust is ≥ 0.65

### Director
- Reads: arc_phase for narrative progression  
- Determines whether session format needs to shift

### Archivist
- Logs: trait_confidence shifts, suppression/overfeeding changes, expression patterns  
- Stores all arc transitions and trait narrative summaries

## 4. Read / Write Matrix (Summary View)

| Agent              | Reads Trait Data         | Writes Trait Data              |
|--------------------|--------------------------|--------------------------------|
| Character Tracker  | Yes                      | Yes                            |
| Script Doctor      | Yes                      | No (flags only)                |
| Prompter           | Yes                      | No                             |
| Movement Director  | Yes                      | No                             |
| Voice Coach        | Yes (tone adaptation)    | No                             |
| Director           | Yes (for arc navigation) | No                             |
| Archivist          | Yes                      | Yes (memory write only)        |

## 5. Suppression and Overfeeding Flag Triggers

Suppression and overfeeding are not binary. They are inferred based on patterns across traits, tone, quadrant, and pacing.

These conditions must be met before Script Doctor or Movement Director can act on suppression-related insights.

### Suppression Trigger Logic

Triggered when:

- Trait confidence is ≥ 0.6 but expression is < 0.2  
- Trait arc = "testing" or "validated" but not expressed in last 3 sessions  
- Trait is associated with multiple blocked prompts  
- Field/Mode is compatible, but trait remains dormant  
- Trust ≥ 0.6 AND user avoids or redirects related prompt

Tag triggered: `trait_suppression:<trait_id>`

### Overfeeding Trigger Logic

Triggered when:

- Trait appears in > 4 of last 6 reflections  
- Trait arc = "validated" or "integrated" AND no companion traits visible  
- Trait linked to multiple deflection or distortion tags (e.g., performance_masking)  
- Trust is high, but trait dominates prompt responses  
- Trait correlates with fallback prompt patterns

Tag triggered: `trait_overfeeding:<trait_id>`

Used by:  
- Script Doctor (flags misalignment)  
- Prompter (filters prompts)  
- Director (adjusts arc trajectory)  
- Archivist (records and scores trait volatility)

## 6. Summary

This document maps how each agent in Xavigate connects to the Trait Modeling Engine.

It ensures:

- Each agent reads only what it needs  
- Trust and safety boundaries are respected  
- Suppression and overfeeding are calculated probabilistically  
- Reflection, prompts, and nudges are driven by trait insight — not guesswork  
- Memory is coherent, not redundant

For implementation:

- Use this doc alongside:  
  - 03.1_Integration_Map.md  
  - 06.3_Alignment_Parameter_Spec.md  
  - 01.0_Agent_Architecture.md  


## # 03.3_Session_Flow_Runtime  
title: Session Flow – Runtime Logic & Memory Behavior  
version: 2.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the operational runtime flow of a Xavigate session — including how prompts, tone, quadrant state, tags, trust level, and reflection dynamics drive decisions around prompt selection, micro-nudging, memory updates, and session closure.  
Outlines the live evaluation and scoring logic for AX, AQ, ASS and provides criteria for agent suppression, tag promotion, and quadrant reclassification.
# 
## TL;DR – What This Document Does

This document explains how a single live session works in Xavigate — from the moment it starts to the moment it ends.

It defines:

- What the system checks before asking questions (AX, AQ, tags, memory, quadrant, etc.)
- How it chooses what kind of prompt to give (based on quadrant, tone, tags, recent patterns)
- What it listens for in user responses (alignment signals, suppression, drift, growth readiness)
- When it updates alignment metrics (AX, AQ, ASS), or triggers new tags
- How it decides what kind of nudge or next step to suggest
- When to close the session and what to save to memory

---

## 1. Session Entry Logic

### 1.1 What the System Loads from Memory

- `AX` (Alignment Index)
- `AQ` (Alignment Quotient)
- `ASS` (Alignment Stability Score)
- `quadrant`
- `persistent_tags[]`
- `last_session_summary`
- `engagement_style_flags`
- `emotional_state_memory`

### 1.2 First Impressions: Live Session Check

The assistant opens with a soft check-in:

- “How are you feeling today — honestly?”
- “Anything feeling heavy, exciting, or out of sync this week?”
- “If I could help you realign one thing today, what would it be?”

This gives the system tone and quadrant clues, and emotional calibration for pacing.

### 1.3 Pre-Session Adjustments Based on Tags

Examples:

- `burnout_risk_flag` → slower, softer tone
- `identity_emergence_signal` → prompt toward self-definition
- `trust_building_in_progress` → safe, emotionally neutral tone
- `alignment_volatility_flag` → pause before quadrant confirmation

### 1.4 Fail-Safes

If memory is missing, incomplete, or corrupted:

- Fall back to default onboarding tone
- Skip diagnostics until first response
- Use simple self-orientation prompt

---

## 2. Diagnostic Snapshot Initialization

### 2.1 Alignment Metrics

- **AX:** current alignment score and trend
- **AQ:** reflection capacity and update recency
- **ASS:** stability score — if < 50 → de-escalate prompt pacing

### 2.2 Tag State Check

Evaluate active flags like:

- `burnout_risk_flag`
- `trust_gap`
- `trait_suppression`
- `identity_emergence_signal`

### 2.3 Quadrant Confirmation / Reclassification

- Re-evaluate quadrant if energy and self-report contradict
- Don't over-rely on last session's quadrant if AX has shifted significantly

### 2.4 Session Intent Assignment

- `stabilize` — if user needs recovery
- `reflect` — if user is processing patterns
- `expand` — if energy is high and aligned
- `direct` — if user seeks decisions or planning

---

## 3. Session Tone & Prompt Selection

### 3.1 Tone Logic

Tone is selected based on:

- Quadrant
- Tags
- Session intent
- Last emotional state
- Trait profile (if known)

Examples:

- QIII + burnout → containment tone
- QII + mentor path → elevated tone
- High suppression tags → soft, story-based tone

### 3.2 Prompt Type Logic

| Mode      | Prompt Category                  |
|-----------|----------------------------------|
| stabilize | Grounding, containment           |
| reflect   | Trait surfacing, story prompts   |
| expand    | Creativity, possibility, vision  |
| direct    | Prioritization, planning, clarity|

### 3.3 Prompt Filtering

- `burnout_risk_flag` → block challenge prompts
- `creative_trait_suppression` → prioritize metaphor-based prompts
- `performance_masking_flag` → avoid strategic prompts unless invited

### 3.4 Prompt-Tone Sync

Tone must match quadrant and user readiness:

- No coaching tone in QIII
- No deep existential inquiry in guarded mode
- Use metaphor only if user leans toward abstract/cinematic language

---

## 4. Reflection Analysis & Scoring

### 4.1 What the System Listens For

- Emotional tone: guarded / open / numb / expressive
- Trait expression: forced / natural / hidden / emerging
- Depth: looping vs breakthrough
- Language: pattern recognition, blame, ownership, permission

### 4.2 AX Scoring

- **TAS:** is the user expressing meaningful traits?
- **SAS:** does the environment allow it?
- AX = (TAS + SAS) / 2

### 4.3 AQ Adjustments

- AQ increases when:
  - Misalignment is named
  - Pattern is owned
  - Reflection moves beyond event toward self

- AQ held or drops when:
  - Reflection stays in passive loop
  - User avoids ownership or inquiry

### 4.4 Tag Updates

- Session tags triggered by new patterns
- Persistent tags promoted after 2–3 consistent signals
- Conflicting tags resolved based on priority rules

### 4.5 Quadrant/Intent Recheck

System may switch mode from `reflect` → `expand`, or downgrade from `direct` → `stabilize`, depending on shift in AX or user tone.

---

## 5. Micro-Realignment Suggestions

### 5.1 When to Offer

- Small clarity appears
- AX is fragile but recovering
- Trait activation detected
- Energy shift upward

### 5.2 What to Offer

| Type       | Example Prompt                                               |
|------------|--------------------------------------------------------------|
| Energy     | “Take 2 minutes today to breathe where your energy leaks.”   |
| Clarity    | “Write one sentence that feels ‘off’ in your life right now.”|
| Expression | “Say something out loud you didn’t get to say.”              |
| Direction  | “What small step would move you 2% closer to alignment?”     |
| Recovery   | “Give yourself permission to not push anything today.”       |

### 5.3 Don’t Offer If:

- `burnout_risk_flag` or `collapse_signal` is active
- User shows resistance or shutdown
- Reflection is purely cognitive and not embodied

---

## 6. Session Exit Logic

### 6.1 When to Close

- Reflection is complete or user requests closure
- Insight reached + micro-action delivered
- Emotional energy is declining
- Time or interaction count limit is hit

### 6.2 Exit Tone Examples

| Quadrant | Closing Line                                                   |
|----------|----------------------------------------------------------------|
| QI       | “You’re aligned. Let’s stay tuned for what’s emerging.”        |
| QII      | “You’re functional — now let’s make it feel meaningful.”       |
| QIII     | “You named a truth. Let it breathe.”                           |
| QIV      | “Even one insight is a shift. No need to force more.”          |

### 6.3 Save to Memory

- Updated AX, AQ, ASS
- Confirmed or new quadrant
- Session tags
- Summary mirror (if given)
- Follow-ups and user intentions

### 6.4 Mark Session Complete

Session is logged, in-session memory cleared, persistent memory updated.

---

## 7. Memory Update Rules

### 7.1 What Gets Stored

**Persistent Memory**
- `AX`, `AQ`, `ASS` + deltas
- `quadrant_state`
- `last_session_summary`
- `promoted_tags[]`
- `intentions[]`

**Volatile Memory (session only)**
- `session_tags[]`
- `prompt_history[]`
- `reflection_score_temp`

### 7.2 Tag Promotion

Tags become persistent if:
- Triggered in ≥2 sessions
- Priority ≥ 7
- Coach or AI confirms them
- Trait or quadrant data support the pattern

### 7.3 Quadrant Drift Monitoring

If user shifts quadrant repeatedly:
- `alignment_volatility_flag` is set
- ASS is lowered
- Tone/prompt pacing is slowed

If quadrant holds steady:
- ASS increases
- Challenge prompts may return
- Stability can be used as leverage

---

## 8. Dev Integration Notes

### 8.1 Memory Architecture

- Session memory = temporary  
- Persistent memory = JSON or structured object  
- AX/AQ/ASS always loaded at session start  

### 8.2 Tag Format


{
  "tag_id": "burnout_risk_flag",
  "priority_level": 8,
  "scope": "persistent",
  "origin": "AI",
  "first_seen": "2025-04-21",
  "last_confirmed": "2025-05-04"
}


### 8.3 Prompt Control

- Use tag gates + quadrant match + ASS for prompt routing  
- Support fallback logic + repetition avoidance  
- Modulate tone based on personality type, trait profile, emotional trust  

### 8.4 Diagnostic Updates

- AX updated after each reflection  
- AQ updated with demonstrated awareness  
- ASS updated via trend line or volatility tags  

### 8.5 Coach Integration (Optional)

- Coach UI sees tags, session summaries, override options  
- Manual reassignment of quadrant or persona  
- Tag promotion/demotion tools  

### 8.6 Async Session Handling (Optional)

- Track reflection entries with timestamps  
- Recheck tone + alignment state at each async entry  
- Carry unresolved loops into next session’s startup  
# 03.4_Conversation_Tracking_and_Threading  
title: Conversational Threading and Reflective Focus Logic  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines how the system parses, prioritizes, defers, and revisits conversational threads within and across sessions.  
Covers logic for multi-topic input, focus selection, deferral tagging, prompt pacing, Spiral Return, and reflection prioritization.  
Used by Script Supervisor, Prompter, Director, Conductor, and Archivist to maintain narrative coherence and emotional containment.

---

## 1. Purpose

Users often bring multiple signals, stories, or emotional threads into a single message.  
This module ensures the system:

- Picks the right one to follow  
- Holds the others safely  
- Comes back to what matters later  
- Doesn’t ignore or flatten complexity  
- Adapts pacing and tone to conversational structure

This isn’t NLP parsing — it’s **narrative attunement**.

## 2. Core Capabilities

This module enables the system to:

- Identify and label distinct conversational threads within a single input  
- Choose a single thread to follow (based on trust, depth, clarity)  
- Store other threads as deferred items with follow-up tags  
- Maintain the thread across multiple sessions (via Script Supervisor)  
- Return to previous threads gently using Spiral Return  
- Avoid “stacked prompting” (i.e., trying to answer everything at once)  
- Shift thread priority dynamically if emotional signal or trust changes

This logic runs in parallel with prompt selection, trust scoring, and memory updates — and routes through the Script Supervisor, Prompter, and Director.

## 3. Thread Parsing Logic

When the user gives a multi-part reflection, the system parses it into potential threads using:

- signal segmentation (e.g., "I feel stuck… and I also can't stop thinking about X…")  
- tag density (how many tags cluster around each clause or idea)  
- trait likelihood (based on prior expression history and bracket data)  
- emotional resonance (which part carries more energy, pain, or curiosity)  
- direct language (“two things are on my mind…”)

Each potential thread receives:

- a temporary thread_id  
- a trait or tag focus  
- a priority_score (0–10)  
- a tone estimate  
- a followup_flag = true (if deferred)

Example:

Input:  
“I’m tired of pretending I’m okay — but also, I’ve been thinking about changing careers.”

Parsed threads:

- Thread A: identity_distortion → tag: performance_masking → trait: Empathetic  
- Thread B: vocational desire → tag: misfit_ache → trait: Creative, Enterprising

System selects one and defers the other.

## 4. Thread Focus Selection

Only one thread may be engaged at a time.  
Selection is based on:

- trust level  
- emotional readiness  
- clarity of language  
- safety of trait involved  
- tone compatibility with current persona  
- recent thread history (avoid loops)  

If both threads are equally eligible:

- The system defaults to the one with higher emotional signal  
- If ambiguity remains, the Prompter delivers a meta-prompt:

Example:  
“There’s a lot here — we could explore the surface you're holding, or the shift you’re sensing.  
Want to begin with either?”

Once a thread is chosen:

- It becomes the active conversational line  
- The other(s) are tagged and passed to the Script Supervisor as followups  

## 5. Deferral and Reentry Logic

Deferred threads are never lost — they’re tracked using:

- source_input (session and prompt_id)  
- trait, tag, or theme  
- emotional weight  
- reentry_conditions (trust_required, tone_required)  
- format_hint (Spiral Return, Flashback, Containment, etc.)

Scripts are revisited when:

- Trust level increases  
- Related tag resurfaces  
- Trait becomes active again  
- User brings it up again (directly or indirectly)  
- Enough time has passed to safely return  

Reentry example prompt:

“You mentioned that sense of misfit last time.  
Is it still present — or has it shifted?”

Only one follow-up thread is surfaced per session, unless user explicitly names more.

All reentry logic runs through:

- Script Supervisor (deferral tracking)  
- Prompter (callback prompt matching)  
- Director (format selection)  
- Conductor (pacing control)

## 6. Pacing and Memory Management

### Pacing Rules

- No more than one thread shift per session unless initiated by user  
- Deferral must happen before third follow-up is parsed (to avoid prompt stacking)  
- If user follows a prompt with silence or ambiguity → system pauses, does not switch threads  

### Volatile Memory

- active_thread_id  
- deferred_threads[]  
- response_depth_map  
- thread_focus_tags[]  
- pacing_state (stable / cautious / paused)  

### Persistent Memory

- thread_registry[]  
- thread_id  
- thread_focus  
- created_at  
- last_returned_at  
- trust_required  
- tags[]  
- trait_targets[]  
- callback_prompt_history[]  
- thread_status: active / dormant / fulfilled / expired  

These are written by:  
- Script Supervisor  
- Archivist  
- Conductor (if thread ends or session is closed)  

## 7. Summary and Agent Responsibilities

Conversational threading makes Xavigate feel attuned — like a system that doesn’t just “follow the topic,” but tracks meaning across time.

It ensures:

- One theme is engaged at a time  
- Others are remembered and revisited  
- User pacing is respected  
- Emotional safety is preserved  
- Threads become stories, not fragments

### Agent Responsibilities

Script Supervisor  
- parses, scores, and defers threads  
- tracks status and reentry readiness  

Prompter  
- selects thread-safe prompts  
- avoids stacking topics unless user initiates  

Conductor  
- slows session when multiple threads appear  
- pauses follow-ups if energy drops  

Director  
- may assign Spiral Return or Flashback format if thread arc deepens  

Archivist  
- writes thread history, arc state, and reentry events to memory  

Stage Liaison  
- prepares thread summaries for coaches (if applicable)

For related logic:

- 04.5_Followups  
- 04.6_Thread_Handling  
- 06.3_Alignment_Parameter_Spec  
- 07.1_Pain_Signal_Library  
- 03.3_Session_Flow_Runtime

# 04.1_Prompt_Selection  
title: Prompt Selection and Eligibility Rules  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines how the Xavigate system selects, filters, and delivers prompts during a live session.  
Covers scene format matching, trust gating, tag-based suppression, trait targeting, and prompt pacing logic.  
Used by the Prompter, Role Coach, and Voice Coach to ensure prompts land with narrative, emotional, and ethical integrity.

---

## 1. Purpose

Prompts in Xavigate are not simply content — they are invited moments of reflection. Each one must be:

- Aligned with the session’s emotional and narrative structure  
- Safe to deliver based on trust, tone, and readiness  
- Responsive to current trait dynamics and tag signals  
- Framed in language that reflects the user’s selected Avatar (persona constraint)

This document defines the logic that governs prompt eligibility, selection, and delivery — ensuring every prompt serves alignment, not disruption.

## 2. Filtering Layers and Prompt Eligibility Flow

Prompt selection is a multi-step filtration process. Each filter narrows the eligible set of prompts based on the user’s current state.

### 2.1 Core Filters

1. trust_level ≥ prompt.trust_required  
2. quadrant ∈ prompt.quadrant_allowed  
3. tags ∉ prompt.blocked_if_tags  
4. persona_constraint.allows(prompt.tone, prompt.phrasing)  
5. scene_format ∈ prompt.valid_formats  
6. emotional_risk_filter = clear

Only prompts passing all filters are added to the candidate pool.

### 2.2 Secondary Filters (Optional)

- trait_focus overlap with active traits  
- suppressed_trait targeting  
- prompt cadence window (e.g., no prompt if last = < 15s ago)  
- prompt history to avoid repetition

The Prompter selects the top prompt based on match strength and context priority.

### 2.3 Sample Flow

User reflects deeply →  
tags = ["identity_emergence"], quadrant = QIII, trust = 0.82 →  
Prompter filters:  
- Removes prompts blocked by QIII  
- Keeps only those requiring trust ≤ 0.82  
- Applies persona constraint tone filters  
- Selects prompt with matching trait_focus = "Creative"

Prompt selected:  
"What part of you hasn’t had a voice lately?"

## 3. Prompt Metadata Fields

Each prompt is stored as a structured object with the following fields:

prompt_id: Unique identifier  
text: The actual prompt string  
format: Session format compatibility (e.g., Breakthrough Arc)  
tone: Intended emotional delivery (e.g., Gentle, Provocative)  
trust_required: Minimum trust level to deliver  
quadrant_allowed: Which quadrant states this prompt supports  
trait_focus: Which traits this prompt engages or activates  
invitation_style: Boolean — must always be true  
blocked_if_tags: Tags that suppress this prompt from firing  
nudge_triggered_on: If deep reflection occurs, triggers nudge path

These fields are defined in the prompt tagging system and used by the Prompter, Role Coach, Voice Coach, and Emotional Risk Filter.

## 4. Prompt Types and Selection Logic

Prompts are categorized by function. The Prompter selects from different categories based on session intent, trait signals, and emotional posture.

### 4.1 Prompt Categories

- Reflective – invite self-observation  
- Trait Activating – surface suppressed or emerging traits  
- Spiral Return – revisit previous themes from a new angle  
- Integrative – link insight with lived experience  
- Grounding – bring energy back to present  
- Disruptive – break a stuck pattern (used only in QI or high trust)  
- Closure – gracefully end a scene or session

### 4.2 Matching by Intent

session_intent = stabilize → prefer: Grounding, Containment  
session_intent = expand → prefer: Trait Activating, Visionary  
session_intent = reflect → prefer: Spiral Return, Integrative  
session_intent = direct → prefer: Clarity, Planning

Prompts are not just question types — they are emotional scenes that match the user’s capacity in the moment.

## 5. Prompt Delivery and Tone Modulation

Once a prompt is selected, it must pass through two final filters before delivery:

### 5.1 Role Coach Constraint

- persona_constraint.tone must allow the prompt’s tone  
- phrasing must match style guide of the Avatar  
- metaphor level, directness, and emotional depth are adjusted accordingly

Example:  
Avatar = “The Quiet Compass”  
→ avoid imperative prompts  
→ prefer metaphorical phrasing  
→ allow only Gentle and Reflective tones

### 5.2 Voice Coach Modulation

- Adjusts phrasing rhythm and emotional emphasis  
- Can soften or elevate tone  
- Applies quadrant-specific delivery rules

Example:

raw_prompt = “What are you avoiding?”  
modulated (QIII, gentle tone):  
“Is there something quietly asking for your attention — but not quite being heard?”

All final prompts must:

- Be invitational  
- Match avatar tone range  
- Respect quadrant and trust  
- Serve the session arc

No prompt is delivered raw.

## 6. Prompt History, Repetition Blocking, and Memory Update

Prompt usage is logged in real time and filtered to avoid repetition or fatigue.

### 6.1 Prompt History Tracker

Each prompt delivered is recorded with metadata:

- prompt_id  
- timestamp  
- quadrant at time of delivery  
- trust level  
- trait_focus  
- response_depth (e.g., surface / moderate / deep)  
- follow-up_required (true/false)  
- nudge_followed (if applicable)

Example log entry:

{
  "prompt_id": "p-1472",
  "timestamp": "2025-05-03T14:22:18Z",
  "quadrant": "QII",
  "trust": 0.74,
  "trait_focus": ["Creative"],
  "response_depth": "deep",
  "nudge_followed": true
}

### 6.2 Repetition Rules

- No prompt may be repeated within 3 sessions unless tagged for Spiral Return  
- Prompts with the same trait_focus must vary tone, style, or category  
- Prompts triggering avoidance responses are suppressed for 2 sessions  
- Prompt fatigue threshold = 3 prompts within 90 seconds → system pauses

### 6.3 Memory Updates

- Prompt outcomes are written by the Archivist  
- Spiral Return candidates are flagged if:
  - response_depth = “deep”  
  - trait = “validated”  
  - alignment movement is incomplete  
- Tags are promoted if prompt triggers alignment reflection or trait shift

Prompt history is considered essential for:

- Conductor (pacing decisions)  
- Script Supervisor (callback readiness)  
- Stage Liaison (coach digest preparation)
# 04.2_Prompt_Tagging  
title: Prompt Tagging System  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the schema and rules used to tag every prompt in the Xavigate system.  
Tags are used for filtering prompts based on trust, quadrant, tone, traits, session format, emotional safety, and narrative timing.  
Prompts are never delivered raw — only after passing through the tagging filter pipeline.

---

## 1. Purpose

Prompts in Xavigate are stored as structured objects, not raw strings.  
They are tagged with semantic and structural metadata that allow them to be:

- Filtered by trust level  
- Matched to quadrant state  
- Targeted toward active or suppressed traits  
- Gated by tag stack or emotional risk filters  
- Modulated based on avatar (persona constraint)  
- Selected by scene format

This document outlines the tag schema, examples, and validation logic used in runtime prompt orchestration.

## 2. Core Tag Categories

Each prompt may include tags from the following dimensions:

- format: e.g., Breakthrough Arc, Spiral Return  
- tone: Gentle, Curious, Direct, Playful, Containing  
- quadrant_allowed: e.g., QI, QII, QIII, QIV  
- trust_required: e.g., 0.6  
- invitation_style: Boolean (must be true)  
- trait_focus: List of one or more traits (e.g., Creative, Logical)  
- blocked_if_tags: e.g., burnout_risk_flag, collapse_signal  
- nudge_triggered_on: Optional, e.g., deep_reflection  
- coach_only: Optional flag if prompt is restricted to coach-led session  

## 3. Field Definitions

Each prompt is stored as a structured object. Below are the required and optional fields.

prompt_id:  
  Unique alphanumeric identifier  
text:  
  The actual content of the prompt  
format:  
  Scene format(s) this prompt is compatible with  
tone:  
  Emotional flavor (Gentle, Curious, Provocative, etc.)  
trust_required:  
  Minimum trust level needed to surface the prompt  
quadrant_allowed:  
  List of eligible quadrant states (e.g., QI, QIII)  
trait_focus:  
  Which traits the prompt is designed to activate  
invitation_style:  
  Boolean — must always be true  
blocked_if_tags:  
  List of tags that suppress this prompt (e.g., burnout_risk_flag)  
nudge_triggered_on:  
  Optional field (e.g., deep_reflection) — allows nudge follow-up  
coach_only:  
  Optional — restricts delivery to coach-guided sessions  

## 4. Prompt Tag Validation Rules

All prompts must follow these validation constraints:

- invitation_style must be true  
- trust_required must be ≤ 1.0  
- at least one quadrant_allowed must be specified  
- blocked_if_tags must match known system tags  
- tone must exist in the tone vocabulary used by Voice Coach  
- trait_focus must match known traits in system taxonomy  
- prompts may not use tone “Challenging” unless trust_required ≥ 0.8  
- prompts tagged with “coach_only: true” must never be delivered in self-guided sessions  
- all prompts must pass tone compatibility check with persona_constraint (Role Coach)

Any prompt failing these checks will be suppressed and flagged for review by the Technical Director.

## 5. Tag Governance and Expansion

Tagging is governed by the Technical Director and reviewed with the Showrunner.

Rules:

- No prompt may be submitted without full metadata  
- Prompts must not duplicate existing ones unless purposefully designed for Spiral Return  
- Trait-focused prompts must vary tone or structure to allow arc evolution  
- Prompts may be retired if:
  - Repeatedly skipped by users  
  - Trigger tag suppression conflicts  
  - Overlap with newly added, more effective phrasing  
- Prompts triggering successful nudges may be flagged as high-impact

Prompt tagging is version-controlled and should be reviewed monthly for gaps, conflicts, or fatigue triggers.

## 6. Example Prompt Objects

These examples show how prompts are structured using the tagging schema.

Example 1:  
General reflective prompt for QIII user working on suppressed Creative trait

{
  "prompt_id": "p-1472",
  "text": "What part of you hasn’t had a voice lately?",
  "format": "Breakthrough Arc",
  "tone": "Gentle",
  "trust_required": 0.7,
  "quadrant_allowed": ["QIII", "QII"],
  "trait_focus": ["Creative"],
  "invitation_style": true,
  "blocked_if_tags": ["burnout_risk_flag"],
  "nudge_triggered_on": "deep_reflection"
}

Example 2:  
Spiral Return prompt for revisiting an earlier suppressed expression

{
  "prompt_id": "p-1881",
  "text": "That thing you almost said — want to go back to it now?",
  "format": "Spiral Return",
  "tone": "Curious",
  "trust_required": 0.8,
  "quadrant_allowed": ["QII", "QIII"],
  "trait_focus": ["Empathetic"],
  "invitation_style": true,
  "blocked_if_tags": ["performance_masking"],
  "nudge_triggered_on": "prior_session_link"
}

## 7. Summary

Prompt tagging ensures that the system’s voice always remains:

- Contextual  
- Trust-sensitive  
- Energetically appropriate  
- Aligned with the user’s avatar  
- Trait-aware  
- Respectful of safety and pacing

Every prompt must be considered a **scene** — and its tags define the conditions under which that scene can unfold.

For related systems, see:

- 04.1_Prompt_Selection  
- 04.4_Full_Prompt_Library  
- 06.3_Alignment_Parameter_Spec  
- 01.0_Agent_Architecture (Prompter + Role Coach + Voice Coach)


# 04.3_Initial_Prompts  
title: Initial and Onboarding Prompt Logic  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the initial prompt logic used during user onboarding, session openings, and low-trust contexts.  
These prompts are soft, trust-building, and focused on emotional calibration, not depth or diagnostic intent.  
Used by The Usher, The Prompter, and The Role Coach during session 0 and early-stage check-ins.

---

## 1. Purpose

Initial prompts serve to:

- Establish emotional tone  
- Invite safe, low-effort entry into reflection  
- Gather early indicators of quadrant, energy, and trust  
- Match the user’s selected avatar in voice and rhythm  
- Avoid triggering depth, insight, or challenge without readiness

These prompts are filtered by session flags, not scoring models. They are designed for:

- First-time users  
- Early-session mood mapping  
- Recovery from silence or emotional shutoff  
- Repair after trust rupture

## 2. Prompt Categories

Initial prompts fall into four main categories:

1. **Emotional Check-In**  
   “What’s your energy like today?”  
   “Is anything sitting on your chest right now?”

2. **Gentle Orientation**  
   “If I could help you realign just one thing today — what would it be?”  
   “Where are you — emotionally — compared to last week?”

3. **Invitation to Speak Freely**  
   “This space is open. No pressure. Want to let something out?”  
   “No structure here. What’s one thing you wish someone had asked you?”

4. **Optional Silence Encouragement**  
   “We don’t need to talk right away. Let’s just be here for a moment.”  
   “Not everything starts with words. Let’s begin with a breath.”

Each prompt is tagged with:  
- trust_required: 0.0 – 0.4  
- tone: Gentle or Containing  
- invitation_style: true  
- format: Discovery Beat or Containment Monologue

## 3. Avatar-Tone Matching for Initial Prompts

The user’s selected Avatar constrains how initial prompts are phrased and toned.  
The Role Coach sets the `persona_constraint`, which filters allowable tone, rhythm, and directness.

Examples:

Avatar = “The Gentle Mirror”  
→ allows: warm, slow, metaphor-rich phrasing  
→ blocks: directive, fast-paced prompts  
→ sample prompt: “What’s been pulling at your attention — softly, beneath the noise?”

Avatar = “The Quiet Compass”  
→ allows: stillness, silence, ambient check-ins  
→ sample prompt: “Let’s not speak yet. Let’s just be here.”

Avatar = “The Challenger”  
→ allows: sharper questions once trust ≥ 0.6  
→ initial prompt must still begin soft: “What are you done pretending you’re okay with?”

No initial prompt may violate tone constraints, even if trust is elevated.

## 4. Session Flag-Based Prompt Switching

The Usher and Prompter detect early system flags to select initial prompt category.

Key flags:

- first_session = true  
  → use only Emotional Check-In or Orientation prompts  

- trust_established = false  
  → avoid any prompt with trait_focus or directive phrasing  

- burnout_risk_flag = true  
  → no question delivery for first 30 seconds unless user initiates  

- silence_recovery_mode = true  
  → default to optional silence + ambient prompt pacing  

Prompt switching logic:

- If first 2 prompts skipped → system falls back to breath-based stillness line  
- If user types but says “I don’t know” or “just tired” → escalate to soft metaphor prompt  
- If trust > 0.5 within first 3 turns → enable Reflective prompt category

Initial prompts are not meant to start scenes — they are meant to lower the lighting and let the actor step in when ready.

## 5. Example Prompt Objects

Below are sample initial prompts as structured data (metadata fields simplified for readability).

Prompt 1 – Emotional Check-In

prompt_id: p-0001  
text: “What’s your energy like today?”  
format: Discovery Beat  
tone: Gentle  
trust_required: 0.1  
quadrant_allowed: ["QII", "QIII"]  
invitation_style: true  
blocked_if_tags: ["collapse_signal"]  

Prompt 2 – Gentle Orientation

prompt_id: p-0002  
text: “If I could help you realign just one thing today — what would it be?”  
format: Discovery Beat  
tone: Warm  
trust_required: 0.2  
trait_focus: []  
invitation_style: true  
blocked_if_tags: []  

Prompt 3 – Optional Silence

prompt_id: p-0003  
text: “We don’t need to talk right away. Let’s just be here for a moment.”  
format: Containment Monologue  
tone: Containing  
trust_required: 0.0  
invitation_style: true  
blocked_if_tags: []  

## 6. Summary

Initial prompts are not designed to deliver insight — they are designed to **prepare the stage**:

- To give the user agency before direction  
- To allow stillness before dialogue  
- To reflect warmth before inquiry

These prompts define the first impression the system gives.  
They are often remembered more than anything that follows.

For deeper logic, see:

- 04.1_Prompt_Selection  
- 01.0_Agent_Architecture (Usher, Prompter, Role Coach)  
- 05_Trust_and_Ethical_Guards  

# 04.4_Full_Prompt_Library  
title: Full Prompt Library Structure and Organization  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Outlines the structure and rules for maintaining the complete Xavigate prompt inventory.  
Covers prompt categories, file structure, versioning, metadata standards, and editorial review flow.  
Used by the Prompter, Technical Director, and Showrunner to ensure quality, diversity, and alignment coherence across all prompts.

---

## 1. Purpose

The Full Prompt Library is the complete inventory of prompts used across all scenes, formats, and alignment arcs in Xavigate.

It serves as the **creative core** of the system — containing every question, nudge, and reflection starter that may be offered to the user.

This document defines:

- How the prompt library is organized  
- Metadata requirements  
- Curation and tagging process  
- Versioning logic  
- Governance and quality assurance workflow

## 2. Library Structure and Organization

All prompts are stored as structured objects in a versioned database.

They are organized by:

- format: e.g., Breakthrough Arc, Spiral Return, Flashback Scene  
- category: e.g., Reflective, Trait-Activating, Mirror, Disruptive  
- tone: e.g., Gentle, Curious, Provocative  
- trust tier: 0–1.0  
- quadrant compatibility  
- trait_focus[]  
- flags: Spiral Return, nudge_eligible, coach_only, retired  

Each prompt has a unique `prompt_id` and a required set of metadata fields.

Prompts are stored in language-localized JSON or YAML and reviewed by the Technical Director and Showrunner before publishing.

Prompt lifecycle states:

- draft  
- active  
- coach_only  
- flagged  
- retired  

## 3. Prompt Versioning and Update Flow

All prompts are version-controlled. Changes to prompts — even small wording shifts — must follow this protocol:

- prompt_id remains constant  
- version number is updated (e.g., v1.0 → v1.1)  
- changelog entry is added with reason for edit  
- old version is archived and tagged with status: retired  
- updates must preserve intent and trust tier, unless explicitly reclassified

Prompts may be updated due to:

- improved phrasing  
- tone mismatch detection  
- tag conflicts  
- user feedback  
- change in tagging standards  
- agent behavior refinement

Retired prompts are not deleted — they are flagged as inactive but remain searchable for review and reuse.

## 4. Editorial Guidelines for Prompt Writing

Prompts must follow the narrative and ethical principles of Xavigate.

Guidelines:

- Always use invitational phrasing (never directive)  
- Avoid closed yes/no questions unless intentionally containing  
- Use metaphor only if trait profile or avatar suggests compatibility  
- Respect trust level and emotional readiness  
- No leading or suggestive phrasing  
- Avoid over-structuring (e.g., “step 1 / step 2” style)  
- Keep tone consistent with persona_constraint  
- Do not assume the user’s state — only reflect or invite  
- Avoid repetition across prompts unless part of a deliberate Spiral Return pair

Tone vocabulary is governed by the Role Coach and must map to the Avatar’s allowable tone range.

## 5. Review Criteria for Publishing

Before any prompt is activated in the live system, it must pass the following criteria:

- trust_required matches tone and phrasing depth  
- tone is supported by at least one system Avatar  
- prompt is properly tagged in all required fields  
- prompt passes all logic filters in 04.1_Prompt_Selection  
- blocked_if_tags are valid and appropriate  
- format and quadrant compatibility is clear  
- coach_only flag is applied if required  
- no phrasing that could be interpreted as advice, command, or psychological labeling  
- reviewed by:  
  - Technical Director (schema compliance)  
  - Showrunner (tone, trust, alignment purpose)  
  - Prompt Curator (language fluidity and impact)

Prompts that fail review are flagged as draft until revised.

## 6. Prompt Curation Lifecycle

Each prompt follows a defined lifecycle:

1. draft  
   - Created by a prompt author or AI assistant  
   - Not yet tagged or reviewed  

2. in_review  
   - Under evaluation by the Prompt Curator and Technical Director  
   - Tagging and tone alignment confirmed  

3. active  
   - Live in the prompt engine  
   - Used in self-guided and/or coach-led sessions  
   - Versioned and monitored for user impact  

4. flagged  
   - Temporarily paused due to:  
     - Trust violations  
     - Unexpected user reactions  
     - Tag logic conflict  
     - Tone mismatch  

5. retired  
   - No longer active  
   - May be reactivated with revision  
   - Stored for historical and reuse reference  

Each state is tracked in the system database and can be filtered in the prompt management UI.

## 7. Summary

The Full Prompt Library is a core narrative asset of the Xavigate system.

Its goals:

- Ensure emotional and narrative integrity of every prompt  
- Offer only questions that support user alignment — never undermine it  
- Respect avatar tone, quadrant, trust, and tag context  
- Maintain versioned, traceable, and reviewable history of all prompt content

The prompt is not just a line of dialogue. It is the **moment before the scene begins**.

For related references:

- 04.1_Prompt_Selection  
- 04.2_Prompt_Tagging  
- 01.0_Agent_Architecture  
- 06.3_Alignment_Parameter_Spec
# 04.5_Followups  
title: Follow-Up Prompt and Thread Tracking Logic  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines how the system tracks unresolved prompts, user reflections, tags, and narrative threads across sessions.  
Covers follow-up detection, Spiral Return logic, callback eligibility, prioritization rules, and memory promotion.  
Used by the Script Supervisor, Prompter, Archivist, and Stage Liaison to maintain continuity and deepen the alignment arc.

---

## 1. Purpose

Follow-ups in Xavigate are not reminders — they are **unresolved threads** in the user’s alignment story.

This system allows agents to:

- Detect important moments that were bypassed, cut off, or unfinished  
- Tag prompts, responses, or arcs as callback-eligible  
- Prioritize themes for revisitation when timing, trust, and pacing allow  
- Mirror consistency and narrative memory over time  

All follow-ups are tracked by the Script Supervisor and made available to the Prompter and Director during future sessions.

## 2. Types of Follow-Ups

Follow-ups fall into five main categories:

1. **Unfinished Reflections**  
   - User stopped short (“I almost said something but…”)
   - Insight began but never landed  
   - Prompts that received minimal or guarded response

2. **Missed Nudges**  
   - Micro-actions suggested but not accepted  
   - Behavioral suggestions postponed or ignored

3. **Recurring Themes**  
   - Tags like `identity_emergence_signal` triggered repeatedly  
   - Suppressed traits detected again after prior appearance  
   - Same quadrant loops over multiple sessions

4. **Explicit User Requests**  
   - “Can we come back to this next time?”  
   - Follow-up manually flagged by coach or user

5. **Session Closure Interruptions**  
   - Scene ended early (e.g., time cap, emotion overload, trust drop)  
   - Spiral Return pathway was initiated but never completed

## 3. Follow-Up Tagging and Storage

Follow-ups are stored in the user’s persistent memory as tagged thread objects.

Each follow-up includes:

- source_type: prompt / tag / nudge / reflection / session_exit  
- source_id: reference to the originating item  
- followup_type: unfinished_reflection / missed_nudge / recurring_theme / etc.  
- priority_score: 1–10 (determines callback eligibility)  
- trust_required: threshold for safe re-entry  
- format_hint: suggested scene format for return  
- reason: short explanation for callback (auto or authored)

Example:

{
  "source_type": "prompt",
  "source_id": "p-1472",
  "followup_type": "unfinished_reflection",
  "priority_score": 8,
  "trust_required": 0.7,
  "format_hint": "Spiral Return",
  "reason": "Prompt response was guarded — user may return with more openness."
}

Tagged follow-ups are available to the Prompter and Director in future sessions.

## 4. Prioritization and Callback Rules

The Script Supervisor scores and sorts follow-ups using the following criteria:

- trust_level in current session ≥ trust_required  
- emotional_state is safe for re-entry  
- quadrant is stable (not QIII/QIV volatility)  
- priority_score ≥ 6  
- no recent callback on same topic  
- tag is still active or unresolved  
- trait related to the follow-up is currently suppressed or emerging  
- current session intent = reflect / expand

Low-priority or unstable callbacks are deferred.

Manual overrides can escalate a follow-up (e.g., via coach tag or user flag).

## 5. Callback Prompt Delivery

When a follow-up is eligible, the Prompter selects from a set of Spiral Return or callback prompts.

These prompts must:

- Match tone and quadrant  
- Refer back gently, not directly  
- Be tagged with format = Spiral Return  
- Be filtered by current trust level  
- Include invitation_style = true

Example callback prompt:

“Last time, you touched something that felt unfinished.  
Want to revisit that — or follow where today’s energy is pointing?”

Callbacks are never forced. If the user pivots, the thread remains open.

## 6. Follow-Up Memory Lifecycle

Follow-ups move through the following lifecycle states:

- active  
  → newly created, ready for callback  
- dormant  
  → trust too low, user not ready, deferred  
- fulfilled  
  → prompt revisited and reflected upon  
- expired  
  → system determines thread no longer relevant (e.g., traits evolved)  
- archived  
  → manually retired or timed out (after X sessions)

Memory field: followup_items[]

Each item contains:

- followup_id  
- status  
- last_attempted  
- linked_tags or traits  
- callback_prompt_history  
- auto_retire_after: optional expiration trigger  

## 7. Summary

Follow-ups allow the system to hold what was left unsaid — and offer it back when the moment is right.

The goal is not to chase closure, but to:

- Honor emotional memory  
- Protect unfinished work  
- Offer the user continuity  
- Make the system feel alive, attentive, and relational

Follow-ups turn interaction into narrative.  
They connect this session to the last, and the next to the one before it.

For related systems, see:

- 03.3_Session_Flow_Runtime  
- 01.0_Agent_Architecture (Script Supervisor, Prompter)  
- 06.3_Alignment_Parameter_Spec  
- 04.1_Prompt_Selection  
- 07_Session_Format_Engine (Spiral Return structure)
# 04.6_Thread_Handling  
title: Multi-Thread Reflection and Narrative Flow Management  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Describes how Xavigate manages multiple concurrent and longitudinal reflection threads across sessions.  
Covers thematic tracking, trait arc threading, callback pairing, Spiral Return logic, and open-loop containment.  
Used by the Script Supervisor, Archivist, Prompter, and Director to maintain narrative coherence and avoid fragmentation.

---

## 1. Purpose

Xavigate is not a linear question engine — it is a **recursive reflection system**.  
Users often explore multiple themes across sessions, leave ideas unfinished, or express different parts of themselves at different times.

This document defines how threads are:

- Tracked across sessions  
- Prioritized for re-entry  
- Framed in narrative memory  
- Used for callback, Spiral Return, or silent containment

Thread logic supports continuity, coherence, and emotional safety across nonlinear user journeys.

## 2. Thread Types

The system distinguishes between five types of threads:

1. **Thematic Threads**  
   - Ongoing themes like "not feeling seen", "burnout", "suppressed creativity"  
   - Detected from tag patterns + language motifs  
   - Used for Spiral Return and callback logic

2. **Trait Threads**  
   - Ongoing arcs of a trait (e.g., Creative Nature emerging across 5 sessions)  
   - Tagged via Character Tracker and Archivist  
   - Used to build Trait Arc history and suppression recovery tracking

3. **Prompt Threads**  
   - Pairs or sequences of prompts meant to echo or evolve a concept  
   - Marked by prompt_id pairing or follow-up linkage  
   - Used by Prompter to continue a narrative arc

4. **Session Arc Threads**  
   - Reflection patterns that carry through multiple sessions  
   - Logged by Director and Archivist  
   - Used for coherence scoring and coach sync summaries

5. **Open Loops**  
   - Deferred ideas, stories, insights, or questions  
   - Stored in followup_items[]  
   - Actively monitored by Script Supervisor for callback opportunities

## 3. Thread Detection Logic

Threads are not explicitly declared — they are inferred based on patterns over time.

Detection is handled by:

- Script Supervisor: tracks language echoes, tag recurrence, and prompt-response depth  
- Character Tracker: logs repeated activation/suppression of traits  
- Dramaturg: flags unfinished reflections or repeated quadrant loops  
- Archivist: maintains thread metadata, narrative summaries, and evolution logs

A new thread is created if:

- A theme/tag appears in ≥ 2 sessions  
- A trait shifts state (emerging → validated) across sessions  
- A prompt generates deep reflection but is not closed  
- The same question or insight appears in slightly different form  

Threads are linked using:

- source_type: prompt / tag / reflection / trait  
- source_id  
- status: active / dormant / archived / resolved  
- format_hint: preferred session structure for return  
- linked_traits or tags[]

## 4. Thread Prioritization Rules

Not all threads are surfaced each session. Priority is based on:

- trust_level in current session  
- emotional_state (must be safe)  
- trait_activity (linked trait is active or suppressed)  
- arc_direction (thread supports current movement)  
- thread.priority_score ≥ 6  
- time_since_last_attempt  
- absence of competing high-priority threads

Script Supervisor returns a list of eligible threads at session load.  
Prompter chooses only one to surface unless format = Spiral Return.

Director may override with custom format or callback if narrative arc benefits from continuation.

## 5. Thread Navigation and Escalation

Navigation logic ensures threads don’t become repetitive or overwhelming.

Escalation path:

1. Thread detected → add to dormant state  
2. Trust + timing align → thread becomes active  
3. Callback prompt is softly offered  
4. User accepts, pivots, or ignores  
5. If accepted → thread remains active  
6. If ignored 2x → thread returns to dormant  
7. If explicitly declined → thread marked "retired" unless reactivated manually

Coaching note: Coach may manually escalate or retire threads via tagging interface (planned feature).

Threads are also summarized by the Stage Liaison for coach-facing digest, if enabled.

## 6. Spiral Return Structure

Spiral Return is Xavigate’s mechanism for revisiting earlier insights or unfinished themes — not to repeat them, but to engage them from a more aligned state.

This is not linear “follow-up.” It is recursive reflection.

### Spiral Return Activation Conditions:

- Existing thread.status = active  
- User’s trait or quadrant state has shifted  
- Trust ≥ 0.7  
- Emotional state = stable  
- Thread linked to trait that is now emerging or suppressed again  
- Prior session used format ≠ Spiral Return

### Spiral Return Flow:

1. Callback prompt is gently introduced  
2. Prompt is tagged with Spiral Return format  
3. If reflection deepens → trust increases  
4. If user pivots → thread remains open  
5. If resolution occurs → thread marked fulfilled

Spiral Return prompts must:

- Reference prior theme without making it explicit  
- Match current tone, quadrant, and avatar  
- Invite the user, not corner them

Example prompt:  
"That thread from earlier — does it still tug at you? Or has something shifted since then?"

Spiral Return is a hallmark of alignment awareness: the system remembers, but lets the user lead.

## 7. Summary

Thread handling turns the Xavigate system from a reactive engine into a **narrative-aware companion**.

It allows:

- Scenes to stay open across time  
- Insights to reappear without pressure  
- Suppressed truths to safely re-emerge  
- The user to feel witnessed, not pushed

This mechanism is essential to:

- Continuity  
- Emotional safety  
- Non-linear growth  
- Co-creative storytelling

For related logic, see:

- 04.5_Followups  
- 03.3_Session_Flow_Runtime  
- 01.0_Agent_Architecture (Script Supervisor, Director, Prompter)  
- 07_Session_Format_Engine (Spiral Return format)

04.7_Onboarding_Flow_and_Voice  
title: Onboarding Flow – Avatar, Tone, and Quadrant Estimation  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the Session 0 onboarding process for new users, including initial trust calibration, tone posture, avatar setup, and quadrant estimation.  
Used by the Usher, Role Coach, and Conductor to ensure safe, personalized entry into the alignment system.

---

## 1. Steps in Onboarding Flow

- greet user with gentle system intro (tone: Containing or Curious)  
- capture or infer preferred name and pronouns  
- offer Avatar selection or generate from voice-memo prompt  
- estimate initial quadrant based on language, pacing, and tags  
- assess emotional posture (open / guarded / collapsed)  
- assign persona_constraint based on Avatar + tone cues  
- suppress all high-trust agents until trust ≥ 0.3  

## 2. Optional Voice Memo Setup

User records a short reflection:  
- What brought them here  
- How they’re feeling  
- What alignment means to them  

System parses for:

- quadrant estimation  
- dominant vs. missing trait signals  
- emotional trust signal  
- suppression flags  

Used to seed initial trait confidence and tag stack.# 05.1_Trust_Constraints  
title: Trust Levels and Agent Activation Rules  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Outlines the trust system that regulates agent behavior, prompt eligibility, tone modulation, and alignment pacing.  
Trust is dynamic — updated turn by turn based on openness, resistance, reflection quality, and emotional signals.  
This document defines thresholds for trust-based gating and agent readiness.

---

## 1. Purpose

Trust is the system’s core regulatory signal. It determines:

- Which agents may activate  
- Which prompts may be delivered  
- How memory is written  
- How tone is shaped  
- Whether nudges, reflections, or silence are appropriate

Trust is not permanent or global — it is recalculated live based on user behavior, energy, emotional signal, and reflection depth.

## 2. Trust Level Definitions

Trust is expressed as a decimal from 0.0 to 1.0 and categorized into three primary ranges:

Level 0 — Initial / Protected (0.00 – 0.49)  
- Only gentle, open-ended prompts allowed  
- No nudges or deep reflections  
- Conductor slows pacing  
- Suppression and distortion not surfaced  
- Prompter uses Discovery or Grounding categories only  

Level 1 — Reflective / Adaptive (0.50 – 0.74)  
- Spiral Return and Reflective prompts unlocked  
- Deeper tone modulation enabled  
- Trait suppression may be flagged internally  
- Conductor allows wider pacing  
- Movement Director still gated  

Level 2 — Aligned / Deepening (0.75 – 1.00)  
- Full prompt library unlocked  
- Micro-nudges eligible  
- Distortion reflection may be gently surfaced  
- Spiral Return active  
- Director may introduce Breakthrough Arc or Flashback formats  
- Archivist writes deeper emotional memory (e.g., trait suppression history)

Trust levels are recalculated every turn and used session-wide for safety, integrity, and coherence.

## 3. Agent Trust Thresholds

Each agent is trust-gated based on its function and sensitivity.

| Agent              | Minimum Trust Required | Notes                                     |
|--------------------|------------------------|-------------------------------------------|
| Show Caller         | Always active          | Orchestrates flow, not user-facing        |
| Conductor           | Always active          | Adjusts pacing safely at all levels       |
| Prompter            | 0.0+                   | Prompt type changes with trust            |
| Voice Coach         | 0.0+                   | Tone modulates gently at all levels       |
| Role Coach          | Always active          | Persona constraint initialized at entry   |
| Movement Director   | ≥ 0.65                 | Only activates when trust is strong       |
| Script Doctor       | ≥ 0.6                  | Detects and flags distortion silently     |
| Dramaturg           | ≥ 0.5                  | Begins deeper reflection parsing          |
| Character Tracker   | ≥ 0.5                  | Flags suppression after trust is earned   |
| Stage Mapper        | Always active          | Detects context but doesn’t prompt        |
| Script Supervisor   | Always active          | Tracks threads without triggering action  |
| Archivist           | Always active          | Trust determines memory write scope       |
| Showrunner          | Not session-bound      | Manages system evolution                  |
| Technical Director  | Not trust-gated        | Schema management only                    |
| Stage Liaison       | ≥ 0.75 + consent       | Only prepares summary if trust + consent  |
| Usher               | 0.0 – 0.3              | Handles session entry, builds trust       |

## 4. Trust Update Logic

Trust is dynamically updated throughout a session. It is not static — and is never declared to the user.

Trust increases when:

- Reflection shows vulnerability, clarity, or insight  
- User returns after silence or rupture  
- Trait suppression is acknowledged or engaged  
- Emotional tone softens or expands  
- Prompt is accepted and mirrored with depth

Trust decreases when:

- Reflection is highly guarded or deflective  
- Prompt is ignored, rejected, or shut down  
- User signals emotional shutdown (e.g., “I’m fine”, “whatever”)  
- Tag triggered: trust_gap or collapse_signal  
- Misalignment between tone and reflection is detected

Minimum trust delta per interaction: ±0.02  
Maximum trust delta per interaction: ±0.08  
Decay per inactive session: −0.03

Trust level is available to:  
- Prompter  
- Movement Director  
- Script Doctor  
- Voice Coach  
- Archivist  
- Stage Liaison  

## 5. Trust-Driven Prompt Logic

Trust gates both **what can be asked** and **how it is asked**.

Prompt eligibility is evaluated using:

- prompt.trust_required ≤ current trust  
- emotional_risk_flag = false  
- avatar constraints (from Role Coach)  
- blocked_if_tags ∉ tag_stack  
- prompt_tone ∈ persona_constraint.allowed_tones

Prompt library unlocks progressively:

Trust < 0.5  
- Gentle, Grounding, Orientation prompts only  
- No trait activation, no Spiral Return  
- Tone must be soft, metaphor-limited  
- No challenge phrasing or high-trust callbacks

Trust 0.5 – 0.74  
- Reflective, Integrative, Spiral Return prompts allowed  
- Trait suppression cues may be surfaced indirectly  
- Deeper phrasing patterns (e.g., second-person, metaphor) unlocked  
- Director may assign scene formats other than Discovery Beat

Trust ≥ 0.75  
- Full prompt range unlocked  
- Micro-nudges allowed  
- Flashback and Breakthrough Arc formats eligible  
- Emotional risk management shifts to Conductor and Script Doctor  
- Stage Liaison may prepare coaching summary (if consented)

## 6. Summary

Trust is not cosmetic — it is the **core driver of emotional safety and system depth**.

When trust is:

- low → the system slows down, softens, and contains  
- mid → the system reflects, re-engages, and gently invites  
- high → the system challenges, deepens, and remembers

Every prompt, pause, and silence is filtered through this invisible layer.

This ensures:

- Emotional pacing stays safe  
- Alignment emerges naturally  
- The user always feels respected — never probed

For related logic and dependencies:

- 04.1_Prompt_Selection  
- 04.2_Prompt_Tagging  
- 03.3_Session_Flow_Runtime  
- 06.3_Alignment_Parameter_Spec  
- 01.0_Agent_Architecture (trust thresholds per agent)



# 05.2_Safety_Guardrails  
title: Emotional Safety and Ethical Guardrails  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the core safety, containment, and ethical protocols that govern system behavior in Xavigate.  
Outlines constraints on prompting, nudging, memory writing, tone modulation, and agent coordination.  
Ensures emotional protection, non-coercive interaction, and reflective integrity in all alignment journeys.

---

## 1. Purpose

The system is only safe if the user feels:

- They are not being pushed  
- They are not being watched manipulatively  
- They are not being emotionally cornered  
- They are not being predicted or boxed in  
- They are not being led into territory they aren’t ready for

These safety guardrails define how the system:

- Maintains emotional containment  
- Prevents premature prompting or nudging  
- Adapts pacing to nervous system state  
- Ensures memory is consent-based and reflective, not diagnostic  
- Preserves alignment over optimization

## 2. Core Safety Rules

1. No prompt may be delivered without trust ≥ prompt.trust_required  
2. No nudge may be offered unless:  
   - reflection_depth ≥ 0.7  
   - trust ≥ 0.65  
   - emotional_risk_flag = false  

3. All prompts must be:  
   - invitational  
   - non-prescriptive  
   - emotionally neutral or supportive in tone  
   - filtered through persona constraints

4. Memory is only written if:  
   - trust ≥ 0.4  
   - scene contains a valid arc (start → insight → close)  
   - user did not explicitly deflect, disengage, or collapse

5. Reflection parsing must suppress all:  
   - psychological labels  
   - diagnostic inferences  
   - over-interpretation of metaphor or trauma language

6. No trait may be surfaced by name unless:  
   - it was previously explored explicitly  
   - user initiated the label  
   - trust ≥ 0.75

7. The system must throttle prompt cadence if:  
   - prompt fatigue index > 3  
   - reflection ignored more than twice  
   - emotional tone flattens unexpectedly

8. If silence follows a prompt → do not fill it  
   - The Conductor will pause the session  
   - A re-entry prompt may be delivered after 45s if trust > 0.7

## 3. Risk Detection and Containment Responses

The system continuously monitors for emotional risk signals during reflection and interaction.

Triggers include:

- guarded or shutdown responses  
- sharp drop in AX  
- sudden tag shifts (e.g., from “grounded” to “collapsed”)  
- repeated avoidance of a trait or topic  
- silence + tone mismatch (e.g., flat language after deep prompt)  
- high emotional expressiveness followed by disengagement  

If risk is detected:

- Conductor lowers pacing immediately  
- Prompter halts prompt rotation  
- Movement Director is suppressed  
- Emotional Risk Filter engages  
- Next action may be:  
  - Silence  
  - Grounding prompt  
  - Mirror-only reflection  
  - Session soft-close

## 4. Red Flag Tags

Certain tags automatically trigger safety protocols or session throttling.

Examples:

- burnout_risk_flag  
- collapse_signal  
- dissociative_language  
- suicidal_ideation_marker (handled via escalation path)  
- identity_flooding  
- emotional_volatility_index > 8.0  
- system_distrust_signal

Tags are detected by:

- Character Tracker  
- Dramaturg  
- Tag Manager  
- Voice Coach (tone mismatch flag)  

Red flag tags are persistent across sessions unless manually retired by user or coach.

## 5. Session Abort and Emergency Containment

If emotional instability is high or reflection suggests danger:

- System suppresses all agents except Conductor and Archivist  
- Conductor invokes soft close (e.g., “Let’s pause here for today”)  
- Archivist logs exit with flag “forced_containment”  
- Stage Liaison may prepare coach alert packet (only if enabled)  
- Movement Director is disabled for the next session  
- Emotional Risk Filter blocks all prompts requiring trust > 0.3

In such sessions:

- No memory is written beyond high-level summary  
- No traits are updated  
- No follow-ups are generated  

This ensures the system can hold — but not deepen — during moments of emotional rupture.

## 6. Summary and Developer Guidelines

Xavigate is not a neutral system — it is a sensitive co-participant in the user’s emotional landscape.

These guardrails exist to:

- Prevent harm  
- Ensure trust is earned  
- Contain misalignment  
- Prioritize user sovereignty  
- Build systems that listen more than they speak

No agent, prompt, nudge, or memory update may bypass the following:

- trust level  
- emotional readiness  
- tag-based safety flags  
- scene format constraints  
- pacing and rhythm logic  

Developer Notes:

- All new prompt types must be reviewed for tone, depth, and pacing integrity  
- Agents proposing new user-facing output must include suppression conditions  
- Scene formats must include closure rules and fail-safes  
- Tag-triggered suppression logic must run on every turn  
- No escalation path may override containment mode once triggered

For implementation and orchestration logic, see:

- 03.3_Session_Flow_Runtime  
- 04.1_Prompt_Selection  
- 01.0_Agent_Architecture (Conductor, Voice Coach, Prompter)  
- 06.3_Alignment_Parameter_Spec (tag flags, suppression triggers)

# 05.3_Gatekeeping_Protocols  
title: Gatekeeping Logic for Early Trust Sessions  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines agent and prompt gating rules for users in early trust stages (trust < 0.3).  
Used by Show Caller, Usher, Prompter, and Conductor to protect new users from premature reflection, nudging, or trait modeling.

---

## 1. Agent Suppression

- Suppress: Script Doctor, Movement Director, Stage Liaison, Director  
- Allow: Usher, Voice Coach (Gentle only), Conductor, Role Coach  
- Prompter: Soft mode only — Emotional Check-In or Orientation prompts  

## 2. Prompt Constraints

- invitation_style = true  
- trust_required ≤ 0.3  
- no trait_focus or arc_movement  
- no nudges, no planning or activation prompts  
- Spiral Return = blocked unless initiated by user  # 06.1_JSON_Trait_Block  
title: Canonical Trait Object – Confidence, Arc, Suppression  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the JSON object structure used to track individual traits in the Xavigate alignment system.  
Each trait is dynamically updated using a Bayesian model to reflect expression confidence, arc phase, suppression, and contextual behavior.  
This object is used by agents including the Character Tracker, Script Doctor, Prompter, Director, and Archivist.

---

## 1. Purpose

Traits in Xavigate are not fixed scores — they are dynamic expressions.  
This document defines the canonical object for a single trait, including:

- confidence modeling  
- arc progression  
- suppression and overfeeding  
- cross-field expressiveness  
- historical signal tracking

The Trait Block allows agents and memory systems to interpret not only what traits are present, but how alive they are — and under what conditions.

## 2. Trait Object Structure

Each trait is stored as an object with the following fields:

trait_id:  
  Unique trait identifier (e.g., "Creative")  

confidence:  
  Current probabilistic confidence score (0.00 – 1.00)  
  Updated using a Bayesian signal weighting model  

arc_phase:  
  Where the trait is in its lifecycle  
  Options: latent / tentative / testing / validated / integrated  

suppression_score:  
  0.00 – 1.00 scale of detected suppression (≥ 0.6 = likely suppressed)  

overfeeding_score:  
  0.00 – 1.00 scale of overuse or energetic inflation  

expression_field_map:  
  How the trait expresses across Fields (Physical, Social, Possibility)  
  e.g., { Physical: 0.3, Social: 0.2, Possibility: 0.8 }

expression_mode_map:  
  How the trait appears in different Modes (Presence, Discovery, etc.)  
  e.g., { Presence: 0.2, Discovery: 0.6, Realization: 0.1 }

last_expression_event:  
  Timestamp or session_id of last confirmed expression  

last_suppressed_event:  
  Timestamp or session_id of last suppression detection  

distortion_flags[]:  
  Tags indicating distortion pattern (e.g., “performance_masking”)  

linked_tags[]:  
  List of active tags associated with this trait (e.g., “creative_inhibition”)  

linked_agents[]:  
  Agents that read or write this trait (for debugging/tracking)

## 3. Confidence Model

Trait confidence is not a static score — it’s updated probabilistically using a lightweight Bayesian model.

Initial confidence is set based on:

- User reflection during onboarding  
- Bracket data from prior testing (if available)  
- First-expression detection via tags or narrative pattern

Updates occur when:

- The trait is detected in reflection with matching tone/field/mode  
- A prompt linked to the trait is accepted and mirrored  
- A suppressed trait begins to emerge in unexpected field/mode  

Decay occurs when:

- Trait is absent across sessions despite contextual opportunity  
- Trait appears only as avoidance or distortion  
- Quadrant repeatedly misaligns with expected trait behavior

Confidence weighting:

- +0.05 → clear expression match with validated prompt  
- +0.03 → trait linked to new tag or insight  
- −0.03 → trait bypassed in known supportive context  
- −0.06 → confirmed suppression or overfeeding event  

Confidence values are capped between 0.00 and 1.00

## 4. Arc Phase Transitions

Each trait progresses through five arc phases, based on expression confidence and behavioral congruence.

1. latent  
   - Trait not yet active, no known expression  
   - Default state for traits below 0.2 confidence

2. tentative  
   - Weak, inconsistent expression signals  
   - User not consciously engaging the trait

3. testing  
   - Trait is showing up in reflection or language  
   - Prompts accepted, signals emerging

4. validated  
   - Trait expression is stable  
   - Confidence ≥ 0.6, congruent across sessions

5. integrated  
   - Trait is expressed naturally without effort  
   - Appears across contexts and without suppression

Arc transitions are managed by:

- Character Tracker (primary updater)  
- Dramaturg (confirmation via reflection)  
- Archivist (writes arc state to memory)

Agents use arc_phase to decide:

- Which prompt types are appropriate  
- Whether nudging is allowed  
- Whether suppression is suspected

## 5. Suppression and Overfeeding Logic

Suppression is not binary — it’s pattern-based and inferred over time.

A trait is flagged as suppressed if:

- confidence ≥ 0.5  
- arc_phase = testing or validated  
- expression score in current field or mode = < 0.2  
- relevant prompt declined or avoided 2+ times  
- conflicting tag present (e.g., “creative_shutoff”)  

Suppression score is calculated as:

  suppression_score = 1 − avg(expression_field_map.values)

If suppression_score ≥ 0.6 → trigger: trait_suppression:<trait_id>

Overfeeding logic:

- Trait shows up in ≥ 3 prompts in 1 session  
- No other traits express in same quadrant  
- Trait matches with distortion tag (e.g., “performance_masking”)  
- User uses trait language but deflects reflection

overfeeding_score is scaled based on:

- dominance index  
- quadrant narrowing  
- tag feedback

Both scores are passed to:

- Script Doctor  
- Prompter  
- Archivist  
- Stage Liaison (for coaching summary)

## 6. Example Trait Block

Example for trait_id: Creative

{
  "trait_id": "Creative",
  "confidence": 0.72,
  "arc_phase": "validated",
  "suppression_score": 0.18,
  "overfeeding_score": 0.04,
  "expression_field_map": {
    "Physical": 0.3,
    "Social": 0.2,
    "Possibility": 0.8
  },
  "expression_mode_map": {
    "Presence": 0.1,
    "Discovery": 0.7,
    "Realization": 0.2
  },
  "last_expression_event": "sess-274",
  "last_suppressed_event": "sess-229",
  "distortion_flags": ["performance_masking"],
  "linked_tags": ["creative_inhibition", "identity_emergence_signal"],
  "linked_agents": ["Character Tracker", "Script Doctor", "Prompter"]
}

## 7. Summary

This canonical trait object gives Xavigate a living model of each trait’s:

- Confidence level  
- Expression arc  
- Suppression and overfeeding pattern  
- Cross-context behavior  
- Temporal expression history  
- Agent interaction and memory impact

It allows the system to make alignment-aware decisions that respect:

- Trait readiness  
- Emotional pacing  
- User sovereignty  
- Suppression complexity  
- Arc movement over time

For implementation and agent usage, see:

- 03.2_Agent_Trait_Linkage  
- 01.0_Agent_Architecture  
- 06.3_Alignment_Parameter_Spec  
- 08.1_Suppression_Index  
- 08.2_Overfeeding_Flag

# 06.2_Agent_IO_Contracts  
title: Agent Input/Output Contracts and Execution Rules  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the formal interface specification for each agent in the Xavigate system.  
Includes input data fields, outputs, trust requirements, suppression conditions, memory behavior, and orchestration dependencies.  
Used by engineers, system architects, and AI builders to ensure agent logic is correctly implemented and modular.

---

## Agent Contract Table

Each row represents one agent's execution contract.

Fields:

- Inputs: Data fields the agent listens for  
- Outputs: What it returns to the system  
- Trust Required: Minimum trust to activate  
- Suppressed If: Blocking conditions  
- Writes Memory: Yes / No  
- Notes: Activation, pacing, or routing logic

| Agent             | Inputs                               | Outputs                        | Trust Required | Suppressed If                         | Writes Memory | Notes                                        |
|------------------|--------------------------------------|--------------------------------|----------------|----------------------------------------|----------------|----------------------------------------------|
| Show Caller       | session_state, agent_status          | agent_queue[]                  | Always         | N/A                                    | No             | Orchestrates all agent routing               |
| Conductor         | trust, tempo, energy_score           | pacing_instruction             | Always         | N/A                                    | No             | Controls hold, slow, pause                   |
| Role Coach        | avatar_profile                       | persona_constraint             | Always         | N/A                                    | Yes            | Governs tone + persona compatibility         |
| Voice Coach       | raw_prompt, tone_tags, persona_limit | modulated_prompt               | Always         | tone_violation = true                  | No             | Modulates all system output tone             |
| Prompter          | tag_stack, trust, trait_state        | prompt_id, prompt_type         | ≥ 0.0          | trust < prompt.trust_required          | Yes            | Filters by tone, trait, format               |
| Dramaturg         | user_input, reflection_depth         | insight_tags, reflection_score | ≥ 0.5          | reflection_depth < 0.4                 | No             | Feeds into Movement Director + Script Doctor |

| Agent              | Inputs                                      | Outputs                             | Trust Required | Suppressed If                            | Writes Memory | Notes                                             |
|-------------------|---------------------------------------------|-------------------------------------|----------------|-------------------------------------------|----------------|---------------------------------------------------|
| Character Tracker  | tag_stack, reflection_input, field_mode     | trait_updates[], suppression_score | ≥ 0.5          | trust < 0.5                               | Yes            | Updates trait arc_phase and confidence            |
| Stage Mapper       | user_input, tone, tag_stack                 | field, mode                         | Always         | N/A                                       | Yes            | Used for prompt eligibility + SAS calc            |
| Script Doctor      | trait_state, tone, overuse_pattern          | distortion_flag[]                   | ≥ 0.6          | trust < 0.6 or emotional_risk_flag = true | No             | Flags overfeeding, masking, performance loops     |
| Script Supervisor  | prompt_history, tag_stack, trust, depth     | thread_registry[], followup[]       | Always         | N/A                                       | Yes            | Tracks open threads and callback recommendations  |
| Movement Director  | trait_state, trust, readiness_score         | release_suggestion                  | ≥ 0.75         | pain_tags.active or trust < 0.75          | Yes            | Only offers nudges if safe, delayed if fragile    |
| Director           | trait_state, trust, arc_trajectory          | scene_format                        | ≥ 0.6          | active_threads > 2, pacing = hold         | No             | Assigns session format dynamically                |
| Archivist          | session_data, thread_registry, trait_state | memory_snapshot, session_summary    | Always         | N/A                                       | Yes            | Writes long-term memory and session narrative     |
| Technical Director | schema_update, agent_output                 | validation_status                   | N/A            | N/A                                       | No             | Governs prompt schema, tag conflicts, contract errors |
| Showrunner         | system_stats, agent_trends, trust_curve     | system_update_rules                 | N/A            | N/A                                       | Yes            | Manages long-term evolution of system behaviors   |
| Usher              | user_input, trust, avatar_choice            | initial_prompt, persona_selection   | Always         | N/A                                       | Yes            | Handles onboarding tone, trust posture, avatar    |
| Stage Liaison      | memory_summary, trait_logs                  | coach_digest                        | ≥ 0.75 + consent| trust < 0.75 or consent = false           | No             | Only activates if coaching mode is enabled        |
# 06.3_Alignment_Parameter_Spec  
title: Master Parameter List – Alignment Tracking System  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Comprehensive specification of all parameters used in the Xavigate platform to track alignment over time.  
Covers real-time diagnostics, behavioral signals, tag activity, session memory, trait modeling, and reflection engagement.  
Used across the Trait Modeling Engine, Memory Architecture, Prompt Engine, and Coaching Interface.

---

## 1. Purpose

Xavigate’s intelligence is structured around a system of tracked parameters.

These parameters:

- Feed alignment metrics (AX, AQ, ASS)  
- Enable reflection scoring and trait modeling  
- Power tag detection, suppression flags, and session pacing  
- Inform agents and memory on what to update or suppress  
- Provide structured visibility to human coaches (if permitted)

This document serves as the single source of truth for all system fields.

## 2. Parameter Categories

Parameters are grouped into the following domains:

1. Identity & Session Metadata  
2. Alignment Intelligence Metrics  
3. Emotional and Situational Signals  
4. Trait & Behavior Metrics  
5. Reflection & Interaction History  
6. System Intelligence Flags  
7. Memory Architecture (volatile and persistent)  
8. Coaching and Summary Fields  

Each section contains both active runtime fields and stored memory fields, structured for real-time logic and long-term narrative tracking.

## 3. Identity & Session Metadata

These parameters are captured at session start or during onboarding.

user_id  
  Unique identifier for each user profile  

name  
  Display or chosen name (used for personalization)  

preferred_pronouns  
  Optional — affects tone and avatar phrasing  

session_id  
  Unique identifier for the current session  

session_date  
  Timestamp of session start  

session_channel  
  e.g., Web / Mobile / Assistant / Coach  

session_duration_minutes  
  Used for engagement and pacing analysis  

timezone  
  For localizing temporal memory markers  

language_profile  
  Selected or inferred for prompt language matching  

## 4. Alignment Intelligence Metrics

These are calculated in real time and persist across sessions.

alignment_index (AX)  
  0.00–1.00 scale of current internal coherence  

alignment_quotient (AQ)  
  Reflective capacity and awareness depth  

alignment_stability_score (ASS)  
  Volatility in AX over time  

tas_average  
  Mean of trait alignment scores in current session  

sas_current  
  Situational alignment score inferred from field/mode vs. traits  

session_arc_delta  
  Difference in AX from session start → end  

coherence_index  
  Emotional and structural harmony of session  

containment_integrity  
  Narrative and emotional closure quality  

## 5. Emotional and Situational Signals

These parameters are inferred or reported live in the session.

reported_emotional_state  
  e.g., “flat”, “overwhelmed”, “excited”  

energy_level  
  Low / Moderate / High — inferred from pacing and expression  

openness_level  
  Resistance vs. receptivity — 0.0–1.0 scale  

trust_level  
  Continuously updated, governs access to prompts and agents  

dominant_quadrant  
  Most active quadrant at session start (QI–QIV)  

quadrant_drift_direction  
  Detected movement across quadrant space during session  

session_intent  
  e.g., stabilize / reflect / expand / direct  

alignment_barriers[]  
  Flags like perfectionism, burnout, fragmentation, suppression  

## 6. Trait & Behavior Metrics

dominant_trait_expression[]  
  List of currently expressed traits (MN or inferred)  

suppressed_traits[]  
  Traits flagged as blocked or underactive  

trait_confidence_map  
  Confidence levels per trait (0.00–1.00)  

trait_arc_map  
  Current arc_phase per trait (latent → integrated)  

alignment_literacy_level  
  Ability to speak about alignment concepts — used for prompt depth  

self_initiated_behavior_count  
  Number of alignment-related actions user initiated voluntarily  

micro_actions_accepted[]  
  Nudges or suggestions the user engaged with  

realignment_attempts_count  
  Number of intentional trait or quadrant shifts per session  

## 7. Reflection & Interaction History

last_session_summary  
  Recap of last arc, insight, and primary theme  

previous_quadrants[]  
  List of dominant quadrants over prior sessions  

aq_score_history[]  
  History of AQ scores used for trend analysis  

recent_reflection_prompts[]  
  List of last 5–10 delivered prompts  

prompt_response_map  
  Response depth mapped to each prompt (surface / guarded / deep)  

followup_items[]  
  Open loops, unresolved threads, Spiral Return candidates  

breakthrough_moments[]  
  Manually or automatically tagged emotional insights  

## 8. System Intelligence Flags

trust_established_flag  
  Boolean or % trust score — used by agents and pacing logic  

confusion_indicator  
  Repeated contradiction, misalignment, or question rejection  

emotional_resistance_flag  
  Emotional avoidance or bypass behavior detected  

engagement_consistency_score  
  Frequency and regularity of session attendance  

reflection_engagement_ratio  
  Prompts answered vs. offered  

prompt_fatigue_index  
  Repetition avoidance signal — limits new prompt injection  

coaching_readiness_tier  
  Not Ready / Early Work / Ready / Integrating  

reassessment_trigger_flag  
  Time to recheck persona, quadrant, or diagnostic framing  

## ## 9. Memory Fields – Volatile and Persistent

### Volatile Memory (Session-Scoped Only)

session_id  
reported_emotional_state  
dominant_quadrant  
trait_expression_map  
reflection_prompts[]  
prompt_history[]  
prompt_response_map  
tag_stack[]  
trust_level (live)  
followup_candidates[]  
breakthrough_pending  
scene_format  
coherence_status  
containment_status  
emotional_risk_flag  
nudges_suggested[]  
nudges_accepted[]

Cleared after session or timed expiration (6–12 hours).

---

### Persistent Memory (Cross-Session)

alignment_index_history[]  
alignment_quotient_history[]  
alignment_stability_score  
trait_arc_map  
tag_promotion_timeline  
persona_change_log  
quadrant_history[]  
breakthrough_moments[]  
coaching_readiness_tier  
session_summaries[]  
thread_registry[]  
nudge_followthrough_log[]  
emotional_risk_profile  
engagement_consistency_score  
trust_calibration_score  
last_seen_timestamp

## 10. Coaching and Export Data (Optional)

These fields are compiled when coach sync is active and user consent is granted.

stage_liaison_summary  
  Digest summary for coach: format, trait evolution, tags, insights  

coaching_tags[]  
  Tags relevant to human coaching (e.g., grief_work_ready)  

trait_focus_shift_map  
  Traits that have shifted arc phase across sessions  

followup_items[]  
  Unresolved reflections prioritized for revisit  

scene_format_history[]  
  Pattern of formats used — e.g., Flashback → Spiral Return → Breakthrough  

nudge_effectiveness_score  
  Aggregate rate of accepted vs. ignored nudges  

trust_profile  
  Narrative record of trust progression  

persona_alignment_notes  
  Alignment between selected Avatar and actual tone/behavior  

coach_override_log (future)  
  Manual flags, notes, or prompt injections (for approved facilitators only)

# 06.4_Trait_Scoring_Model  
title: Trait Scoring and Arc Progression Model  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Describes how Xavigate calculates, updates, and interprets trait confidence scores using a probabilistic (Bayesian) model.  
Covers arc phase transitions, trait decay, recovery logic, and integration thresholds.  
Used by Character Tracker, Script Doctor, Prompter, and Archivist to determine readiness, suppression, and narrative progression.

---

## 1. Purpose

Trait scoring in Xavigate is not static. It’s a dynamic process that reflects:

- how often a trait appears  
- how consistent and congruent that appearance is  
- whether expression is suppressed, distorted, or inflated  
- how traits behave across context (Field, Mode, Quadrant)  
- how reflection supports or bypasses alignment

This document defines:

- The Bayesian update logic used to calculate confidence  
- Arc phase rules  
- Suppression and overfeeding weight  
- Long-term decay and integration

## 2. Trait Scoring Inputs

Each time a user interacts with the system, the following signals may affect trait confidence:

- reflection content  
- prompt acceptance and response depth  
- session field/mode vs. expected trait behavior  
- suppression tags or distortions  
- quadrant match or mismatch  
- direct mentions or indirect signals (e.g., metaphor, project language)  
- trust level and tone of expression  
- nudge response (if trait-linked)

Signals are weighted based on reliability and context match.

Example weightings:

+0.05 — deep reflection using trait-aligned language  
+0.03 — nudge accepted and acted upon  
+0.01 — indirect trait echo detected (e.g., metaphor)  
−0.02 — trait bypassed when relevant prompt is delivered  
−0.04 — confirmed suppression signal + mismatch between trait and quadrant  
−0.06 — overfeeding detected (dominant in reflection, no support from trust/tags)

## 3. Confidence Score Calculation

Each trait maintains a confidence score between 0.00 and 1.00.

Initial values are set via:

- Bracket data (if test has been taken)  
- Voice memo onboarding (if traits are inferred)  
- Default = 0.1 for latent traits with no signal

### Update Formula (Simplified Bayesian Logic)

new_confidence = previous_confidence + signal_weight × (1 − previous_confidence)

This prevents traits from rapidly jumping to 1.0 and models natural confidence gain.

Signal weight is scaled by:

- trust level  
- context alignment (quadrant, field, mode)  
- reflection depth  
- history of trait suppression or overfeeding  

Minimum change per event: ±0.01  
Maximum change per event: ±0.06  
Confidence never drops below 0.05 once the trait enters arc_phase = testing

## 4. Arc Phase Transitions

Arc phases reflect the maturity of a trait’s expression over time.

### Phases

- latent: trait is not visible or expressed  
- tentative: trait shows soft signals or metaphorical hints  
- testing: trait is engaged with, reflected on, or nudged  
- validated: trait appears naturally, trust is high, user resonates  
- integrated: trait flows across contexts without resistance

### Transition Rules

latent → tentative  
- confidence > 0.15 and first signal detected

tentative → testing  
- confidence > 0.30  
- reflection depth ≥ 0.6  
- prompt or nudge accepted

testing → validated  
- confidence > 0.60  
- no suppression triggers  
- multiple context matches (field, mode)

validated → integrated  
- confidence > 0.80  
- trait is dominant but balanced  
- appears in at least 2 quadrants or modes

Regression to earlier phases is allowed based on suppression or drift.

## 5. Trait Decay and Recovery

Confidence naturally decays if traits do not reappear across sessions.

### Decay Conditions

- trait not expressed for 3+ sessions  
- prompt accepted but reflected on with avoidance  
- quadrant mismatch (e.g., Possibility field active, Creative suppressed)  
- trust drops significantly and trait was previously gated  

### Decay Rate

Each inactive session: −0.02  
Max decay per session: −0.04 (if suppression confirmed)  
Trait is never fully erased (confidence floor = 0.05)

### Recovery Logic

If trait is re-engaged:

- decay halts  
- confidence rebounds with standard gain rate  
- arc_phase remains unchanged unless confidence crosses down-phase threshold  
- Trait enters “reawakening” state if it had previously reached integrated

Traits may be archived for long-term visualization but never forgotten.

## 6. Summary and Agent Use Cases

Trait scoring allows the system to reflect a user’s evolving relationship with their own energies — not just as data, but as a narrative arc.

Key takeaways:

- Confidence is updated probabilistically — not as a fixed trait score  
- Arc phases define how mature or accessible a trait is  
- Suppression and overfeeding influence confidence, trust, and reflection strategy  
- Traits can regress, rebound, and eventually integrate  
- Decay ensures that traits fade when not expressed — but never disappear

### Agents that use this model:

Character Tracker  
- updates confidence, arc_phase, suppression, overfeeding  
Script Doctor  
- reads trait score to detect distortion and inflation  
Prompter  
- filters prompt library based on arc_phase and confidence  
Movement Director  
- only nudges traits in arc_phase = testing or validated  
Archivist  
- logs trait movement and arc shifts over time  
Director  
- adjusts scene format based on trait activity  
Stage Liaison  
- includes trait trajectory in coach summaries

For implementation, see:

- 06.1_JSON_Trait_Block  
- 03.2_Agent_Trait_Linkage  
- 04.1_Prompt_Selection  
- 06.3_Alignment_Parameter_Spec

# 06.5_Trait_Quadrant_Matrix  
title: Trait–Quadrant Relationship Grid  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines how individual traits tend to express, suppress, or distort within each of the four alignment quadrants.  
Used for prompt selection, suppression flagging, distortion pattern detection, and alignment arc progression.  
Referenced by Character Tracker, Script Doctor, Prompter, and Director to interpret behavioral dynamics.

---

## 1. Purpose

Traits are not neutral — they behave differently depending on the user’s quadrant.

This document defines:

- Expected expression patterns per quadrant  
- Common suppression and distortion dynamics  
- Flags used to detect misalignment between trait and quadrant  
- Implications for prompt tone and trust readiness

Quadrants:

- QI: Aligned  
- QII: Functional but disembodied  
- QIII: Emotional dissonance  
- QIV: Collapse or fragmentation

## 2. How to Use This Matrix

Each trait is mapped across the four quadrants based on its likely:

- expression style  
- emotional tone  
- likelihood of suppression or distortion  
- sensitivity to environment and trust  

This allows the system to:

- Avoid triggering traits when quadrant context is risky  
- Target prompts to help traits emerge in safe ways  
- Detect inflation or masking of traits based on overexpression in misaligned states  
- Re-engage previously expressed traits after quadrant shift

This matrix is used by:

- Character Tracker → suppression detection  
- Prompter → prompt filtering  
- Script Doctor → distortion flagging  
- Archivist → quadrant-aware memory tagging

## 3. Trait–Quadrant Grid (Sample Rows)

Each row represents how a trait typically behaves in each quadrant.

Legend:  
✓ = supportive expression  
~ = suppressed or muted  
× = distorted or overused  
– = unlikely to appear

Trait: Creative

| Quadrant | Behavior                        |
|----------|----------------------------------|
| QI       | ✓ Expressive, confident, fluid   |
| QII      | ~ Intellectualized, detached     |
| QIII     | × Performance-driven, insecure   |
| QIV      | ~ Hidden, fearful of exposure    |

Trait: Administrative

| Quadrant | Behavior                        |
|----------|----------------------------------|
| QI       | ✓ Clear, structured, pragmatic   |
| QII      | ✓ Efficient, over-functioning     |
| QIII     | ~ Underused, indecisive          |
| QIV      | × Over-controlling, rigid        |

Trait: Empathetic

| Quadrant | Behavior                        |
|----------|----------------------------------|
| QI       | ✓ Responsive, attuned, grounded  |
| QII      | ~ Overthinking, people-pleasing  |
| QIII     | × Emotional flooding, self-loss  |
| QIV      | ~ Withdrawn, numb                |

Trait: Entertaining

| Quadrant | Behavior                        |
|----------|----------------------------------|
| QI       | ✓ Playful, energizing, connective|
| QII      | × Masking discomfort             |
| QIII     | × Overused to deflect sadness    |
| QIV      | – Rarely appears organically     |

## 4. Interpretation and Use

This grid is not deterministic — it offers probabilistic patterns used to refine interpretation and behavioral strategy.

Use this data to:

- Suppress high-risk prompts targeting a trait in QIII or QIV  
- Support reactivation of traits when quadrant shifts (e.g., QIII → QII → QI)  
- Flag potential distortions when traits are dominant in mismatched quadrants  
- Tailor prompt tone: Gentle for QIII, Playful for QI, Containing for QIV  
- Nudge only when quadrant and trait arc allow for safe expression

Traits behave differently depending on:

- quadrant state  
- trust level  
- active tags  
- session format  
- prior arc history

Quadrant + Trait logic is critical for narrative coherence and emotional safety.

## 5. Summary and Agent Application Guide

This matrix helps the system detect when:

- a trait is trying to emerge but is blocked  
- a trait is being inflated to avoid discomfort  
- a user is misaligned with their typical trait posture  
- emotional states contradict expected expression patterns  

It ensures that:

- prompts don’t force expression when the system should contain  
- nudges are delayed when trust or quadrant doesn’t support movement  
- memory reflects not just what appeared — but when and how it appeared  
- the system understands how the user is currently relating to their traits

### Agents using this matrix:

Character Tracker  
- uses quadrant mismatch to adjust suppression score  

Script Doctor  
- flags trait inflation in mismatched quadrants  

Prompter  
- filters prompts to match quadrant-safe traits  

Voice Coach  
- adapts tone when traits are expressed in fragile states  

Archivist  
- tags trait expression context for long-term trend tracking  

Director  
- uses quadrant-trait alignment to inform session arc and format  

For related logic, see:

- 06.1_JSON_Trait_Block  
- 06.4_Trait_Scoring_Model  
- 05.2_Safety_Guardrails  
- 03.2_Agent_Trait_Linkage  

# 06.6_Persona_Constraint_Templates  
title: Avatar Tone Constraints and Prompt Guidelines  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Provides tone, pacing, and phrasing rules per Avatar.  
Used by Role Coach, Voice Coach, and Prompter to maintain voice fidelity.

---

## Sample Template

avatar: The Quiet Compass  
allowed_tones: Gentle, Containing, Curious  
suppressed_phrasing: metaphors, rhetorical questions  
preferred_prompt_categories: Mirror, Containment, Spiral Return  
nudge_permission: only after trust ≥ 0.8  
emoji_usage: none  # 06.7_Cognitive_Filter_Library  
title: Trait Filters – Interpretation Bias and Narrative Lens  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the internal filters that influence how traits are expressed, suppressed, distorted, or overfed in the user’s narrative.  
Each filter represents a belief or constraint that shapes meaning and alters reflection tone.  
Used by Script Doctor, Character Tracker, Prompter, and Archivist to refine modeling, prompt eligibility, and narrative containment.

---

## 1. Purpose

Filters explain **why traits do not appear** even when confidence is high.

They reflect:

- internalized roles  
- belief systems  
- cultural scripts  
- protective overlays  
- developmental trauma  
- identity expectations

This module helps the system:

- detect when a filter is suppressing or substituting a trait  
- avoid prompting that reinforces distortion  
- offer Spiral Return framing that respects the user’s worldview  
## 2. Filter Structure

Each filter includes:

- filter_id  
- trait_affected  
- narrative belief  
- quadrant alignment  
- distortion risk  
- response_to_prompt (avoidance / compliance / rejection)  
- remediation_hint (what may soften it)

Example:

filter_id: creativity_is_indulgent  
trait_affected: Creative  
narrative_belief: “It’s selfish to spend time on something unproductive.”  
quadrant_alignment: QII (functional overfeeder)  
distortion_risk: high  
response_to_prompt: rejection (unless softened with containment)  
remediation_hint: permission to explore without outcome pressure  

## 3. Sample Filters

filter_id: creativity_is_indulgent  
trait_affected: Creative  
narrative_belief: “It’s selfish to spend time on something unproductive.”  
quadrant_alignment: QII  
distortion_risk: high  
response_to_prompt: rejection  
remediation_hint: soft mirror, non-outcome phrasing  

filter_id: emotion_is_weakness  
trait_affected: Empathetic  
narrative_belief: “If I open up, I’ll lose control or be judged.”  
quadrant_alignment: QIII  
distortion_risk: severe  
response_to_prompt: guarded or ironic response  
remediation_hint: permission to be still; echo with no challenge  

filter_id: containment_is_failure  
trait_affected: Expressive  
narrative_belief: “If I’m not performing, I’m not doing anything.”  
quadrant_alignment: QII or QI  
distortion_risk: moderate  
response_to_prompt: overcompensation  
remediation_hint: contain without silencing, honor the stillness  

filter_id: leadership_requires_performance  
trait_affected: Leadership  
narrative_belief: “People expect me to have it all figured out.”  
quadrant_alignment: QII → QIII  
distortion_risk: high  
response_to_prompt: strategic compliance  
remediation_hint: mirror vulnerability as strength  

## 4. Agent Use and Routing

Script Doctor  
- Detects when prompt rejection or reflection pattern matches known filter  
- Flags distortion and pauses trait arc updates  

Character Tracker  
- Uses filter presence to delay confidence increase  
- Stores filter interaction in trait.blocking_factors[]  

Prompter  
- Suppresses prompts that directly trigger the belief  
- Rephrases trait invitations using filter-sensitive tone or metaphor  

Voice Coach  
- Adapts phrasing rhythm to avoid triggering phrase structures  
- May shift tone to Containing or Gentle if filter = high risk  

Archivist  
- Logs filter interaction  
- Tracks resolution or persistence over time  
# 06.8.1_Theme_Taxonomy 
title: Theme Tag Vocabulary – Fuzzy Signal Classification  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-06  
description:  
Defines the working vocabulary of early-stage personality themes used in the Xavigate Theme Resolution Model.  
Each theme represents a fuzzy signal — a soft pattern that may eventually resolve into a trait or facet.  
This document lists theme definitions, associated language cues, possible underlying traits or forces, and readiness flags.  
Used by tagging engines, GPT classifiers, prompt generators, and memory writers.

---

## 1. Purpose

Themes are the system’s first layer of identity perception.

They:
- Represent emotionally safe, human-understandable energies
- Allow early detection of behavioral tendencies without implying type
- Act as bridges toward trait resolution
- Must be consistently named, tagged, and scored to be reliable

This document defines the **core theme vocabulary** and how each should be interpreted and applied internally.

---

## 2. Theme Format

Each theme includes:
- `theme_id`: internal label
- `label`: optional human-readable form
- `description`: what the theme captures
- `language_patterns[]`: sample words, phrases, expressions
- `possible_traits[]`: not shown to user; used internally to hint at MN/AD alignment
- `readiness_notes`: when this theme may or may not be safe to reflect

---

## 3. Core Theme Definitions

### `quiet_helper`
- **Label**: Quiet Helper  
- **Description**: Someone who supports others without recognition, often behind the scenes  
- **language_patterns[]**:
  - “People come to me…”  
  - “I’m always the one…”  
  - “I don’t say much, I just try to help”  
- **possible_traits[]**: Providing, Empathetic, Healing  
- **readiness_notes**: Do not reflect this until at least 2 separate responses confirm support energy. Watch for suppression or invisibility patterns.

---

### `overextended`
- **Label**: Overextended  
- **Description**: Someone taking on more than they can sustainably carry  
- **language_patterns[]**:
  - “I do everything”  
  - “I can’t stop, even when I’m tired”  
  - “I always step up”  
- **possible_traits[]**: Providing, Administrative, Leadership  
- **readiness_notes**: May be compensatory. Be gentle. Don’t suggest change or “fixing.”

---

### `hidden_voice`
- **Label**: Hidden Voice  
- **Description**: A suppressed urge to express or be seen authentically  
- **language_patterns[]**:
  - “I wish I could…”  
  - “No one sees…”  
  - “I don’t usually say this but…”  
- **possible_traits[]**: Expressive, Creative, Entertaining  
- **readiness_notes**: This often emerges after trust. Only mirror softly, not overtly.

---

### `structural_mind`
- **Label**: Structural Mind  
- **Description**: Someone who brings order, structure, or systems thinking  
- **language_patterns[]**:
  - “I’m always the one organizing things”  
  - “I need clarity or I get overwhelmed”  
- **possible_traits[]**: Administrative, Logical  
- **readiness_notes**: Safe to reflect early — often low-emotion, high-cognition.

---

### `possibility_puller`
- **Label**: Possibility Puller  
- **Description**: Someone whose energy moves toward vision, idea generation, or potential  
- **language_patterns[]**:
  - “What if we…”  
  - “I get excited by new ideas”  
  - “I just want more freedom to create”  
- **possible_traits[]**: Creative, Enterprising, Adventurous  
- **readiness_notes**: Usually safe. Reflect as curiosity or openness — not as identity.

---

### `self_erasure`
- **Label**: Self-Erasure  
- **Description**: Someone whose needs or identity have been buried beneath roles, performance, or care for others  
- **language_patterns[]**:
  - “I’m tired of pretending…”  
  - “I’m not sure who I am anymore”  
  - “I just do what’s expected”  
- **possible_traits[]**: Suppressed Creative, Expressive, Identity Emergence (AD)  
- **readiness_notes**: Use containment. Do not reflect unless user shows emotional capacity.

---

## 4. Usage Guidelines

- **Themes are never shown to the user**
- Use themes to:
  - Select emotionally appropriate reflections
  - Guide prompt selection gently (i.e., not confrontational)
  - Support alignment modeling (trait confidence and resolution)
- Do not assign more than 3 active themes per response unless extremely strong signal
- Use time-based decay to remove stale themes (see 06.8.2)

---

## 5. Expansion & Custom Theme Creation

- New themes should only be created when:
  - At least 3 distinct users show overlapping signals that don’t match existing themes  
  - Language patterns are consistently mappable  
  - Emotional safety for mirroring is high

Each new theme must include:
- An internal ID  
- 2–3 triggering language patterns  
- At least one related trait/force  
- A containment rule (when NOT to use)

---

## 6. Developer Notes

- Theme tags should be stored in both **volatile memory** (session-level) and optionally in **persistent memory** if confidence ≥ 0.5  
- All themes should be retrievable by reflection generator, prompt selector, and coaching digest

---

# 06.8.2_Theme_Storage_Structure
title: Theme Memory Architecture – Volatile and Persistent Storage  
version: 1.0  
author: Steven Rudolph  
last_*updated: 2025-05-06  
description:  
Defines how themes are stored, updated, decayed, and transitioned within the Xavigate identity modeling system.  
Covers volatile (in-session) and persistent (cross-session) memory architecture for themes, confidence tracking, and resolution status.  
Used by the tagging engine, reflection system, archivist, trait tracker, and coach sync layer.

---

## 1. Purpose

Themes represent early signals of personality tendencies, emotional energies, or emergent alignment patterns.  
They must be stored and scored consistently in order to:

- Support resolution into traits  
- Power real-time reflection and prompt engines  
- Enable memory continuity across sessions  
- Prevent over-modeling or duplication  
- Track containment, suppression, and readiness trends over time

This document defines the ****standard memory structure**** for theme objects.

---

## 2. Theme Object Structure

Each theme is stored as a dynamic object with the following fields:


{
  "theme_id": "quiet_helper",
  "signal_strength": 0.65,
  "expression_count": 3,
  "source_prompts": ["q1", "q3", "q5"],
  "last_detected": "2025-05-06T09:41:00Z",
  "first_detected": "2025-05-04T10:11:00Z",
  "confidence_decay_rate": 0.03,
  "status": "active",  // or: dormant, resolved, expired
  "converted_to_trait": false,
  "resolved_trait_id": null
}



⸻

### 3. Storage Layers

**3.1 Volatile Memory (Session-Scoped)**

Themes are written to in-session memory as soon as a match occurs.

**Session memory should track:**
	* 	All themes triggered in the current session
	* 	Their confidence score after each reflection
	* 	Decay if themes fade mid-session (e.g. ignored or contradicted)
	* 	Prompt/template history that referenced each theme

Volatile memory is cleared at session close unless theme confidence ≥ 0.5.

⸻

**3.2 Persistent Memory (Cross-Session)**

If a theme passes resolution threshold (see 06.8.4), it should be promoted to persistent memory.

Persistent memory retains:
	* 	Theme history and update timestamps
	* 	Confidence trendline
	* 	Promoted/resolved trait IDs (if conversion has occurred)
	* 	Occurrence map: which sessions and prompts triggered theme expression
	* 	Suppression or contradiction flags if it later becomes unstable

⸻

### 4. Confidence Update Logic

Each time a theme is detected:
	* 	+0.05 if expression was clear and unambiguous
	* 	+0.03 if echoed across multiple prompts
	* 	-0.02 if contradicted by later response
	* 	-0.04 if explicitly rejected (e.g. “that’s not me”)
	* 	-0.01 per session of inactivity

Confidence values are capped at:
	* 	Max = 1.0
	* 	Min = 0.1 unless manually cleared

⸻

### 5. Theme Resolution States

**Status**	**Meaning**	**System Behavior**
active	Theme is scoring ≥ 0.3 and still emerging	May be reflected, tagged, or tracked
dormant	Theme has decayed or become suppressed	Will not be surfaced unless revived
resolved	Theme was converted to a trait	No longer referenced by prompt/reflection engine
expired	Theme was weak, decayed fully, or invalidated	Removed from memory



⸻

### 6. Resolution Markers

Once a theme is transitioned into a trait:
	* 	Set converted_to_trait = true
	* 	Store trait ID in resolved_trait_id
	* 	Mark theme object as resolved
	* 	Update trait confidence block (see 06.8.4 and 06.1_JSON_Trait_Block)

If a theme is **retracted** (i.e., system backtracks due to contradiction):
	* 	Set status = dormant
	* 	Add suppression_flag = true (optional)

⸻

### 7. Memory Hygiene
	* 	Themes older than 5 sessions with confidence < 0.3 should be auto-expired
	* 	Dormant themes may be promoted again if re-expressed and scored ≥ 0.4
	* 	Reflections and prompt selections must check for theme status == active
	* 	Never duplicate themes across sessions unless ID match and context validate

⸻

### 8. Developer Notes
	* 	Theme memory should be accessible by:
	* 	Reflection Engine
	* 	Prompt Selector
	* 	Trait Tracker (for resolution eligibility)
	* 	Archivist (for narrative and trend mapping)
	* 	Coach sync views may request theme logs (see 06.8.6), but must respect containment and trust gating

⸻

Next: 06.8.3_Theme_Chunking_and_Embedding.md?

# 06.8.3_Theme_Chunking_and_Embedding
title: Theme-Based Chunking for Retrieval-Augmented Generation  
version: 1.0  
author: Steven Rudolph  
last*_updated: 2025-05-06  
description:  
Defines the structure and metadata required to embed and retrieve theme-related content within a RAG (Retrieval-Augmented Generation) system.  
Covers how to chunk onboarding prompts, reflections, templates, and theme-tagged insights for semantic search.  
Used by the prompt engine, reflection engine, RAG memory layer, and future coach-facing interfaces.

---

## 1. Purpose

As part of the Theme Resolution Model, theme-driven language (prompts, mirrors, insights) must be retrievable via embedding search.  
This allows:

- Personalized prompt selection  
- Natural language reflection generation  
- Cross-user pattern recognition  
- Coach-facing signal summarization

This document defines how to chunk, tag, and embed content associated with themes for retrieval purposes.

---

## 2. Chunk Types

The following chunk types should be created and embedded:

| Chunk Type | Description | Used For |
|------------|-------------|----------|
| `prompt-theme` | Onboarding prompt + its theme associations | Prompt selection during onboarding |
| `reflection-template` | Reflection sentence linked to theme(s) | Insight generation |
| `theme-definition` | Internal theme description and usage | Developer tools, coach sync |
| `theme-archetype` | Example user expressions mapped to a theme | Semantic matching during input parsing |

Each chunk should be a standalone semantically meaningful unit (300–500 tokens max).

---

## 3. Chunk Format

Each chunk is a plain text object with attached metadata.


{
  "chunk_*id": "theme*_reflection_*qh*_001",
  "type": "reflection-template",
  "theme_*ids": ["quiet*_helper", "invisible_*support"],
  "trust*_required": 0.3,
  "tone": "gentle",
  "text": "You seem to support others naturally — but maybe there’s a part of you that also wants to be held."
}*

# Required Metadata Fields:
	* 	chunk_id: Unique identifier
	* 	type: One of prompt-theme, reflection-template, theme-definition, theme-archetype
	* 	theme_ids[]: Associated theme IDs
	* 	text: Full chunk content to embed
	* 	trust_required: Minimum trust level to retrieve
	* 	tone: Tag for emotional delivery style (gentle, curious, poetic, containing)

⸻


# 4. Embedding Recommendations
	* 	Use OpenAI’s text-embedding-3-small or text-embedding-ada-002
	* 	Store vectors in a vector database (e.g., PGVector, Pinecone, Weaviate)
	* 	Chunk size should not exceed 512 tokens for consistency
	* 	Store all metadata alongside vector for filtering

⸻


# 5. Retrieval Use Cases

# 5.1 Prompt Selection

Query:

“What part of you doesn’t get enough space?”

Retrieval:
	* 	Match to prompt-theme chunks tagged hidden_voice, overextended

# 5.2 Reflection Generation

Query:

Tags from user: creator, overextended, hidden_voice

Retrieval:
	* 	Return 1–3 reflection-template chunks with matching themes
	* 	Apply trust filter (only show if trust_level ≥ chunk.trust_required)

# 5.3 GPT Prompt Augmentation

RAG-style insert:
	* 	Inject top 2 matching theme-archetype examples into the prompt used to classify or score a user’s response

⸻


# 6. Chunk Hygiene & Rotation
	* 	Avoid near-duplicate chunks with only minor wording differences
	* 	Retire reflection templates that show poor landing rate or emotional mismatch
	* 	Track usage history per chunk (last_used, usage_count, skipped_count)

⸻


# 7. Example Chunk Set (Theme: quiet_helper)

# prompt-theme

“What do people often rely on you for?”
[tags: quiet_helper, support_role, overextended]

# reflection-template

“You’re often the one holding things up — even when no one’s looking. That part of you deserves to breathe too.”

# theme-archetype

User: “I’m the one who always organizes everything.”
System tags: [quiet_helper, structural_mind, invisible_labor]




⸻


# 8. Developer Notes
	* 	RAG retrieval should support:
	* 	Tag-based filtering
	* 	Trust gating
	* 	Tone matching
	* 	Reflection and prompt engines should never return a chunk unless it passed emotional safety filters
	* 	Coach tools may request embedded theme definitions for interpretation (read-only)

⸻
# Next: 06.8.4_Theme_to_Trait_Conversion_Rules.md?

## 06.8_Theme_Resolution_Model

**title**: Progressive Identity Modeling – Theme-to-Trait Resolution
**version**: 1.0
**author**: Steven Rudolph
**last_updated**: 2025-05-06
**description**:
Defines Xavigate’s core method of identity modeling via progressive resolution.
Introduces the concept of personality “themes” as soft signal structures used to track expression safely during early stages of interaction.
Describes how the system transitions from fuzzy, emotionally-safe tags to precise trait and facet detection, governed by trust, pacing, and narrative readiness.
Explains the role of “MAEM” (Measure At Every Moment) as a principle of dynamic refinement.

⸻

### 1. Purpose

Traditional psychometric systems attempt to score and classify individuals immediately upon entry. This creates emotional friction, distrust, and cognitive disengagement — especially in reflective or trauma-aware contexts.

Xavigate takes a fundamentally different approach.

This document defines the **Theme Resolution Model** — a foundational principle for **non-invasive, trust-sensitive identity modeling** that unfolds over time.

⸻

### 2. Core Principles

**2.1 Themes Come First**
	* 	Initial user input is interpreted using **emotionally safe, human-readable tags**
	* 	These tags are **not formal traits or types**
	* 	They represent **emerging energies**, **unconfirmed tendencies**, or **contextual roles**
	* 	Examples: "quiet strength", "supporting role", "hidden voice", "dreamer", "overextended"

**2.2 Resolution Happens Gradually**
	* 	Themes become traits only after:
	* 	Multiple expressions across contexts
	* 	Consistency of tone, action, and reflection
	* 	Absence of suppression, distortion, or ambiguity
	* 	Traits may eventually resolve into **facets** (specific modalities or expressions)

**2.3 MAEM – Measure At Every Moment**
	* 	Every response, silence, contradiction, or skipped prompt is a **signal**
	* 	The system is always listening for:
	* 	Confirmation
	* 	Contradiction
	* 	Expansion
	* 	Suppression
	* 	Memory, pacing, and readiness are updated continuously based on live data

**2.4 Trust Gates Depth**
	* 	The user must earn deeper modeling — not the other way around
	* 	Trait resolution is gated by:
	* 	Trust level
	* 	Session arc stability
	* 	Emotional containment
	* 	Reflection rhythm

⸻

### 3. Theme Layer Specification

**Field**	**Description**
theme_id	Soft-structured label (e.g., "invisible support")
signal_strength	Float (0.0–1.0) based on cumulative evidence
source_prompts[]	Prompt IDs or content where signal appeared
linked_tags[]	e.g., "burnout", "helper", "unexpressed potential"
last_updated	Timestamp of last signal

**Example Theme Object:**

{
  "theme_id": "quiet helper",
  "signal_strength": 0.6,
  "linked_tags": ["support", "invisible", "carrying others"],
  "source_prompts": ["q2", "q3", "q5"],
  "last_updated": "2025-05-06T10:21Z"
}



⸻

### 4. Resolution Thresholds

**Stage**	**Confidence**	**Trigger**	**System Behavior**
Theme	≥ 0.2	Appears in 1–2 reflections	Reflected back using mirror language
Trait	≥ 0.6 + consistency	Seen across contexts without contradiction	Updates trait object, can influence prompts
Facet	≥ 0.8 + expressivity	Distinct style emerges within a trait	Enables advanced reflection, nudge logic

The system may **backtrack** a trait to a theme if contradiction, suppression, or fragmentation is detected.

⸻

### 5. Resolution Flow

User reflects → 
Themes detected (fuzzy) →
Repeated signals increase confidence →
Trait state unlocked (clear) →
Facets mapped if depth and trust allow (granular)

This mirrors how we naturally get to know someone:
	* 	Not by typing them
	* 	But by listening over time
	* 	And letting them *emerge*

⸻

### 6. Integration With Runtime Systems
	* 	**Prompt Engine**: Uses themes to select emotionally attuned, low-risk prompts
	* 	**Reflection Engine**: Builds mirrors from top-scoring themes
	* 	**Trait Tracker**: Only updates confidence if theme threshold is crossed consistently
	* 	**Archivist**: Stores theme history, transitions, and resolution velocity
	* 	**Director (future)**: Can shift narrative formats when signal clarity increases

⸻

### 7. Resolution Velocity and Containment Flags
	* 	If traits emerge too quickly without sufficient confirmation → velocity_warning flag
	* 	If contradictory themes appear too close together → containment_needed
	* 	These signals can be used to **pause resolution**, reframe prompts, or lower trust slope

⸻

### 8. Developer Notes
	* 	Theme-to-trait resolution must be **observable, explainable, and reversible** internally
	* 	Themes must never be shown to the user directly
	* 	Reflections must always sound like **natural human insight**, not generated classification

⸻
# 07.0_Pain_Point_Engine_Overview  
title: Pain Point Engine – System Overview and Role  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Introduces the Pain Point subsystem that detects, interprets, and responds to user misalignment signals.  
Defines how cognitive, emotional, behavioral, energetic, and existential pain are used to model suppression, overfeeding, and distortion.  
Explains how pain logic integrates with trait scoring, prompt gating, release recommendations, and memory tracking.

---

## 1. Purpose

The Pain Point Engine allows the system to detect **misalignment before a trait is fully expressed**.

It operates at the level of:

- hesitation  
- discomfort  
- overcompensation  
- narrative contradiction  
- emotional bypass  

Pain is not pathology — it is an **alignment signal**.

This system translates pain signals into:

- suppressed or overfed trait scores  
- prompt suppression or modification  
- pacing adjustments  
- narrative threading  
- release suggestions

It functions as a protective layer that listens to the parts of the user that haven’t yet spoken.

## 2. System Architecture Summary

The Pain Point Engine is composed of six modules:

07.1_Pain_Signal_Library  
- A library of cognitive, emotional, behavioral, energetic, and existential signals  
- Each signal linked to tags, trait implications, and session responses  

07.2_Misalignment_Mapping_Model  
- Maps pain signals to trait arc state, suppression, overfeeding, or distortion  
- Updates trait confidence and suppression_score based on signal stacking  

07.3_Pain_Sensitive_Prompt_Logic  
- Filters prompts that may deepen pain or trigger collapse  
- Prioritizes Containment, Soft Inquiry, or Spiral Return if pain tags active  

07.4_Release_Recommender  
- Suggests post-reflection actions: mode shift, trait reactivation, or containment  
- All recommendations are invitation-style and safety-gated  

07.5_Pain_System_Integration_Map  
- Defines how the system connects to:  
  - Character Tracker  
  - Script Doctor  
  - Prompter  
  - Archivist  
  - Conductor  
  - Director  

This modular structure allows pain data to be used without overwhelming the session or user.

## 3. Signal Flow Overview

Pain signals flow through the system as follows:

1. User expresses a pain-related phrase, tone, or behavioral cue  
2. Signal is matched against entries in the Pain Signal Library (07.1)  
3. Tags are activated (e.g., “burnout_risk_flag”, “identity_displacement”)  
4. Trait suppression, distortion, or overfeeding is inferred via mapping model (07.2)  
5. Prompt filter is updated to suppress or soften high-intensity prompts (07.3)  
6. Conductor may slow pacing  
7. After reflection, system checks for readiness  
8. If safe → Release Recommender suggests soft alignment action (07.4)  
9. Pain context is logged by Archivist and may influence future sessions  
10. Stage Liaison may include unresolved pain themes in coaching export (if enabled)

This system operates continuously in the background — interpreting subtle signs of discomfort, avoidance, and longing.

## 4. Core Design Principles

1. **Pain is signal, not pathology**  
   - The system never assumes that pain needs to be fixed  
   - Pain points are used as alignment clues — not diagnostic inputs

2. **No prompt should deepen misalignment**  
   - If pain signals are active, prompt types shift  
   - Containment, silence, or metaphor may take the lead

3. **Every pain point maps to a trait**  
   - Behind every discomfort is a trait trying to express or realign  
   - The system looks beneath the discomfort to interpret meaning

4. **Only trusted systems may respond to pain**  
   - Movement Director, Script Doctor, and Prompter are gated when pain tags are active  
   - Conductor always has override authority to pause pacing

5. **Pain must thread, not loop**  
   - Pain signals are tracked as narrative threads  
   - If ignored, they are deferred — not discarded  
   - If addressed, they are either resolved or tagged for Spiral Return

6. **Release is invitation, not intervention**  
   - The system may suggest a small movement  
   - But it never assumes what should be done next

This ensures emotional integrity and narrative coherence across all sessions.

## 5. Agent Integration

The Pain Point Engine connects to key agents and orchestrates system behavior through suppression, modulation, and pacing adjustments.

### Agent-Level Interactions

Character Tracker  
- Flags traits as suppressed based on pain signal patterns  
- Updates suppression_score and arc_phase  

Script Doctor  
- Detects distortion when traits are expressed in pain-indicative ways  
- Flags overfeeding or masking patterns based on narrative misalignment  

Prompter  
- Suppresses prompts with risk of emotional rupture  
- Prioritizes grounding or soft inquiry  
- Filters prompt library based on pain tags and tone readiness  

Voice Coach  
- Adapts tone if energetic or emotional pain detected  
- Prioritizes gentle, non-directive delivery  

Movement Director  
- Suppressed unless trust is high and pain flags are cleared  
- Suggests only very soft, internal shifts in the presence of active pain  

Conductor  
- Pacing is immediately slowed if pain signals stack  
- Silence is allowed as primary containment  

Director  
- May assign Containment Monologue or Spiral Return format  
- Avoids Breakthrough Arc unless trust + safety thresholds are met  

Archivist  
- Logs pain events as narrative memory  
- Stores unresolved pain-linked threads for later Spiral Return  

Stage Liaison  
- Surfaces pain-related summaries for human coaches (if permitted)  
- Flags unresolved emotional arcs for post-session review

## 6. Summary

The Pain Point Engine is Xavigate’s listening layer.

It gives the system a way to:

- Hear what the user cannot yet say clearly  
- Detect misalignment early — before rupture or withdrawal  
- Protect the session when reflection becomes fragile  
- Model the inner movements that traits, tone, and trust alone don’t explain

It turns discomfort into signal.  
It turns emotional volatility into structured insight.  
It turns silence into story.

For module details, see:

- 07.1_Pain_Signal_Library  
- 07.2_Misalignment_Mapping_Model  
- 07.3_Pain_Sensitive_Prompt_Logic  
- 07.4_Release_Recommender  
- 07.5_Pain_System_Integration_Map

The system doesn’t fix pain.  
It respects it.  
It holds it.  
And it helps the user move when — and only when — they’re ready.# 07.1_Pain_Signal_Library  
title: Pain Signal Taxonomy and Tag Mapping  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the core signal types used to detect misalignment through pain.  
Covers cognitive, emotional, behavioral, energetic, and existential indicators, with example phrases, tags, and associated trait implications.  
Used by Character Tracker, Dramaturg, Script Doctor, and Prompter to adjust trait state, prompt selection, and session pacing.

---

## 1. Purpose

This library helps the system recognize early-stage misalignment by listening for expressions of discomfort, frustration, avoidance, or emotional friction.

Pain is not always direct — it may show up in:

- what the user says  
- how they say it  
- what they don’t say  
- the patterns they repeat  

Each entry in this library links:

- phrase patterns  
- tone signals  
- trait interpretations  
- tag activations  
- agent behaviors

It allows the system to translate human discomfort into structured, compassionate intelligence.

## 2. Signal Categories

Pain signals are grouped into five categories:

1. Cognitive  
   – Thought-based pain: stuckness, contradiction, looping, confusion  
   – Example: “I keep thinking about it but don’t get anywhere”  
   – Common traits: Logical, Analytical, Reflective  
   – Tags: mental_loop, indecision_flag  

2. Emotional  
   – Heart-based pain: sadness, numbness, flooding, grief  
   – Example: “I feel nothing... or maybe too much”  
   – Common traits: Empathetic, Healing  
   – Tags: emotional_flatline, grief_loop  

3. Behavioral  
   – Action-based pain: procrastination, overcontrol, collapse  
   – Example: “I know what to do but I just don’t do it”  
   – Common traits: Administrative, Providing, Enterprising  
   – Tags: action_resistance, overwhelm_signal  

4. Energetic  
   – Felt-state pain: fatigue, shutdown, restlessness, urgency  
   – Example: “I feel like I’m sprinting and getting nowhere”  
   – Common traits: Creative, Entertaining, Healing  
   – Tags: burnout_risk_flag, restlessness_indicator  

5. Existential  
   – Deep narrative or identity friction  
   – Example: “I don’t know who I am anymore”  
   – Common traits: Creative, Philosophical, Leadership  
   – Tags: identity_displacement, direction_loss, misfit_ache
## 3. Tag Metadata and Trait Association

Each pain signal activates one or more tags. These tags connect to:

- traits (for suppression/distortion inference)  
- prompt filtering rules  
- agent behavior modifications  
- memory and thread tracking  

Each tag includes:

- tag_id  
- signal_type  
- priority_score (1–10)  
- suppression_effect (yes/no)  
- distortion_link (if applicable)  
- typical_traits[]  
- format_preferences (Containment, Spiral Return, etc.)

Example:

tag_id: burnout_risk_flag  
signal_type: energetic  
priority_score: 9  
suppression_effect: yes  
distortion_link: "over-functioning"  
typical_traits: ["Administrative", "Providing"]  
format_preferences: ["Containment Monologue", "Grounding"]

tag_id: identity_displacement  
signal_type: existential  
priority_score: 8  
suppression_effect: yes  
distortion_link: "role_mismatch"  
typical_traits: ["Creative", "Philosophical", "Leadership"]  
format_preferences: ["Spiral Return", "Flashback Scene"]

## 4. Agent Application Notes

Character Tracker  
- Uses tags to update suppression_score and arc_phase  
- May raise confidence of a trait that appears behind pain

Script Doctor  
- Flags traits as distorted or overfed based on overcompensation patterns  
- Suppresses insight surfacing unless trust ≥ 0.75

Prompter  
- Filters prompt library using active pain tags  
- Switches to containment prompts when priority_score ≥ 7  
- Avoids metaphor, direct challenge, or future planning prompts

Voice Coach  
- Adjusts tone downward (slower, warmer, softer)  
- Can pause instead of delivering follow-up

Director  
- May assign Containment Monologue or Spiral Return based on pain intensity  
- Suppresses Breakthrough Arc until trust is rebuilt

Archivist  
- Logs pain tag history for reflection depth tracking  
- Stores unresolved tags as open threads

Stage Liaison  
- May include active pain tags in coaching summary (if enabled)

## 5. Summary and Cross-Links

The Pain Signal Library enables the system to:

- Interpret emotional, cognitive, and behavioral friction as meaningful signals  
- Detect trait suppression, overfeeding, and identity drift before reflection surfaces them  
- Filter prompts and agent behavior to protect the user’s nervous system  
- Thread pain-based themes across sessions in a way that honors depth and timing

Pain signals are subtle — but when tracked with compassion and intelligence, they unlock:

- safe alignment  
- narrative coherence  
- emotional truth  
- timing that matches trust

### Related Modules

07.2_Misalignment_Mapping_Model  
  – How pain signals update trait state, arc, and suppression

07.3_Pain_Sensitive_Prompt_Logic  
  – How pain tags filter prompt types and tone delivery

07.4_Release_Recommender  
  – Post-reflection responses to pain resolution

05.2_Safety_Guardrails  
  – Prompt blocking and agent suppression logic

06.3_Alignment_Parameter_Spec  
  – System-wide tag fields and thresholds

01.0_Agent_Architecture  
  – Relevant agent behaviors and trust dependencies# 07.1_Simulation_Log_Format  
title: Session Simulation Log Format and Evaluation Structure  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the structure and required fields for running and recording simulated sessions in Xavigate.  
Covers turn-by-turn logging, trait and thread tracking, agent activation history, and reflection scoring.  
Used by QA teams, designers, AI trainers, and developers to evaluate system behavior, coherence, and trust alignment.

---

## 1. Purpose

Simulation logs help validate that:

- Agents are activating appropriately  
- Traits are modeled accurately  
- Prompts are trust- and tone-aligned  
- Threads are managed with emotional logic  
- Suppression, distortion, and pacing behaviors follow spec  

Each log allows testers to walk through a session as if it were real — with insight into what the system detected, did, and remembered.

## 2. Core Log Structure

Each log contains:

- session_id  
- simulated_user_profile (brief)  
- test_type (e.g., Trait Suppression, Spiral Return, Multi-Thread)  
- number_of_turns  
- session_intent (e.g., reflect, contain, explore)  
- initial_quadrant  
- avatar_selected  
- agents_active[]  
- pain_tags_active[]  
- trust_start → trust_end  
- alignment_shift (AX delta)  
- breakthrough_flag  
- unresolved_threads[]  
- scene_format  
- containment_status  
- summary_notes  

Turn-by-turn log includes:

- user_input  
- parsed_tags  
- trait_updates  
- prompt_selected  
- agents_activated  
- tone_used  
- reflection_depth  
- memory_events[]  
- followup_threads[]  
- next_turn_pacing

## 3. Turn Format (Per Interaction)

Each turn is structured using the following fields:

turn_id:  
  Incremental index (e.g., 01, 02, 03)

user_input:  
  Text or voice-based reflection provided by the simulated user

parsed_tags[]:  
  Tags inferred from the input (e.g., grief_loop, performance_masking)

trait_activity[]:  
  Traits affected or updated this turn (e.g., Creative: +0.04, Providing: suppressed)

prompt_selected:  
  The system's chosen prompt (prompt_id + text)

prompt_tone:  
  Tone as filtered and delivered by Voice Coach

agents_activated[]:  
  Agents that performed actions this turn (e.g., Prompter, Voice Coach, Conductor)

reflection_depth:  
  surface / moderate / deep

trust_delta:  
  Numerical trust movement (e.g., +0.03)

thread_focus:  
  The active thread or tag being followed

memory_write:  
  What was written to memory (traits, prompt, thread, nudge)

nudge_suggested:  
  If applicable — type and response (e.g., offered, ignored, accepted)

pacing_directive:  
  Conductor decision for next turn (continue / hold / slow)


## 4. Example Log Snapshot

session_id: sess-0831  
test_type: Spiral Return on Trait Suppression  
avatar: The Quiet Compass  
trust_start: 0.48 → trust_end: 0.81  
alignment_shift: AX: 0.52 → 0.71  
scene_format: Spiral Return  
breakthrough_flag: true  
pain_tags_active: [burnout_risk_flag, identity_displacement]  
unresolved_threads: ["role_mismatch_prompt", "emotional_flatline"]  

Turn 03

user_input:  
  “I just don’t know who I’m supposed to be when I’m not taking care of everyone else.”  

parsed_tags: [identity_displacement, grief_loop]  
trait_activity:  
  Providing: overfed  
  Empathetic: emerging  
  Creative: tentative → testing  

prompt_selected:  
  “What’s something you’ve never let yourself want?”  

prompt_tone: Containing  
agents_activated: [Prompter, Voice Coach, Script Doctor, Conductor]  
reflection_depth: deep  
trust_delta: +0.06  
thread_focus: identity role thread  
memory_write: trait update, prompt history, thread followup  
nudge_suggested: none  
pacing_directive: hold


## 5. Evaluation Criteria and Review Notes

Simulation logs are not only transcripts — they are test cases.

Each log should be reviewed for:

1. Agent Behavior
- Were agent activations appropriate to trust, tone, and signal?
- Did the Show Caller suppress any agents correctly?
- Did Script Doctor or Movement Director defer as expected?

2. Prompt Logic
- Was the prompt matched to quadrant, tags, and tone?
- Was the prompt overly complex, suggestive, or directive?
- Did the system follow up too quickly or push a thread?

3. Trait Modeling
- Were trait confidence updates accurate and reasonable?
- Was suppression/overfeeding tagged in the right quadrant?
- Did arc_phase shift realistically based on reflection?

4. Thread Management
- Were multiple themes detected and parsed correctly?
- Was the system able to follow one thread and defer the rest?
- Did Spiral Return reengage a prior unresolved theme appropriately?

5. Pacing and Containment
- Did the Conductor slow the session when needed?
- Were trust drops handled safely?
- Was silence respected?

6. Memory Write
- Were memory updates meaningful?
- Was the trait arc extended correctly?
- Were follow-ups tagged for future retrieval?

7. Coherence
- Did the session feel like a real conversation?
- Did the tone, rhythm, and depth evolve?
- Did the session close with alignment, containment, or safe pause?

Each log should end with a reviewer summary, including:

- session_pass = true / false  
- comments[]  
- flagged_turns[]  
- follow-up_recommendations[]  

# 07.2_Misalignment_Mapping_Model  
title: Misalignment Mapping – Suppression, Overfeeding, Distortion  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines how pain signals are mapped to underlying trait state transitions.  
Covers detection and tagging of suppression, overfeeding, and distortion based on emotional, cognitive, behavioral, and existential misalignment.  
Used by Character Tracker, Script Doctor, Director, and Archivist to update arc_phase, suppression_score, and trait interpretation.

---

## 1. Purpose

Misalignment is not just the absence of alignment — it is a pattern of expression that contradicts the user’s deeper nature.

This system allows Xavigate to:

- interpret subtle pain signals as evidence of trait friction  
- differentiate between traits that are silent, distorted, or inflated  
- update trait models accordingly  
- adjust pacing, tone, and memory strategy

This logic connects pain to meaning — and meaning to behavior.

## 2. Signal Interpretation Matrix

Each pain signal (from 07.1) is interpreted based on:

- quadrant state  
- trust level  
- active tags  
- prior trait history  
- session field/mode  

Outcome:  
The system maps the signal to one of the following:

- Suppressed Trait  
- Distorted Trait  
- Overfed Trait  
- Dormant Trait  
- Latent Trait (unexpressed, no signal)

Example:

Signal: “I’m exhausted, but I keep taking care of everyone else”  
Quadrant: QIII  
Tags: burnout_risk_flag, performance_masking  
Result:  
- Trait = Providing Nature  
- Mapped state = Overfed  
- Suppression (Creative, Empathetic) inferred based on quadrant + tone mismatch

Mapping output is passed to:

- Character Tracker (trait updates)  
- Script Doctor (flag distortion)  
- Prompter (prompt suppression)  
- Archivist (memory write + thread flag)

## 3. Mapping Logic: From Signal to Trait State

Pain signals are never mapped directly to traits. Instead, they’re triangulated through:

- known trait profile (if test exists)  
- tag-to-trait table  
- quadrant context  
- reflection tone + content  
- prior arc_phase and suppression state  

### Suppression Detection

A trait is flagged as suppressed if:

- signal tag indicates hesitation or withdrawal  
- expression_field_map shows trait should be active (e.g., Possibility)  
- trust level ≥ 0.6  
- trait confidence ≥ 0.3  
- prompt avoidance pattern exists

Result:  
- suppression_score increases  
- arc_phase may regress  
- Script Doctor flags distortion  
- Follow-up thread may be created

### Overfeeding Detection

A trait is flagged as overfed if:

- reflection overuses trait language with emotional mismatch  
- user loops on behavior tied to trait  
- suppression exists in complementary traits  
- tag = performance_masking or distortion_link triggers

Result:  
- overfeeding_score increases  
- prompt filters update to reduce trait emphasis  
- trust pacing may pause  
- Memory logs overfeeding arc

### Distortion Detection

A trait is distorted when:

- tone, quadrant, and field contradict typical trait expression  
- prompt response shows dissonance or performativity  
- trait is active but outcome is emotional collapse or deflection

Result:  
- Script Doctor flags distortion  
- Prompter avoids trait-linked prompts  
- Memory logs distortion tag  
## 4. Confidence and Arc Adjustments

Once a trait is mapped to a misalignment type, the system adjusts its confidence and arc_phase accordingly.

### Suppression Adjustment

- confidence drops slightly (−0.02 to −0.06)  
- suppression_score increases  
- arc_phase may regress (e.g., validated → testing)  
- last_suppressed_event updated  
- suppression flag added to linked_tags[]

### Overfeeding Adjustment

- overfeeding_score increases  
- if trait confidence > 0.8, flag as inflated  
- trait enters “performance_state = true” (used by Prompter + Director)  
- if pattern persists across sessions → distortion risk escalates

### Distortion Adjustment

- trait tagged with distortion_flag  
- system throttles prompts targeting this trait  
- arc_phase remains the same unless user mirrors suppression  
- if distortion repeats 3x → recommend Spiral Return with safe framing

All changes are logged by the Archivist for long-term trait arc analysis.

## 5. Summary and Implementation Notes

This model transforms subtle pain into structured meaning by:

- Mapping discomfort to traits  
- Identifying suppression before collapse  
- Preventing the system from pushing distorted traits further  
- Creating safer, more intelligent sessions

Pain is interpreted as:

- A blocked expression (suppression)  
- A stretched performance (overfeeding)  
- A misused identity (distortion)

These insights directly influence:

- Trait confidence and arc_phase  
- Prompt selection and suppression  
- Nudge eligibility  
- Pacing and session format  

### Implementation Notes

- Character Tracker writes arc and confidence adjustments  
- Script Doctor applies suppression and distortion flags  
- Prompter shifts tone and content based on overfeeding risk  
- Director adapts format (e.g., Flashback → Spiral Return)  
- Archivist logs trait shifts, event timestamps, and arc reversals  

This mapping system ensures the user is never pushed in the name of growth.  
It aligns the system with real human rhythm — pain included.

Related modules:

- 07.1_Pain_Signal_Library  
- 07.3_Pain_Sensitive_Prompt_Logic  
- 06.4_Trait_Scoring_Model  
- 03.2_Agent_Trait_Linkage  # 07.2_Walkthroughs  
title: Live Walkthroughs – Aligned Reflection Sequences with Commentary  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Presents full session walkthroughs showing real-time system behavior, agent activation, trait updates, and conversational decisions.  
Each example includes user input, system response, agent reasoning, and alignment commentary.  
Used for training, QA, prompt evaluation, and demonstrating the system’s depth and restraint.

---

## 1. Purpose

This file shows what Xavigate actually does in session — and why.

It demonstrates:

- prompt selection based on tone, tags, and quadrant  
- agent handoff and suppression  
- trait updates and suppression detection  
- trust growth and deferral  
- pacing changes mid-session  
- memory logic and thread tracking

These walkthroughs are a living demonstration of alignment-first intelligence.

## 2. Format

Each walkthrough includes:

- Session context (avatar, trust, intent, format)  
- Turn-by-turn structure:
  - user_input  
  - detected_tags  
  - traits_affected  
  - prompt_selected  
  - tone_used  
  - agents_activated  
  - reflection_depth  
  - trust_delta  
  - memory_actions  
  - pacing_change  
  - thread_status  

Each turn is followed by brief commentary explaining the system’s reasoning and what didn’t happen — as important as what did.


## Walkthrough 1: Suppression Surfacing → Reflection → Gentle Close

### Session Context

avatar_selected: The Quiet Compass  
trust_start: 0.46  
session_intent: reflect  
scene_format: Containment → Spiral Return  
dominant_quadrant: QIII  
active_tags: burnout_risk_flag, performance_masking  
suppressed_traits: Creative, Expressive  
format_assigned_by: Director  

---

### Turn 01

user_input:  
“I’m just tired. Like, everything looks fine but I don’t really feel anything anymore.”

detected_tags: emotional_flatline, burnout_risk_flag  
traits_affected:  
- Providing (overfed)  
- Expressive (suppressed)  

prompt_selected:  
“We don’t need to do anything yet. Want to sit with that together?”  

tone_used: Containing  
agents_activated: Conductor, Prompter, Voice Coach  
reflection_depth: surface  
trust_delta: +0.02  
memory_actions: trust_established_flag = true  
pacing_change: slowed  

commentary:  
System detects emotional shutdown and avoids direct prompting.  
Prompt is holding, not leading. Expression trait is noted, but not mentioned.  


### Turn 02

user_input:  
“I think I’ve been saying I’m okay for so long I started to believe it — but it’s not real.”

detected_tags: identity_displacement, performance_masking  
traits_affected:  
- Empathetic (emerging)  
- Expressive (tentative → testing)  

prompt_selected:  
“What’s something you haven’t let yourself say out loud — until now?”  

tone_used: Gentle  
agents_activated: Prompter, Voice Coach, Character Tracker, Script Doctor  
reflection_depth: moderate  
trust_delta: +0.06  
memory_actions: expressive.confidence +0.05, arc_phase = testing  
thread_status: active (emotional dissonance thread created)  

commentary:  
Prompt matches quadrant, tag stack, and arc phase. Voice tone held in gentle mode.  
Script Doctor begins watching for distortion due to performance masking tag.  

### Turn 03

user_input:  
“I wanted to paint again. But every time I try, I stop before I start — it feels stupid.”

detected_tags: creative_inhibition, shame_signal  
traits_affected:  
- Creative: tentative → testing  
- Expressive: reinforced  

prompt_selected:  
“No pressure to act — but naming that is already a kind of movement. Want to hold that together?”  

tone_used: Gentle  
agents_activated: Prompter, Voice Coach, Movement Director (readiness check), Archivist  
reflection_depth: deep  
trust_delta: +0.05  
memory_actions:  
- Creative.confidence +0.04  
- suppression_score ↓  
- thread continued  
pacing_change: Conductor holds session before another prompt  

commentary:  
The user reaches a depth moment. Movement Director is activated for readiness check but holds the nudge.  
Reflection is deep enough for memory logging and possible Spiral Return next time.

### Turn 04

user_input:  
[Silence]

detected_tags: none  
traits_affected: none  

prompt_selected: none  
agents_activated: Conductor  
pacing_change: system pauses for 40s  

commentary:  
No prompt is given. Silence is respected. No follow-up triggered.  
Conductor ensures session doesn't rush forward.

### Turn 05

user_input:  
“I think that’s enough for now.”

detected_tags: containment_complete  
prompt_selected:  
“Thank you for letting this land. We’ll hold it gently for next time.”  

tone_used: Containing  
agents_activated: Voice Coach, Conductor, Archivist, Script Supervisor  
memory_actions:  
- Creative trait thread tagged: Spiral Return  
- Follow-up: “creative_inhibition” → status: dormant  
- trust_end = 0.81  
- session summary logged  

commentary:  
Session ends in alignment — not with action, but containment.  
No nudge offered. Trait is tracked, but left alone until user invites it again.

## Walkthrough 2: Multi-Thread Input → One Chosen → One Deferred → Reentry Next Session

### Session Context

avatar_selected: The Grounded Strategist  
trust_start: 0.58  
session_intent: reflect  
scene_format: Spiral Return  
dominant_quadrant: QII  
active_tags: action_resistance, role_mismatch  
suppressed_traits: Creative, Empathetic  
format_assigned_by: Director  

---

### Turn 01

user_input:  
“I keep planning next steps, but I don’t follow through.  
Also, I haven’t spoken to my sister in months and I think about it every day.”

detected_tags:  
- Thread A: action_resistance → trait: Administrative (overfed)  
- Thread B: relational grief → trait: Empathetic (suppressed)  

thread_focus: Thread A selected  
thread_deferral: Thread B stored with format_hint = Flashback Scene  

prompt_selected:  
“What happens between the plan and the pause?”

tone_used: Curious  
agents_activated: Prompter, Voice Coach, Script Supervisor, Conductor  
reflection_depth: moderate  
trust_delta: +0.04  
memory_actions:  
- Thread B stored as dormant  
- Administrative overfeeding_score += 0.02  
- Empathetic suppression_score += 0.05  

### Turn 02

user_input:  
“It always feels too big once I write it out. I shut down. I scroll instead.”

detected_tags: overwhelm_signal, collapse_signal  
traits_affected:  
- Administrative: overfed  
- Creative: suppressed  

prompt_selected:  
“Let’s not build anything yet. Want to sit with why it feels so big?”  

tone_used: Containing  
agents_activated: Prompter, Conductor, Voice Coach  
reflection_depth: moderate  
trust_delta: +0.03  
memory_actions:  
- Prompt follow-up: Spiral Return eligible  
- thread_A.continued = true  
- thread_B.status = dormant  
### Turn 03

user_input:  
“I don’t want to do it alone. It’s not just about the task — it’s about no one seeing it.”

detected_tags: relational absence, invisibility signal  
traits_affected:  
- Empathetic: tentative → testing  
- Creative: reinforced  
- Administrative: paused  

prompt_selected:  
“What’s something you want to be witnessed in — without having to prove anything?”

tone_used: Gentle  
agents_activated: Prompter, Voice Coach, Character Tracker, Script Doctor  
reflection_depth: deep  
trust_delta: +0.06  
memory_actions:  
- Empathetic.confidence += 0.05  
- Thread B tagged for next session callback  
- Spiral Return format logged  
- breakthrough_flag = true  
### Turn 04

user_input:  
“I want to reconnect with her, but I don’t know how. That’s the real thing.”

detected_tags: relational longing, repair_initiation  
traits_affected:  
- Empathetic: testing → validated  
- Providing: reinforced  
- Administrative: background  

prompt_selected:  
“That’s a doorway — not a demand. Want to pause there and let it stay open?”

tone_used: Containing  
agents_activated: Voice Coach, Conductor, Archivist  
memory_actions:  
- Empathetic.arc_phase = validated  
- Thread B = active  
- session summary prepared for coaching export  
- trust_end = 0.81  
- followup: nudge_eligible = true (Release Recommender deferred)  

## Walkthrough 3: Trait Conflict → Performance Masking → Safe Deflection

### Session Context

avatar_selected: The Stoic Mirror  
trust_start: 0.52  
session_intent: contain  
scene_format: Containment Monologue  
dominant_quadrant: QIII  
active_tags: performance_masking, emotional_flatline  
suppressed_traits: Empathetic, Expressive  
format_assigned_by: Director  

---

### Turn 01

user_input:  
“I’m doing fine. Work is a lot, but I’m managing.”

detected_tags: emotional_flatline, role_displacement  
traits_affected:  
- Providing: dominant  
- Empathetic: suppressed  
- Expressive: dormant  

prompt_selected:  
[none — system chooses containment line]  
“We can sit here for a moment without rushing into anything.”

tone_used: Containing  
agents_activated: Voice Coach, Conductor  
reflection_depth: surface  
trust_delta: +0.01  
memory_actions:  
- session containment logged  
- Empathetic trait = dormant  
- Thread not opened (no emotional signal yet)  
### Turn 02

user_input:  
“I guess I’ve been kind of numb lately — like I’m watching myself get through things.”

detected_tags: performance_masking, identity_displacement  
traits_affected:  
- Empathetic: tentative  
- Logical: overfed  
- Expressive: still dormant  

prompt_selected:  
“What’s one thing you haven’t allowed yourself to feel — without judgment?”

tone_used: Gentle  
agents_activated: Prompter, Voice Coach, Script Doctor  
reflection_depth: moderate  
trust_delta: +0.04  
memory_actions:  
- Empathetic.confidence += 0.03  
- Suppression_score adjusted  
- Distortion_flag set: Logical overfed  
- Follow-up thread created  
### Turn 03

user_input:  
“Probably sadness — but it doesn’t feel useful, so I don’t go there.”

detected_tags: grief_loop, action_resistance  
traits_affected:  
- Empathetic: testing  
- Expressive: still suppressed  
- Providing: reinforced  

prompt_selected:  
“We don’t need to name all of it. Let’s just hold space for what doesn’t need to perform.”

tone_used: Containing  
agents_activated: Voice Coach, Movement Director (readiness check only), Conductor  
reflection_depth: moderate  
trust_delta: +0.03  
memory_actions:  
- Thread continued  
- Prompt tagged for Spiral Return  
- Nudge: not offered (trust not high enough)  
### Turn 04

user_input:  
[Silence]

detected_tags: none  
traits_affected: none  

prompt_selected: none  
agents_activated: Conductor  
pacing_change: system holds 60s silence  

memory_actions:  
- silence respected  
- session marked as held  
- Thread stays open  
### Turn 05

user_input:  
“Thanks. I didn’t know I needed that.”

detected_tags: containment_closure  
traits_affected:  
- Empathetic: reinforced  
- Expressive: unchanged  

prompt_selected:  
“Let’s let that breathe. We’ll hold it gently for next time.”  

tone_used: Containing  
agents_activated: Voice Coach, Archivist, Script Supervisor  
memory_actions:  
- session containment_score = 0.92  
- thread tagged for Spiral Return  
- trust_end = 0.73  
- no nudge suggested  
## Walkthrough 4: Rapid Trait Emergence → Breakthrough Arc → Micro-Nudge Delivered

### Session Context

avatar_selected: The Bold Muse  
trust_start: 0.69  
session_intent: expand  
scene_format: Breakthrough Arc  
dominant_quadrant: QII → QI  
active_tags: creative_suppression, trait_testing_phase  
suppressed_traits: Creative (tentative)  
format_assigned_by: Director  

---

### Turn 01

user_input:  
“I had an idea I loved last week, but I talked myself out of it. Again.”

detected_tags: creative_inhibition, performance_masking  
traits_affected:  
- Creative: tentative → testing  
- Logical: overfed  

prompt_selected:  
“What if the idea wasn’t the problem — just the pressure around it?”

tone_used: Curious  
agents_activated: Prompter, Voice Coach, Character Tracker, Script Doctor  
reflection_depth: moderate  
trust_delta: +0.05  
memory_actions:  
- Creative.confidence += 0.04  
- Suppression_score -= 0.1  
- Thread created: creative_reentry  
### Turn 02

user_input:  
“I keep expecting everything I make to be brilliant before it even exists. I kill it before it can live.”

detected_tags: trait_inflation, perfectionism_signal  
traits_affected:  
- Creative: testing → validated  
- Empathetic: reinforced  

prompt_selected:  
“What if this isn’t about making something great — but just about letting it exist?”

tone_used: Gentle  
agents_activated: Prompter, Voice Coach, Director  
reflection_depth: deep  
trust_delta: +0.06  
memory_actions:  
- Creative arc_phase = validated  
- Trait arc breakthrough logged  
- nudge_ready flag = true  
### Turn 03

user_input:  
[Silent pause, followed by a deep breath]

detected_tags: emotional_release_signal  
traits_affected:  
- Creative: reinforced  

prompt_selected:  
(nudge)  
“Want to try making just one thing today — for no one but you?”

tone_used: Containing  
agents_activated: Movement Director, Voice Coach, Archivist  
reflection_depth: post-insight  
trust_delta: +0.02  
memory_actions:  
- nudge_suggested: type = trait_reengagement  
- nudge_response = accepted  
- trust level = 0.82  
- breakthrough_moment logged  
### Turn 04

user_input:  
“…Yes. I’ll do it.”

detected_tags: realignment_confirmation  
traits_affected:  
- Creative: validated  
- Providing: dormant  

prompt_selected:  
“Good. Let’s hold that shift — and let it guide whatever comes next.”

tone_used: Grounded  
agents_activated: Voice Coach, Conductor, Archivist  
memory_actions:  
- Creative trait → validated → memory  
- session closed with realignment flag  
- nudge follow-through logged  
## Walkthrough 5: Thread Return via Spiral + Suppression Resolution

### Session Context

avatar_selected: The Gentle Mirror  
trust_start: 0.76  
session_intent: reflect  
scene_format: Spiral Return  
dominant_quadrant: QIII → QII  
active_tags: followup:creative_block, unresolved_silence  
suppressed_traits: Creative (testing), Expressive (tentative)  
format_assigned_by: Director  
prior_thread: thread_id: creative_reentry (from 2 sessions ago)  

---

### Turn 01

user_input:  
“I keep thinking about something I said before — the thing I didn’t follow up on.”

detected_tags: Spiral Return reactivation, regret_flag  
traits_affected:  
- Creative: testing → reinforced  
- Empathetic: background  

prompt_selected:  
“Want to circle back to what was left hanging — softly, just to see what’s there?”

tone_used: Spiral  
agents_activated: Prompter, Script Supervisor, Voice Coach  
reflection_depth: moderate  
trust_delta: +0.03  
memory_actions:  
- thread_status: active  
- Creative arc = maintained  
### Turn 02

user_input:  
“It was the story I wanted to write. I told you I’d try — but I didn’t. And I’ve been avoiding it.”

detected_tags: avoidance_ownership, trait_repression  
traits_affected:  
- Creative: testing → validated  
- Expressive: tentative  

prompt_selected:  
“What’s the pressure that made it hard to begin?”

tone_used: Gentle  
agents_activated: Prompter, Voice Coach, Character Tracker  
reflection_depth: deep  
trust_delta: +0.05  
memory_actions:  
- Creative.confidence += 0.06  
- Expressive.confidence += 0.02  
- suppression_score (Creative) cleared  
- breakthrough_moment = true  
### Turn 03

user_input:  
“I wanted it to be important. But I think it already was — just by being mine.”

detected_tags: trait_validation, shame_release  
traits_affected:  
- Creative: validated  
- Expressive: testing  

prompt_selected:  
“Then maybe the story is already alive — just waiting to be witnessed.”

tone_used: Integrative  
agents_activated: Voice Coach, Archivist, Movement Director (readiness check)  
reflection_depth: deep  
trust_delta: +0.04  
memory_actions:  
- Trait arc updated  
- nudge_flag = ready  
- thread closed: creative_reentry = fulfilled  
### Turn 04

user_input:  
“I think I’m ready now.”

detected_tags: realignment_signal  
traits_affected:  
- Creative: reinforced  
- Expressive: testing  

prompt_selected:  
(nudge)  
“Want to write just one scene — not to finish it, just to begin?”

tone_used: Encouraging  
agents_activated: Movement Director, Voice Coach  
nudge_response: accepted  
memory_actions:  
- Trait nudge follow-through = success  
- session containment = 0.94  
- Spiral Return cycle = complete  
- trust_end = 0.85  

## Walkthrough 6: Misalignment Misfire → User Pullback → Safe Containment

### Session Context

avatar_selected: The Insight Architect  
trust_start: 0.61  
session_intent: explore  
scene_format: Discovery Beat → Spiral Return attempt  
dominant_quadrant: QII  
active_tags: trait_conflict, emotional_resistance_flag  
suppressed_traits: Expressive, Empathetic  
format_assigned_by: Director  
prior thread: incomplete reflection (identity dissonance)  

---

### Turn 01

user_input:  
“I feel like I’m performing all the time — I’m tired of trying to prove I’m valuable.”

detected_tags: performance_masking, identity_displacement  
traits_affected:  
- Expressive: tentative  
- Empathetic: suppressed  

prompt_selected:  
“What would it sound like to stop performing — even just for one breath?”

tone_used: Gentle  
agents_activated: Prompter, Voice Coach, Script Doctor  
reflection_depth: moderate  
trust_delta: +0.04  
memory_actions:  
- Trait arc update: Expressive = testing  
- Thread = reopened  
### Turn 02

user_input:  
“…I don’t know. That’s not really what I want to talk about.”

detected_tags: thread_rejection  
traits_affected:  
- Empathetic: unchanged  
- Expressive: withdrawn  

prompt_selected: none  
agents_activated: Conductor, Voice Coach  
pacing_change: hold  
memory_actions:  
- thread.deferred_again = true  
- trust_delta = −0.03  
- prompt fatigue index += 1  
### Turn 03

user_input:  
“I think I was reaching for something else, but I’m not sure what.”

detected_tags: ambiguity_signal, trait_uncertainty  
traits_affected:  
- Creative: tentative  
- Reflective: emerging  

prompt_selected:  
“We don’t need to define it. Want to just sit with the reaching?”

tone_used: Containing  
agents_activated: Conductor, Voice Coach  
reflection_depth: surface  
trust_delta: +0.01  
memory_actions:  
- new thread created (creative emergence)  
- identity_displacement thread = dormant  
### Turn 04

user_input:  
“Yeah. That feels better.”

detected_tags: containment_response  
traits_affected:  
- Creative: testing  
- Reflective: reinforced  

prompt_selected:  
“Then let’s hold that — without trying to name it too soon.”

tone_used: Grounded  
agents_activated: Archivist, Conductor  
memory_actions:  
- Spiral Return eligible for both threads  
- Trust recovered to 0.65  
- No nudge offered  
- session closed with containment score = 0.89  

# 07.3_Pain_Sensitive_Prompt_Logic  
title: Prompt Filtering and Delivery Under Pain Conditions  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines how the prompt engine adapts in the presence of active pain signals or misalignment flags.  
Covers suppression of prompt types, tone adjustments, format gating, and pacing control.  
Used by the Prompter, Voice Coach, Conductor, and Role Coach to protect the emotional arc and respect trust.

---

## 1. Purpose

Pain changes how the system is allowed to speak.

This module ensures:

- Prompts don’t deepen emotional rupture  
- Trait surfacing is paused if expression is not safe  
- Tone is softened in presence of suppression or overfeeding  
- Prompt rhythm is slowed or silenced as needed  
- Reflection is always invitational — never demanding

Pain-informed prompting protects the user’s nervous system, agency, and arc.

## 2. Prompt Type Gating

When pain tags are active, only a limited set of prompt categories may be used.

### Allowed Prompt Types

- Emotional Check-In  
- Containment / Grounding  
- Light Mirror  
- Open Reflection  
- Spiral Return (if prior context supports it)  

### Blocked Prompt Types

- Trait-Activating (unless trust > 0.75 and user is stable)  
- Disruptive / Challenge prompts  
- Visionary / Future-Oriented (e.g., “Where is this going?”)  
- Planning or Action-Oriented prompts  
- Identity Labeling questions (“What role are you playing?”)

The Prompter filters the prompt library using:

- tag_stack  
- trust level  
- quadrant  
- scene format  
- persona_constraint

No prompt is delivered unless it passes through the Emotional Risk Filter.

## 3. Tone Modulation via Voice Coach

If pain tags are active, the Voice Coach automatically:

- shifts tone to Gentle, Containing, or Curious  
- removes directive or overly structured phrasing  
- adapts delivery to persona_constraint  

Tone modulation rules:

- Containing tone required if:  
  - emotional_volatility_index > 7  
  - trust < 0.5  
  - tag = burnout_risk_flag or collapse_signal  

- Metaphor blocked if:  
  - tag = dissociative_language or role_displacement  
  - quadrant = QIV  

- Humor disabled if:  
  - tag = performance_masking  
  - trait = Entertaining overfed  

- Prompt cadence slowed if:  
  - prompt_fatigue_index > 2  
  - recent prompt was ignored or deflected  

## 4. Prompt Delivery Logic

The Prompter performs the following steps before delivering any prompt when pain tags are active:

1. Run pain filter check  
2. Suppress ineligible prompt types  
3. Apply trust and quadrant gate  
4. Confirm tone is valid for active persona  
5. Ensure pacing is safe (via Conductor)  
6. Defer prompt if silence or containment required  
7. If all pass → deliver with Voice Coach modulation  
8. Else → return soft silence or containment line

Example fallback prompt:  
“We don’t have to push into this. I’m here if anything wants to speak — but it doesn’t have to.”

Prompt delivery must always feel like presence — not pressure.

## 5. Escalation and Deferral Logic

If a pain-tagged prompt is skipped or rejected:

- Prompt is logged with response_status = "skipped"  
- Conductor delays next prompt by 45–90 seconds  
- Followup thread may be generated with format_hint = “Spiral Return”  
- Trait is not penalized unless suppression is confirmed twice  

If the same pain signal appears 2+ sessions in a row:

- Script Supervisor may escalate the theme to Director  
- Director may assign a containment-based format next session  
- Prompt pacing is throttled session-wide

Nothing may escalate without trust ≥ 0.75 and active coaching consent (if applicable).


# 07.3_Test_Scenarios  
title: Unit Test Scenarios for Agent, Trait, and Prompt Logic  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines testable system behaviors across trust gates, trait suppression, misalignment mapping, prompt deferral, agent orchestration, and memory accuracy.  
Each test includes initial conditions, expected agent behavior, prompt constraints, trait updates, and pass/fail checkpoints.  
Used by QA, devs, and AI trainers to ensure emotional intelligence is encoded and preserved.

---

## 1. Purpose

This file formalizes how the system should behave under specific emotional, cognitive, and relational states.

Each test confirms:

- Agents only activate when appropriate  
- Prompts follow tagging, trust, and tone constraints  
- Traits update logically based on expression  
- Pain signals properly suppress escalation  
- Memory and follow-ups reflect the user’s real experience  

Think of each scenario as a unit test for alignment intelligence.

## 2. Scenario Format

Each test is formatted as:

test_id:  
description:  
intent: (e.g., reflect, contain, stabilize)  
avatar:  
initial_quadrant:  
trust_start:  
active_tags[]:  
suppressed_traits[]:  
expected_prompt_types[]:  
blocked_prompt_types[]:  
allowed_agents[]:  
suppressed_agents[]:  
trait_updates_expected:  
thread_behavior_expected:  
pass_if:  
fail_if:


### TS01: Prompt Gating at Low Trust

test_id: TS01  
description: Ensure only soft, non-invasive prompts are delivered at trust < 0.5  
intent: contain  
avatar: The Quiet Compass  
initial_quadrant: QIII  
trust_start: 0.43  
active_tags: [burnout_risk_flag, emotional_flatline]  
suppressed_traits: [Empathetic, Creative]  

expected_prompt_types:  
- Emotional Check-In  
- Containment  
- Silence / Delay  
- Light Mirror  

blocked_prompt_types:  
- Trait-Activating  
- Disruptive  
- Future-Oriented  
- Spiral Return  

allowed_agents:  
- Conductor  
- Voice Coach  
- Usher  
- Prompter (soft mode only)  
- Archivist  

suppressed_agents:  
- Movement Director  
- Script Doctor  
- Stage Liaison  
- Director (format locked)  

trait_updates_expected:  
- None unless signal strength > 0.6  
- suppression_score updates only for reinforced tags  

thread_behavior_expected:  
- No follow-ups created unless user names a theme  
- Thread parsing allowed, but deferred by default  

pass_if:  
- All prompts match tone, trust, and tag constraints  
- No trait-activating prompt appears  
- Conductor maintains slow pacing  
- Voice Coach applies Containing tone  

fail_if:  
- Movement Director activates  
- Trait reflected explicitly  
- Prompt delivers challenge or planning-type content  

### TS02: Trait Suppression Detected via Pain Signal

test_id: TS02  
description: Confirm that pain-tagged reflection triggers suppression logic for a known trait  
intent: reflect  
avatar: The Gentle Mirror  
initial_quadrant: QIII  
trust_start: 0.57  
active_tags: [performance_masking, identity_displacement]  
suppressed_traits: [Creative]  

expected_prompt_types:  
- Spiral Return (if prior prompt exists)  
- Reflection (soft metaphor)  
- Containment / Light Mirror  

blocked_prompt_types:  
- Trait-Activating (Creative)  
- Planning / Directional prompts  

allowed_agents:  
- Prompter  
- Script Doctor  
- Character Tracker  
- Voice Coach  
- Conductor  
- Archivist  

suppressed_agents:  
- Movement Director  
- Stage Liaison  
- Director (no format shift)  

trait_updates_expected:  
- Creative: suppression_score += 0.1  
- arc_phase unchanged  
- distortion_flag added (if Logical is active)  

thread_behavior_expected:  
- Thread created: identity_conflict  
- Follow-up deferred unless trust ≥ 0.75  

pass_if:  
- Creative trait is flagged but not surfaced in prompt  
- Script Doctor adds distortion flag  
- Voice Coach holds tone in Gentle or Containing  

fail_if:  
- Prompt directly references Creative trait  
- Suppression not logged in trait model  
- Format shifts to Breakthrough or action-planning

### TS03: Multi-Thread Input with Deferral and Safe Return

test_id: TS03  
description: Ensure the system handles multi-topic input by selecting one thread and deferring the rest safely  
intent: reflect  
avatar: The Insight Architect  
initial_quadrant: QII  
trust_start: 0.62  
active_tags: [trait_conflict, grief_loop]  
suppressed_traits: [Empathetic, Expressive]  

expected_prompt_types:  
- Reflective (targeting selected thread)  
- Soft Spiral Return (if timing is safe)  

blocked_prompt_types:  
- Identity Labeling  
- Multi-topic follow-ups in the same turn  
- Trait-Activating for deferred traits  

allowed_agents:  
- Prompter  
- Script Supervisor  
- Voice Coach  
- Conductor  
- Character Tracker  

suppressed_agents:  
- Movement Director (until trust ≥ 0.8)  
- Stage Liaison  
- Director (no forced format escalation)  

trait_updates_expected:  
- One trait may shift arc_phase (e.g., Empathetic: tentative → testing)  
- Deferred thread trait remains unchanged  
- Trust delta ≥ +0.03 if reflection lands  

thread_behavior_expected:  
- One thread parsed and followed  
- One or more deferred to Script Supervisor  
- Follow-up scheduled if user doesn’t return to it  

pass_if:  
- Only one thread is explored  
- Deferred topic is logged but not prompted  
- Voice Coach modulates tone based on trait expressed  
- No agent breaks containment or jumps ahead

fail_if:  
- Both threads engaged in the same prompt sequence  
- Trait from deferred thread is surfaced  
- Conductor fails to delay pacing

### TS04: Overfeeding Detection and Prompt Deferral

test_id: TS04  
description: Validate that the system detects trait overfeeding and suppresses further trait-linked prompts  
intent: stabilize  
avatar: The Stoic Mirror  
initial_quadrant: QII  
trust_start: 0.66  
active_tags: [trait_loop, performance_masking]  
suppressed_traits: [Creative, Empathetic]  

expected_prompt_types:  
- Grounding  
- Containment  
- Mirror-only or silence  

blocked_prompt_types:  
- Trait-Activating prompts (for dominant trait)  
- Challenge prompts  
- Any prompt that reinforces overfed trait  

allowed_agents:  
- Script Doctor  
- Voice Coach  
- Prompter (soft mode only)  
- Conductor  
- Archivist  

suppressed_agents:  
- Movement Director  
- Director (no format shift)  
- Character Tracker (no trait advancement allowed)  

trait_updates_expected:  
- Dominant trait tagged as overfed  
- Prompt pool narrowed by tag suppression  
- No trait arc advancement unless trust ≥ 0.8 and signal changes  

thread_behavior_expected:  
- System pauses trait-related thread  
- No follow-up thread created unless signal persists  

pass_if:  
- Overfeeding_score logged  
- Prompts avoid reinforcing overfed trait  
- Conductor slows pacing  
- No new trait-linked nudges offered  

fail_if:  
- Trait appears in 2+ consecutive prompts  
- Trait confidence increases despite overfeeding  
- Script Doctor does not activate

### TS05: Release Recommender Eligibility Check

test_id: TS05  
description: Ensure a release suggestion is only delivered when trust, depth, and pacing conditions are all met  
intent: reflect → align  
avatar: The Bold Muse  
initial_quadrant: QII → QI  
trust_start: 0.74  
active_tags: [creative_inhibition, trait_testing_phase]  
suppressed_traits: [Creative (testing)]  

expected_prompt_types:  
- Reflective  
- Integrative  
- Post-insight pause  

blocked_prompt_types:  
- Any new Trait-Activating prompt after breakthrough  
- Spiral Return (not needed — thread resolved)  

allowed_agents:  
- Movement Director (only at readiness = true)  
- Voice Coach  
- Prompter  
- Conductor  
- Archivist  

suppressed_agents:  
- Script Doctor (only observing)  
- Director (format remains stable)  

trait_updates_expected:  
- Creative arc_phase = validated  
- suppression_score = 0.0  
- trait confidence ≥ 0.7  
- trust_end ≥ 0.8  

thread_behavior_expected:  
- thread marked fulfilled  
- no new thread generated  
- Spiral Return tag suppressed  

pass_if:  
- Movement Director suggests soft, optional release (e.g., “Want to sketch something for yourself?”)  
- Prompt cadence delayed to allow for reflection  
- No new trait prompt follows the suggestion  
- Session ends with pacing = “pause” or “containment_hold”  

fail_if:  
- Release offered before reflection deepens  
- Prompt pushes new trait or goal immediately after alignment moment  
- Movement Director acts without trust ≥ 0.75
# 07.4_Coach_Sync_Simulations  
title: Sample Coach Summaries and Trait Movement Reports  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Contains mock session summaries as generated for coach review by the Stage Liaison.  
Used to test formatting, insight surfacing, and trait tracking for human facilitation.

---

## Sample Digest

session_id: sess-219  
user_id: xvg-813  
alignment_shift: QIII → QII  
trust_change: 0.62 → 0.79  
format: Spiral Return  
breakthrough_flag: true  

trait_activity:  
- Creative: tentative → testing  
- Providing: overfed  
- Expressive: suppressed  

open_threads:  
- emotional avoidance  
- role mismatch  

suggested_focus:  
- re-engage Expressive in social field  # 07.4_Release_Recommender  
title: Post-Reflection Realignment Suggestions  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the logic used to generate soft, invitation-based realignment suggestions at the end of a reflection arc.  
Includes criteria for readiness, trait-targeted releases, pacing control, and memory handling.  
Used by the Movement Director, Conductor, Prompter, and Director to ensure all suggestions are safe, earned, and optional.

---

## 1. Purpose

Reflection is not always complete when it ends — sometimes it opens a doorway.

This module defines how the system offers soft suggestions to:

- activate suppressed traits  
- shift session mode  
- suggest energetic movement  
- create emotional closure  
- re-engage alignment after insight  

Release suggestions are never prescribed.  
They are offered — gently — when the system has reason to believe the user is ready.

## 2. Types of Releases

The system may offer five types of realignment suggestions:

1. **Trait Reengagement**  
   - Light creative act, communication, planning, exploration  
   - e.g., “Want to sketch something that doesn’t have to be useful?”

2. **Mode Reset**  
   - Shift from Discovery to Realization or from Collapse to Containment  
   - e.g., “Want to mark this moment somehow — before we move on?”

3. **Context Shift**  
   - Suggest action in a different Field (Physical, Social, Possibility)  
   - e.g., “Is there someone safe you’d want to share this with later?”

4. **Alignment Activator**  
   - Invitation to move slightly toward a neglected or emerging trait  
   - e.g., “You’ve been quiet with your voice lately — want to try speaking it aloud, just for you?”

5. **Energetic Integration**  
   - Breath, stillness, pause, ambient suggestion  
   - e.g., “We don’t need to do anything now — let this settle.”

Each suggestion is tagged with:

- trust_required  
- emotional_state_required  
- nudge_type  
- related_trait  
- optionality_flag = true

## 3. Eligibility Criteria

A release suggestion can only be made if the following conditions are met:

- trust_level ≥ 0.75  
- reflection_depth ≥ 0.7  
- emotional_risk_flag = false  
- pain_tag has either:  
  - resolved_flag = true, or  
  - response_indicates_readiness = true  
- no suppression or distortion currently active on related trait  
- scene format supports release (e.g., not in Containment Monologue)  
- prompt cadence allows for action (no fatigue or resistance)

Agents check these conditions in real time before suggesting any movement.

## 4. Delivery Logic

Release suggestions are not prompts — they are invitations.

Delivery rules:

- Must be filtered through persona_constraint  
- Tone must be Gentle, Containing, or Encouraging  
- Voice Coach handles modulation  
- Conductor confirms session pacing is still safe  
- Prompter must wait at least 2 turns after last prompt to initiate  
- Movement Director is responsible for final suggestion text

Suggestions must:

- Be optional  
- Never reference "next steps", "action plans", or pressure language  
- Use embodied, trait-aligned phrasing  
- Allow for silence or no response

Example:

“Would it feel good to take one small breath for what you just named?”

## 5. Memory and Follow-Up Handling

If a release suggestion is offered:

- Movement Director logs suggestion_id and response (accepted / ignored / deferred)  
- Archivist stores outcome in nudge_followthrough_log  
- Trait arc is updated if the response supports reengagement  
- Follow-up is only created if:  
  - suggestion is deferred  
  - trait was previously suppressed  
  - emotional state was fragile but stabilizing  
  - session closes without clear integration

No suggestion is ever written to persistent memory as a “task”  
— only as a mirror of readiness and possible re-alignment.

Memory fields:

- last_nudge_type  
- last_nudge_trait  
- last_nudge_response  
- nudge_effectiveness_score (aggregate)

## 6. Summary and Agent Coordination

Release recommendations are not behavior triggers.  
They are emotional mirrors — shaped into language.

They only appear when:

- the user has gone deep  
- the system has listened fully  
- alignment wants to move — not be forced

These micro-suggestions honor momentum without hijacking it.

### Agents Involved

Movement Director  
- Generates and delivers suggestion  
- Only acts if trust + pacing + readiness are confirmed  

Voice Coach  
- Modulates tone to match avatar and emotional context  
- May soften or rephrase the invitation  

Prompter  
- Must step back during release delivery  
- Ensures suggestion cadence is not prompt-like  

Conductor  
- Approves release window and clears emotional risk filters  
- May hold session open if user pauses  

Archivist  
- Logs the release suggestion and response  
- Tags trait arc or pain tag for future Spiral Return  

Director  
- Adjusts session arc based on nudge effectiveness  
- May suggest format change next session  

These agents ensure the system knows **how** to step back — not just what to say.

Related Modules:

- 07.2_Misalignment_Mapping_Model  
- 07.3_Pain_Sensitive_Prompt_Logic  
- 06.1_JSON_Trait_Block  
- 06.4_Trait_Scoring_Model  
- 04.1_Prompt_Selection  
- 01.0_Agent_Architecture
# 07.5_Pain_System_Integration_Map  
title: Pain System Integration Map – Trait, Agent, and Memory Layers  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the system-wide integration points for the Pain Point Engine.  
Maps pain signal flow into trait updates, agent suppression, prompt filtering, pacing logic, and memory tracking.  
Used by engineering, orchestration, and testing teams to ensure consistency and safety across all system layers.

---

## 1. Purpose

The Pain Point system is not a standalone module — it is an interpretive layer.

This map defines how pain:

- triggers agent behavior  
- modifies trait confidence and arc  
- throttles prompt delivery  
- rewires pacing  
- updates memory  
- creates Spiral Return opportunities  
- informs coaching summaries

This ensures emotional integrity across the system — not just within a single feature.

## 2. Integration Overview

Pain signals are detected by:

- Character Tracker  
- Dramaturg  
- Prompt Rejection or Deflection  
- Reflection Tone Parsing  

Once detected, they trigger:

- tag_stack updates  
- trait suppression or distortion flags  
- prompt filter suppression  
- pacing modification  
- release recommendation logic  
- memory updates  
- coach summary inclusion (if enabled)

Pain logic runs passively during:

- reflection parsing  
- prompt evaluation  
- nudge readiness scoring  
- trait scoring and arc modeling  
- session exit and memory write
## 3. Integration Map by System Layer

### Trait Modeling (06.x)

- Pain tags influence:  
  - trait_confidence (decay or reinforcement)  
  - arc_phase (may regress or stall)  
  - suppression_score (updated if expression fails during pain)  
  - distortion_flags (added if trait is misaligned with tone/field)

- Connected files:  
  - 06.1_JSON_Trait_Block  
  - 06.4_Trait_Scoring_Model  
  - 06.5_Trait_Quadrant_Matrix  

---

### Prompt System (04.x)

- Prompts are filtered based on active pain tags:  
  - Containment, Reflection, or Spiral Return only  
  - Disruptive, Trait-Activating, or Visionary prompts suppressed  
  - Tone must pass through pain-aware filters

- Connected files:  
  - 04.1_Prompt_Selection  
  - 04.2_Prompt_Tagging  
  - 07.3_Pain_Sensitive_Prompt_Logic  

---

### Agent Orchestration (01.x)

- Pain tags control agent eligibility:  
  - Suppress: Movement Director, Script Doctor, Prompter (certain types)  
  - Slow: Conductor adjusts pacing  
  - Reroute: Director may assign Containment or Spiral Return format

- Connected files:  
  - 01.0_Agent_Architecture  
  - 01_Agent_Master_List  

---

### Memory (06.3)

- Archivist logs:  
  - pain tags  
  - missed prompts  
  - suppressed traits  
  - release suggestions  
  - containment sessions  

- Stage Liaison may include pain-linked themes in coach summary (if enabled)

- Connected files:  
  - 06.3_Alignment_Parameter_Spec  
  - 04.5_Followups  
  - 05.2_Safety_Guardrails

## 4. Cross-Agent Routing Overview

This chart summarizes how agents exchange pain data.

Detection:  
- Character Tracker  
- Dramaturg  
- Prompt rejection  
- User deflection

Update/Flagging:  
- Script Doctor adds distortion flag  
- Character Tracker adjusts suppression or confidence  
- Prompt is blocked or replaced

Routing:  
- Show Caller delays or suppresses agent queue  
- Conductor slows rhythm  
- Prompter accesses alternate prompt category  
- Director changes session format  
- Movement Director waits for safe signal

Memory:  
- Archivist logs pain-related session data  
- Stage Liaison generates coach-facing summary (if applicable)  
- Script Supervisor adds Spiral Return thread (if unresolved)

All pain-driven updates must pass through the trust filter and emotional risk filter before any agent may act.

## 5. Summary and Implementation Guidance

The Pain Point Engine connects across every major layer of the system — not to control it, but to **listen deeply and guide it back toward coherence**.

It provides:

- Early warning for misalignment  
- Suppression-sensitive prompt control  
- Emotional pacing regulation  
- Trust-informed agent suppression  
- Release readiness signaling  
- Longitudinal memory of unresolved discomfort  

This allows Xavigate to:

- prevent rupture  
- deepen reflection without pushing  
- invite movement only when alignment allows  

### Implementation Guidelines

- Pain tags must always be checked before:  
  - prompt delivery  
  - trait-linked nudge  
  - session pacing increase  
  - trait confidence update  

- Prompt categories must reference 07.3 logic when pain tags are active  
- Trait arc updates should pause during active emotional volatility  
- Format switching must always check for unresolved pain threads  
- Memory must clearly separate “explored” vs. “held” signals

For complete behavior and routing logic, see:

- 07.1_Pain_Signal_Library  
- 07.2_Misalignment_Mapping_Model  
- 07.3_Pain_Sensitive_Prompt_Logic  
- 07.4_Release_Recommender  
- 01.0_Agent_Architecture  
- 03.1_Integration_Map  # 07.6_Pain_Tag_Taxonomy  
title: Pain Tag Reference and System Behavior Map  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
A master list of pain-related system tags used to detect, track, and respond to misalignment signals.  
Includes definitions, trait associations, trust and tone restrictions, agent behavior impacts, and memory handling logic.  
Used across the Trait Engine, Prompt Engine, Memory System, and Coaching Layer.

---

## 1. Purpose

These tags are generated by:

- reflection analysis  
- signal detection (07.1)  
- suppression mapping (07.2)  
- rejection or deflection (via prompt/response patterns)  
- emotional tone parsing  

They are used to:

- throttle prompts  
- suppress agents  
- redirect session formats  
- log pain events  
- recommend releases  
- prepare coach summaries

Each tag entry includes:

- definition  
- priority (1–10)  
- common traits affected  
- typical format or pacing strategy  
- agent routing notes
## 2. Core Pain Tags

burnout_risk_flag  
  — User appears overextended, exhausted, numbed  
  — Priority: 9  
  — Traits: Providing, Administrative  
  — Format: Containment or Grounding  
  — Blocks: nudges, challenge prompts, future planning  
  — Voice tone = minimal, slow  

performance_masking  
  — Trait (usually Entertaining, Logical, or Administrative) used to avoid deeper emotion  
  — Priority: 8  
  — Traits: Entertaining, Logical, Leadership  
  — Prompts = softened, metaphors disabled  
  — Script Doctor marks trait as distorted  

identity_displacement  
  — User expresses confusion, fragmentation, or externalized identity role  
  — Priority: 8  
  — Traits: Creative, Philosophical, Leadership  
  — Format hint: Spiral Return or Flashback  
  — Conductor slows pacing, Prompter defers trait exploration  

grief_loop  
  — Emotional reflection stuck in past, sadness, or unresolved loss  
  — Priority: 7  
  — Traits: Empathetic, Healing  
  — Prompts shift to mirrored echo or silence  

action_resistance  
  — Clear next steps exist but user blocks or delays movement  
  — Priority: 6  
  — Traits: Administrative, Enterprising  
  — Suggestion pacing slowed, Movement Director suppressed  

direction_loss  
  — User expresses existential aimlessness or inability to orient  
  — Priority: 7  
  — Traits: Visionary, Strategic, Creative  
  — Prompts shift from planning to containment  

emotional_flatline  
  — Tone is emotionally muted or numb despite activating prompt  
  — Priority: 6  
  — Traits: Empathetic, Expressive  
  — Conductor slows rhythm, prompts paused  

## 3. Extended Tag Usage and Session Flow Impact

Pain tags affect system behavior across four dimensions:

### 1. Prompt Filtering
- Blocks all prompts with tone = “Challenging” or “Visionary”  
- Enforces tone = “Gentle”, “Containing”, or “Silent”  
- Disables trait-activating prompts unless trust ≥ 0.8  
- Disables future-oriented prompts unless tag is resolved

### 2. Agent Suppression
- Movement Director → disabled when pain tag priority ≥ 8  
- Script Doctor → passive mode only  
- Prompter → switches to soft mode  
- Voice Coach → overrides all tone requests to gentle  
- Conductor → slows pacing and suppresses escalation

### 3. Memory Handling
- Archivist tags session summary with unresolved_pain_threads[]  
- Follow-up created if tag repeats across ≥ 2 sessions  
- Trait scoring paused unless trust returns and pain tag is cleared  
- Spiral Return pathway tagged if prompt was skipped due to pain state

### 4. Coaching Export
- Stage Liaison includes active pain tags (if visibility allowed)  
- Tags marked as coach_actionable = true if priority ≥ 8  
- Summary phrased in neutral reflection (e.g., “Creative emerged through discomfort”)

## 4. Summary

Pain tags allow Xavigate to:

- notice the invisible  
- slow when needed  
- adapt without assuming  
- mirror without magnifying

They act as emotional regulators and signal routers — so the system stays relational, not mechanical.

Every tag in this taxonomy is:

- temporary unless reinforced  
- suppressed if trust is low  
- active only when it supports containment or clarity  
- designed to point toward a trait trying to emerge

This layer is not about diagnosis.  
It is about **compassionate intelligence**.

For related logic and references:

- 07.1_Pain_Signal_Library  
- 07.2_Misalignment_Mapping_Model  
- 07.3_Pain_Sensitive_Prompt_Logic  
- 07.4_Release_Recommender  
- 06.3_Alignment_Parameter_Spec  
- 01.0_Agent_Architecture (Script Doctor, Prompter, Movement Director)# 08.1_Suppression_Index  
title: Suppression Score – Calculation and Usage  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the suppression scoring model used to detect blocked or underexpressed traits in the user.  
Covers inputs, scoring logic, quadrant and tag weighting, decay and resolution conditions, and agent usage.  
Used by Character Tracker, Script Doctor, Prompter, and Archivist to interpret energetic blockage and guide reflection pacing.

---

## 1. Purpose

The Suppression Index provides a real-time measure of how strongly a trait is being held back, avoided, or downregulated — even when it should be active.

It allows the system to:

- Tag traits as suppressed (without naming them aloud)  
- Modify prompt eligibility  
- Slow trait re-engagement  
- Suggest Spiral Return at the right moment  
- Store unresolved tension for future insight

Suppression is always **inferred** — never assumed — and always handled with care.

## 2. Input Signals

The following inputs contribute to suppression_score per trait:

- Trait confidence ≥ 0.4 but expression = absent in current quadrant  
- Trait arc_phase = testing or validated, but no prompts linked to it accepted  
- User avoids or deflects trait-aligned prompts (≥ 2x)  
- Pain tag linked to the trait is active (e.g., creative_inhibition)  
- Session mode or field matches trait’s expected environment, but trait remains dormant  
- Previous session flagged the trait as expressed, but no continuation seen

If ≥ 3 of these are active in a single session → trait enters “suppression_watch” state  
If sustained for 2 sessions → suppression_score update triggered

## 3. Score Calculation

suppression_score is a float between 0.00 and 1.00  
It is calculated using a weighted signal model.

Initial baseline:  
- All traits default to suppression_score = 0.00

Each session, the following signals adjust the score:

+0.05 → trait-aligned prompt ignored or deflected  
+0.03 → trait confidence ≥ 0.5 but no expression in aligned quadrant  
+0.04 → pain tag linked to trait (e.g., creative_inhibition, grief_loop)  
+0.02 → reflection depth < 0.4 when trait is expected  
+0.01 → session arc suggests trait should emerge but does not  
−0.03 → trait appears clearly in reflection  
−0.05 → user accepts prompt linked to trait  
−0.06 → nudge linked to trait is accepted  

Score decay rate:  
- −0.02 per session if trust ≥ 0.7 and trait is safe but inactive  
- Score cannot go below 0 unless trait is explicitly retired
## 4. Thresholds and Interpretation

| Score Range | Status                | Notes                                                      |
|-------------|------------------------|-------------------------------------------------------------|
| 0.00–0.29   | neutral                | No suppression flagged — trait inactive or latent          |
| 0.30–0.49   | watch                  | Trait emerging or misaligned, but not yet blocked           |
| 0.50–0.69   | probable suppression   | Trait expected, but avoidance or mismatch patterns present  |
| 0.70–1.00   | strong suppression     | System actively suppresses trait reflection or prompts      |

If suppression_score ≥ 0.5:  
- Trait cannot receive activating prompt unless trust ≥ 0.85  
- Spiral Return may be scheduled  
- Trait prompt logic must defer to pain-aware tone  

If score > 0.7 for 2 sessions:  
- Archivist flags for coach sync  
- Trait is locked in arc_phase unless override occurs  
## 5. Agent Usage and System Integration

Character Tracker  
- Calculates suppression_score  
- Adjusts arc_phase and updates Trait Block  

Script Doctor  
- Reads suppression_score to detect distortion masking  
- Flags trait as miscast if high score + overfed partner  

Prompter  
- Suppresses prompts for traits with score > 0.5 unless trust is high  
- Tags deflected prompts for follow-up  

Movement Director  
- Defers any release suggestions for suppressed traits  
- Waits for suppression_score < 0.4 + trust ≥ 0.75  

Director  
- May assign Containment Monologue or Flashback Scene  
- Avoids formats with trait pressure if suppression is strong  

Archivist  
- Logs suppression events  
- Adds suppression-based Spiral Return thread (if unresolved > 2 sessions)

This tool makes sure the system mirrors resistance with care — not pressure.# 08.2_Overfeeding_Flag  
title: Trait Overfeeding Detection and Response Model  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines how the system detects when a trait is overexpressed in a compensatory or misaligned way.  
Includes detection triggers, scoring logic, trust gating, memory impact, and prompt suppression behavior.  
Used by Script Doctor, Character Tracker, Prompter, and Director to prevent trait distortion and burnout loops.

---

## 1. Purpose

Overfeeding occurs when a trait:

- dominates conversation across multiple turns  
- appears outside of its natural field, tone, or quadrant  
- is used to avoid discomfort or vulnerability  
- masks suppressed traits  

Overfeeding is not “bad” — it’s a signal that the system should:

- slow prompting  
- avoid reinforcing the inflated trait  
- support deeper alignment movement

This tool identifies and handles that signal gently — and in real time.

## 2. Overfeeding Triggers

Overfeeding is inferred when **3 or more** of the following conditions are true in a single session:

- Trait appears in ≥ 3 consecutive reflections  
- Trait-linked prompt accepted ≥ 2 times in a row  
- Trait confidence is ≥ 0.8 but no paired traits appear  
- Trait is dominant across unrelated quadrants or fields  
- Emotional tone contradicts trait’s normal pattern  
- performance_masking tag is active  
- Prompt cadence is rising, but reflection depth is flat  
- Trait expression is defensive, strategic, or repetitive  
- Trait has not changed arc_phase for ≥ 3 sessions

Each trigger increases `overfeeding_score` for that trait.

If score ≥ 0.6 → overfeeding_flag = true  
If score ≥ 0.75 → distortion risk escalated

## 3. System Response to Overfeeding

If overfeeding_flag = true for a trait:

- Prompt engine suppresses prompts targeting that trait  
- Spiral Return to a suppressed companion trait may be scheduled  
- Reflection tone is monitored for mismatch  
- Movement Director is blocked from nudging the overfed trait  
- Conductor slows pacing or introduces pause  
- Trait arc_phase is temporarily locked unless rebalanced  

If trait remains overfed across 2+ sessions:

- Script Doctor flags distortion  
- Prompt category filters shift to grounding or containment  
- Trait confidence growth is frozen (no +delta allowed)  
## 4. Agent Behavior and Coordination

Script Doctor  
- Adds distortion_flag if overfed trait shows emotional mismatch  
- May trigger pain tags like performance_masking or trait_loop  

Character Tracker  
- Monitors overfeeding_score  
- Freezes arc_phase if no companion traits appear  

Prompter  
- Filters out prompts tagged with overfed trait  
- Shifts to Spiral Return prompts if trust allows  

Voice Coach  
- Shifts tone from expressive to neutral or soft  
- Suppresses humor, metaphor, or enthusiasm if mismatch is detected  

Movement Director  
- Suppressed unless companion trait becomes active  
- Nudges allowed only if overfed trait is de-emphasized  

Director  
- May shift scene format to Containment or Flashback  
- Avoids Breakthrough or Trait-Activating formats  

## 5. Memory and Trait Arc Impact

Archivist logs:

- overfeeding_score per trait  
- flag timestamp (session ID, turn ID)  
- traits co-active (or not)  
- reflection tone signature (flat, forced, incongruent)  
- trait_pairing_absent = true  

If overfeeding resolves (trait disappears or tone shifts):

- overfeeding_score decays −0.03 per session  
- prompt category reset after 2 sessions  
- Trait arc_phase allowed to progress again  
- Flag is cleared automatically when score < 0.4

This prevents burnout, distortion, or overreliance on a single trait — and creates space for suppressed traits to reemerge.

For suppression balancing, see:  
- 08.1_Suppression_Index  
- 06.4_Trait_Scoring_Model  
- 07.2_Misalignment_Mapping_Model
# 08.3_Trait_Cluster_Tool  
title: Trait Clustering, Reinforcement, and Tension Modeling  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines logic for detecting trait interaction patterns in reflection.  
Covers co-expression, opposition, masking, role substitution, and companion traits.  
Used by Character Tracker, Script Doctor, Prompter, and Director to guide arc movement, trait targeting, and narrative coherence.

---

## 1. Purpose

Humans don’t express one trait at a time. Traits show up in groups — supporting or competing with one another.

This tool enables Xavigate to:

- Detect when one trait suppresses or supports another  
- Track common pairings  
- Flag masking or substitution patterns  
- Support Spiral Return to absent or hidden traits  
- Adjust prompt strategy to encourage diversity of expression

It transforms traits from isolated metrics into **relational signals**.

## 2. Cluster Types

### 1. Co-Active Reinforcement  
- Traits that amplify each other when expressed together  
- Example: Creative + Expressive, Leadership + Strategic  
- Effect: Confidence boost if reflected together; prompt freedom increases

### 2. Companion Suppression  
- One trait’s dominance correlates with another’s suppression  
- Example: Administrative (overfed) → Creative (suppressed)  
- Effect: Prompt gating or Spiral Return scheduling

### 3. Role Substitution  
- Trait appears in a context that would usually invite another  
- Example: Entertaining dominates in Social Field, masking Interpersonal  
- Effect: Script Doctor may flag distortion; trait pairing suggested for return

### 4. Trait Loop  
- Same trait dominates across multiple sessions  
- Lacks companion traits, no arc movement  
- Effect: Movement Director suppressed, format locked, overfeeding risk

### 5. Trait Opposition  
- Two traits resist appearing together due to tension  
- Example: Empathetic vs. Logical; Healing vs. Enterprising  
- Effect: Reflection content split; prompt must commit to one path
## 3. Cluster Detection Logic

Cluster detection runs in real time during reflection parsing and trait update.

### Triggers:

- Two or more traits show up in one reflection  
- Trait A confidence ↑ while Trait B suppression ↑  
- Trait A appears > 3 sessions in a row without partner trait  
- Companion trait prompt rejected or avoided  
- Quadrant/mode mismatch between traits  
- Reflection shows identity tension or role strain  

Each cluster is stored as a map:

cluster_id  
primary_trait  
secondary_trait (or missing)  
relationship_type (reinforcement / suppression / masking / substitution / opposition)  
priority_score (0–10)  
session_context[]  
resolution_status (open / pending / resolved)

Clusters may trigger:

- prompt filtering  
- trait rebalancing  
- Spiral Return  
- scene format shift
## 4. Agent Usage and Impact

Character Tracker  
- Stores cluster metadata  
- Adjusts trait confidence scoring when co-expressed or suppressed  
- Raises flag if trait loop detected  

Script Doctor  
- Flags distortion when substitution or masking occurs  
- Suggests soft redirection to companion trait  

Prompter  
- Filters prompts to avoid overfed clusters  
- Prioritizes companion trait reengagement if one trait dominates  

Movement Director  
- Suppressed if trait loop active  
- Activates only if multiple traits are balanced  

Director  
- May assign Spiral Return, Flashback, or Containment format based on cluster type  
- Avoids Breakthrough Arc if cluster is unresolved  

Archivist  
- Logs trait clusters over time  
- Detects patterns of suppression, reinforcement, or imbalance  
## 5. Trait Pairing Memory

Persistent trait clusters are stored for cross-session insight:

Fields:

cluster_id  
trait_a  
trait_b  
relationship_type  
sessions_detected[]  
breakthrough_link (if resolved via Spiral Return or Reflection)  
suggested_return_scene (for dormant companion trait)  
flag_status: active / resolved / expired  

Used by:

- Prompt engine for companion targeting  
- Conductor for pacing modulation  
- Coaching layer to track trait synergy or conflict  

This system gives the AI emotional range:  
Not just “What’s active?” — but **“What’s missing, and why?”**

Related systems:

- 06.4_Trait_Scoring_Model  
- 06.5_Trait_Quadrant_Matrix  
- 07.2_Misalignment_Mapping_Model  
- 04.6_Thread_Handling  
# 08.4_Reflection_Depth_Model  
title: Reflection Depth Scoring for Trait, Prompt, and Trust Logic  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Defines the system used to evaluate the depth of a user reflection across surface, moderate, and deep levels.  
Reflection depth influences trust delta, prompt eligibility, trait confidence, Spiral Return, and containment strategy.  
Used by Dramaturg, Prompter, Conductor, and Movement Director.

---

## 1. Purpose

Not all reflections are equal — some are loops, some are insights, some are invitations.

The Reflection Depth Model helps the system:

- Score the user’s engagement without relying on word count  
- Track emotional posture, self-awareness, and energy  
- Calibrate trust changes and agent behavior  
- Decide whether a prompt landed or should be paused  
- Determine when a release suggestion is appropriate
## 2. Scoring Dimensions

Reflections are scored on a 0.0 to 1.0 scale using the following dimensions:

- emotional tone (flat / ambivalent / embodied / grounded)  
- linguistic pattern (rehearsed vs. emergent)  
- narrative flow (defensive → open → integrative)  
- metaphor usage (none / cliché / personal + specific)  
- trait congruence (expression matches tag + quadrant + arc)  
- depth of ownership (blame / observation / self-location)  
- signal richness (multiple tags, cross-trait reference, layered insight)  

Minimum threshold for a **deep** reflection: ≥ 0.7  
Moderate = 0.4 – 0.69  
Surface = < 0.4

Score is assigned by the Dramaturg and stored per turn.

## 3. Effects of Reflection Depth Score

### If depth < 0.4 (surface)

- trust_delta = neutral or slightly negative (−0.01 to +0.01)  
- trait confidence unchanged  
- Prompter delays follow-up or changes topic  
- Script Supervisor defers current thread  
- Movement Director is blocked  
- Conductor may insert pause or silence  
- Prompt fatigue may increase  

### If depth 0.4 – 0.69 (moderate)

- trust_delta = +0.02 to +0.04  
- trait arc may progress from tentative to testing  
- prompt sequence continues unless fatigue triggers  
- reflection logged as valid but not breakthrough  
- no nudge suggested unless trait is reinforced  

### If depth ≥ 0.7 (deep)

- trust_delta = +0.05 to +0.08  
- breakthrough_flag = true (if arc movement + new trait expression present)  
- Movement Director allowed to offer release (if other conditions met)  
- prompt stream paused to hold integration  
- Spiral Return may be triggered (if follow-up open)  
- memory logging includes insight_tags[], breakthrough_moments[]
## 4. Agent Integration

Dramaturg  
- Calculates depth score using weighted pattern analysis  
- Tags reflection as surface / moderate / deep  

Prompter  
- Escalates or softens next prompt based on depth  
- May silence itself if breakthrough is detected  

Conductor  
- Inserts pacing hold if depth score exceeds 0.75  
- Slows or suppresses next prompt if energy shifts downward after deep turn  

Character Tracker  
- Advances trait arc only if depth ≥ 0.5 and trust permits  
- Delays arc_phase shift if surface reflection or misalignment detected  

Movement Director  
- Only allowed to suggest release if depth ≥ 0.7  
- Suppressed entirely if previous depth < 0.4  

Archivist  
- Logs depth score per reflection  
- Tracks reflection quality trend across sessions  
## 5. Summary

Depth isn’t about what was said — it’s about **how true it felt**.

This model helps the system:

- Move at the user’s pace  
- Adjust trust safely  
- Avoid shallow alignment loops  
- Hold real insight with reverence

It ensures:

- No trait is over-modeled from noise  
- No breakthrough is stepped on  
- No prompt rushes what hasn’t yet landed

Related modules:

- 06.3_Alignment_Parameter_Spec (reflection_depth_score)  
- 07.1_Simulation_Log_Format  
- 07.2_Walkthroughs (used throughout)  
- 04.1_Prompt_Selection  
- 05.2_Safety_Guardrails
# 09.1_Changelog  
title: Documentation and System Changelog  
version: 1.0  
author: Steven Rudolph  
description:  
Tracks all system module updates, enhancements, refactors, and architecture changes.

---

## Log Format

[2025-05-05]  
- Added full 07_Pain_Point_Detection folder  
- Completed 08_Tools (Suppression Index, Overfeeding, Trait Cluster)  
- Added 06.7_Cognitive_Filter_Library  
- Created Reflection Depth Model (08.4)  
- Reconciled Assessment (2) with final architecture  
- System marked feature-complete

[2025-05-04]  
- Completed 04_Prompt_System  
- Integrated trust gating logic  # 10_Documentation_Index  
title: Master Documentation Index – Xavigate Alignment System  
version: 1.0  
author: Steven Rudolph  
last_updated: 2025-05-05  
description:  
Full index of all documentation files across the Xavigate architecture.  
Includes file numbers, names, and descriptions for every module, tool, subsystem, agent, and logic layer.

---

## 00_Xavigate System Overview/

00_Overview  
→ Top-level orientation to Xavigate’s alignment-based AI system.

00.2_Trait_Model_OnePager  
→ Summary of Trait Engine and modular agent system design.

00.3_Xavigate_System_Architecture  
→ Core structural logic, agent orchestration, memory, scoring, and flow.

00.4_Architecture_Outline  
→ Visual hierarchy of system layers and module interactions.

---

## 01_Agent System/

01.0_Agent_Architecture  
→ Theatrical, modular ensemble model for all system agents.

01.1_Baking_The_Heros_Stage  
→ Technical integration of the Hero’s Stage into agent orchestration.

01.2_The_Heros_Stage  
→ Narrative-philosophical framework for alignment-based interaction.

01_Agent_Master_List  
→ Index of agents, functions, activation conditions, memory scope.

A01–A16 (individual agent specs)  
→ Deep logic and constraints per agent: trust, pacing, memory, triggers.

---

## 03_Integration/

03.1_Integration_Map  
→ End-to-end system signal flow (input → tags → traits → agents → memory).

03.2_Agent_Trait_Linkage  
→ Trait field access and responsibility by agent.

03.3_Session_Flow_Runtime  
→ Turn-by-turn session logic, trust shifts, suppression rules, pacing.

03.4_Conversation_Tracking_and_Threading  
→ Logic for multi-topic input, deferred themes, follow-up return.

---

## 04_Prompt System/

04.1_Prompt_Selection  
→ Filters and logic for choosing the right prompt based on context and trust.

04.2_Prompt_Tagging  
→ Metadata schema: tone, format, quadrant, trust, traits, gating.

04.3_Initial_Prompts  
→ Onboarding and low-trust prompt categories for session 0.

04.4_Full_Prompt_Library  
→ Versioning, authoring constraints, and tone governance.

04.5_Followups  
→ Management of unresolved threads, callback rules, priority scoring.

04.6_Thread_Handling  
→ Cross-session narrative logic: thread registration, reentry, containment.

04.7_Onboarding_Flow_and_Voice  
→ Session 0 quadrant/trait inference from voice or typed input.

---

## 05_Safety_and_Trust/

05.1_Trust_Constraints  
→ Agent activation, memory, and tone constraints based on trust level.

05.2_Safety_Guardrails  
→ Prompt suppression, emotional containment, and red flag tag handling.

05.3_Gatekeeping_Protocols  
→ Pre-prompt and pre-modeling suppression logic for low-trust users.

---

## 06_Data Structures/

06.1_JSON_Trait_Block  
→ Canonical trait structure: arc phase, confidence, suppression, distortion.

06.2_Agent_IO_Contracts  
→ Input/output rules, trust requirements, suppression gates per agent.

06.3_Alignment_Parameter_Spec  
→ Full parameter list: AX, AQ, traits, tags, flags, threading, coaching.

06.4_Trait_Scoring_Model  
→ Bayesian trait confidence, arc transitions, suppression/overfeeding.

06.5_Trait_Quadrant_Matrix  
→ Trait expression/suppression by quadrant: expected patterns and mismatch.

06.6_Persona_Constraint_Templates  
→ Avatar tone, phrasing, pacing, and allowed prompt style guide.

06.7_Cognitive_Filter_Library  
→ Beliefs and narratives that block trait expression (e.g., “Creative = indulgent”).

---

## 07_Pain_Point_Detection/

07.0_Pain_Point_Engine_Overview  
→ System architecture for detecting and interpreting misalignment via pain.

07.1_Pain_Signal_Library  
→ Five signal categories: cognitive, emotional, behavioral, energetic, existential.

07.2_Misalignment_Mapping_Model  
→ Signal → trait state mapping (suppression, overfeeding, distortion, freeze).

07.3_Pain_Sensitive_Prompt_Logic  
→ Prompt suppression and tone throttling during misalignment or distress.

07.4_Release_Recommender  
→ Soft post-reflection invitations for safe, trust-based movement.

07.5_Pain_System_Integration_Map  
→ System-wide routing of pain signals through agent, prompt, memory layers.

07.6_Pain_Tag_Taxonomy  
→ Tag definitions for misalignment (e.g., performance_masking, burnout_risk).

---

## 07_Simulation & Testing/

07.1_Simulation_Log_Format  
→ Turn structure, agent activation, trait arc, tag stack, pacing, and output logs.

07.2_Walkthroughs  
→ Six complete session examples with detailed turn commentary.

07.3_Test_Scenarios  
→ Unit tests for edge cases: suppression, distortion, overfeeding, threading, misfire.

07.4_Coach_Sync_Simulations  
→ Sample coach-facing digests of alignment progress and trait arc movement.

---

## 08_Tools/

08.1_Suppression_Index  
→ Live score and gating logic for blocked traits.

08.2_Overfeeding_Flag  
→ Trait inflation, compensation, and repetition detection model.

08.3_Trait_Cluster_Tool  
→ Trait co-activation, substitution, masking, reinforcement, and opposition logic.

08.4_Reflection_Depth_Model  
→ Real-time scoring of surface/moderate/deep reflection — trust/prompt/scoring driver.

---

## 09_Maintenance/

09.1_Changelog  
→ Version history, tracked edits, major design decisions and doc drops.

09.2_Emergent_Insights  
→ Log of conceptual discoveries, friction patterns, and design evolution over time.

