"""
FastAPI Backend for LangGraph Marketing Agent with Human Approval
Provides REST API and WebSocket endpoints for the React frontend
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, List, TypedDict, Literal
from typing_extensions import Annotated
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# LangGraph and AI imports
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# AgentState definition
class AgentState(TypedDict):
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
    """Research node that simulates researching a topic."""
    initial_request = state["initial_request"]
    
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
    
    return {
        **state,
        "research_findings": mock_research
    }

def copywriting_node(state: AgentState) -> AgentState:
    """Copywriting node that creates or refines a marketing post."""
    research = state["research_findings"]
    initial_request = state["initial_request"]
    critiques = state.get("critiques", [])
    iteration_count = state.get("iteration_count", 0)
    
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    if iteration_count == 0:
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
    else:
        current_draft = state["draft_post"]
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
    
    messages = [
        SystemMessage(content="You are a skilled marketing copywriter focused on creating engaging, conversion-optimized content."),
        HumanMessage(content=copywriter_prompt)
    ]
    
    response = model.invoke(messages)
    draft_post = response.content
    
    return {
        **state,
        "draft_post": draft_post,
        "iteration_count": iteration_count + 1
    }

def critic_node(state: AgentState) -> AgentState:
    """Critic node that analyzes the draft post and provides improvement suggestions."""
    draft_post = state["draft_post"]
    initial_request = state["initial_request"]
    research = state["research_findings"]
    
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
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
    
    if "No critiques - the post is ready." in critique_response.lower():
        critiques = []
    else:
        critique_lines = [line.strip() for line in critique_response.split('\n') if line.strip()]
        critiques = []
        
        for line in critique_lines:
            if any(line.startswith(prefix) for prefix in ['1.', '2.', '3.', '•', '-', '*']):
                critiques.append(line)
        
        if not critiques and critique_response:
            critiques = [critique_response]
    
    return {
        **state,
        "critiques": critiques
    }

def human_approval_node(state: AgentState) -> AgentState:
    """
    Human approval node that requests human review and approval of the draft post.
    This will be handled via WebSocket interaction with the frontend.
    """
    return state  # State will be updated by WebSocket handler

def should_continue(state: AgentState) -> Literal["human_approval", "copywriting", "END"]:
    """Conditional edge function that determines the next step in the workflow."""
    critiques = state.get("critiques", [])
    iteration_count = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 3)
    human_approved = state.get("human_approved", False)
    
    # If human has already approved, end the process
    if human_approved:
        return "END"
    
    # If no critiques from critic_node, proceed to human approval
    if not critiques and iteration_count > 0:
        return "human_approval"
    
    # If there are critiques and we haven't reached max iterations, continue refining
    elif critiques and iteration_count < max_iterations:
        return "copywriting"
    
    # If we've reached max iterations, still go to human approval for final decision
    elif iteration_count >= max_iterations:
        return "human_approval"
    
    # Default fallback
    else:
        return "human_approval"

def create_marketing_agent():
    """Creates and compiles the marketing agent StateGraph."""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("research", research_node)
    workflow.add_node("copywriting", copywriting_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("human_approval", human_approval_node)
    
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
            "END": END                           # Finish if approved
        }
    )
    
    # Add conditional edge from human approval
    workflow.add_conditional_edges(
        "human_approval",
        lambda state: "END" if state.get("human_approved", False) else "copywriting",
        {
            "copywriting": "copywriting",  # Loop back if rejected/feedback given
            "END": END                    # Finish if approved
        }
    )
    
    app = workflow.compile()
    return app

def generate_markdown_report(state: Dict[str, Any], filename: str = None) -> str:
    """Generates a comprehensive markdown report of the marketing agent process and results."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"marketing_report_{timestamp}.md"
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)
    
    research = state.get("research_findings", {})
    draft_post = state.get("draft_post", "")
    initial_request = state.get("initial_request", "")
    iteration_count = state.get("iteration_count", 0)
    critiques = state.get("critiques", [])
    human_approved = state.get("human_approved", False)
    approval_attempts = state.get("approval_attempts", 0)
    
    markdown_content = f"""# Marketing Agent Report

## 📋 Executive Summary

**Generated on**: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
**Initial Request**: {initial_request}
**Process Status**: {"✅ Approved" if human_approved else "⏸️ Incomplete"}
**Total Refinement Iterations**: {iteration_count}
**Human Approval Attempts**: {approval_attempts}

---

## ✍️ Final Marketing Post

```
{draft_post if draft_post else "No content generated"}
```

### Content Statistics
- **Character Count**: {len(draft_post)}
- **Word Count**: {len(draft_post.split())}

---

## 🔬 Research Findings

### Key Insights
{chr(10).join('- ' + point for point in research.get('key_points', ['No key points available']))}

### Target Audience Profile
- **Age Range**: {research.get('audience_demographics', {}).get('age_range', 'Not specified')}
- **Primary Platforms**: {', '.join(research.get('audience_demographics', {}).get('platforms', ['Not specified']))}
- **Interests**: {', '.join(research.get('audience_demographics', {}).get('interests', ['Not specified']))}

### Outstanding Critiques
{chr(10).join('- ' + critique for critique in critiques) if critiques else "No outstanding critiques"}

---

## 👤 Human Review Process

### Approval Status
**Status**: {"✅ Approved by human reviewer" if human_approved else "❌ Pending human approval"}
**Review Attempts**: {approval_attempts}

---

**Generated by**: LangGraph Marketing Agent Web Version
"""

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        return filepath
    except Exception as e:
        print(f"❌ Error generating markdown report: {e}")
        return None

