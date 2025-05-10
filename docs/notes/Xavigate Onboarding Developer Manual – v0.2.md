# Xavigate Onboarding Developer Manual – v0.2  
version: 2.0  
author: Steven Rudolph  
last_updated: 2025-05-06  
description:  
This is the technical implementation guide for building the first-time onboarding flow in Xavigate.  
The onboarding flow now includes the **Theme Resolution Layer** — a trust-sensitive, fuzzy signal system for detecting early personality energies and safely reflecting them back to the user.  
This manual covers prompt delivery, theme detection, memory storage, reflection generation, and unlock logic.  
It is designed for engineers building the onboarding pipeline, frontend, memory schema, and early trust logic in the Xavigate alignment engine.



## 1. Introduction

The onboarding experience in Xavigate is not a form, test, or chatbot script. It is a **scene**.

This document describes how to build Session 0 — the user’s first experience inside the system — using a flow that feels:

- Gentle  
- Contained  
- Insightful  
- And above all: **emotionally safe**

Rather than scoring traits or delivering advice, the system listens for **themes** — soft, emergent expressions of who the user might be.

These themes are:

- Detected invisibly  
- Scored probabilistically  
- Never exposed to the user  
- Used to generate one meaningful reflection  
- Stored for future trait conversion (if trust and signal increase)

---

### 1.1 Core Objectives of the Flow

- Deliver 3–5 emotionally attuned prompts  
- Let the user respond (or skip) at their own pace  
- Detect 1–2 dominant themes from language patterns  
- Score each theme for confidence and expression strength  
- Generate a mirror-like reflection from the highest-scoring theme  
- Offer no trait, type, score, or interpretation  
- Unlock the next stage of the system when readiness conditions are met

---

### 1.2 Why Themes (Not Traits)

Themes are intentionally fuzzy. They allow the system to:

- Begin modeling without violating emotional pacing  
- Avoid over-labeling the user before trust is earned  
- Reflect something real without claiming to “know” the user  
- Capture energy, not identity

Instead of saying:  
> “You’re a helper.”

The system says:  
> “You seem to show up quietly for others — even when it takes something from you.”

---

### 1.3 What This Document Covers

- Full onboarding session flow  
- Prompt selection and tagging logic  
- Theme detection and confidence scoring  
- Reflection generation engine  
- Theme memory schema  
- Trust posture initialization  
- Unlock conditions and transitions  
- Safety filters, fail-safes, and developer checklists  
- Appendix of prompts, themes, and templates

---

### 1.4 Who This Is For

This manual is for:

- Engineers building the onboarding frontend  
- Developers implementing the prompt engine  
- Backend devs building the memory and theme scoring pipeline  
- Prompt designers creating safe prompts and reflections  
- Architects embedding trust, pacing, and containment logic into the early user journey

## 2. System Design Philosophy  
**Themes, Trust, and the Art of Emergence**

---

Xavigate’s onboarding experience is built on one foundational belief:

> **You cannot know someone until they feel safe enough to show you who they are.**

This section explains the underlying principles that guide how the system behaves — not just technically, but emotionally — during a user’s first interaction.

---

### 2.1 Themes First, Traits Later

Traits are precise.  
Themes are suggestive.

**Themes are the first brushstrokes** — subtle indicators of personality, pattern, or energy. They are:

- Loosely defined  
- Inferred from language  
- Scored for signal strength  
- Never shown to the user

This is the opposite of standard psychometrics, which begin with rigid classifications. Xavigate starts with **soft awareness** and lets truth **emerge over time**.

---

### 2.2 Trust Is the Gatekeeper of Depth

No prompt, nudge, or trait conversion can occur unless the **trust posture** supports it.

- Low trust (0.0–0.3): gentle prompts only  
- Medium trust (0.4–0.6): themes can be scored and mirrored  
- High trust (0.7+): traits may be inferred (but still not shown)

**Trust governs all expression.**  
The system must earn it — not assume it.

---

### 2.3 MAEM – Measure At Every Moment

Even when the user is skipping prompts or writing “I don’t know,” the system is listening.

- Every phrase, silence, contradiction, or deflection is **data**  
- Every expression is **evidence of pacing, suppression, or emergence**

MAEM means the system watches **everything** — but acts only when safe.

