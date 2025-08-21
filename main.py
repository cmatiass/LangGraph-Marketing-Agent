"""
LangGraph Marketing Agent - Task 2: Critique & Refine Loop

This module implements a marketing agent with self-correction capabilities:
1. Researches a topic (placeholder function with mock data)
2. Creates a draft marketing post based on the research
3. Critiques the draft post for improvements
4. Refines the post based on critiques (iterative loop)

The agent uses LangGraph's StateGraph with conditional edges for the refinement loop.
"""

import os
from typing import TypedDict, List, Dict, Any, Literal
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
    State management for the marketing agent with critique & refine loop.
    
    Attributes:
        initial_request: The original user request for the marketing content
        research_findings: Research data gathered about the topic
        draft_post: The generated marketing post draft
        critiques: List of critiques for improving the draft post
        iteration_count: Number of refinement iterations completed
        max_iterations: Maximum number of refinement iterations allowed
        messages: Chat history for the conversation
    """
    initial_request: str
    research_findings: Dict[str, Any]
    draft_post: str
    critiques: List[str]
    iteration_count: int
    max_iterations: int
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
        },
        "success_criteria": [
            "Clear value proposition",
            "Engaging hook",
            "Strong call-to-action",
            "Appropriate tone for target audience",
            "Optimal length for platform"
        ]
    }
    
    print(f"🔍 Research completed for: {initial_request}")
    print(f"📊 Found {len(mock_research['key_points'])} key insights")
    
    return {
        **state,
        "research_findings": mock_research
    }

def copywriting_node(state: AgentState) -> AgentState:
    """
    Copywriting node that creates or refines a marketing post.
    
    This node takes the research data and generates a compelling marketing post
    using an LLM. If critiques exist, it incorporates them for refinement.
    
    Args:
        state: Current agent state with research findings and optional critiques
        
    Returns:
        Updated state with the generated/refined draft post
    """
    research = state["research_findings"]
    initial_request = state["initial_request"]
    critiques = state.get("critiques", [])
    iteration_count = state.get("iteration_count", 0)
    
    # Initialize the language model
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,  # Slightly creative for marketing copy
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create different prompts based on whether this is initial creation or refinement
    if iteration_count == 0:
        # Initial creation prompt
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
        
        Success Criteria:
        {chr(10).join('• ' + criterion for criterion in research['success_criteria'])}
        
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
        print(f"✍️ Creating initial marketing post...")
    else:
        # Refinement prompt
        current_draft = state["draft_post"]
        copywriter_prompt = f"""
        You are an expert marketing copywriter refining a marketing post. 
        
        ORIGINAL REQUEST: "{initial_request}"
        
        CURRENT DRAFT:
        {current_draft}
        
        CRITIQUES TO ADDRESS:
        {chr(10).join('• ' + critique for critique in critiques)}
        
        RESEARCH CONTEXT:
        Key Points: {', '.join(research['key_points'])}
        Success Criteria: {', '.join(research['success_criteria'])}
        Target Audience: {research['audience_demographics']['age_range']} year-olds on {', '.join(research['audience_demographics']['platforms'])}
        
        Please revise the marketing post to address all the critiques while maintaining its strengths. 
        Ensure the refined version:
        1. Addresses each specific critique mentioned above
        2. Maintains the overall marketing effectiveness
        3. Stays true to the original request
        4. Follows best practices for the target platforms
        
        Generate the refined marketing post:
        """
        print(f"🔄 Refining marketing post (iteration {iteration_count + 1})...")
    
    # Generate the marketing post
    messages = [
        SystemMessage(content="You are a skilled marketing copywriter focused on creating engaging, conversion-optimized content."),
        HumanMessage(content=copywriter_prompt)
    ]
    
    response = model.invoke(messages)
    draft_post = response.content
    
    print(f"📝 Post generated! Length: {len(draft_post)} characters")
    
    return {
        **state,
        "draft_post": draft_post,
        "iteration_count": iteration_count + 1
    }

def critic_node(state: AgentState) -> AgentState:
    """
    Critic node that analyzes the draft post and provides improvement suggestions.
    
    This node evaluates the draft against the original request and research findings,
    producing a list of critiques for refinement.
    
    Args:
        state: Current agent state with draft post and research findings
        
    Returns:
        Updated state with critiques list
    """
    draft_post = state["draft_post"]
    initial_request = state["initial_request"]
    research = state["research_findings"]
    iteration_count = state["iteration_count"]
    
    # Initialize the language model
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,  # Lower temperature for more consistent critique
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    critic_prompt = f"""
    You are an expert marketing critic with years of experience in social media marketing, 
    content strategy, and conversion optimization. Your job is to provide constructive, 
    specific critiques of marketing content.
    
    ORIGINAL REQUEST: "{initial_request}"
    
    DRAFT MARKETING POST TO CRITIQUE:
    {draft_post}
    
    RESEARCH CONTEXT:
    Success Criteria: {', '.join(research['success_criteria'])}
    Key Points: {', '.join(research['key_points'])}
    Target Audience: {research['audience_demographics']['age_range']} year-olds interested in {', '.join(research['audience_demographics']['interests'])}
    Primary Platforms: {', '.join(research['audience_demographics']['platforms'])}
    Competitor Insights: {', '.join(research['competitor_insights'])}
    
    Please evaluate this marketing post and provide specific, actionable critiques. 
    Focus on these key areas:
    
    1. **Hook & Engagement**: Does it grab attention in the first line?
    2. **Value Proposition**: Are the benefits clear and compelling?
    3. **Target Audience**: Is the tone and content appropriate for the target demographic?
    4. **Call-to-Action**: Is there a clear, compelling CTA?
    5. **Platform Optimization**: Is it optimized for the intended social platforms?
    6. **Length & Readability**: Is it the right length and easy to read?
    7. **Hashtag Usage**: Are hashtags relevant and not excessive?
    8. **Original Request Alignment**: Does it fulfill the original request?
    
    IMPORTANT INSTRUCTIONS:
    - If the post is already excellent and meets all criteria, respond with exactly: "No critiques - the post is ready."
    - If there are issues, provide 1-3 specific, actionable critiques
    - Each critique should be clear, specific, and explain WHY it needs improvement
    - Focus on the most important issues first
    - Be constructive, not just critical
    
    Your response should be either "No critiques - the post is ready." OR a numbered list of specific critiques:
    """
    
    messages = [
        SystemMessage(content="You are a marketing expert providing constructive critique to improve content quality."),
        HumanMessage(content=critic_prompt)
    ]
    
    response = model.invoke(messages)
    critique_response = response.content.strip()
    
    print(f"🔍 Critique analysis completed (iteration {iteration_count})")
    
    # Parse the critiques
    if "No critiques - the post is ready." in critique_response.lower():
        critiques = []
        print("✅ No critiques found - post is ready!")
    else:
        # Extract individual critiques (assuming they're numbered)
        critique_lines = [line.strip() for line in critique_response.split('\n') if line.strip()]
        critiques = []
        
        for line in critique_lines:
            # Look for numbered items or bullet points
            if any(line.startswith(prefix) for prefix in ['1.', '2.', '3.', '•', '-', '*']):
                critiques.append(line)
        
        # If no numbered items found, treat the whole response as one critique
        if not critiques and critique_response:
            critiques = [critique_response]
        
        print(f"📝 Found {len(critiques)} critique(s):")
        for i, critique in enumerate(critiques, 1):
            print(f"   {i}. {critique}")
    
    return {
        **state,
        "critiques": critiques
    }

def should_continue(state: AgentState) -> Literal["copywriting", "END"]:
    """
    Conditional edge function that determines whether to continue refining or finish.
    
    Args:
        state: Current agent state with critiques
        
    Returns:
        "copywriting" if refinement needed, "END" if post is ready
    """
    critiques = state.get("critiques", [])
    iteration_count = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 3)
    
    # Check if we should continue refining
    if not critiques:
        print("🎉 No critiques found - post is ready!")
        return "END"
    elif iteration_count >= max_iterations:
        print(f"⚠️ Maximum iterations ({max_iterations}) reached - finishing with current draft")
        return "END"
    else:
        print(f"🔄 Critiques found - continuing to refinement (iteration {iteration_count + 1})")
        return "copywriting"

def create_marketing_agent():
    """
    Creates and compiles the marketing agent StateGraph with critique & refine loop.
    
    The agent follows this flow:
    START → research → copywriting → critic → [continue/end decision]
              ↑                                    ↓
              └─────────← (if critiques exist) ───┘
    
    Returns:
        Compiled LangGraph agent ready for execution
    """
    # Create the StateGraph
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("research", research_node)
    workflow.add_node("copywriting", copywriting_node)
    workflow.add_node("critic", critic_node)
    
    # Define the flow
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "copywriting")
    workflow.add_edge("copywriting", "critic")
    
    # Add conditional edge from critic
    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {
            "copywriting": "copywriting",  # Loop back for refinement
            "END": END                     # Finish if no critiques
        }
    )
    
    # Compile the graph
    app = workflow.compile()
    
    return app

def run_marketing_agent(request: str, max_iterations: int = 3) -> Dict[str, Any]:
    """
    Runs the marketing agent with critique & refine loop.
    
    Args:
        request: The initial marketing request from the user
        max_iterations: Maximum number of refinement iterations (default: 3)
        
    Returns:
        Dictionary containing the final state with research, critiques, and final post
    """
    print(f"🚀 Starting marketing agent with critique & refine loop")
    print(f"📝 Request: '{request}'")
    print(f"🔄 Max iterations: {max_iterations}\n")
    
    # Create the agent
    agent = create_marketing_agent()
    
    # Initialize the state
    initial_state = {
        "initial_request": request,
        "research_findings": {},
        "draft_post": "",
        "critiques": [],
        "iteration_count": 0,
        "max_iterations": max_iterations,
        "messages": [HumanMessage(content=request)]
    }
    
    # Run the agent
    final_state = agent.invoke(initial_state)
    
    return final_state

def main():
    """
    Main function demonstrating the marketing agent with critique & refine loop.
    """
    print("=" * 70)
    print("🎯 LANGGRAPH MARKETING AGENT - TASK 2: CRITIQUE & REFINE LOOP")
    print("=" * 70)
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
    
    # Get max iterations preference
    while True:
        max_iter_input = input(f"\n🔄 Max refinement iterations (1-5, press Enter for 3): ").strip()
        if not max_iter_input:
            max_iterations = 3
            break
        elif max_iter_input.isdigit() and 1 <= int(max_iter_input) <= 5:
            max_iterations = int(max_iter_input)
            break
        else:
            print("❌ Please enter a number between 1 and 5")
    
    print(f"⚙️ Using {max_iterations} max iterations")
    print("\n" + "=" * 70)
    
    try:
        # Run the agent
        result = run_marketing_agent(user_input, max_iterations)
        
        # Display results
        print("\n" + "=" * 70)
        print("📋 FINAL RESULTS")
        print("=" * 70)
        
        print(f"\n� REFINEMENT SUMMARY:")
        print("-" * 35)
        print(f"Total iterations completed: {result['iteration_count']}")
        print(f"Final critiques: {len(result.get('critiques', []))}")
        
        if result.get('critiques'):
            print("\nFinal critiques that couldn't be resolved:")
            for i, critique in enumerate(result['critiques'], 1):
                print(f"  {i}. {critique}")
        
        print(f"\n🔍 RESEARCH FINDINGS:")
        print("-" * 30)
        research = result["research_findings"]
        print(f"Topic: {research['topic']}")
        print(f"\nKey Points ({len(research['key_points'])}):")
        for point in research["key_points"]:
            print(f"  • {point}")
        
        print(f"\n✍️ FINAL MARKETING POST:")
        print("-" * 30)
        print(result["draft_post"])
        
        print("\n" + "=" * 70)
        print("✅ Marketing agent with critique & refine loop completed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error running marketing agent: {str(e)}")
        print("Please check your OpenAI API key in the .env file")

if __name__ == "__main__":
    main()
