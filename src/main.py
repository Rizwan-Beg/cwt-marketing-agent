import os
import sys
from src.ads_manager import AdsManagerAgent
from src.script_agent import ScriptAgent
from src.video_agent import VideoAgent

def main():
    print("========================================")
    print(" CrowdWisdomTrading Video Ads Generator ")
    print("========================================")
    print("\n[Phase 1] Ads Manager Agent")
    ads_manager = AdsManagerAgent()
    keywords = "trading signals OR copy trading OR algo trading"
    ads = ads_manager.search_successful_ads(keywords)
    insights = ads_manager.extract_marketing_concepts(ads)
    
    print("\n[Phase 2] Script Agent")
    script_agent = ScriptAgent()
    scripts = script_agent.generate_scripts()
    
    print("\n[Phase 3] Video Agent")
    video_agent = VideoAgent()
    # Prompt the user for which script to use
    print("Which script type would you like to render? (pain, data, wisdom)")
    script_type = "data" # Default to 'data' for automated runs
    if len(sys.argv) > 1:
        script_type = sys.argv[1]
    video_agent.prepare_video_prompt(script_type)
    
    print("\n========================================")
    print(" Pipeline complete!")
    print(" Now run the generated prompt through your AI agent to trigger OpenMontage.")
    print("========================================")

if __name__ == "__main__":
    main()
