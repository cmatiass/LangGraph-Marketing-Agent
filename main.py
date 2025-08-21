"""
LangGraph Marketing Agent - Task 1: Foundational Agent

This module implements a simple, sequential marketing agent that:
1. Researches a topic (placeholder function with mock data)
2. Creates a draft marketing post based on the research

The agent uses LangGraph's StateGraph for sequential execution.
"""

import os
from typing import TypedDict, List, Dict, Any
from typing_extensions import Annotated

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class AgentState(TypedDict):
    """
    State management for the marketing agent.
    
    Attributes:
        initial_request: The original user request for the marketing post
        research_findings: Research data gathered about the topic
        draft_post: The generated marketing post draft
        messages: Chat history for the conversation
    """
    initial_request: str
    research_findings: Dict[str, Any]
    draft_post: str
    messages: Annotated[List[HumanMessage], add_messages]

def research_node(state: AgentState) -> AgentState:
    """
    Research node that simulates researching a topic.
    
    In this foundational version, this returns mock research data.
    In future iterations, this could integrate with web search APIs,
    knowledge bases, or other research tools.
    
    Args:
        state: Current agent state containing the initial request
        
    Returns:
        Updated state with research findings
    """
    initial_request = state["initial_request"]
    
    # Mock research data - in a real implementation, this would:
    # - Search the web for relevant information
    # - Query knowledge databases
    # - Analyze competitor content
    # - Gather market insights
    
    mock_research = {
        "topic": initial_request,
        "key_points": [
            "Current market trends show high engagement with authentic content",
            "Target audience prefers concise, value-driven messaging",
            "Visual elements increase engagement by 40%",
            "Best posting times are typically 9-11 AM and 2-4 PM"
        ],
        "competitor_insights": [
            "Top competitors focus on storytelling approaches",
            "User-generated content performs 50% better",
            "Behind-the-scenes content drives authenticity"
        ],
        "trending_hashtags": [
            "#marketing2024", "#digitalstrategy", "#contenttips", 
            "#socialmedia", "#brandstory"
        ],
        "audience_demographics": {
            "age_range": "25-45",
            "interests": ["business", "entrepreneurship", "digital marketing"],
            "platforms": ["LinkedIn", "Instagram", "Twitter"]
        }
    }
    
    print(f"🔍 Research completed for: {initial_request}")
    print(f"📊 Found {len(mock_research['key_points'])} key insights")
    
    return {
        **state,
        "research_findings": mock_research
    }

def copywriting_node(state: AgentState) -> AgentState:
    """
    Copywriting node that creates a marketing post based on research findings.
    
    This node takes the research data and generates a compelling marketing post
    using an LLM with specific prompting for marketing copy.
    
    Args:
        state: Current agent state with research findings
        
    Returns:
        Updated state with the generated draft post
    """
    research = state["research_findings"]
    initial_request = state["initial_request"]
    
    # Initialize the language model
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,  # Slightly creative for marketing copy
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create a detailed prompt for the copywriter
    copywriter_prompt = f"""
    You are an expert marketing copywriter. Based on the research provided below, 
    create an engaging marketing post for the following request: "{initial_request}"
    
    Research Findings:
    
    Key Points:
    {chr(10).join('• ' + point for point in research['key_points'])}
    
    Competitor Insights:
    {chr(10).join('• ' + insight for insight in research['competitor_insights'])}
    
    Trending Hashtags: {', '.join(research['trending_hashtags'])}
    
    Target Audience: {research['audience_demographics']['age_range']} year-olds interested in {', '.join(research['audience_demographics']['interests'])}
    
    Primary Platforms: {', '.join(research['audience_demographics']['platforms'])}
    
    Instructions for the marketing post:
    1. Create a compelling hook in the first line
    2. Include 2-3 key value propositions
    3. Use conversational yet professional tone
    4. Include a clear call-to-action
    5. Integrate 3-5 relevant hashtags naturally
    6. Keep it concise (under 300 words for social media)
    7. Make it platform-appropriate (professional for LinkedIn, engaging for Instagram)
    
    Generate the marketing post now:
    """
    
    # Generate the marketing post
    messages = [
        SystemMessage(content="You are a skilled marketing copywriter focused on creating engaging, conversion-optimized content."),
        HumanMessage(content=copywriter_prompt)
    ]
    
    response = model.invoke(messages)
    draft_post = response.content
    
    print(f"✍️ Marketing post generated!")
    print(f"📝 Post length: {len(draft_post)} characters")
    
    return {
        **state,
        "draft_post": draft_post
    }

