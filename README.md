# 🤖 AI Agent Capstone — Gemini 2.5 Flash + Google ADK

> Built by **Partha Das**, M.Sc Computer Science (NIELIT Guwahati)  
> Submission for the **Google × Kaggle 5-Day AI Agent Challenge**

---

## 🌟 Overview

This project demonstrates a **fully functional autonomous AI agent** built using **Google’s Agent Development Kit (ADK)** and powered by **Gemini 2.5 Flash**.  
It simulates an intelligent multi-tool workflow — capable of **researching**, **writing**, and **critiquing** — showing how LLM-based agents can perform reasoning-driven, goal-oriented tasks.

The agent acts as a **mini research assistant** that:
1. Collects relevant information (mock research tool),
2. Synthesizes it into a coherent report (writer tool),
3. Reviews the generated content (critic tool).

---

## 🧠 System Workflow

**Agent Name:** `root_agent`  
**Model Used:** `gemini-2.5-flash`

### 🧩 Workflow Stages

| Stage | Tool | Purpose |
|-------|------|----------|
| 1️⃣ | `research_tool(topic)` | Gathers relevant snippets about a user topic. |
| 2️⃣ | `writer_tool(context)` | Generates a structured Markdown report using the snippets. |
| 3️⃣ | `critic_tool(report, context)` | Evaluates coverage and coherence of the report. |

---

## 🧰 Project Architecture

