import sys
import uuid
import asyncio
from typing import Dict, Any, List

# =====================================================================
# INTERFACE BINDING LOADS: LINKING SYSTEM MODULES
# =====================================================================
from heterarchy_engine import HeterarchyEngine
from turn_controller import TurnController
from difficulty_tuner import DifficultyTuner
from agent_registration_pipeline import AgentRegistrationPipeline
from network_topology_spawner import NetworkTopologySpawner
from llm_prompt_bridge import LLMNarrativeBridge
from llm_client import HeterarchyLLMClient
from telemetry_logger import TelemetryLogger
from heterarchy_visualizer import HeterarchyVisualizer

# Importing our new live scraping procurement modules
from market_drivers import ProcurementNetworkDrivers
from procurement_scraper import ProcurementScraperEngine

def run_clear_banner():
    print("\n" * 2)
    print("=====================================================================")
    print("      GLOBAL CRISIS RESOLUTION FRAMEWORK - HETERARCHY ENGINE PROTO   ")
    print("=====================================================================")

async def execute_procurement_market_phase(player_id: str, current_crisis_type: str, engine: Any):
    """
    Feature Integration Window: Scrapes live web feeds, customizes priority, 
    and handles spending node capital directly during a turn phase execution.
    """
    print(f"\n🛒 [MARKET ENTRY]: Querying web markets for current trend: '{current_crisis_type}'...")
    
    # Initialize procurement layers
    drivers = ProcurementNetworkDrivers()
    scraper_logic = ProcurementScraperEngine(engine)
    
    # 1. Asynchronously fetch live listings from across the web
    tasks = [
        drivers.fetch_live_material_resources(current_crisis_type),
        drivers.fetch_live_knowledge_archives(current_crisis_type),
        drivers.fetch_live_talent_leadership(current_crisis_type)
    ]
    resources, knowledge, talent = await asyncio.gather(*tasks)
    
    raw_listings = {
        "RESOURCES": resources,
        "KNOWLEDGE": knowledge,
        "TALENT_LEADERSHIP": talent
    }
    
    # 2. Score and contextually prioritize listings using internal matrix parameters
    prioritized_data = scraper_logic.prioritize_listings_by_utility(raw_listings, current_crisis_type, player_id)
    
    # Flatten everything into a single indexed list for clear terminal interactions
    flat_market_catalog: List[Dict[str, Any]] = []
    for category, items in prioritized_data.items():
        for i in items:
            i["category_vector"] = category
            flat_market_catalog.append(i)
            
    if not flat_market_catalog:
        print(" -> Warning: No external listings scraped due to network timeout limits. Skipping marketplace phase.")
        return

    # 3. Present the live market pricing matrix ledger window
    print("\n" + "="*95)
    print(f" LIVE WEB-SCRAPED MARKETPLACE LEDGER (Active Crisis Vector Focus: {current_crisis_type})")
    print("="*95)
    print(f"{'ID':<3} | {'Item Listing Profile Description':<40} | {'Category':<15} | {'Type':<5} | {'Cost':<10} | {'Priority':<8}")
    print("-" * 95)
    
    # Sort options by cost ascending so cheap entries/open access bubble up first
    flat_market_catalog = sorted(flat_market_catalog, key=lambda x: x["base_cost"])
    
    for idx, item in enumerate(flat_market_catalog, 1):
        print(f" [{idx}] | {item['title'][:38]:<40} | {item['category_vector']:<15} | {item['type']:<5} | ${item['base_cost']:<9.2f} | {item['priority_utility_score']:<8}")

    player_wallet = engine.network.nodes[player_id].get("resources", 0.0)
    print(f"\nYour current Node Financial Reserves Available: ${player_wallet:.2f}")
    
    market_input = input("Enter an item ID to purchase/rent, or press [ENTER] to skip this phase: ").strip()
    if not market_input or not market_input.isdigit():
        print("Skipping procurement step. Progressing straight to narrative loop...")
        return

    item_selection_id = int(market_input)
    if 1 <= item_selection_id <= len(flat_market_catalog):
        target_item = flat_market_catalog[item_selection_id - 1]
        cost = target_item["base_cost"]
        
        # 4. Enforce financial guardrails and process procurement transactions
        if player_wallet >= cost:
            # Deduct capital from the player's active network graph node
            engine.network.nodes[player_id]["resources"] = round(player_wallet - cost, 2)
            print(f" -> Transaction Processed: Spending ${cost:.2f} on item '{target_item['title']}'...")
            
            # Apply programmatic inventory/knowledge state mutations based on asset type
            if target_item["type"] == "BUY": # Material items
                item_name = f"SCRAPED_{current_crisis_type}_ASSET"
                engine.adjust_node_inventory(player_id, item_name, delta=50.0)
                print(f" -> Success: Added 50 units of {item_name} directly to your warehouse inventory ledger.")
                
            elif target_item["type"] == "RENT": # Knowledge or talent subscriptions
                # If they bought expertise, update the global Knowledge Commons directly
                current_kb = engine.knowledge_commons.get(current_crisis_type, 0.0)
                engine.knowledge_commons[current_crisis_type] = min(1.0, current_kb + 0.15)
                print(f" -> Success: Node synchronized. Global Knowledge Commons for '{current_crisis_type}' boosted by +15%.")
        else:
            print("❌ Transaction Blocked: Insufficient financial resources at node to fulfill transaction.")
    else:
        print("Invalid item registration coordinates. Skipping marketplace processing steps.")