It’s the difference between:
- *Monitoring* and *modeling*
- *Collecting* and *confronting*

---

### 2.4 Reflections Are Mirrors, Not Labels

No part of onboarding uses diagnostic language.  
Instead, the system generates a single **soft reflection** based on the top-scoring theme.

This reflection is:
- Short  
- Gentle  
- Emotionally true  
- Energetically resonant  
- Always written as an **invitation** — not a judgment

---

### 2.5 Conversion Is Earned

A theme does not become a trait until the system has:
- Observed the theme in multiple contexts  
- Seen the user reflect on it  
- Detected it without contradiction  
- Gained sufficient trust

Only then does the system create a trait object (in memory only), beginning arc tracking and confidence modeling.

---

### 2.6 Onboarding Is a Scene, Not a Survey

This is not intake.  
This is not assessment.

The onboarding flow is a **scene** from the Hero’s Stage:
- The user steps in  
- The ensemble (agents) listens, softly prompts, and holds  
- A moment of recognition occurs  
- The curtain closes

---

### 2.7 Safety Above All

Onboarding must never:
- Prompt too deeply too soon  
- Reflect more than the user revealed  
- Interpret when mirroring is enough  
- Offer advice, goals, or nudges  
- Expose traits, scores, types, or quadrants

The **primary output** of onboarding is:
- A reflection  
- A soft internal map of themes  
- A provisional trust score  
- Permission to continue

---

## 3. Full Session Flow  
****Entry → Prompts → Theme Detection → Reflection → Unlock****

---

This section defines the entire flow of the onboarding session from the system’s perspective — what happens, when, why, and what is stored.

---

### 3.1 Overview

The onboarding flow consists of ****five phases****:

1. ****Welcome & Containment****  
   - System greets the user and sets tone
   - No typing pressure; ambient safety is created

2. ****Prompt Sequence****  
   - 3 to 5 soft, trust-safe questions are shown one at a time  
   - User may skip any or all  
   - Prompts are tagged with possible `theme_ids`

3. ****Theme Detection & Scoring****  
   - User responses are parsed  
   - Each response is scored for 0 or more themes  
   - Signal strength is tracked across prompts

4. ****Reflection Generation****  
   - Once ≥1 theme scores ≥ 0.4  
   - A soft mirror statement is shown to the user  
   - Only one reflection is delivered

5. ****Unlock & Transition****  
   - If ≥3 prompts answered AND a reflection is generated  
   - Unlock dashboard, session access, or avatar path  
   - Trust posture is scored and stored

---

### 3.2 Visual Flow

[ User Arrives ]
↓
[ Welcome Message ] ←→ [ Silence allowed ]
↓
[ Prompt 1 ]
↓
[ Prompt 2 ]
↓
[ Prompt 3 ]
↓
[ Response(s) → Theme(s) Detected + Scored ]
↓
[ Reflection Shown ]
↓
[ Unlock Triggered → Onboarding Complete ]

---

### 3.3 Unlock Criteria

The system only transitions when all of the following are true:

- ✅ At least 3 prompts answered (not skipped)  
- ✅ One theme scored ≥ 0.4 (`signal_strength`)  
- ✅ A reflection was generated from that theme  
- ✅ Trust posture estimated ≥ 0.3

Once met, the system moves to:
- Dashboard  
- First guided session  
- Avatar selection (optional)  
- Or next format (e.g. Discovery Beat)

---

### 3.4 Data Logged from Onboarding

The following objects are written to `onboarding_state`:


{
  "theme_map": [
    {
      "theme_id": "quiet_helper",
      "signal_strength": 0.6,
      "expression_count": 2,
      "converted_to_trait": false
    }
  ],
  "answered_prompts": ["p001", "p003", "p004"],
  "skipped_prompts": ["p002"],
  "reflection_text": "You often carry things for others without showing how much it costs you.",
  "trust_posture": 0.32,
  "onboarding_complete": true
}

This is passed forward into the session system and persistent memory.

⸻

## 4. Prompt Engine  
****Delivery Rules, Metadata, and Trust Filters****

---

In the onboarding flow, prompts are the user’s first encounter with the system’s voice. They must be:

- Gentle  
- Emotionally attuned  
- Trust-safe  
- Internally tagged for theme detection  
- Skippable and non-directive

