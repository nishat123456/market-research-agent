"""
LangGraph workflow for the market research pipeline.
Orchestrates the multi-agent research process.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from agents import create_research_planner, create_researcher, create_writer
from tools import search_web, search_news
import operator


class ResearchState(TypedDict):
    """State that flows through the research pipeline."""
    topic: str
    sub_questions: list[str]
    current_question_idx: int
    findings: Annotated[dict, operator.or_]  # Merge findings as we go
    final_report: str


def plan_research(state: ResearchState) -> ResearchState:
    """Break down the topic into sub-questions."""
    print(f"\n🎯 Planning research for: {state['topic']}")
    planner = create_research_planner()
    questions = planner(state["topic"])
    print(f"📋 Generated {len(questions)} research questions")
    for i, q in enumerate(questions, 1):
        print(f"   {i}. {q}")
    return {
        **state,
        "sub_questions": questions,
        "current_question_idx": 0,
        "findings": {}
    }


def research_question(state: ResearchState) -> ResearchState:
    """Research the current question using web search."""
    import time
    
    idx = state["current_question_idx"]
    question = state["sub_questions"][idx]
    
    print(f"\n🔍 Researching ({idx + 1}/{len(state['sub_questions'])}): {question}")
    
    # Add delay between searches to avoid rate limits
    if idx > 0:
        time.sleep(2)
    
    # Search the web
    search_results = search_web(question, max_results=5)
    time.sleep(1)  # Small delay between web and news search
    news_results = search_news(question, max_results=3)
    all_results = search_results + news_results
    
    print(f"   Found {len(all_results)} sources")
    
    # Analyze with researcher agent
    researcher = create_researcher()
    insight = researcher(question, all_results)
    
    # Update findings
    new_findings = {**state["findings"], question: insight}
    
    return {
        **state,
        "findings": new_findings,
        "current_question_idx": idx + 1
    }


def should_continue_research(state: ResearchState) -> str:
    """Decide whether to continue researching or move to writing."""
    if state["current_question_idx"] < len(state["sub_questions"]):
        return "research"
    return "write"


def write_report(state: ResearchState) -> ResearchState:
    """Synthesize all findings into a final report."""
    print(f"\n✍️  Writing final report...")
    writer = create_writer()
    report = writer(state["topic"], state["findings"])
    print("✅ Report complete!")
    return {
        **state,
        "final_report": report
    }


def create_research_graph():
    """Build the LangGraph workflow."""
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("plan", plan_research)
    workflow.add_node("research", research_question)
    workflow.add_node("write", write_report)
    
    # Set entry point
    workflow.set_entry_point("plan")
    
    # Add edges
    workflow.add_edge("plan", "research")
    workflow.add_conditional_edges(
        "research",
        should_continue_research,
        {
            "research": "research",
            "write": "write"
        }
    )
    workflow.add_edge("write", END)
    
    return workflow.compile()


# Export the compiled graph
graph = create_research_graph()
