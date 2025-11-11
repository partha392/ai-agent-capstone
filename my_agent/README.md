# AI Agent (Gemini + ADK)

A simple yet functional AI Agent built using **Google ADK (Agent Development Kit)** and **Gemini API**.

It demonstrates a modular, multi-agent pipeline:
> Research → Write → Critique

---

## ⚙️ Setup

```bash
conda create -n ai_agent python=3.10 -y
conda activate ai_agent
pip install -r requirements.txt

# Configure your API key
cp my_agent/.env.template my_agent/.env
# Then edit .env and insert your actual Google API key
export $(grep GOOGLE_API_KEY my_agent/.env | xargs)

Run
adk run my_agent

For To open the web UI
adk web --port 8000

