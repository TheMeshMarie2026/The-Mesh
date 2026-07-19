🕸️ The Mesh
A Crisis Simulation Engine for Collective Intelligence, Adaptive Leadership, and Networked Decision‑Making
The Mesh is a modular, graph‑driven crisis simulation engine.
It models how teams, institutions, and coalitions respond to dynamic, multi‑layered crises — and how their decisions reshape the network around them.

At its core, The Mesh blends:

NetworkX graph modeling

LLM‑driven narration and validation

Action mechanics and protocol execution

Impact propagation across nodes and edges

Scenario‑based crisis orchestration

The result is a living simulation where every choice alters trust, resources, relationships, and future possibilities.

🌳 Repository Structure
The Mesh is organized into clear, functional layers.
Each folder represents a subsystem of the engine.

Code
The-Mesh-REPO/
│
├── main.py
├── requirements.txt
├── LICENSE
│
├── engine/
│   ├── graph/
│   ├── impact/
│   ├── narrator/
│   └── (core orchestrators)
│
├── mechanics/
│
├── schemas/
│   ├── actions/
│   ├── protocols/
│   └── scenarios/
│
├── docs/
│
└── assets/
Below is a breakdown of each subsystem.

⚙️ engine/ — Core Orchestration Layer
The engine coordinates the entire simulation:

turn cycles

crisis loops

LLM connectors

scenario overlays

protocol dynamics

This is where the game actually runs.

Includes:
game-Blueprint-wrapper-main-game.py

Phase-2-LLM-Connector.py

Student-VS-Corporate-Overlay.py

Protocol-Dynamics.py

🧩 engine/graph/ — Dynamic Graph System
The Mesh represents every crisis as a living graph:

nodes = actors

edges = relationships

attributes = trust, resources, influence

assets = capabilities or constraints

This folder contains everything that builds, mutates, or analyzes the graph.

Includes:
asset-features.py

Cross-Node-Coordination-Model.py

Node-Merge.py

Node-Merge.json

Technical-Infrastructure-Models.py

Network-Scan.json (graph utility)

🔥 engine/impact/ — Impact Modeling & Propagation
Every action produces ripple effects across the network.
This subsystem calculates and applies those effects.

Includes:
Balance-Carbon-Units.py

Difficulty-Levels.py

Difficulty-Scaling.py

Turns-ThreatDecay-NarrativeHooks.py

🎙️ engine/narrator/ — LLM Narration & Validation
The narrator interprets actions, generates story beats, and validates outputs against the graph.

Includes:
Python-Prompt-Loader.py

SR-PROMPT-VERIFICATION-AT-MULTIPLE-GRAPH-LEVELS.py

Lovable-Prompt-Registry.yaml

🛠️ mechanics/ — Action Implementations
Mechanics are the executable behaviors behind each action schema.
They define how an action actually affects the graph.

Includes:
Classroom-Team-Negotiation.py

Conflict-Negotiation.py

Information-Sharing.py

Intelligence.py

Knowledge-Pooling-Mechanic.py

Resource-Routing-Engine.py

Resource-Routing-Negotiation-Trigger.py

SR-Demonstration.py

Crisis-Forecast.py

PROCUREMENT-Data-DRIVERS.py

Rules-Checklist.py

📜 schemas/ — JSON Definitions
Schemas define the structure of actions, protocols, and scenarios.

actions/
Single-step actions with "action_type":

Crisis-Forecast.json

Intelligence-Sprint.json

JSON-Schema-Advanced-Gameplay-Actions.json

Referendum-Voting.json

PayloadPassing.json

protocols/
Multi-step procedures:

Patch-Deployment.json

Protocol-Rewrite.json

N8n-schema.json

scenarios/
Full crisis setups:

(Add your scenario JSONs here)

📚 docs/ — Documentation & Notes
Human-readable guides, architecture notes, and workflow explanations.

Includes:
N8n-JSON-notes.txt

(Add your other docs here)

🎒 assets/ — External Utilities
Non-Python helpers, API wrappers, and JS utilities.

Includes:
deterministic-safe-response.js

Lovable-n8n-API-wrapper.py

🚀 Running The Mesh
The entry point is:

Code
python main.py
Main handles:

loading scenarios

initializing the graph

registering mechanics

loading schemas

starting the crisis loop

invoking the narrator

applying impacts

updating the graph state

🧠 Core Concepts
Actions
Atomic decisions taken by nodes.
Defined in schemas/actions/, executed in mechanics/.

Protocols
Multi-step procedures (audits, deployments, escalations).
Defined in schemas/protocols/.

Scenarios
Crisis worlds with initial conditions.
Defined in schemas/scenarios/.

Impacts
Changes to trust, resources, edge weights, or node attributes.
Processed in engine/impact/.

Narration
LLM-driven interpretation of events.
Handled in engine/narrator/.

Graph State
The living network that evolves with every decision.
Managed in engine/graph/.

🛠️ Extending The Mesh
You can add:

New Actions
Create a JSON schema in schemas/actions/

Implement the mechanic in mechanics/

Add narrator prompts in engine/narrator/

New Protocols
Add a JSON file to schemas/protocols/.

New Scenarios
Add a JSON file to schemas/scenarios/.

New Graph Features
Add Python modules to engine/graph/.

🖤 About the Project
The Mesh is built for:

crisis leadership training

collective intelligence research

organizational resilience modeling

classroom simulations

enterprise decision-making games

narrative-driven crisis storytelling

It is modular, extensible, and designed for experimentation.