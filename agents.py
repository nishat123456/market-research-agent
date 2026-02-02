"""
Agent definitions for the market research system.
Each agent has a specific role in the research pipeline.
"""

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize the LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
)


def create_research_planner():
    """
    The Planner agent breaks down a research topic into specific sub-questions.
    """
    system_prompt = """You are a Research Planner. Your job is to take a broad research topic 
and break it down into 3-5 specific, searchable sub-questions that will help build 
a comprehensive understanding of the topic.

Output ONLY the numbered list of sub-questions, nothing else.

Example:
Topic: "Electric vehicle market in Southeast Asia"
1. What is the current market size and growth rate of EVs in Southeast Asia?
2. Which countries in Southeast Asia have the highest EV adoption rates?
3. What government policies and incentives exist for EVs in Southeast Asian countries?
4. Who are the major EV manufacturers and brands operating in Southeast Asia?
5. What are the main challenges for EV adoption in Southeast Asia?"""

    def plan(topic: str) -> list[str]:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Topic: {topic}")
        ]
        response = llm.invoke(messages)
        # Parse numbered list into array
        lines = response.content.strip().split("\n")
        questions = [line.split(". ", 1)[-1].strip() for line in lines if line.strip()]
        return questions
    
    return plan


def create_researcher():
    """
    The Researcher agent analyzes search results and extracts key insights.
    """
    system_prompt = """You are a Research Analyst. Given a question and search results, 
extract and synthesize the most relevant information into clear, factual insights.

Be specific with numbers, dates, and sources when available.
Keep your response concise but informative (2-3 paragraphs max)."""

    def research(question: str, search_results: list[dict]) -> str:
        # Format search results for the LLM
        formatted_results = "\n\n".join([
            f"**{r.get('title', 'No title')}**\n{r.get('body', r.get('description', 'No content'))}"
            for r in search_results
        ])
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Question: {question}\n\nSearch Results:\n{formatted_results}")
        ]
        response = llm.invoke(messages)
        return response.content
    
    return research


def create_writer():
    """
    The Writer agent synthesizes all research into a final report.
    """
    system_prompt = """You are a Report Writer. Given a collection of research findings on various 
sub-topics, synthesize them into a well-structured, professional research report.

Your report should include:
1. Executive Summary (2-3 sentences)
2. Key Findings (organized by theme)
3. Conclusion and Outlook

Use markdown formatting. Be concise but comprehensive."""

    def write_report(topic: str, findings: dict[str, str]) -> str:
        # Format findings
        formatted_findings = "\n\n".join([
            f"### {question}\n{answer}"
            for question, answer in findings.items()
        ])
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Research Topic: {topic}\n\nFindings:\n{formatted_findings}")
        ]
        response = llm.invoke(messages)
        return response.content
    
    return write_report