This section defines how prompts are selected, structured, filtered, and recorded.

---

### 4.1 Prompt Delivery Rules

- ****Only one prompt is shown at a time****  
- Prompts are selected from a fixed onboarding-safe list  
- User may choose to skip any prompt  
- After each prompt, the system waits for input, then proceeds  
- Prompt cadence = manual advance (not time-triggered)

---

### 4.2 Prompt Eligibility Criteria

| Field            | Constraint                        |
|------------------|-----------------------------------|
| `trust_required` | Must be ≤ 0.3                     |
| `invitation_style` | Must be `true`                 |
| `tone`           | Must be `Gentle`, `Containing`, or `Curious` |
| `trait_focus`    | Must be `null` (no trait scoring yet) |
| `theme_ids[]`    | Must be defined (1–3 per prompt) |

No prompt may contain:  
- Directive phrasing (“Do this…”)  
- Coaching tone  
- Trait language  
- Analysis triggers

---

### 4.3 Prompt Metadata Structure

Every prompt is a structured object:


{
  "prompt_id": "p-001",
  "text": "What gives you energy — even when you’re tired?",
  "theme_ids": ["creator", "dreamer", "hidden_voice"],
  "trust_required": 0.2,
  "invitation_style": true,
  "tone": "Gentle",
  "format": "Discovery Beat"
}




⸻


### 4.4 Prompt Chunking & Embedding

To support semantic retrieval (if needed):
	* 	Each prompt can be embedded as a prompt-theme chunk
	* 	Indexed by:
	* 	theme_ids[]
	* 	tone
	* 	format
	* 	trust_required
	* 	Retrieved by theme tag or emotional search if dynamic flow needed later

⸻


### 4.5 Prompt Logging

Each delivered prompt is stored in the session as:

{
  "prompt_id": "p-001",
  "delivered_at": "2025-05-06T10:21Z",
  "was_skipped": false
}

#### Used for:
•	Reflection generation
•	Prompt history
•	Memory continuity
•	Skipped prompt analysis

⸻

### 4.6 Sample Prompts (Safe for Onboarding)
	1.	“What do people often rely on you for?” → quiet_helper, overextended
	2.	“What part of you doesn’t get enough space lately?” → hidden_voice, creator
	3.	“What are you good at — but kind of tired of doing?” → structural_mind, giver
	4.	“When do you feel most like yourself?” → dreamer, authentic_mode
	5.	“What’s something you wish someone had asked you this week?” → invisible_labor, unseen_emotion

## 5. Theme Detection & Scoring  
****How the System Extracts Fuzzy Signals and Builds Confidence****

---

Themes are ****the first measurable signal**** in the Xavigate onboarding process.

This section defines how the system detects, scores, and tracks themes from user responses — without assigning traits, types, or labels.

---

### 5.1 What Is a Theme?

A ****theme**** is a soft, fuzzy identity signal.  
It is:
- Mapped from user language  
- Not shown to the user  
- Scored with confidence (0.0–1.0)  
- Used only to generate reflection and guide internal modeling

Themes can be things like:
- `quiet_helper`  
- `creator`  
- `overextended`  
- `hidden_voice`  
- `possibility_puller`

Each maps (privately) to one or more traits or forces — but ****never exposes that mapping to the user****.

---

### 5.2 Detection Pipeline

For each user response:

1. ****Extract text****  
2. ****Run matcher engine****:
   - Keyword → theme  
   - Phrase match (e.g., “I always end up taking care of things”)  
   - GPT fallback (optional)  
3. ****Score each matched theme****
4. ****Update theme***_map[]**

---

### 5.3 Scoring Logic

Each theme gets a `signal_***strength` score (0.0–1.0), initialized as follows:

| Signal Quality                 | Score Increase |
|-------------------------------|----------------|
| Direct match (strong phrase)  | +0.3           |
| Soft match                    | +0.15          |
| Repeated across prompts       | +0.1           |
| Contradiction in later prompt | −0.2           |
| Skipped prompt                | −0.05          |

Minimum theme signal to generate a reflection = ****0.4**  
Promotion to trait occurs ≥ 0.6 (post-onboarding only)

---

### 5.4 Theme Object Format