async def start_game_session():
    # 1. Initialize Base Data Structure Engine Layers
    engine = HeterarchyEngine()
    turn_loop = TurnController(engine)
    telemetry = TelemetryLogger()
    session_id = f"PLAYTEST_{uuid.uuid4().hex[:8].upper()}"
    
    run_clear_banner()
    print(f"Initializing secure playtest session: [{session_id}]...")

    # 2. UI Configuration Capture Phase (Matching your screen mockup format)
    username = input("Enter Agent Designation (username): ").strip()
    if not username: username = "Beta_Tester_Alpha"
    
    print("\nAvailable Domains: CLIMATE, HEALTH, ECONOMICS, TECHNOLOGY, POLICY, EDUCATION, FOOD, WATER, CONFLICT")
    selected_domain = input("Select Primary Domain allocation: ").strip().upper()
    if not selected_domain: selected_domain = "ECONOMICS"
    
    mission_brief = input("Describe your motivation (Optional Mission Brief): ").strip()
    
    print("\nTarget Playtest Persona Profile [1-2]:\n [1] Corporate Leaders\n [2] University Students")
    profile_choice = input("Choice: ").strip()
    audience_profile = "Corporate Leaders" if profile_choice == "1" else "University Students"
    
    print("\nFramework Scale Difficulty Selector [1-3]:\n [1] Local Community (Easy)\n [2] National Scope (Medium)\n [3] Global Network (Hard)")
    scale_choice = input("Choice: ").strip()
    scale_mapping = {"1": "local", "2": "national", "3": "global"}
    scale_level = scale_mapping.get(scale_choice, "local")

    # 3. Dynamic Optimization Rule Filter Scaling Injections
    profile_config = DifficultyTuner.apply_combined_tuning(engine, turn_loop, audience_profile, scale_level)

    # 4. Process Agent UI Registration Injection
    registration_suite = AgentRegistrationPipeline(engine, DifficultyTuner)
    reg_receipt = registration_suite.register_user_agent(username, selected_domain, mission_brief, audience_profile)
    player_node_id = reg_receipt["assigned_id"]
    
    # Seeding some initial starting resources into the player node to test market purchasing power
    engine.network.nodes[player_node_id]["resources"] = 5000.0 

    # 5. Execute Scale-Free Topology Procedural Network Grid Assembly
    spawner = NetworkTopologySpawner(engine)
    spawner.spawn_network_mesh(profile_config, player_node_id)

    # 6. Seed a Global Macro Crisis Core
    turn_loop.set_crisis(crisis_type=selected_domain, severity=0.5, demands={selected_domain: 0.75})
    
    # 7. Setup Live Remote LLM API Clients
    llm_connector = HeterarchyLLMClient(provider="openai") 
    narrative_bridge = LLMNarrativeBridge(target_profile=audience_profile, scale_level=scale_level)

    # =====================================================================
    # PRIMARY CORE LOOP CYCLE EXECUTION LAYER WITH INTEGRATED PROCUREMENTS
    # =====================================================================
    MAX_TURNS = 3
    for current_turn_step in range(1, MAX_TURNS + 1):
        print(f"\n=====================================================================")
        print(f"🔄 PLAYING TURN CYCLE TIMELINE: [TURN {turn_loop.current_turn} / {MAX_TURNS}]")
        print("=====================================================================")
        
        # A. Run background network structural calculations (Decays, resource drains)
        turn_snapshot = turn_loop.advanced_turn_loop()
        if turn_snapshot["game_status"] in ["VICTORY", "COLLAPSE"]:
            print(f"\n🚨 Game terminated via state check: {turn_snapshot['game_status']}")
            break

        # NEW STEP INTEGRATION: Open the Web-Scraped Procurement Phase before processing narrative steps
        await execute_procurement_market_phase(player_node_id, selected_domain, engine)

        # B. Query and Compile AI Narrative Matrix Layout blocks using live backend data flags
        compiled_prompts = narrative_bridge.execute_narrative_generation(turn_snapshot)
        live_rpg_event = llm_connector.fetch_rpg_event(
            system_prompt=compiled_prompts["generated_system_prompt"],
            user_prompt=compiled_prompts["generated_user_prompt"]
        )

