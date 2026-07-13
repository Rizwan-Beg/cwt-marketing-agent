import os
import json
from openai import OpenAI
from src.config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL, DATA_DIR

class ScriptAgent:
    def __init__(self):
        if LLM_API_KEY:
            self.llm_client = OpenAI(
                base_url=LLM_BASE_URL,
                api_key=LLM_API_KEY
            )
        else:
            self.llm_client = None

    def load_data(self):
        insights_path = os.path.join(DATA_DIR, "extracted_insights.json")
        ud1_path = os.path.join(DATA_DIR, "unique_data_1.json")
        ud2_path = os.path.join(DATA_DIR, "unique_data_2.json")
        
        insights = {}
        ud1 = {}
        ud2 = {}
        
        if os.path.exists(insights_path):
            with open(insights_path, "r") as f:
                insights = json.load(f)
        if os.path.exists(ud1_path):
            with open(ud1_path, "r") as f:
                ud1 = json.load(f)
        if os.path.exists(ud2_path):
            with open(ud2_path, "r") as f:
                ud2 = json.load(f)
                
        return insights, ud1, ud2

    def generate_scripts(self):
        print("Generating video ad scripts...")
        insights, ud1, ud2 = self.load_data()
        
        if not self.llm_client:
            print("WARNING: No LLM API key set. Returning mock scripts.")
            return self._get_mock_scripts()
            
        prompt = f"""
        You are an expert copywriter for CrowdWisdomTrading.
        Create 3 video ad scripts (30-60 seconds each) based on the following data:
        
        Marketing Insights (from successful ads): {json.dumps(insights)}
        Unique Data Example 1 (Nasdaq-100 analysis): {json.dumps(ud1)}
        Unique Data Example 2 (Snowflake stock analysis): {json.dumps(ud2)}
        
        The 3 scripts must be:
        1. Identified pain: Address the pain points of retail traders losing money or trading emotionally.
        2. Our unique data: Showcase the actual data from the Unique Data Examples (e.g. professional trader consensus, sentiment weights).
        3. How crowd wisdom can help: Focus on the platform's core value proposition of aggregating data to improve trading results.
        
        For each script, create a scroll-stopping hook for the first 3 seconds.
        
        Format the output as a JSON array of objects, where each object has:
        - "type": "pain" | "data" | "wisdom"
        - "hook": "The first 3 seconds scroll-stopping hook"
        - "script": "The full ad script with visual cues"
        - "visuals": "Brief description of visuals for the video generator"
        """
        
        try:
            response = self.llm_client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
                # To enforce array output in JSON object, we requested a JSON object in the prompt
                # But let's wrap it in an object to be safe: {"scripts": [...]}
            )
            # update prompt dynamically if needed, but let's assume it returns {"scripts": []} 
            content = response.choices[0].message.content
            scripts_data = json.loads(content)
            if "scripts" not in scripts_data:
                scripts_data = {"scripts": scripts_data} # fallback
                
            output_path = os.path.join(DATA_DIR, "ad_scripts.json")
            with open(output_path, "w") as f:
                json.dump(scripts_data, f, indent=2)
                
            print(f"Saved {len(scripts_data.get('scripts', []))} scripts to {output_path}")
            return scripts_data
        except Exception as e:
            print(f"Error generating scripts: {e}")
            return self._get_mock_scripts()

    def _get_mock_scripts(self):
        mock_scripts = {
            "scripts": [
                {
                    "type": "pain",
                    "hook": "90% of retail traders lose money. Are you one of them?",
                    "script": "Stop trading alone. The market is designed to trigger your emotions and take your money. But what if you could trade with the confidence of the crowd? CrowdWisdomTrading removes the emotion and gives you the edge.",
                    "visuals": "Frustrated trader looking at red charts, transitioning to a calm, ascending green chart."
                },
                {
                    "type": "data",
                    "hook": "We tracked 10,000 professional traders today, and here's what they're buying.",
                    "script": "Look at this data on the Nasdaq-100. Our sentiment weights from YouTube, X, and Reddit show a unified 85% confidence level for a LONG position. The megacap tech strength is pouring in. This is the exact unique data you get with CrowdWisdomTrading.",
                    "visuals": "Animated data visualization showing sentiment weights (YouTube 25%, X 25%, etc) and price targets."
                },
                {
                    "type": "wisdom",
                    "hook": "What if you could harness the wisdom of the crowd to beat the market?",
                    "script": "Trading isn't about guessing; it's about aggregate intelligence. By combining professional trader consensus with real-time social sentiment, CrowdWisdomTrading gives you high-probability setups before they happen.",
                    "visuals": "Abstract network of glowing nodes coming together to form a clear upward trend line."
                }
            ]
        }
        output_path = os.path.join(DATA_DIR, "ad_scripts.json")
        with open(output_path, "w") as f:
            json.dump(mock_scripts, f, indent=2)
        return mock_scripts

if __name__ == "__main__":
    agent = ScriptAgent()
    agent.generate_scripts()