{
  "theme_id": "quiet_helper",
  "signal_strength": 0.6,
  "expression_count": 2,
  "source_prompts": ["p-001", "p-003"],
  "status": "active",
  "converted_to_trait": false,
  "last_detected": "2025-05-06T10:39:00Z"
}




⸻


### 5.5 Storage

Themes are stored in:
	* 	theme_map[] (in session memory)
	* 	Promoted to persistent memory if:
	* 	signal_strength ≥ 0.5
	* 	expression_count ≥ 2
	* 	trust_posture ≥ 0.4

⸻


### 5.6 Sample Detection Output

User responds:

“I’m always organizing things for people — but I wish I didn’t have to.”

→ Detected:
	* 	quiet_helper: +0.3
	* 	overextended: +0.25
	* 	structural_mind: +0.1

Updates stored:

{
  "theme_id": "quiet_helper",
  "signal_strength": 0.55,
  "expression_count": 1
}




## 6. Reflection Engine  
****How the System Mirrors Theme Signals Without Labeling the User****

---

Once a theme reaches sufficient signal strength, the system reflects something meaningful back to the user — not by explaining or typing them, but by ****mirroring an emotional truth****.

This section defines how that reflection is generated.

---

### 6.1 When a Reflection Is Triggered

The system generates a reflection when:

- ✅ At least one theme in `theme_map[]` has `signal_strength ≥ 0.4`  
- ✅ That theme has not been contradicted in later prompts  
- ✅ At least 3 prompts were answered  
- ✅ Trust posture ≥ 0.3 (inferred)

Only one reflection is delivered in onboarding.  
It is the user’s ****first moment of feeling seen****.

---

### 6.2 Reflection Design Principles

All onboarding reflections must be:

- ****Mirror-like**** – no interpretation, no labeling  
- ****Safe**** – written for low trust and emotional fragility  
- ****Theme-based**** – pulled from `reflection-template` matched to top `theme_id`  
- ****Narrative-consistent**** – aligned with prompt tone and avatar

****NEVER say:****
- “You’re a quiet helper”  
- “You’re an INFP”  
- “Your trait is…”  
- “I’ve detected that…”

****INSTEAD say:****
> “You seem to support others quietly — maybe even when no one notices.”

---

### 6.3 Reflection Generation Flow

1. Identify top theme with `signal_strength ≥ 0.4`  
2. Retrieve a `reflection-template` chunk from theme-indexed RAG  
3. Apply trust filter (template must be `trust_required ≤ 0.3`)  
4. Deliver modulated version to user

---

### 6.4 Template Format

Each reflection template is a chunked unit with metadata:


{
  "chunk_id": "theme_reflection_qh_001",
  "type": "reflection-template",
  "theme_ids": ["quiet_helper"],
  "trust_required": 0.3,
  "tone": "gentle",
  "text": "You seem to show up quietly for others — even when it’s not easy to carry what you’re holding."
}

These are never generated on the fly — they are prewritten for emotional safety and vetted.

⸻


## 6.5 Sample Reflections by Theme

#### Theme: quiet_helper

“You often support others without needing attention — but that doesn’t mean you don’t deserve some.”

#### Theme: creator

“There may be a part of you that wants to bring something new into the world — but hasn’t had room to yet.”

#### Theme: hidden_voice

“It sounds like something in you might want to be heard — even if it’s been quiet for a long time.”

⸻


### 6.6 Logging the Reflection

Store reflection metadata in onboarding_state:

{
  "reflection_text": "You seem to support others quietly — even when no one sees it.",
  "reflected_theme_id": "quiet_helper",
  "reflection_time": "2025-05-06T10:43Z"
}



## 7. Theme Memory Structure  
****How Themes Are Tracked Over Time and Across Sessions****

---

This section defines how themes — once detected — are stored, updated, and transitioned into longer-term modeling.

Themes begin as ****session-scoped**** signals but may persist and evolve across sessions if they show up consistently and clearly.

---

### 7.1 Memory Layers

There are two layers of theme memory:

| Type         | Scope      | Usage                          |
|--------------|------------|--------------------------------|
| Volatile     | Session    | Used for real-time scoring and reflection  
| Persistent   | Cross-session | Used for tracking resolution, trait eligibility, narrative recall  

---

### 7.2 Volatile Theme Storage (`theme*_map[]`)