# C. Render Live Scenario Block inside terminal environment text matrices
print(f"\n🔴 EMERGENCY NARRATIVE LOG: [ {live_rpg_event.get('title', 'Systemic Shift')} ]")
print("-" * 65)
print(live_rpg_event.get("scenario"))
print("-" * 65)
choices_list = live_rpg_event.get("choices", [])
for choice in choices_list:
print(f" [{choice['id']}] {choice['text']}")
# D. Process Player Choice Command Input Block
valid_input = False
selected_id = 1
while not valid_input:
user_input = input(f"\nSelect your structural response path [1-{len(choices_list)}]: ").strip()
if user_input.isdigit() and 1 <= int(user_input) <= len(choices_list):
selected_id = int(user_input)
valid_input = True
else:
print("Invalid operational coordinate. Select a valid matrix branch.")
# E. Process Telemetry Logging Append operations
logged_data = telemetry.log_player_decision(session_id, profile_config, turn_snapshot, live_rpg_event, selected_id)
print(f" -> Telemetry logged. Decision Alignment Factor Score: {logged_data['alignment_score']}")
# F. Apply chosen choice impacts back to the active network graph parameters
chosen_impact = choices_list[selected_id - 1].get("impact", {})
for neighbor in engine.network.neighbors(player_node_id):
engine.network.nodes[neighbor]['resources'] = max(0.0, engine.network.nodes[neighbor]['resources'] + chosen_impact.get("resource_delta", 0.0) / 2.0)
# =====================================================================
# POST-GAME SHUTDOWN: DIAGNOSTIC REPORT AND METRICS RENDER
# =====================================================================
print("\n=====================================================================")
print(" SIMULATION COMPLETE - GENERATING EVALUATION ANALYTICS ")
print("=====================================================================")
visualizer = HeterarchyVisualizer(turn_history=turn_loop.turn_history, engine=engine)
visualizer.generate_endgame_dashboard(output_path=f"dashboard_{session_id}.png")
if name == "main":
# Launch main loop safely inside an asynchronous worker framework
asyncio.run(start_game_session())


