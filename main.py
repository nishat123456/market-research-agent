#!/usr/bin/env python3
"""
Autonomous Market Research Agent
A multi-agent system that automates deep-dive market analysis.

Usage:
    python main.py "Your research topic here"
    python main.py  # Interactive mode
"""

import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API key is set
if not os.getenv("GROQ_API_KEY"):
    print("❌ Error: GROQ_API_KEY not found!")
    print("   1. Copy .env.example to .env")
    print("   2. Add your Groq API key from https://console.groq.com/keys")
    sys.exit(1)

from graph import graph


def run_research(topic: str) -> str:
    """Run the full research pipeline on a topic."""
    print("=" * 60)
    print(f"🚀 Starting Market Research Agent")
    print(f"📌 Topic: {topic}")
    print("=" * 60)
    
    # Initialize state
    initial_state = {
        "topic": topic,
        "sub_questions": [],
        "current_question_idx": 0,
        "findings": {},
        "final_report": ""
    }
    
    # Run the graph
    result = graph.invoke(initial_state)
    
    return result["final_report"]


def save_report(topic: str, report: str) -> str:
    """Save the report to a file."""
    os.makedirs("outputs", exist_ok=True)
    
    # Create filename from topic
    safe_topic = "".join(c if c.isalnum() or c == " " else "_" for c in topic)
    safe_topic = safe_topic.replace(" ", "_")[:50]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/{safe_topic}_{timestamp}.md"
    
    with open(filename, "w") as f:
        f.write(f"# Market Research: {topic}\n\n")
        f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("---\n\n")
        f.write(report)
    
    return filename


def main():
    # Get topic from command line or prompt
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        print("🔬 Autonomous Market Research Agent")
        print("-" * 40)
        topic = input("Enter your research topic: ").strip()
        if not topic:
            print("No topic provided. Exiting.")
            sys.exit(0)
    
    # Run research
    report = run_research(topic)
    
    # Save and display
    filename = save_report(topic, report)
    
    print("\n" + "=" * 60)
    print("📄 FINAL REPORT")
    print("=" * 60)
    print(report)
    print("\n" + "=" * 60)
    print(f"💾 Report saved to: {filename}")
    print("=" * 60)


if __name__ == "__main__":
    main()