Themes detected during onboarding are stored in the session’s `theme_*map[]`.

Each theme includes:


{
  "theme_id": "quiet_helper",
  "signal_strength": 0.58,
  "expression_count": 2,
  "status": "active",
  "converted_to_trait": false,
  "source_prompts": ["p-001", "p-003"],
  "last_detected": "2025-05-06T10:46:00Z"
}

#### Fields:
	* 	theme_id: short slug (e.g., "overextended", "hidden_voice")
	* 	signal_strength: 0.00–1.00, confidence of match
	* 	expression_count: how many unique prompts expressed this theme
	* 	status: "active", "dormant", "resolved"
	* 	converted_to_trait: boolean
	* 	source_prompts[]: list of prompt_ids
	* 	last_detected: ISO timestamp

⸻


### 7.3 Persistent Storage Criteria

Themes are promoted to persistent memory if:
	* 	signal_strength ≥ 0.5
	* 	Seen in ≥2 sessions
	* 	No active contradiction flags
	* 	Trust posture ≥ 0.4
	* 	Expression not decayed in last 2 sessions

If promoted, themes are stored under:

user_profile.themes[] = {
  theme_id,
  signal_history,
  resolution_status,
  trait_candidate_id (optional),
  last_updated
}




⸻


### 7.4 Status Field Usage

Status	Meaning
active	Theme is current and may generate reflection
dormant	Signal has faded, not expressed in 2+ sessions
resolved	Theme converted into trait (via conversion rules)




⸻


### 7.5 Theme Decay

If a theme is not re-expressed:
	* 	−0.05 signal_strength per inactive session
	* 	Downgrade to dormant if:
	* 	signal_strength < 0.3
	* 	No activity for 3 sessions
	* 	User contradicts it explicitly

Decayed themes are not deleted. They may reactivate if new evidence appears.

⸻


### 7.6 Memory Summary Example

{
  "user_id": "u-29401",
  "theme_memory": {
    "quiet_helper": {
      "signal_strength": 0.58,
      "expression_count": 3,
      "status": "active",
      "converted_to_trait": false,
      "last_detected": "2025-05-06"
    },
    "creator": {
      "signal_strength": 0.62,
      "expression_count": 2,
      "status": "resolved",
      "converted_to_trait": true,
      "resolved_trait_id": "Creative"
    }
  }
}



## 8. Unlock Logic

**When the User Is Ready to Proceed and What Happens Next**

⸻

This section defines the precise conditions under which the onboarding flow completes and the user is transitioned into the full Xavigate experience.

Unlocking is not based on form completion — it’s based on *readiness signals*.

⸻

### **8.1 Unlock Conditions**

The system will unlock the next phase of experience only when **all** of the following are true:
	* 	At least **3 prompts have been answered** (not skipped)
	* 	At least **one theme** in theme_map[] has signal_strength ≥ 0.4
	* 	A reflection has been generated and delivered
	* 	Trust posture (inferred) is **≥ 0.3**

These conditions ensure that the user:
	* 	Has engaged meaningfully
	* 	Has received a relevant mirror
	* 	Has shown emotional openness
	* 	Has not been rushed or bypassed

⸻

### **8.2 Unlockable Destinations**

Once onboarding completes, the system can route the user to:
	* 	**Main Dashboard** – overview of their alignment tools
	* 	**First Guided Session** – with adjusted format (Discovery Beat)
	* 	**Avatar Selection Path** – if persona constraints are being applied
	* 	**Exploration Mode** – light, curiosity-based reflection session

Destination is determined by system settings, use case, or trust profile.

⸻

### **8.3 Transition Messaging (UI Copy)**

Example messages shown to the user after unlocking:
	* 	“Thanks for sharing. Based on what you said, we have something to show you.”
	* 	“You might not realize it, but what you just shared tells us a lot.”
	* 	“Let’s keep going — there’s something quietly forming.”

These are soft, non-analytical transitions. No scoring or insight should be declared here.

⸻

### **8.4 Unlock Metadata Logging**

Upon successful onboarding, the following block is added to memory:

onboarding_complete: true
trust_posture: 0.34
top_theme: “quiet_helper”
reflection_shown: true
unlock_time: “2025-05-06T10:48:00Z”
next_scene_format: “Discovery Beat”

⸻

