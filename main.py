"""
LangGraph Marketing Agent by Carlos Matías Sáez 
GitHub: https://github.com/cmatiass

This module implements a marketing agent with self-correction capabilities:
1. Researches a topic (placeholder function with mock data)
2. Creates a draft marketing post based on the research
3. Critiques the draft post for improvements
4. Refines the post based on critiques (iterative loop)
5. Seeks human approval for the final post

"""

import os
from typing import TypedDict, List, Dict, Any, Literal
from typing_extensions import Annotated
from datetime import datetime

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class AgentState(TypedDict):
    """
    State management for the marketing agent with critique & refine loop and human approval.
    
    Attributes:
        initial_request: The original user request for the marketing content
        research_findings: Research data gathered about the topic
        draft_post: The generated marketing post draft
        critiques: List of critiques for improving the draft post
        iteration_count: Number of refinement iterations completed
        max_iterations: Maximum number of refinement iterations allowed
        human_approved: Boolean indicating if the post has been approved by a human
        approval_attempts: Number of times human approval has been requested
        messages: Chat history for the conversation
    """
    initial_request: str
    research_findings: Dict[str, Any]
    draft_post: str
    critiques: List[str]
    iteration_count: int
    max_iterations: int
    human_approved: bool
    approval_attempts: int
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
        
        # Check if we have human feedback vs AI critiques
        has_human_feedback = any("Human feedback:" in critique for critique in critiques)
        feedback_type = "HUMAN FEEDBACK" if has_human_feedback else "AI CRITIQUES"
        
        copywriter_prompt = f"""
        You are an expert marketing copywriter refining a marketing post. 
        
        ORIGINAL REQUEST: "{initial_request}"
        
        CURRENT DRAFT:
        {current_draft}
        
        {feedback_type} TO ADDRESS:
        {chr(10).join('• ' + critique for critique in critiques)}
        
        RESEARCH CONTEXT:
        Key Points: {', '.join(research['key_points'])}
        Success Criteria: {', '.join(research['success_criteria'])}
        Target Audience: {research['audience_demographics']['age_range']} year-olds on {', '.join(research['audience_demographics']['platforms'])}
        
        IMPORTANT: {"This is direct feedback from a human reviewer. Please follow their specific instructions carefully and prioritize their requirements above all else." if has_human_feedback else "These are AI-generated critiques for improvement."}
        
        Please revise the marketing post to address all the feedback while maintaining its strengths. 
        Ensure the refined version:
        1. Addresses each specific point mentioned above {"(especially the human feedback)" if has_human_feedback else ""}
        2. Maintains the overall marketing effectiveness
        3. Stays true to the original request
        4. Follows best practices for the target platforms
        
        Generate the refined marketing post:
        """
        feedback_source = "human feedback" if has_human_feedback else f"AI critiques"
        print(f"🔄 Refining marketing post based on {feedback_source} (iteration {iteration_count + 1})...")
    
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

def human_approval_node(state: AgentState) -> AgentState:
    """
    Human approval node that requests human review and approval of the draft post.
    
    This node presents the finalized draft post to a human reviewer and waits
    for their approval or rejection decision.
    
    Args:
        state: Current agent state with draft post ready for human review
        
    Returns:
        Updated state with human approval status
    """
    draft_post = state["draft_post"]
    initial_request = state["initial_request"]
    iteration_count = state["iteration_count"]
    approval_attempts = state.get("approval_attempts", 0)
    
    print("\n" + "=" * 60)
    print("👤 HUMAN APPROVAL REQUIRED")
    print("=" * 60)
    
    print(f"\n📝 Original Request: {initial_request}")
    print(f"🔄 Refinement Iterations Completed: {iteration_count}")
    print(f"👥 Approval Attempt: {approval_attempts + 1}")
    
    print(f"\n📋 DRAFT POST FOR REVIEW:")
    print("-" * 40)
    print(draft_post)
    print("-" * 40)
    
    # Human approval loop
    while True:
        try:
            approval = input("\n👤 Do you approve this marketing post? [y/n/feedback]: ").strip().lower()
            
            if approval in ['y', 'yes']:
                print("✅ Post approved by human reviewer!")
                return {
                    **state,
                    "human_approved": True,
                    "approval_attempts": approval_attempts + 1
                }
            
            elif approval in ['n', 'no']:
                print("❌ Post rejected by human reviewer.")
                print("🔄 Returning to critique & refine loop for improvements...")
                return {
                    **state,
                    "human_approved": False,
                    "approval_attempts": approval_attempts + 1,
                    "critiques": ["Human reviewer requested improvements to the overall post quality and effectiveness."],
                    "iteration_count": 0  # Reset iteration count for new refinement cycle
                }
            
            elif approval in ['feedback', 'f']:
                print("\n💬 Please provide specific feedback for improvement:")
                human_feedback = input("Your feedback: ").strip()
                if human_feedback:
                    print(f"📝 Human feedback recorded: {human_feedback}")
                    print("🔄 Returning to critique & refine loop with human feedback...")
                    return {
                        **state,
                        "human_approved": False,
                        "approval_attempts": approval_attempts + 1,
                        "critiques": [f"Human feedback: {human_feedback}"],
                        "iteration_count": 0  # Reset iteration count for new refinement cycle
                    }
                else:
                    print("❌ No feedback provided. Please try again.")
            
            else:
                print("❌ Invalid input. Please enter 'y' for yes, 'n' for no, or 'feedback' for specific feedback.")
                
        except KeyboardInterrupt:
            print("\n⚠️ Human approval interrupted. Treating as rejection.")
            return {
                **state,
                "human_approved": False,
                "approval_attempts": approval_attempts + 1,
                "critiques": ["Human approval process was interrupted."],
                "iteration_count": 0
            }
        except Exception as e:
            print(f"❌ Error during human approval: {e}")
            print("Treating as rejection and continuing...")
            return {
                **state,
                "human_approved": False,
                "approval_attempts": approval_attempts + 1,
                "critiques": ["Error occurred during human approval process."],
                "iteration_count": 0
            }

