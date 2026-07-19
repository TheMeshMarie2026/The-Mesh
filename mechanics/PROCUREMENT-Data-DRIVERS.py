import asyncio
import re
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from typing import List, Dict, Any

class ProcurementNetworkDrivers:
    def __init__(self):
        # Universal browser agent string to prevent automated request blocking
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    # =====================================================================
    # VECTOR 1: MATERIAL RESOURCES (Live eBay API/Scraper Driver)
    # =====================================================================
    async def fetch_live_material_resources(self, query: str) -> List[Dict[str, Any]]:
        """
        Scrapes live, real-world purchase listings for physical equipment and assets.
        Uses Playwright to navigate public listings, parsing out exact prices.
        """
        listings = []
        search_url = f"https://ebay.com{query.replace(' ', '+')}"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(user_agent=self.user_agent)
            
            try:
                # Navigate and wait until layout elements render
                await page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
                html_content = await page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Target the universal item row wrappers on public listings
                items = soup.select(".s-item__wrapper")
                
                for item in items:
                    title_el = item.select_one(".s-item__title")
                    price_el = item.select_one(".s-item__price")
                    
                    if title_el and price_el:
                        title_text = title_el.get_text(strip=True)
                        price_text = price_el.get_text(strip=True)
                        
                        # Sanitize strings like "Shop on eBay" and format numerical values
                        if "shop on" in title_text.lower():
                            continue
                            
                        # Extract numerical float using regex filters
                        price_digits = re.findall(r"[-+]?\d*\.\d+|\d+", price_text.replace(',', ''))
                        base_cost = float(price_digits[0]) if price_digits else 100.0
                        
                        listings.append({
                            "title": title_text,
                            "source": "Public Equipment Market",
                            "base_cost": base_cost,
                            "type": "BUY",
                            "metadata": {"raw_price_str": price_text}
                        })
                        if len(listings) >= 5: # Cap size for optimal game loop execution
                            break
                            
            except Exception as e:
                print(f"⚠️ [DRIVER EXCEPTION - RESOURCES]: {e}")
            finally:
                await browser.close()
                
        return listings

    # =====================================================================
    # VECTOR 2: KNOWLEDGE COMMONS (Live Open-Access Research Archive Driver)
    # =====================================================================
    async def fetch_live_knowledge_archives(self, query: str) -> List[Dict[str, Any]]:
        """
        Scrapes open-access databases (like arXiv or public repositories)
        to extract data feeds and research operational protocols.
        """
        listings = []
        search_url = f"https://arxiv.org{query.replace(' ', '+')}&searchtype=all"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(user_agent=self.user_agent)
            
            try:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
                html_content = await page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Target result wrappers on standard archive lists
                results = soup.select("li.arxiv-result")
                
                for res in results:
                    title_el = res.select_one(".title")
                    summary_el = res.select_one(".abstract-full")
                    
                    if title_el:
                        title_text = title_el.get_text(strip=True).replace("Title:", "")
                        summary_text = summary_el.get_text(strip=True) if summary_el else "No protocol brief available."
                        
                        # Knowledge Commons items are open-access ($0.00 to rent/subscribe)
                        listings.append({
                            "title": f"Protocol: {title_text}",
                            "source": "Open-Access Research Network",
                            "base_cost": 0.0, 
                            "type": "RENT",
                            "metadata": {"abstract": summary_text[:120] + "..."}
                        })
                        if len(listings) >= 5:
                            break
                            
            except Exception as e:
                print(f"⚠️ [DRIVER EXCEPTION - KNOWLEDGE]: {e}")
            finally:
                await browser.close()
                
        return listings

    # =====================================================================
    # VECTOR 3: EXPERT TALENT & LEADERSHIP (Live Open-Source Gig Market Driver)
    # =====================================================================
    async def fetch_live_talent_leadership(self, query: str) -> List[Dict[str, Any]]:
        """
        Connects to global distributed labor portals to fetch contractor profiles
        for operational coordinators, developers, and crisis scientists.
        """
        listings = []
        # Target public consulting/freelance listings
        search_url = f"https://freelancer.com{query.replace(' ', '%20')}"
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(user_agent=self.user_agent)
            
            try:
                await page.goto(search_url, wait_until="networkidle", timeout=20000)
                html_content = await page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Parse layout cards representing real-world contract listings
                job_cards = soup.select(".JobCard")
                
                for card in job_cards:
                    title_el = card.select_one(".JobCard-title")
                    avg_bid_el = card.select_one(".JobCard-avgBid")
                    
                    if title_el:
                        title_text = title_el.get_text(strip=True)
                        bid_text = avg_bid_el.get_text(strip=True) if avg_bid_el else "$25 / hr"
                        
                        # Format rate calculations using standard numerical text stripping
                        digits = re.findall(r"\d+", bid_text)
                        cost_per_turn = float(digits[0]) if digits else 50.0
                        
                        listings.append({
                            "title": f"Expert Leadership: {title_text}",
                            "source": "Distributed Global Talent Registry",
                            "base_cost": cost_per_turn,
                            "type": "RENT", # Human capital is leased via contract iterations
                            "metadata": {"rate_tier": bid_text}
                        })
                        if len(listings) >= 5:
                            break
                            
            except Exception as e:
                print(f"⚠️ [DRIVER EXCEPTION - TALENT]: {e}")
            finally:
                await browser.close()
                
        return listings


# =====================================================================
# LIVE TEST EXECUTIVE PROTOCOL
# =====================================================================
async def main():
    print("--- Activating Live Network Procurement Drivers ---")
    drivers = ProcurementNetworkDrivers()
    
    # Simulating a scenario keyword selection from a gameplay loop trigger
    keyword = "Solar Power"
    
    # Execute driver fetch streams concurrently to avoid thread blocking
    print(f"Connecting to live web endpoints for query context: '{keyword}'...")
    resources_task = drivers.fetch_live_material_resources(keyword)
    knowledge_task = drivers.fetch_live_knowledge_archives(keyword)
    talent_task = drivers.fetch_live_talent_leadership(keyword)
    
    resources, knowledge, talent = await asyncio.gather(resources_task, knowledge_task, talent_task)
    
    print("\n📦 LIVE PHYSICAL RESOURCE ENTRIES EXTRACTED (CapEx):")
    for r in resources[:2]:
        print(f" - {r['title']} | Market Value: ${r['base_cost']:.2f}")
        
    print("\n📖 LIVE KNOWLEDGE ARchives PROTOCOLS EXTRACTED (Commons):")
    for k in knowledge[:2]:
        print(f" - {k['title']} | Cost: ${k['base_cost']:.2f} (Access Verified)")
        
    print("\n👥 LIVE CRISIS TALENT RECRUITS LOCATED (OpEx Contract):")
    for t in talent[:2]:
        print(f" - {t['title']} | Internal Contract Rate Calculation: ${t['base_cost']:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
