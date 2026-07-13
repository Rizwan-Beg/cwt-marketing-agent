# CrowdWisdomTrading Video Ads Agent

This project implements a multi-agent system using the **Hermes Agent Framework** to automatically scrape successful Meta ads, extract marketing themes, generate ad scripts, and render 30-60 second video ads for CrowdWisdomTrading using OpenMontage.

## Prerequisites

1. Python 3.10+
2. FFmpeg (`brew install ffmpeg` or `sudo apt install ffmpeg`)
3. Node.js 18+ (Required by OpenMontage/Remotion)

## Setup Instructions

1. **Install Python dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   # Install Hermes Agent (requires git)
   pip install git+https://github.com/NousResearch/hermes-agent.git
   ```

2. **Set up Environment Variables:**
   Copy `.env.example` to `.env` and fill in your keys:
   ```bash
   cp .env.example .env
   ```
   *Required:*
   - `APIFY_API_TOKEN`: To scrape Meta Ads Library
   - `OPENROUTER_API_KEY` (or `NVIDIA_API_KEY`): For the LLM agent processing
   - `TELEGRAM_BOT_TOKEN`: To connect to Telegram
   - `TELEGRAM_USER_ID`: To restrict access to yourself

3. **Install OpenMontage dependencies:**
   The `OpenMontage` folder is cloned in this repo.
   ```bash
   cd OpenMontage
   make setup
   cd ..
   ```

## Usage

### 1. Run the Python Pipeline Manually
You can run the entire pipeline through the CLI:
```bash
python3 src/main.py
```

### 2. Hermes Kanban & Telegram Gateway
To use the Hermes Kanban board and Telegram gateway:

1. **Install the Skill:**
   The skill is located in `hermes/video_ads_skill`. You can link or copy this to your `~/.hermes/skills/` directory.
   ```bash
   mkdir -p ~/.hermes/skills/video-ads-generator
   cp hermes/video_ads_skill/SKILL.md ~/.hermes/skills/video-ads-generator/
   ```

2. **Start the Telegram Gateway:**
   Configure Telegram in Hermes and start the gateway:
   ```bash
   hermes config set messaging.telegram.allowed_users "[$TELEGRAM_USER_ID]"
   hermes gateway setup
   hermes gateway start
   ```

3. **Launch the Kanban Dashboard:**
   ```bash
   hermes dashboard
   ```
   Open `http://127.0.0.1:9119` in your browser to view the Kanban board.
   
4. **Chat with your Agent:**
   Open Telegram, find your bot, and say:
   `Create a new video ad for crowd wisdom trading based on recent successful meta ads.`
   The agent will break this into Kanban tasks, execute the python scripts in this repository, and deliver the final video.
