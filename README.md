# LangGraph Marketing Agent

A Python-based marketing agent that generates, critiques, and refines marketing posts with human-in-the-loop capabilities using LangGraph and OpenAI GPT-4o.

## Overview

This project implements an intelligent marketing content generator that uses AI to create high-quality marketing posts through an iterative self-correction process. The agent researches topics, generates content, critiques its own work, and refines the output until it meets quality standards or receives human approval.

## Workflow

```
START → Research → Copywriting → Critic → Quality Check
                      ↑                        ↓
                      └── (refine loop) ──────┘
                      |                        ↓
                      |                 Human Approval
                      |                        ↓
                      └───if Rejected── {Approved/Rejected}
                                               ↓
                                              END
```

### Flow Steps:
1. **Research**: Gathers mock research data about the topic
2. **Copywriting**: Creates or refines marketing post using GPT-4o
3. **Critic**: Analyzes the draft against quality criteria
4. **Quality Check**: Decides whether to refine further or seek human approval
5. **Human Approval**: Final review and approval by human user

## Features

- **Self-Correction Loop**: Iterative refinement based on AI critiques
- **Human-in-the-Loop**: Final human approval with feedback capability
- **Quality Assessment**: 8-point evaluation framework
- **Interactive Configuration**: Customizable max iterations (1-5)
- **Progress Tracking**: Real-time iteration and quality monitoring

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   # Create .env file with:
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the agent:
```bash
python main.py
```

Follow the interactive prompts to:
- Select or enter your marketing request
- Configure refinement parameters
- Review and approve the generated content

## Dependencies

- LangGraph: State graph management
- LangChain: LLM integration
- OpenAI: GPT-4o for content generation
- Python-dotenv: Environment variable management

## Author

Carlos Matías Sáez  
GitHub: [@cmatiass](https://github.com/cmatiass)
