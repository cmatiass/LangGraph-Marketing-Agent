# LangGraph Marketing Agent

A sophisticated marketing post generation system built with LangGraph that evolves from a simple sequential agent to a more advanced system with feedback loops and human oversight.

## 🎯 Mission

Build a LangGraph agent that generates marketing posts, starting with a foundational sequential approach and evolving through three distinct stages:

1. **Task 1: Foundational Agent** - Simple sequential marketing agent
2. **Task 2: Enhanced Agent** - Adding feedback loops and validation
3. **Task 3: Human-in-the-loop** - Incorporating human oversight and approval

## 🏗️ Current Implementation (Task 1)

### Architecture

The foundational agent implements a simple sequential workflow:

```
START → Research Node → Copywriting Node → END
```

### Core Components

#### AgentState (TypedDict)
- `initial_request`: Original user request for marketing content
- `research_findings`: Mock research data and market insights
- `draft_post`: Generated marketing post
- `messages`: Chat history for conversation flow

#### Nodes

1. **research_node**: Simulates topic research with mock data including:
   - Market trends and insights
   - Competitor analysis
   - Trending hashtags
   - Audience demographics

2. **copywriting_node**: Generates marketing posts using GPT-4o with:
   - Compelling hooks and value propositions
   - Platform-appropriate tone
   - Clear call-to-actions
   - Strategic hashtag integration

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

Run the marketing agent:

```bash
python main.py
```

The agent will prompt you for a marketing request or use a default example. Try these sample requests:

- "Create a marketing post for a new AI-powered productivity app"
- "Generate content promoting a sustainable fashion brand"  
- "Write a post for a local coffee shop's grand opening"

## 📁 Project Structure

```
langgraph-marketing-agent/
├── main.py              # Core agent implementation
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── README.md           # Project documentation
└── .github/
    └── copilot-instructions.md  # Development guidelines
```

## 🔧 Technical Details

### Dependencies

- **langchain**: Core LangChain framework
- **langchain-openai**: OpenAI integration
- **langgraph**: State graph implementation
- **python-dotenv**: Environment variable management
- **typing-extensions**: Enhanced type hints

### State Management

The agent uses LangGraph's `StateGraph` with a TypedDict-based state system that maintains:
- Request context throughout the workflow
- Research findings for informed copywriting
- Generated content for review and refinement

### LLM Integration

- **Model**: GPT-4o for high-quality content generation
- **Temperature**: 0.7 for creative yet consistent marketing copy
- **Prompting**: Structured prompts with research context and copywriting guidelines

## 🎨 Example Output

### Input Request
"Create a marketing post for a new AI-powered productivity app"

### Research Findings
- Market trends toward authentic, value-driven content
- Competitor focus on storytelling and user-generated content
- Optimal posting times and engagement strategies
- Target audience demographics and platform preferences

### Generated Marketing Post
A compelling marketing post with:
- Attention-grabbing hook
- Clear value propositions
- Professional yet conversational tone
- Strategic call-to-action
- Relevant hashtags

## 🔄 Roadmap

### Task 2: Enhanced Agent (Coming Soon)
- Feedback loop integration
- Content quality validation
- Multi-iteration refinement
- Performance metrics

### Task 3: Human-in-the-loop (Coming Soon)  
- Human review checkpoints
- Approval workflows
- Collaborative editing
- Quality assurance gates

## 🛠️ Development

### Running Tests
```bash
# Tests will be added in future iterations
python -m pytest tests/
```

### Code Style
The project follows PEP 8 guidelines with comprehensive docstrings and type hints.

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For questions, issues, or contributions, please open an issue in the GitHub repository.

---

**Note**: This is Task 1 of a three-stage development process. The current implementation provides a solid foundation with mock research data. Future iterations will add sophisticated feedback mechanisms, real-time research capabilities, and human oversight features.