def should_continue(state: AgentState) -> Literal["human_approval", "copywriting", "END"]:
    """
    Conditional edge function that determines the next step in the workflow.
    
    Args:
        state: Current agent state with critiques and iteration count
        
    Returns:
        "human_approval" if no critiques and ready for human review
        "copywriting" if refinement needed
        "END" if human approved or max attempts reached
    """
    critiques = state.get("critiques", [])
    iteration_count = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 3)
    human_approved = state.get("human_approved", False)
    approval_attempts = state.get("approval_attempts", 0)
    
    # If human has already approved, end the process
    if human_approved:
        print("🎉 Human approved - process complete!")
        return "END"
    
    # If no critiques from critic_node, proceed to human approval
    if not critiques and iteration_count > 0:
        print("✅ No AI critiques found - proceeding to human approval")
        return "human_approval"
    
    # If there are critiques and we haven't reached max iterations, continue refining
    elif critiques and iteration_count < max_iterations:
        print(f"🔄 Critiques found - continuing to refinement (iteration {iteration_count + 1})")
        return "copywriting"
    
    # If we've reached max iterations, still go to human approval for final decision
    elif iteration_count >= max_iterations:
        print(f"⚠️ Maximum iterations ({max_iterations}) reached - proceeding to human approval")
        return "human_approval"
    
    # Default fallback
    else:
        return "human_approval"

def create_marketing_agent():
    """
    Creates and compiles the marketing agent StateGraph with critique & refine loop and human approval.
    
    Returns:
        Compiled LangGraph agent ready for execution
    """
    # Create the StateGraph
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("research", research_node)
    workflow.add_node("copywriting", copywriting_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("human_approval", human_approval_node)
    
    # Define the flow
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "copywriting")
    workflow.add_edge("copywriting", "critic")
    
    # Add conditional edge from critic
    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {
            "copywriting": "copywriting",        # Loop back for refinement
            "human_approval": "human_approval",  # Proceed to human review
            "END": END                           # Finis if approved
        }
    )
    
    # Add conditional edge from human approval
    workflow.add_conditional_edges(
        "human_approval",
        lambda state: "END" if state.get("human_approved", False) else "copywriting",
        {
            "copywriting": "copywriting",  # Loop back if rejected
            "END": END                    # Finish if approved
        }
    )
    
    # Compile the graph
    app = workflow.compile()
    
    return app

def generate_markdown_report(state: Dict[str, Any], filename: str = None) -> str:
    """
    Generates a comprehensive markdown report of the marketing agent process and results.
    
    Args:
        state: Final state from the marketing agent
        filename: Optional filename for the report (auto-generated if not provided)
        
    Returns:
        Path to the generated markdown file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"marketing_report_{timestamp}.md"
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)
    
    research = state.get("research_findings", {})
    draft_post = state.get("draft_post", "")
    initial_request = state.get("initial_request", "")
    iteration_count = state.get("iteration_count", 0)
    critiques = state.get("critiques", [])
    human_approved = state.get("human_approved", False)
    approval_attempts = state.get("approval_attempts", 0)
    
    # Generate the markdown content
    markdown_content = f"""# Marketing Agent Report

## 📋 Executive Summary

**Generated on**: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
**Initial Request**: {initial_request}
**Process Status**: {"✅ Approved" if human_approved else "⏸️ Incomplete"}
**Total Refinement Iterations**: {iteration_count}
**Human Approval Attempts**: {approval_attempts}

---

## 🔬 Research Findings

### Topic Analysis
**Subject**: {research.get('topic', 'Not specified')}

### Key Insights
{chr(10).join('- ' + point for point in research.get('key_points', ['No key points available']))}

