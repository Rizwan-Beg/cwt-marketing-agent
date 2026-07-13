import os
import json
from apify_client import ApifyClient
from openai import OpenAI
from src.config import APIFY_API_TOKEN, LLM_BASE_URL, LLM_API_KEY, LLM_MODEL, DATA_DIR

class AdsManagerAgent:
    def __init__(self):
        self.apify_client = ApifyClient(APIFY_API_TOKEN) if APIFY_API_TOKEN else None
        
        if LLM_API_KEY:
            self.llm_client = OpenAI(
                base_url=LLM_BASE_URL,
                api_key=LLM_API_KEY
            )
        else:
            self.llm_client = None

    def search_successful_ads(self, keywords):
        print(f"Searching Meta Ads for keywords: {keywords}")
        if not self.apify_client:
            print("WARNING: APIFY_API_TOKEN not set. Skipping real scrape and using mock data.")
            return self._get_mock_ads()

        url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q={keywords.replace(' ', '%20')}&search_type=keyword_unordered"
        run_input = {
            "startUrls": [{"url": url}],
            "resultsLimit": 15,
        }
        
        try:
            # Note: The exact actor is apify/facebook-ads-scraper
            run = self.apify_client.actor("apify/facebook-ads-scraper").call(run_input=run_input)
            results = []
            for item in self.apify_client.dataset(run["defaultDatasetId"]).iterate_items():
                # Filter for text length to ensure there's ad copy
                if item.get("primaryText") and len(item["primaryText"]) > 50:
                    results.append({
                        "id": item.get("id"),
                        "pageName": item.get("pageName"),
                        "primaryText": item.get("primaryText"),
                        "startDate": item.get("startDate")
                    })
            
            output_path = os.path.join(DATA_DIR, "scraped_ads.json")
            with open(output_path, "w") as f:
                json.dump(results, f, indent=2)
            print(f"Saved {len(results)} ads to {output_path}")
            return results
        except Exception as e:
            print(f"Error scraping ads: {e}")
            return self._get_mock_ads()

    def extract_marketing_concepts(self, ads_data):
        print("Extracting marketing pain points and concepts from ads...")
        if not self.llm_client:
            print("WARNING: No LLM API key set. Returning mock extraction.")
            return self._get_mock_insights()

        # Combine ad texts
        ad_texts = "\n---\n".join([ad.get("primaryText", "") for ad in ads_data[:10]])
        
        prompt = f"""
        Analyze the following successful Facebook ads in the trading/investing niche.
        Extract the key marketing concepts, common pain points addressed, and overall messaging strategies.
        
        Ads:
        {ad_texts}
        
        Return the result as a JSON object with the following keys:
        - target_audience (string)
        - pain_points (list of strings)
        - marketing_concepts (list of strings)
        - common_hooks (list of strings)
        """

        try:
            response = self.llm_client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            insights = json.loads(content)
            
            output_path = os.path.join(DATA_DIR, "extracted_insights.json")
            with open(output_path, "w") as f:
                json.dump(insights, f, indent=2)
            
            print(f"Saved extracted insights to {output_path}")
            return insights
        except Exception as e:
            print(f"Error extracting concepts: {e}")
            return self._get_mock_insights()

    def _get_mock_ads(self):
        mock_data = [
            {
                "id": "mock1",
                "pageName": "Trading Pro",
                "primaryText": "Stop trading alone. 90% of retail traders lose money because they rely on emotion instead of data. Join our community and trade alongside professionals.",
                "startDate": "2026-06-01"
            },
            {
                "id": "mock2",
                "pageName": "Algorithmic Wealth",
                "primaryText": "Tired of guessing the market direction? Our signals use aggregate data to find high-probability setups before they happen.",
                "startDate": "2026-06-15"
            }
        ]
        output_path = os.path.join(DATA_DIR, "scraped_ads.json")
        with open(output_path, "w") as f:
            json.dump(mock_data, f, indent=2)
        return mock_data

    def _get_mock_insights(self):
        mock_insights = {
            "target_audience": "Retail traders losing money and looking for an edge",
            "pain_points": [
                "Trading alone is emotionally exhausting",
                "Relying on guesswork instead of data",
                "Losing money consistently"
            ],
            "marketing_concepts": [
                "Community driven success",
                "Professional data access",
                "High-probability setups"
            ],
            "common_hooks": [
                "Stop trading alone.",
                "Tired of guessing?"
            ]
        }
        output_path = os.path.join(DATA_DIR, "extracted_insights.json")
        with open(output_path, "w") as f:
            json.dump(mock_insights, f, indent=2)
        return mock_insights

if __name__ == "__main__":
    agent = AdsManagerAgent()
    ads = agent.search_successful_ads("trading signals OR copy trading")
    agent.extract_marketing_concepts(ads)
