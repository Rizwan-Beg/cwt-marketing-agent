---
name: Video Ads Generator (CrowdWisdomTrading)
description: A marketing agent team workflow that scrapes Meta ads, generates video scripts, and renders video ads via OpenMontage using a Kanban board.
version: 1.0.0
tags:
  - marketing
  - video
  - ads
  - kanban
---

# Video Ads Generator Skill

This skill teaches the Hermes Agent how to manage the CrowdWisdomTrading Video Ads pipeline using the built-in Kanban board.

## Prerequisites
- Apify API token configured in `.env`.
- LLM API Key (OpenRouter or NVIDIA) in `.env`.
- OpenMontage installed in the project root.

## Kanban Workflow

When the user requests to "create a new video ad", follow this process:

### 1. Initialize the Kanban Board
If the board isn't initialized, run:
```bash
hermes kanban init
```

### 2. Create Tasks
Create the following tasks on the Kanban board:
1. `kanban_create`: "Ads Manager: Scrape and Analyze Ads"
2. `kanban_create`: "Script Agent: Generate Ad Scripts"
3. `kanban_create`: "Video Agent: Render Video Ad"

### 3. Execute Tasks

**Task 1: Ads Manager**
- Move task to IN PROGRESS.
- Run the Ads Manager:
  ```bash
  python3 src/ads_manager.py
  ```
- Once complete, verify `data/scraped_ads.json` and `data/extracted_insights.json` exist.
- Move task to DONE.

**Task 2: Script Agent**
- Move task to IN PROGRESS.
- Run the Script Agent:
  ```bash
  python3 src/script_agent.py
  ```
- Verify `data/ad_scripts.json` is created and contains the hooks and scripts.
- Move task to DONE.

**Task 3: Video Agent**
- Move task to IN PROGRESS.
- Run the Video Agent to prepare the prompt (e.g., using the "data" script type):
  ```bash
  python3 src/video_agent.py data
  ```
- The prompt is saved to `video_generation_prompt.txt`.
- Now, act as the video director. Use your internal OpenMontage tools (or instruct the user to run OpenMontage) using the prompt in `video_generation_prompt.txt`.
- Once the render is complete, move task to DONE.

### Telegram Gateway Note
If this skill is triggered via Telegram, ensure you send status updates back to the chat as tasks transition from To Do -> In Progress -> Done, so the user knows exactly what the agent team is working on.