# Pydantic models for API
class MarketingRequest(BaseModel):
    request: str
    max_iterations: int = 3

class MarketingResponse(BaseModel):
    success: bool
    task_id: str
    message: str

class TaskStatus(BaseModel):
    task_id: str
    status: str  # "running", "completed", "error", "awaiting_approval"
    progress: int  # 0-100
    current_step: str
    result: Dict[str, Any] = None
    error: str = None

class HumanFeedback(BaseModel):
    action: str  # "approve", "reject", "feedback"
    feedback: str = ""  # Optional feedback text

# Global state management
active_tasks = {}
websocket_connections = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 LangGraph Marketing Agent API starting...")
    yield
    # Shutdown
    print("🛑 LangGraph Marketing Agent API shutting down...")

# Create FastAPI app
app = FastAPI(
    title="LangGraph Marketing Agent API",
    description="REST API and WebSocket interface for the LangGraph Marketing Agent with critique & refine loop and human approval",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for React frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    # Mount the React static files (CSS, JS, etc.)
    react_static_dir = os.path.join(static_dir, "static")
    if os.path.exists(react_static_dir):
        app.mount("/static", StaticFiles(directory=react_static_dir), name="react_static")
    
    # Also mount the root static directory for other files (favicon, manifest, etc.)
    app.mount("/assets", StaticFiles(directory=static_dir), name="assets")

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        await self.send_personal_message("Connected to LangGraph Marketing Agent", client_id)

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(message)
            except:
                self.disconnect(client_id)

    async def send_json_message(self, data: dict, client_id: str):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(json.dumps(data))
            except:
                self.disconnect(client_id)

manager = WebSocketManager()

async def run_marketing_agent_async(request: str, max_iterations: int, client_id: str) -> Dict[str, Any]:
    """
    Async version of the marketing agent that sends real-time updates via WebSocket
    """
    try:
        # Send initial status
        await manager.send_json_message({
            "type": "status",
            "status": "starting",
            "progress": 0,
            "current_step": "Initializing agent",
            "message": f"Starting marketing agent for: '{request}'"
        }, client_id)

        # Create the agent
        await manager.send_json_message({
            "type": "status",
            "status": "running",
            "progress": 10,
            "current_step": "Creating agent",
            "message": "Setting up LangGraph marketing agent..."
        }, client_id)
        
        agent = create_marketing_agent()
        
        # Initialize state
        await manager.send_json_message({
            "type": "status",
            "status": "running",
            "progress": 20,
            "current_step": "Starting research",
            "message": "Initializing agent state and beginning research phase..."
        }, client_id)
        
        initial_state = {
            "initial_request": request,
            "research_findings": {},
            "draft_post": "",
            "critiques": [],
            "iteration_count": 0,
            "max_iterations": max_iterations,
            "human_approved": False,
            "approval_attempts": 0,
            "messages": []
        }
        
        # Research phase
        await manager.send_json_message({
            "type": "status",
            "status": "running",
            "progress": 30,
            "current_step": "Researching topic",
            "message": "🔍 Conducting market research and analysis..."
        }, client_id)
        
        state = research_node(initial_state)
        
        await manager.send_json_message({
            "type": "research_complete",
            "research_findings": state["research_findings"],
            "message": f"📊 Research completed - found {len(state['research_findings']['key_points'])} key insights"
        }, client_id)
        
        # Main agent loop - continue until human approval or completion
        while not state.get("human_approved", False):
            # Copywriting phase
            progress_base = 50 + (state.get("iteration_count", 0) * 10)
            await manager.send_json_message({
                "type": "status",
                "status": "running",
                "progress": min(progress_base, 90),
                "current_step": f"Creating draft (iteration {state.get('iteration_count', 0) + 1})",
                "message": "✍️ Generating/refining marketing post..."
            }, client_id)
            
            state = copywriting_node(state)
            
            await manager.send_json_message({
                "type": "draft_created",
                "draft_post": state["draft_post"],
                "iteration": state["iteration_count"],
                "message": f"📝 Draft {'created' if state['iteration_count'] == 1 else 'refined'} ({len(state['draft_post'])} characters)"
            }, client_id)
            
            # Critic phase
            await manager.send_json_message({
                "type": "status",
                "status": "running",
                "progress": min(progress_base + 5, 90),
                "current_step": f"Analyzing draft (iteration {state['iteration_count']})",
                "message": "🔍 Analyzing draft for improvements..."
            }, client_id)
            
            state = critic_node(state)
            
            if not state["critiques"]:
                await manager.send_json_message({
                    "type": "critique_complete",
                    "critiques": [],
                    "message": "✅ No critiques found - ready for human review!"
                }, client_id)
                
                # Proceed to human approval
                await manager.send_json_message({
                    "type": "awaiting_human_approval",
                    "draft_post": state["draft_post"],
                    "research_findings": state["research_findings"],
                    "iteration_count": state["iteration_count"],
                    "message": "👤 Ready for human review - awaiting your approval..."
                }, client_id)
                
                # Wait for human feedback
                return state
                
            elif state["critiques"] and state["iteration_count"] < max_iterations:
                await manager.send_json_message({
                    "type": "critique_complete",
                    "critiques": state["critiques"],
                    "message": f"📝 Found {len(state['critiques'])} improvements to make - continuing refinement..."
                }, client_id)
                # Continue the loop for refinement
                
            else:
                # Max iterations reached
                await manager.send_json_message({
                    "type": "critique_complete",
                    "critiques": state["critiques"],
                    "message": f"⚠️ Maximum iterations ({max_iterations}) reached - proceeding to human review..."
                }, client_id)
                
                # Proceed to human approval
                await manager.send_json_message({
                    "type": "awaiting_human_approval",
                    "draft_post": state["draft_post"],
                    "research_findings": state["research_findings"],
                    "iteration_count": state["iteration_count"],
                    "message": "👤 Ready for human review - awaiting your approval..."
                }, client_id)
                
                # Wait for human feedback
                return state
        
        # Generate report if approved
        await manager.send_json_message({
            "type": "status",
            "status": "running",
            "progress": 95,
            "current_step": "Generating report",
            "message": "📄 Creating comprehensive report..."
        }, client_id)
        
        report_path = generate_markdown_report(state)
        if report_path:
            state["report_path"] = report_path
        
        # Complete
        await manager.send_json_message({
            "type": "status",
            "status": "completed",
            "progress": 100,
            "current_step": "Process complete",
            "message": "🎉 Marketing agent process completed successfully!"
        }, client_id)
        
        return state
        
    except Exception as e:
        await manager.send_json_message({
            "type": "status",
            "status": "error",
            "progress": 0,
            "current_step": "Error occurred",
            "message": f"❌ Error: {str(e)}",
            "error": str(e)
        }, client_id)
        raise

@app.get("/")
async def root():
    """Serve the React frontend index.html"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    index_file = os.path.join(static_dir, "index.html")
    
    if os.path.isfile(index_file):
        return FileResponse(index_file)
    else:
        return {"message": "Frontend not built. Please build the React app first.", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/marketing/generate", response_model=MarketingResponse)
async def generate_marketing_post(request: MarketingRequest):
    """Start a new marketing post generation task"""
    task_id = str(uuid.uuid4())
    
    # Store task info
    active_tasks[task_id] = {
        "id": task_id,
        "status": "pending",
        "progress": 0,
        "current_step": "Queued",
        "request": request.request,
        "max_iterations": request.max_iterations,
        "created_at": datetime.now().isoformat(),
        "result": None,
        "error": None,
        "state": None
    }
    
    return MarketingResponse(
        success=True,
        task_id=task_id,
        message=f"Marketing post generation task created with ID: {task_id}"
    )

@app.post("/api/marketing/{task_id}/human-feedback")
async def submit_human_feedback(task_id: str, feedback: HumanFeedback):
    """Submit human feedback for a task awaiting approval"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = active_tasks[task_id]
    state = task.get("state")
    
    if not state:
        raise HTTPException(status_code=400, detail="Task state not available")
    
    # Update approval attempts
    state["approval_attempts"] = state.get("approval_attempts", 0) + 1
    
    if feedback.action == "approve":
        state["human_approved"] = True
        task["status"] = "completed"
        
        # Generate final report
        report_path = generate_markdown_report(state)
        if report_path:
            state["report_path"] = report_path
        
        task["result"] = state
        
        return {"message": "Post approved successfully", "status": "completed"}
        
    elif feedback.action == "reject":
        state["human_approved"] = False
        state["critiques"] = ["Human reviewer requested general improvements to the overall post quality and effectiveness."]
        state["iteration_count"] = 0  # Reset for new refinement cycle
        
        return {"message": "Post rejected - will continue refinement", "status": "continuing"}
        
    elif feedback.action == "feedback":
        if not feedback.feedback:
            raise HTTPException(status_code=400, detail="Feedback text required")
            
        state["human_approved"] = False
        state["critiques"] = [f"Human feedback: {feedback.feedback}"]
        state["iteration_count"] = 0  # Reset for new refinement cycle
        
        return {"message": "Feedback received - will continue refinement", "status": "continuing"}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

@app.get("/api/marketing/status/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """Get the status of a marketing post generation task"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = active_tasks[task_id]
    return TaskStatus(**{k: v for k, v in task.items() if k != "state"})

@app.get("/api/marketing/examples")
async def get_example_requests():
    """Get example marketing requests"""
    return {
        "examples": [
            "Create a marketing post for a new AI-powered productivity app",
            "Generate content promoting a sustainable fashion brand",
            "Write a post for a local coffee shop's grand opening",
            "Marketing campaign for a fitness app launch",
            "Social media content for a tech startup funding announcement"
        ]
    }

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time communication"""
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "start_generation":
                task_id = message["task_id"]
                
                if task_id not in active_tasks:
                    await manager.send_json_message({
                        "type": "error",
                        "message": "Task not found"
                    }, client_id)
                    continue
                
                task = active_tasks[task_id]
                
                # Update task status
                task["status"] = "running"
                task["progress"] = 0
                task["current_step"] = "Starting"
                
                try:
                    # Run the marketing agent
                    result = await run_marketing_agent_async(
                        task["request"],
                        task["max_iterations"],
                        client_id
                    )
                    
                    # Store state for human approval
                    task["state"] = result
                    task["status"] = "awaiting_approval"
                    task["current_step"] = "Awaiting human approval"
                    task["completed_at"] = datetime.now().isoformat()
                    
                    # Send to human approval phase
                    await manager.send_json_message({
                        "type": "awaiting_human_approval",
                        "task_id": task_id,
                        "draft_post": result["draft_post"],
                        "research_findings": result["research_findings"],
                        "iteration_count": result["iteration_count"],
                        "critiques": result.get("critiques", [])
                    }, client_id)
                    
                except Exception as e:
                    task["status"] = "error"
                    task["error"] = str(e)
                    task["completed_at"] = datetime.now().isoformat()
                    
                    await manager.send_json_message({
                        "type": "generation_error",
                        "task_id": task_id,
                        "error": str(e)
                    }, client_id)
            
            elif message["type"] == "human_feedback":
                task_id = message["task_id"]
                feedback_data = message["feedback"]
                
                if task_id not in active_tasks:
                    await manager.send_json_message({
                        "type": "error",
                        "message": "Task not found"
                    }, client_id)
                    continue
                
                task = active_tasks[task_id]
                state = task.get("state")
                
                if feedback_data["action"] == "approve":
                    state["human_approved"] = True
                    task["status"] = "completed"
                    
                    # Generate final report
                    report_path = generate_markdown_report(state)
                    if report_path:
                        state["report_path"] = report_path
                    
                    task["result"] = state
                    
                    await manager.send_json_message({
                        "type": "generation_complete",
                        "task_id": task_id,
                        "result": state,
                        "message": "🎉 Post approved! Process completed successfully."
                    }, client_id)
                
                elif feedback_data["action"] in ["reject", "feedback"]:
                    # Continue refinement with feedback
                    state["human_approved"] = False
                    
                    if feedback_data["action"] == "feedback" and feedback_data.get("feedback"):
                        state["critiques"] = [f"Human feedback: {feedback_data['feedback']}"]
                    else:
                        state["critiques"] = ["Human reviewer requested improvements."]
                    
                    state["iteration_count"] = 0  # Reset iteration count
                    task["status"] = "running"
                    
                    await manager.send_json_message({
                        "type": "status",
                        "status": "running",
                        "progress": 50,
                        "current_step": "Refining based on human feedback",
                        "message": "🔄 Continuing refinement based on your feedback..."
                    }, client_id)
                    
                    # Continue the agent process
                    try:
                        result = await run_marketing_agent_async(
                            task["request"],
                            task["max_iterations"],
                            client_id
                        )
                        
                        task["state"] = result
                        task["status"] = "awaiting_approval"
                        
                        await manager.send_json_message({
                            "type": "awaiting_human_approval",
                            "task_id": task_id,
                            "draft_post": result["draft_post"],
                            "research_findings": result["research_findings"],
                            "iteration_count": result["iteration_count"],
                            "critiques": result.get("critiques", [])
                        }, client_id)
                        
                    except Exception as e:
                        task["status"] = "error"
                        task["error"] = str(e)
                        
                        await manager.send_json_message({
                            "type": "generation_error",
                            "task_id": task_id,
                            "error": str(e)
                        }, client_id)
            
            elif message["type"] == "ping":
                await manager.send_json_message({
                    "type": "pong"
                }, client_id)
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)

# Serve React frontend (catch-all route must be last)
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """Serve React frontend for all non-API routes"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    index_file = os.path.join(static_dir, "index.html")
    
    # If requesting a specific file that exists, serve it
    if full_path and full_path != "":
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
    
    # Otherwise serve index.html for React routing
    if os.path.isfile(index_file):
        return FileResponse(index_file)
    else:
        return {"message": "Frontend not built. Please build the React app first."}

if __name__ == "__main__":
    print("🚀 Starting LangGraph Marketing Agent API Server...")
    print("📊 API Documentation available at: http://localhost:8000/docs")
    print("🔌 WebSocket endpoint: ws://localhost:8000/ws/{client_id}")
    print("🌐 CORS enabled for: http://localhost:3000")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
