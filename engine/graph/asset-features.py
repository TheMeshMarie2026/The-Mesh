import asyncio
import random
import math
from typing import Dict, Any, List

class ProcurementScraperEngine:
    def __init__(self, engine_reference: Any):
        """Passes in a reference to your central HeterarchyEngine state."""
        self.engine = engine_reference
        
    # =====================================================================
    # FEATURE 1: MULTI-STREAM ASSET NORMALIZATION (ORGANIZE)
    # =====================================================================
    async def scrape_market_listings(self, query_keyword: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Simulates an asynchronous web-scraper pool pulling unstructured listings
        across major job networks, material markets, and knowledge indices.
        Normalizes outputs into organized structural payload matrices.
        """
        print(f"🌐 [SCRAPER ENGAGED]: Spawning web-workers for query context: '{query_keyword}'...")
        # Simulate network latency of scraping concurrent remote streams
        await asyncio.sleep(0.4) 
        
        # Normalized inventory arrays mapping directly to your 3 required vectors
        scraped_payload = {
            "RESOURCES": [
                {"title": f"Bulk {query_keyword} Tactical Deployment Kits", "source": "IndustrialMarketplace", "base_cost": 4500.0, "type": "BUY", "quantity_available": 40},
                {"title": f"Standard {query_keyword} Logistics Cargo Pallet", "source": "GlobalSupplyLink", "base_cost": 1200.0, "type": "BUY", "quantity_available": 150}
            ],
            "KNOWLEDGE": [
                {"title": f"Proprietary {query_keyword} Multi-Variant Data Feed", "source": "SciDocs_Premium", "base_cost": 300.0, "type": "RENT", "duration_turns": 1},
                {"title": f"Open-Access {query_keyword} Core Protocol Specs Document", "source": "KnowledgeCommons_Archive", "base_cost": 0.0, "type": "RENT", "duration_turns": 99}
            ],
            "TALENT_LEADERSHIP": [
                {"title": "Senior Crisis Operations Director (Contractor)", "source": "TalentPool_Network", "base_cost": 850.0, "type": "RENT", "per_turn_rate": True},
                {"title": f"Specialized Graduate {query_keyword} Research Team", "source": "AcademicGigGrid", "base_cost": 400.0, "type": "RENT", "per_turn_rate": True}
            ]
        }
        return scraped_payload

    # =====================================================================
    # FEATURE 2: CONTEXTUAL VECTOR UTILITY RANKER (PRIORITIZE)
    # =====================================================================
    def prioritize_listings_by_utility(self, raw_listings: Dict[str, List[Dict[str, Any]]], active_crisis_type: str, current_player_node: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Calculates a priority index score for each listing based on situational utility.
        Formula favors low cost, alignment with the active crisis, and minimal network friction.
        """
        prioritized_matrix = {}
        
        for category, listings in raw_listings.items():
            evaluated_listings = []
            for item in listings:
                cost = item["base_cost"]
                
                # Context Alignment Bonus: High match scores if the title aligns with the active crisis
                alignment_bonus = 1.5 if active_crisis_type.upper() in item["title"].upper() else 1.0
                
                # Base Utility Math: Inversely proportional to cost (cheaper = more accessible)
                # Adding 1.0 avoids divide-by-zero errors for open-access assets
                base_utility = (1000.0 / (cost + 1.0)) * alignment_bonus
                
                # Network Friction Factor: Deduct utility if the node hosting the transaction has low trust
                # (Simulation default: models 10% structural decay if routing over long distances)
                structural_cohesion_multiplier = 0.90
                
                final_priority_score = round(base_utility * structural_cohesion_multiplier, 2)
                
                # Inject the computed score back into the item payload tracking dictionary
                item["priority_utility_score"] = final_priority_score
                evaluated_listings.append(item)
            
            # Sort the category list based on the calculated priority score
            prioritized_matrix[category] = sorted(evaluated_listings, key=lambda x: x["priority_utility_score"], reverse=True)
            
        return prioritized_matrix

    # =====================================================================
    # FEATURE 3: ASYMMETRIC MARKET SORTING MATRIX (SORT BY PRICE / TRANSACTION TYPE)
    # =====================================================================
    def generate_sorted_procurement_ledger(self, prioritized_data: Dict[str, List[Dict[str, Any]]]) -> None:
        """
        Renders a cleanly structured market pricing ledger in the terminal.
        Sorts listings across vectors by cost to let players balance immediate CapEx vs long-term OpEx.
        """
        print("\n=====================================================================================")
        print("          REALTIME PROCUREMENT LEDGER: PROCUREMENT MARKETPLACE MATRIX                ")
        print("=====================================================================================")
        
        for category, items in prioritized_data.items():
            print(f"\n📊 CATEGORY CLASS VECTOR: [{category}]")
            print(f"{'Item Listing Description':<52} | {'Source':<18} | {'Type':<6} | {'Price':<10} | {'Priority':<8}")
            print("-" * 102)
            
            # Sort explicitly by numerical cost ascending (lowest prices bubble up first)
            sorted_by_price = sorted(items, key=lambda x: x["base_cost"])
            
            for i in sorted_by_price:
                price_str = f"${i['base_cost']:.2f}"
                print(f"{i['title'][:50]:<52} | {i['source']:<18} | {i['type']:<6} | {price_str:<10} | {i['priority_utility_score']:<8}")


# =====================================================================
# SIMULATION WORKFLOW: RUNNING DYNAMIC PROCUREMENT LOOPS
# =====================================================================
async def main():
    # Mocking standard engine reference container block for compilation checks
    class MockEngine: network = None
    mock_engine = MockEngine()

    # 1. Initialize our newly extended Procurement Module
    procurement_layer = ProcurementScraperEngine(mock_engine)

    # 2. Execute Feature 1: Scrape real-time listings across web vectors asynchronously
    raw_scraped_data = await procurement_layer.scrape_market_listings(query_keyword="Water_Filtration")

    # 3. Execute Feature 2: Contextually prioritize listings against the active crisis state
    prioritized_data = procurement_layer.prioritize_listings_by_utility(
        raw_listings=raw_scraped_data,
        active_crisis_type="WATER_FILTRATION",
        current_player_node="Player_Node_Beta"
    )

    # 4. Execute Feature 3: Render sorted procurement ledger data table matrix
    procurement_layer.generate_sorted_procurement_ledger(prioritized_data)

if __name__ == "__main__":
    asyncio.run(main())