def create_marketing_agent():
    """
    Creates and compiles the marketing agent StateGraph.
    
    The agent follows a simple sequential flow:
    START → research_node → copywriting_node → END
    
    Returns:
        Compiled LangGraph agent ready for execution
    """
    # Create the StateGraph
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("research", research_node)
    workflow.add_node("copywriting", copywriting_node)
    
    # Define the flow
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "copywriting")
    workflow.add_edge("copywriting", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

def run_marketing_agent(request: str) -> Dict[str, Any]:
    """
    Runs the marketing agent with a given request.
    
    Args:
        request: The initial marketing request from the user
        
    Returns:
        Dictionary containing the final state with research findings and draft post
    """
    print(f"🚀 Starting marketing agent for request: '{request}'\n")
    
    # Create the agent
    agent = create_marketing_agent()
    
    # Initialize the state
    initial_state = {
        "initial_request": request,
        "research_findings": {},
        "draft_post": "",
        "messages": [HumanMessage(content=request)]
    }
    
    # Run the agent
    final_state = agent.invoke(initial_state)
    
    return final_state

def main():
    """
    Main function demonstrating the marketing agent.
    """
    print("=" * 60)
    print("🎯 LANGGRAPH MARKETING AGENT - TASK 1: FOUNDATIONAL AGENT")
    print("=" * 60)
    print()
    
    # Example marketing requests
    example_requests = [
        "Create a marketing post for a new AI-powered productivity app",
        "Generate content promoting a sustainable fashion brand",
        "Write a post for a local coffee shop's grand opening"
    ]
    
    print("📋 Choose an option:")
    print("   1. Use example requests")
    print("   2. Enter custom marketing request")
    print("\n" + "-" * 40)
    
    # Get user choice
    while True:
        choice = input("\nSelect option (1 or 2): ").strip()
        
        if choice == "1":
            print("\n📋 Example requests:")
            for i, req in enumerate(example_requests, 1):
                print(f"   {i}. {req}")
            
            while True:
                example_choice = input(f"\nSelect example (1-{len(example_requests)} or press Enter for 1): ").strip()
                
                if not example_choice:
                    user_input = example_requests[0]
                    print(f"✅ Using: {user_input}")
                    break
                elif example_choice.isdigit() and 1 <= int(example_choice) <= len(example_requests):
                    user_input = example_requests[int(example_choice) - 1]
                    print(f"✅ Using: {user_input}")
                    break
                else:
                    print(f"❌ Invalid choice. Please enter 1-{len(example_requests)}")
            break
            
        elif choice == "2":
            while True:
                user_input = input("\n✍️  Enter your custom marketing request: ").strip()
                if user_input:
                    print(f"✅ Using custom request: {user_input}")
                    break
                else:
                    print("❌ Please enter a valid marketing request")
            break
        else:
            print("❌ Invalid option. Please enter 1 or 2")
    
    print("\n" + "=" * 60)
    
    try:
        # Run the agent
        result = run_marketing_agent(user_input)
        
        # Display results
        print("\n" + "=" * 60)
        print("📋 FINAL RESULTS")
        print("=" * 60)
        
        print("\n🔍 RESEARCH FINDINGS:")
        print("-" * 30)
        research = result["research_findings"]
        print(f"Topic: {research['topic']}")
        print(f"\nKey Points ({len(research['key_points'])}):")
        for point in research["key_points"]:
            print(f"  • {point}")
        
        print(f"\nCompetitor Insights ({len(research['competitor_insights'])}):")
        for insight in research["competitor_insights"]:
            print(f"  • {insight}")
        
        print(f"\nTrending Hashtags: {', '.join(research['trending_hashtags'])}")
        
        print(f"\n✍️ GENERATED MARKETING POST:")
        print("-" * 30)
        print(result["draft_post"])
        
        print("\n" + "=" * 60)
        print("✅ Marketing agent completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error running marketing agent: {str(e)}")
        print("Please check your OpenAI API key in the .env file")

if __name__ == "__main__":
    main()
