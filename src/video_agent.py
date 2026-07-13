import os
import json
from src.config import DATA_DIR, BASE_DIR

class VideoAgent:
    def __init__(self):
        pass

    def prepare_video_prompt(self, script_type="data"):
        print(f"Preparing video generation prompt for script type: {script_type}")
        scripts_path = os.path.join(DATA_DIR, "ad_scripts.json")
        
        if not os.path.exists(scripts_path):
            print("Error: ad_scripts.json not found. Run ScriptAgent first.")
            return None
            
        with open(scripts_path, "r") as f:
            data = json.load(f)
            
        scripts_data = data.get("scripts", data)
        scripts = []
        if isinstance(scripts_data, list):
            scripts = scripts_data
        elif isinstance(scripts_data, dict):
            # Llama sometimes wraps in {"ads": [...]} or similar
            for key, val in scripts_data.items():
                if isinstance(val, list):
                    scripts = val
                    break
            if not scripts:
                scripts = [scripts_data]
        target_script = next((s for s in scripts if s.get("type") == script_type), None)
        
        if not target_script:
            print(f"Error: Script of type '{script_type}' not found.")
            # fallback to first
            if scripts:
                target_script = scripts[0]
            else:
                return None
                
        prompt_content = f"""Make a 45-second animated explainer video for CrowdWisdomTrading.
        
Use the following script and visuals:

Hook: {target_script.get('hook')}
Script: {target_script.get('script')}
Visuals Guide: {target_script.get('visuals')}

Please generate the scenes, find royalty-free music, and render the final video using the Animated Explainer pipeline.
"""
        
        output_path = os.path.join(BASE_DIR, "video_generation_prompt.txt")
        with open(output_path, "w") as f:
            f.write(prompt_content)
            
        print(f"Saved video generation prompt to {output_path}")
        print("To generate the video, open the directory in your agent (e.g. Claude Code or Hermes) and run the prompt in video_generation_prompt.txt using OpenMontage.")
        return prompt_content

if __name__ == "__main__":
    agent = VideoAgent()
    agent.prepare_video_prompt("data")