### **8.5 If Unlock Criteria Are Not Met**

If user:
	* 	Skips all prompts
	* 	Never expresses a theme clearly
	* 	Does not trigger a reflection

Then:
	* 	System gently pauses onboarding
	* 	Offers soft fallback:
“No need to rush. We can come back to this later.”
	* 	Records:
onboarding_complete: false
trust_posture: 0.1
fallback_triggered: true

On next session start, system resumes onboarding with stored responses intact.

⸻

## 9. Trust Initialization

**How the System Establishes Safe Depth for Session 0**

⸻

Trust is a **hidden core variable** that governs which parts of the system can activate — including prompts, agents, nudges, and memory writes.

During onboarding, trust is never shown to the user — but it is **measured and updated** behind the scenes.

⸻

### 9.1 What Is Trust?
	* 	A decimal value: trust_posture = 0.00 – 1.00
	* 	Starts at **0.0** by default
	* 	Slowly increases based on:
	* 	Reflection depth
	* 	Openness of language
	* 	Acceptance of prompts
	* 	Emotional signals (warmth, honesty, curiosity)

⸻

### 9.2 Trust Score Tiers in Onboarding

**Trust Range**	**Meaning**	**System Behavior**
0.00–0.29	Guarded / Uncertain	Only safe prompts shown; reflection delayed
0.30–0.49	Receptive	Themes may be reflected; unlock enabled
0.50–0.69	Open	Trait tracking begins (internal only)
0.70+	Trust Deep	Ready for next format (e.g., Spiral Return)

Typical onboarding sessions result in trust scores between **0.3–0.4**.

⸻

### 9.3 What Affects Trust During Onboarding

**Event Type**	**Trust Change**
Prompt answered with insight	+0.05
Prompt skipped	−0.01
Reflection matched by user	+0.04
User shows resistance (e.g., “I don’t know”)	−0.03
Repeated evasion or shutdown	−0.05

Trust changes are clamped:
	* 	Minimum increment: ±0.01
	* 	Maximum increment: ±0.06 per interaction

⸻

### 9.4 Logging Trust Posture

At the end of onboarding, store:

trust_posture: 0.34
trust_history[]:
	* 	t1: 0.00 (start)
	* 	t2: 0.08 (after 1st prompt)
	* 	t3: 0.19 (after 2nd prompt)
	* 	t4: 0.34 (post-reflection)

This is written to user_profile.trust_log for the Director and Conductor to read in the next session.

⸻

### 9.5 Trust and Agent Activation

In Session 0:
	* 	Only the following agents are allowed to activate:
	* 	Usher
	* 	Prompter
	* 	Voice Coach
	* 	Conductor
	* 	Archivist

All other agents (Dramaturg, Script Doctor, Movement Director, etc.) are **suppressed** until trust ≥ 0.5.

⸻

### 9.6 Carryover

Trust posture is passed forward into:
	* 	First full session (for pacing and prompt gating)
	* 	Avatar suggestions
	* 	Nudge eligibility (suppressed if trust < 0.6)
	* 	Memory access permissions

⸻
### 10. Memory Schema & Logging

**What Gets Saved, Where, and Why**

⸻

This section defines how onboarding session data is recorded in memory — both **volatile** (session-only) and **persistent** (cross-session).

It ensures that:
	* 	Reflections and signals can influence future sessions
	* 	Trust and themes are carried forward
	* 	Nothing is over-stored or prematurely typed

⸻

### 10.1 Memory Layers Used

**Memory Type**	**Scope**	**Purpose**
Volatile	Session-only	Real-time flow, prompt tracking
Persistent	Cross-session	Theme history, trust evolution, coaching



⸻

### 10.2 Onboarding State Object (Volatile)

During the session, all onboarding data is stored in a single state object:

onboarding_state = {
answered_prompts[]: [“p-001”, “p-002”, “p-004”],
skipped_prompts[]: [“p-003”],
theme_map[]: [
{
theme_id: “quiet_helper”,
signal_strength: 0.58,
expression_count: 2,
status: “active”
}
],
reflection_text: “You seem to support others quietly — even when it takes something from you.”,
reflection_shown: true,
trust_posture: 0.34,
unlock_triggered: true
}

This is cleared from volatile memory after onboarding concludes.

⸻

