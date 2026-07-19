# The-Mesh
The Mesh educational game
📘 The Mesh — Crisis Simulation Engine & Educational Game
The Mesh is an interactive crisis‑simulation engine designed for classrooms, universities, and corporate leadership development.
It blends network science, game theory, LLM‑driven narration, and real‑world crisis scenarios to teach decision‑making, coordination, negotiation, and resilience under pressure.

The Mesh is built as a modular, extensible engine where JSON schemas define gameplay actions, and Python modules execute the logic, update the graph, and generate narrative feedback.

🌐 What The Mesh Is
The Mesh is:

A turn‑based crisis simulation where players act as nodes in a dynamic network.

A graph‑driven system where actions modify relationships, resources, trust, and threat levels.

A narrative engine that explains consequences, forecasts risks, and guides players.

A teaching tool for:

crisis leadership

negotiation

coalition‑building

ethical decision‑making

resource management

systems thinking

The Mesh can run:

Classroom Mode — collaborative learning, guided facilitation, structured crisis cycles.

Corporate Mode — high‑pressure scenarios, competitive negotiation, complex resource constraints.

⚙️ How the Engine Works
The Mesh engine processes each turn through a unified pipeline:

Players submit actions  
(Actions are defined in /schemas/actions/*.json)

Actions are validated

Schema validation

Rule checks

Difficulty scaling

Context checks

Impacts are applied to the graph

NetworkX graph updates

Trust, threat, resources, alliances

Node merges, splits, coordination models

Narrator generates feedback

Consequences

Forecasts

Threat decay

Narrative hooks

Crisis loop updates global state

Crisis escalation

Protocol triggers

Emergency overrides

Scenario progression

Turn cycle advances

New actions unlocked

New constraints applied

New crisis events introduced

▶️ How to Run It
The Mesh is modular. A typical run looks like:

bash
python main.py
Your repo currently contains:

Turn-Cycle-Engine.py

Full-Crisis-Processing-Loop.py

Crisis-Based-Leadership-Loop.py

Classroom-orchestration-loop.py

Once you create main.py, it should:

Load a scenario (e.g., University-Crisis-Scenarios.json)

Initialize the graph (Dynamic-Graph-Initialization.py)

Start the crisis loop

Process player actions

Call the narrator pipeline

Advance turns until resolution

I can generate main.py for you if you want.

🧩 How JSON Schemas Map to Gameplay
Your JSON files define the rules of the world.

Action Schemas (/schemas/actions/)
Examples:

Arbitration.json

Resource-Bidding.json

Trust-Pledge.json

Voting.json

These define:

allowed parameters

required fields

difficulty modifiers

impact types

narrative hooks

Protocol Schemas (/schemas/protocols/)
Examples:

Emergency-Protocol.json

Ethical-Sourcing-Audit.json

Carbon-Rebalance.json

These define:

crisis triggers

escalation rules

override conditions

global impacts

Scenario Schemas
Examples:

Corp-Crisis-Scenarios.json

University-Crisis-Scenarios.json

These define:

initial graph

crisis events

win/loss conditions

resource pools

The Python logic files read these schemas and execute the mechanics.

                   ┌──────────────────────────┐
                   │      JSON Schemas        │
                   │ actions / protocols      │
                   │ crisis scenarios         │
                   └─────────────┬────────────┘
                                 │
                                 ▼
                     ┌────────────────────┐
                     │   Action Engine    │
                     │  (mechanics/*.py)  │
                     └──────────┬─────────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │   Impact Engine    │
                     │  (impact/*.py)     │
                     └──────────┬─────────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │   Graph Model      │
                     │ (NetworkX updates) │
                     └──────────┬─────────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │   Narrator Engine  │
                     │ narrator/*.py      │
                     └──────────┬─────────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │   Crisis Loop      │
                     │ turn_cycle.py      │
                     └──────────┬─────────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │   Classroom/Corp   │
                     │   Mode Overlay     │
                     └────────────────────┘

🔄 Example Turn Cycle
Turn 1
Players submit:

Arbitration

Resource Bidding

Trust Pledge

Knowledge Exchange

Engine Processing
Validate schemas

Apply impacts

Update graph

Narrator generates:

consequences

threat decay

new crisis forecast

Turn 2
Crisis escalates

Emergency Protocol triggers

New actions unlocked

New constraints applied

Turn 3
Coalition formation

Reputation broadcast

Node merge

Voting event

And so on until resolution.

🔥 Example Crisis Scenario
Scenario: “Cyberattack on University Infrastructure”

From University-Crisis-Scenarios.json:

Threat Level: High

Impacted Nodes: IT, Finance, Student Services

Constraints:

limited bandwidth

misinformation spread

resource scarcity

Players must:

coordinate patch deployment

negotiate resource routing

manage trust between departments

stabilize the network

The Finance node’s decision to withhold resources increased local threat by 12%.
Student Services formed a coalition with IT, reducing misinformation spread.
Network stability improved, but a secondary breach is now likely within 2 turns.
Recommend initiating Emergency Protocol: Patch Deployment.
The narrator blends:

graph updates

crisis logic

threat forecasting

narrative hooks

🏫 Classroom Mode vs 🏢 Corporate Mode
Classroom Mode
Guided facilitation

Lower difficulty scaling

More narrative explanation

Collaborative decision-making

Educational pacing

Corporate Mode
Competitive negotiation

Higher stakes

Aggressive crisis escalation

Resource scarcity

Realistic leadership pressure

Both modes use the same engine with different overlays.

🛣️ Roadmap
Phase 1 — Core Engine (Complete)
Action schemas

Impact models

Graph updates

Narrator pipeline

Crisis loops

Phase 2 — Classroom & Corporate Modules (In Progress)
Classroom syllabus

Facilitator guide

Corporate scenario pack

Phase 3 — UI + Dashboard
Web interface

Real-time graph visualization

Player dashboards

Phase 4 — Multiplayer
Websocket-based turn submission

Team negotiation rooms

Phase 5 — AI Scenario Generator
Auto-generate crisis scenarios

Difficulty tuning

Adaptive narration

🤝 Contribution Guidelines
Fork the repo

Create feature branches

Follow the folder structure:

/schemas for JSON

/engine for core logic

/mechanics for actions

/docs for documentation

Add tests for new mechanics

Document new schemas

Submit a pull request with:

description

example turn

impact model notes