### Target Audience Profile
- **Age Range**: {research.get('audience_demographics', {}).get('age_range', 'Not specified')}
- **Primary Platforms**: {', '.join(research.get('audience_demographics', {}).get('platforms', ['Not specified']))}
- **Interests**: {', '.join(research.get('audience_demographics', {}).get('interests', ['Not specified']))}

### Competitor Insights
{chr(10).join('- ' + insight for insight in research.get('competitor_insights', ['No competitor insights available']))}

### Trending Hashtags
{', '.join(research.get('trending_hashtags', ['No hashtags identified']))}

### Success Criteria
{chr(10).join('- ' + criterion for criterion in research.get('success_criteria', ['No success criteria specified']))}

---

## ✍️ Final Marketing Post

```
{draft_post if draft_post else "No content generated"}
```

### Content Statistics
- **Character Count**: {len(draft_post)}
- **Word Count**: {len(draft_post.split())}
- **Estimated Reading Time**: {max(1, len(draft_post.split()) // 200)} minute(s)

---

## 🔄 Refinement Process

### Iteration Summary
- **Total Iterations**: {iteration_count}
- **Final Status**: {"Ready for publication" if human_approved else "Requires further refinement"}

### Final Critiques
{chr(10).join('- ' + critique for critique in critiques) if critiques else "No outstanding critiques"}

---

## 👤 Human Review Process

### Approval Status
**Status**: {"✅ Approved by human reviewer" if human_approved else "❌ Pending human approval"}
**Review Attempts**: {approval_attempts}

---

## 📊 Process Metrics

| Metric | Value |
|--------|-------|
| Research Points Identified | {len(research.get('key_points', []))} |
| Competitor Insights Found | {len(research.get('competitor_insights', []))} |
| Trending Hashtags Identified | {len(research.get('trending_hashtags', []))} |
| Success Criteria Defined | {len(research.get('success_criteria', []))} |
| Refinement Iterations | {iteration_count} |
| Outstanding Critiques | {len(critiques)} |
| Human Approval Status | {"Approved" if human_approved else "Pending"} |

---

## 🚀 Next Steps

{"""✅ **Content Ready for Publication**
- The marketing post has been approved by human reviewer
- Content meets all quality standards
- Ready for deployment across target platforms""" if human_approved else """⏸️ **Action Required**
- Human approval still needed
- Consider addressing any outstanding critiques
- Review content against success criteria"""}

---

## 🔧 Technical Details

**Agent Configuration**:
- Max Iterations: {state.get('max_iterations', 'Not specified')}
- AI Model: GPT-4o
- Temperature Settings: Creative (0.7) / Analytical (0.3)

**Generated by**: LangGraph Marketing Agent
"""

    # Write the markdown file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"📄 Marketing report generated: {filename}")
        print(f"📁 File location: {filepath}")
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error generating markdown report: {e}")
        return None

def run_marketing_agent(request: str, max_iterations: int = 3) -> Dict[str, Any]:
    """
    Runs the marketing agent with critique & refine loop and human approval.
    
    Args:
        request: The initial marketing request from the user
        max_iterations: Maximum number of refinement iterations (default: 3)
        
    Returns:
        Dictionary containing the final state with research, critiques, approval status, and final post
    """
    print(f"🚀 Starting marketing agent with critique & refine loop + human approval")
    print(f"📝 Request: '{request}'")
    print(f"🔄 Max iterations: {max_iterations}")
    print(f"👤 Human approval: Required\n")
    
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
        "human_approved": False,
        "approval_attempts": 0,
        "messages": [HumanMessage(content=request)]
    }
    
    # Run the agent
    final_state = agent.invoke(initial_state)
    
    # Generate markdown report automatically
    print("\n📄 Generating comprehensive report...")
    report_path = generate_markdown_report(final_state)
    if report_path:
        final_state["report_path"] = report_path
    
    return final_state

def main():
    """
    Main function demonstrating the marketing agent with critique & refine loop.
    """
    print("=" * 80)
    print("🎯 LANGGRAPH MARKETING AGENT")
    print("=" * 80)
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
    print("👤 Human approval will be required for final review")
    print("\n" + "=" * 80)
    
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
        
        # Show report information
        if "report_path" in result:
            print(f"\n📄 COMPREHENSIVE REPORT:")
            print("-" * 30)
            print(f"Report generated: {os.path.basename(result['report_path'])}")
            print(f"Location: {result['report_path']}")
            print("This report contains detailed analysis, metrics, and the complete process history.")
        
        print("\n" + "=" * 70)
        print("✅ Marketing agent with critique & refine loop completed!")
        if "report_path" in result:
            print(f"📄 Comprehensive report saved as: {os.path.basename(result['report_path'])}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error running marketing agent: {str(e)}")
        print("Please check your OpenAI API key in the .env file")

if __name__ == "__main__":
    main()