### 10.3 Persistent Memory (User Profile)

If onboarding completes successfully, the following items are written to user_profile:

user_profile = {
themes[]: [
{
theme_id: “quiet_helper”,
signal_strength: 0.58,
expression_count: 2,
last_detected: “2025-05-06”
}
],
last_reflection: “You seem to support others quietly…”,
trust_history[]: [0.00, 0.08, 0.19, 0.34],
onboarding_complete: true,
onboarding_timestamp: “2025-05-06T10:50Z”
}

⸻

### 10.4 Additional Logging

Other fields that should be logged for developer tools, debugging, or analysis:
	* 	prompt_history[]: { prompt_id, was_skipped, timestamp }
	* 	reflection_theme_id: e.g., “quiet_helper”
	* 	fallback_triggered: true/false
	* 	trust_score_delta: net gain across session
	* 	theme_conflict_flags[] (if any signals were inconsistent)

⸻

### 10.5 Logging Failure Cases

If onboarding fails (user skips all, leaves early, or does not reflect):

onboarding_complete: false
reason: “insufficient engagement”
fallback_mode: “containment”
theme_map[]: []

This lets the next session know to **retry gently** — not to continue as if onboarding succeeded.

⸻

### 10.6 Memory Access by Other Agents

Post-onboarding, the following agents can access this data:
	* 	**Conductor** – for pacing
	* 	**Director** – to select scene format
	* 	**Prompter** – to avoid repeating initial prompts
	* 	**Archivist** – to begin trait arc tracking
	* 	**Role Coach** – to suggest persona constraints
	* 	**Movement Director** – only if trust > 0.6 (and only reads trust_posture)

⸻

## 11. Theme-to-Trait Conversion

**Rules for Promoting a Theme into Trait Confidence**

⸻

Themes begin as **early signals** of personality energy — safe, soft, and intentionally fuzzy.

But once onboarding is complete, some of those themes may become **candidates for trait resolution**, contributing to the user’s evolving trait confidence map.

This section defines when and how that promotion happens.

⸻

### 11.1 Conversion Conditions

A theme may convert into a trait only if **all of the following** are true:

**Requirement**	**Threshold**
signal_strength	≥ 0.6
expression_count	≥ 2 across different prompts
sessions_seen	≥ 2 (theme reappears post-onboarding)
trust_posture	≥ 0.5
conflict_flags[]	none active
theme_status	"active"

If these are met, the system creates or updates a trait confidence object.

⸻

### 11.2 Conversion Workflow
	1.	Detect eligible theme from persistent memory
	2.	Map theme to trait using 06.8.1_Theme_Taxonomy.md
	3.	Create a new trait entry in trait_confidence_map
	4.	Set arc_phase = tentative
	5.	Initialize confidence = theme.signal_strength - 0.1
	6.	Flag theme as converted_to_trait = true
	7.	Update theme.status = resolved

⸻

### 11.3 Trait Block Output Example

From theme: quiet_helper

Produces:

{
“trait_id”: “Providing”,
“confidence”: 0.48,
“arc_phase”: “tentative”,
“suppression_score”: 0.0,
“expression_field_map”: { “Social”: 0.4 },
“converted_from_theme”: “quiet_helper”
}

This new trait can now evolve independently — but still references its theme origin.

⸻

### 11.4 Post-Conversion Behavior
	* 	Reflections should still refer to *themes*, unless trust ≥ 0.75
	* 	Trait data is now available to:
	* 	Prompter (prompt filtering)
	* 	Script Doctor (suppression detection)
	* 	Director (arc planning)
	* 	Archivist (memory tracking)
	* 	Prompts are still gated by trust, arc phase, and tone
	* 	No trait-based reflection is shown unless the user has initiated naming that trait themselves

⸻

### 11.5 Conflict Handling and Reversion

If a theme converts but later becomes:
	* 	contradicted
	* 	suppressed
	* 	unresolved over 3 sessions

→ its trait_confidence decays, and the system may:
	* 	Set arc_phase = “tentative” or “latent”
	* 	Mark theme.status = “dormant”
	* 	Optionally demote the trait object (but never delete)

⸻

### 11.6 Conversion Log

Each theme → trait conversion should be logged:

