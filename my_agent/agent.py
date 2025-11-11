# my_agent/agent.py
from google.adk.agents.llm_agent import Agent
from typing import Dict, Any, List
import datetime
import pytz
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(message)s")


def trace(tag: str, payload: Dict[str, Any]):
    logging.info(f"[TRACE] {tag} | {json.dumps(payload, default=str)[:1000]}")


# --- Tools ---


def get_current_time(city: str) -> dict:
    """Return current time for a tz string like 'Asia/Kolkata'."""
    try:
        tz = pytz.timezone(city)
        now = datetime.datetime.now(tz)
        return {"status": "success", "city": city, "time": now.strftime("%I:%M %p %Z")}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def research_tool(topic: str) -> dict:
    """Mock research tool: returns canned snippet objects.
    Replace with real retrieval if needed."""
    trace("research_tool.called", {"topic": topic})
    snippets = [
        {"title": f"{topic} - Paper A", "snippet": f"Idea A about {topic}."},
        {"title": f"{topic} - Paper B", "snippet": f"Experiment results on {topic}."},
        {"title": f"{topic} - Review C", "snippet": f"Summary and implications of {topic}."},
    ]
    return {"status": "success", "topic": topic, "snippets": snippets}


def _extract_snippets_from_context(context: Dict[str, Any]) -> List[Dict[str, str]]:
    """Helper: accept different context shapes and return a list of snippets."""
    if context is None:
        return []
    # Direct list
    if isinstance(context.get("snippets"), list):
        return context.get("snippets", [])
    # Some tools return nested response object e.g. research_tool_response
    for key in ("research_tool_response", "research_response", "tool_response"):
        val = context.get(key)
        if isinstance(val, dict) and isinstance(val.get("snippets"), list):
            return val.get("snippets", [])
    # Fallback: look for any list-of-dicts under context
    for v in context.values():
        if isinstance(v, list) and v and isinstance(v[0], dict) and "title" in v[0]:
            return v
    return []


def writer_tool(context: dict) -> dict:
    """Build a small markdown report from context.
    Returns: {'status', 'report', 'final_message'} where final_message is plain text."""
    trace("writer_tool.start", {"keys": list(context.keys()) if context else []})
    topic = context.get("topic") if context and context.get("topic") else context.get("research_topic", "unknown")
    snippets = _extract_snippets_from_context(context) if context else []
    report_lines = [f"# Report on {topic}", ""]
    for s in snippets:
        title = s.get("title", "Untitled")
        snippet = s.get("snippet", "")
        report_lines.append(f"**{title}** - {snippet}")
        report_lines.append("")  # blank line
    report_lines.append("### TL;DR")
    report_lines.append("A short, coherent report about the topic.")
    report_text = "\n".join(report_lines)

    # final_message is a plain-text summary suited for UIs that don't render markdown
    final_message = f"Report on {topic} — " + " ".join([s.get("snippet", "") for s in snippets]) or report_text

    return {"status": "success", "report": report_text, "final_message": final_message}


def critic_tool(report_package: dict, context: dict) -> dict:
    """Check presence of snippet titles in the report text and return a verdict."""
    trace("critic_tool.start", {})
    report = report_package.get("report", "") if report_package else ""
    snippets = _extract_snippets_from_context(context)
    missing = []
    for s in snippets:
        # check by a reasonable token (first word of title) to reduce false negatives
        first_token = s.get("title", "").split()[0] if s.get("title") else ""
        if first_token and first_token not in report:
            missing.append(s.get("title"))
    score = 1 - (len(missing) / max(1, len(snippets)))
    verdict = {"ok": len(missing) == 0, "missing": missing, "score": round(score, 2)}
    trace("critic_tool.finish", verdict)
    return verdict


# --- Expose root_agent at module-level ---
root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Mini pipeline: research -> writer -> critic",
    instruction=(
        "You orchestrate research, writing and critique using tools: "
        "'research_tool(topic)', 'writer_tool(context)', 'critic_tool(report, context)'."
    ),
    tools=[get_current_time, research_tool, writer_tool, critic_tool],
)
