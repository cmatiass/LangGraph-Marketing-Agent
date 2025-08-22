# 🤖 LangGraph Marketing Agent

**AI-Powered Marketing Content Generator with Self-Correction & Human Feedback**

A full-stack application combining artificial intelligence and human supervision to generate high-quality marketing content. Available as both a command-line tool and a modern web interface.

![GitHub](https://img.shields.io/badge/GitHub-cmatiass-blue?style=flat-square&logo=github)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi)

---

## 🌐 Try it here!

You can try the project here: [Case-Study-AI-Agent-Developer-Marketing-MBA](https://front-case-study-ai-agent-developer.onrender.com)  

⚠️ **Note:** The first load may take several minutes since the app is hosted on Render free tier and needs to spin up before being accessible.

---

## 🌟 Key Features

### 🔄 **Self-Correction System**
- **Iterative critique & refine loop**
- **Automated evaluation** with 8 quality criteria
- **Progressive improvement** until professional standards are met

### 👤 **Human Feedback**
- **Interactive approval panel**
- **Three actions**: Approve, Reject, Give Specific Feedback
- **Full control** over the generation process

### 🚀 **Two Versions Available**
1. **CLI (Terminal)**: Original version with command-line interface
2. **Web App**: Modern React interface with FastAPI backend

### 🎯 **Intelligent Generation**
- **Automated market & audience research**
- **Optimized content** for social platforms
- **Relevant hashtags** and effective CTAs
- **Detailed Markdown reports**

---

## 📱 Web Interface (New)

### **Frontend (React)**
- 🎨 **Modern design** with soft gradients
- 📱 **Fully responsive**
- ⚡ **Real-time** via WebSocket
- 🔄 **Live progress monitoring**
- 🎛️ **Intuitive control panel**

### **Backend (FastAPI)**
- 🚀 **Full REST API**
- 🔌 **WebSocket** for real-time communication
- 📊 **Auto-generated Swagger docs**
- 🔄 **Hot-reload** for development
- 📁 **Integrated static file serving**

---

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.8+
- Node.js 16+ (for web version)
- OpenAI account with API Key

### **1. Clone the Repository**
```bash
git clone https://github.com/cmatiass/Front-Case-Study-AI-Agent-Developer-Marketing-MBA.git
cd Front-Case-Study-AI-Agent-Developer-Marketing-MBA
```

### **2. Set Environment Variables**
```bash
# Create a .env file in the project root
OPENAI_API_KEY=your_openai_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langchain_api_key_here 
```

---

## 🚀 Usage

### **Option 1: CLI Version (Original)**

#### **Install**
```bash
# Install Python dependencies
pip install -r requirements.txt
```

#### **Run**
```bash
python main.py
```

#### **CLI Features**
- ✅ Predefined example selection
- ✅ Custom requests
- ✅ Max iteration configuration
- ✅ Interactive human approval
- ✅ Automatic Markdown reports

---

### **Option 2: Web Application (New)**

#### **Full Installation**
```bash
# 1. Backend - Install Python dependencies
cd backend
pip install -r requirements.txt

# 2. Frontend - Install Node.js dependencies
cd ../frontend
npm install

# 3. Build frontend and copy to backend
npm run build
cp -r build/* ../backend/static/
```

#### **Run**
```bash
# From the backend folder
cd backend
python main.py
```
📌 **App available at: http://localhost:8000**

#### **Web Features**
- 🎨 **Modern, attractive UI**
- ⚡ **Real-time progress** via WebSocket
- 📱 **Responsive design** for mobile
- 🎛️ **Interactive approval panel**
- 📊 **Live progress monitoring**
- 💬 **Chat-style specific feedback**
- 📋 **Exportable results**

---

## 📊 Workflow Details

### **1. 🔍 Research Phase**
- Audience analysis
- Market trend identification
- Relevant hashtag collection
- Success criteria definition

### **2. ✍️ Copywriting Phase**
- Generation with GPT-4o (temperature 0.7)
- Focus on engagement & conversion
- Optimization for social platforms
- Integration of research insights

### **3. 🔍 Critique Phase**
- **8 Evaluation Criteria**:
  - Message clarity
  - Call-to-action strength
  - Hashtag usage
  - Appropriate length
  - Engagement potential
  - Audience relevance
  - Professionalism
  - Creativity

### **4. 👤 Human Approval Phase**
- **Three options**:
  - ✅ **Approve**: Finalize and generate report
  - ❌ **Reject**: Continue automatic refinement
  - 💬 **Feedback**: Give specific instructions

---

## 🎯 Example Use Cases

### **Sample Requests**
- 📱 "LinkedIn post about remote work productivity"
- 🏃‍♂️ "Instagram campaign for fitness app targeting millennials"
- 🏢 "Promotional tweet for business networking event"
- 🎓 "Facebook post for online marketing course"

### **Types of Specific Feedback**
- *"Make the tone more casual and friendly"*
- *"Add more statistical data"*
- *"Change the call-to-action to be more direct"*
- *"Limit text to 200 characters max"*

---

## 🔧 Project Structure

```
📦 LangGraph Marketing Agent
├── 📁 backend/                 # FastAPI + LangGraph
│   ├── 📄 main.py             # Main server
│   ├── 📄 requirements.txt    # Python dependencies
│   └── 📁 static/            # Compiled frontend
├── 📁 frontend/               # React + TypeScript
│   ├── 📁 src/
│   │   ├── 📁 components/    # React components
│   │   └── 📄 App.css       # Main styles
│   ├── 📄 package.json      # Node.js dependencies
│   └── 📁 build/           # Production build
├── 📄 main.py                # Original CLI version
├── 📄 requirements.txt       # CLI deps
├── 📄 .env.example          # Env template
└── 📄 README.md            # This documentation
```

---


---

## 👨‍💻 Author

**Carlos Matías Sáez**

- 🔗 **GitHub**: [@cmatiass](https://github.com/cmatiass)
- 💼 **LinkedIn**: [Carlos Matías Sáez](https://www.linkedin.com/in/carlosmatiassaez/)
- 📧 **Email**: [your email here]

---

<div align="center">

**⭐ If you like this project, give it a star ⭐**

**Made with ❤️ by [Carlos Matías Sáez](https://github.com/cmatiass)**

</div>