{
“event”: “theme_promoted”,
“theme_id”: “quiet_helper”,
“trait_id”: “Providing”,
“timestamp”: “2025-05-06T11:00Z”,
“confidence_at_creation”: 0.48
}

Stored in:
	* 	user_profile.conversion_log[]
	* 	archivist.trait_origin[] (for arc tracking)

⸻

### 11.7 Trait Visibility

Converted traits are **internal only** until:
	* 	Trust ≥ 0.75
	* 	User initiates reflection about the trait
	* 	A coach requests access
	* 	Trait reaches arc_phase = validated and is reinforced in multiple fields/modes

Even then, **reflections remain metaphorical or energetic** — never categorical.

⸻

## 12. Chunking & Retrieval

How Prompts, Reflections, and Themes Are Embedded for Future Use

⸻

This section explains how theme-based content in the onboarding flow is prepared for embedding and retrieval using RAG (Retrieval-Augmented Generation) tools.

The goal is to allow Xavigate to retrieve:
	* 	Theme-linked prompts
	* 	Matching reflection templates
	* 	Archetype examples
	* 	Internal theme definitions

All of this supports scalable mirroring, safe retrieval, and semantic coherence.

⸻

### **12.1 What to Chunk**

Chunk the following onboarding-related elements:

**Content Type**	**Purpose**
prompt-theme chunks	Prompts linked to theme_ids
reflection templates	Pre-written mirror messages per theme
theme definitions	Internal descriptions for classification
archetype examples	Natural language expressions tagged with themes



⸻

### **12.2 Chunk Format**

Each chunk should contain:
	* 	chunk_id
	* 	type: one of prompt-theme, reflection-template, theme-definition, theme-archetype
	* 	text: full content to embed
	* 	metadata:
	* 	theme_ids[]
	* 	tone
	* 	trust_required
	* 	format (optional)

Example:

{
“chunk_id”: “reflect_qh_001”,
“type”: “reflection-template”,
“theme_ids”: [“quiet_helper”],
“trust_required”: 0.3,
“tone”: “gentle”,
“text”: “You seem to support others without expecting anything back — but that doesn’t mean it’s easy.”
}

⸻

### **12.3 Embedding Specs**
	* 	Embed using OpenAI text-embedding-3-small or similar
	* 	Recommended chunk size: 100–400 tokens
	* 	Chunk once per prompt or reflection template
	* 	Attach theme_ids[] as metadata for filtering

⸻

### **12.4 Retrieval Use Cases**

Use semantic search to:
	* 	Select a prompt that matches a detected theme
	* 	Retrieve a reflection template for highest-confidence theme
	* 	Feed GPT examples of similar users or reflections
	* 	Provide coach-facing summaries

⸻

### **12.5 Retrieval Filters**

When retrieving chunks:
	* 	match theme_ids[] to top themes in theme_map[]
	* 	respect trust_required ≤ user.trust_posture
	* 	match tone to current persona constraint
	* 	prefer content not previously used in session

⸻

### **12.6 Chunk Management**

Track metadata per chunk:
	* 	last_used
	* 	usage_count
	* 	impact_rating (optional — based on user reactions)
	* 	flag for review (if mismatch or user skips reflection)

Flag underperforming chunks for rewrite if:
	* 	skipped > 3x
	* 	no reflection depth detected
	* 	mismatch with tone or quadrant

⸻

### **12.7 Sample Chunks**

Prompt-Theme:

{
“chunk_id”: “prompt_qh_001”,
“type”: “prompt-theme”,
“theme_ids”: [“quiet_helper”],
“text”: “What do people often rely on you for?”,
“tone”: “curious”,
“trust_required”: 0.2
}

Reflection Template:

{
“chunk_id”: “reflect_qh_002”,
“type”: “reflection-template”,
“theme_ids”: [“quiet_helper”],
“text”: “You often carry others — but maybe there’s a part of you that’s asking to be carried too.”,
“trust_required”: 0.3,
“tone”: “gentle”
}

⸻

### **12.8 Chunk Visibility**

Only these agents may use embedded content from theme chunks:
	* 	Prompter — to select prompts
	* 	Reflection Generator — to deliver mirrors
	* 	Script Supervisor — to store matching threads
	* 	Archivist — to track content usage

Coach sync tools may access chunks only if trust ≥ 0.75 and user consents.

⸻
