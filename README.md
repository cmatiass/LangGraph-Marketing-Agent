# LangGraph Marketing Agent

A sophisticated marketing post generation system built with LangGraph that evolves from a simple sequential agent to a more advanced system with feedback loops and human oversight.

## 🎯 Mission

Build a LangGraph agent that generates marketing posts, starting with a foundational sequential approach and evolving through three distinct stages:

1. **✅ Task 1: Foundational Agent** - Simple sequential marketing agent (COMPLETED)
2. **✅ Task 2: Enhanced Agent** - Adding feedback loops and validation (COMPLETED)
3. **🔄 Task 3: Human-in-the-loop** - Incorporating human oversight and approval (PENDING)

## 🏗️ Current Implementation (Task 2: Critique & Refine Loop)

### Architecture

The enhanced agent implements a self-correcting workflow with critique and refinement:

```
START → Research → Copywriting → Critic → [Decision]
           ↑                                    ↓
           └────← Refine (if critiques) ←──────┘
                        ↓
                   END (if ready)
```

### Core Components

#### AgentState (TypedDict)
- `initial_request`: Original user request for marketing content
- `research_findings`: Mock research data and market insights
- `draft_post`: Generated marketing post (updated through iterations)
- `critiques`: List of specific critiques for improvement
- `iteration_count`: Number of refinement iterations completed
- `max_iterations`: Maximum refinement attempts allowed
- `messages`: Chat history for conversation flow

#### Nodes

1. **research_node**: Simulates topic research with comprehensive mock data:
   - Market trends and key insights
   - Competitor analysis and strategies
   - Trending hashtags and best practices
   - Audience demographics and platform preferences
   - Success criteria for evaluation

2. **copywriting_node**: Generates or refines marketing posts using GPT-4o:
   - **Initial Creation**: Creates compelling posts with hooks, value propositions, and CTAs
   - **Refinement**: Addresses specific critiques while maintaining strengths
   - Platform-appropriate tone and strategic hashtag integration

3. **critic_node** ⭐ **NEW**: Analyzes draft posts for improvements:
   - Evaluates hook & engagement effectiveness
   - Assesses value proposition clarity
   - Checks target audience alignment
   - Reviews call-to-action strength
   - Validates platform optimization
   - Analyzes length and readability
   - Evaluates hashtag usage
   - Confirms original request fulfillment

4. **should_continue**: Conditional routing logic:
   - **Continue**: If critiques exist and max iterations not reached
   - **End**: If no critiques or maximum iterations reached

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd langgraph-marketing-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Usage

Run the enhanced marketing agent:

```bash
python main.py
```

The agent will offer:

1. **Request Options**:
   - Choose from example requests
   - Enter custom marketing requests

2. **Refinement Control**:
   - Set maximum refinement iterations (1-5)
   - Default: 3 iterations for optimal balance

### Example Workflow

```
🎯 LANGGRAPH MARKETING AGENT - TASK 2: CRITIQUE & REFINE LOOP

📋 Choose an option:
   1. Use example requests
   2. Enter custom marketing request

Select option (1 or 2): 1
Select example (1-3 or press Enter for 1): 1
✅ Using: Create a marketing post for a new AI-powered productivity app

🔄 Max refinement iterations (1-5, press Enter for 3): 3
⚙️ Using 3 max iterations

🔍 Research completed for: Create a marketing post for a new AI-powered productivity app
✍️ Creating initial marketing post...
📝 Post generated! Length: 285 characters
🔍 Critique analysis completed (iteration 1)
📝 Found 2 critique(s):
   1. The hook could be more attention-grabbing for the target audience
   2. The call-to-action needs to be more specific and compelling
🔄 Critiques found - continuing to refinement (iteration 2)
🔄 Refining marketing post (iteration 1)...
📝 Post generated! Length: 298 characters
🔍 Critique analysis completed (iteration 2)
✅ No critiques found - post is ready!
```

## 📁 Project Structure

```
langgraph-marketing-agent/
├── main.py              # Enhanced agent with critique & refine loop
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT license
├── README.md           # Project documentation
└── .github/
    └── copilot-instructions.md  # Development guidelines
```

## 🔧 Technical Details

### New Features (Task 2)

#### Self-Correction Loop
- **Automated Critique**: AI-powered analysis of generated content
- **Iterative Refinement**: Continuous improvement until quality standards met
- **Intelligent Stopping**: Ends when content is ready or max iterations reached

#### Enhanced State Management
- **Iteration Tracking**: Monitors refinement cycles
- **Critique Storage**: Maintains feedback history
- **Flexible Configuration**: User-controlled iteration limits

#### Improved User Experience
- **Progress Indicators**: Visual feedback during processing
- **Refinement Summary**: Details on iterations and final critiques
- **Flexible Controls**: Customizable refinement parameters

### Dependencies

- **langchain**: Core LangChain framework
- **langchain-openai**: OpenAI integration
- **langgraph**: State graph implementation with conditional edges
- **python-dotenv**: Environment variable management
- **typing-extensions**: Enhanced type hints with Literal

### Quality Assurance

The critic node evaluates content across 8 key dimensions:
1. **Hook & Engagement** - First impression effectiveness
2. **Value Proposition** - Benefit clarity and appeal
3. **Target Audience** - Tone and content appropriateness
4. **Call-to-Action** - Conversion optimization
5. **Platform Optimization** - Social media best practices
6. **Length & Readability** - Optimal format and flow
7. **Hashtag Usage** - Strategic and balanced integration
8. **Request Alignment** - Original requirement fulfillment

## 🎨 Enhanced Output Example

### Input Request
"Create a marketing post for a new AI-powered productivity app"

### Refinement Process
- **Initial Draft**: Generated with research-based insights
- **Critique 1**: "Hook needs more impact, CTA too generic"
- **Refinement 1**: Improved hook and specific CTA
- **Critique 2**: "No critiques - the post is ready"
- **Result**: High-quality, refined marketing content

### Final Results Display
```
🔄 REFINEMENT SUMMARY:
Total iterations completed: 2
Final critiques: 0

🔍 RESEARCH FINDINGS:
Key insights, competitor analysis, audience data...

✍️ FINAL MARKETING POST:
Polished, critique-refined marketing content ready for use
```

## 🔄 Task Progression

### ✅ Task 1: Foundational Agent (Completed)
- Sequential workflow: research → copywriting
- Mock research data integration
- GPT-4o content generation
- Basic user interface

### ✅ Task 2: Enhanced Agent (Completed)
- Self-correction critique loop
- Iterative refinement capabilities
- Quality assessment and validation
- Enhanced user controls and feedback

### 🔄 Task 3: Human-in-the-loop (Next)
- Human review checkpoints
- Approval workflows
- Collaborative editing interface
- Quality assurance gates

## 🛠️ Development

### Running Tests
```bash
# Test basic functionality
python -c "from main import create_marketing_agent; print('✅ Agent loaded successfully!')"
```

### Code Quality
- **Type Safety**: Comprehensive type hints with TypedDict and Literal
- **Error Handling**: Robust exception management
- **Documentation**: Detailed docstrings and inline comments
- **Modularity**: Clean separation of concerns

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For questions, issues, or contributions, please open an issue in the GitHub repository.

---

**Current Status**: Task 2 completed with fully functional critique & refine loop. The agent now provides self-correcting capabilities that significantly improve content quality through iterative refinement. Ready for Task 3 implementation with human oversight features.
