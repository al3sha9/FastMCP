# Choose Your Own Adventure AI 🎮📚

An interactive AI-powered storytelling application that creates personalized adventure stories based on user themes. The app features a modern web interface and integrates with the Model Context Protocol (MCP) for seamless natural language interactions through Gemini CLI.

## 🎥 Demo Video

[![Demo Video](https://img.shields.io/badge/Watch-Demo%20Video-blue?style=for-the-badge&logo=loom)](https://www.loom.com/share/86592fc45c3c47ae9cc92a89ca74f544?sid=1e788686-cd91-49f4-a400-7ea0eb5e6cc6)

## 🌟 Features

### Core Functionality
- **Theme-Based Story Generation**: Enter any theme (e.g., "space adventure", "medieval fantasy") and get a unique story
- **Interactive Storytelling**: Make choices that affect the story's direction and outcome
- **AI-Powered Content**: Uses OpenAI's GPT models to generate engaging, creative narratives
- **Real-time Updates**: Asynchronous story generation with job status tracking
- **Persistent Storage**: Stories are saved to a database for future reference

### MCP Integration 🤖
- **Natural Language Interface**: Interact with the app using conversational commands through Gemini CLI
- **FastMCP Server**: Custom MCP server that exposes the app's functionality as callable tools
- **Seamless Integration**: Bridge between natural language and the FastAPI backend

## 🏗️ Architecture

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── components/
│   │   ├── StoryGenerator.jsx    # Theme input and story creation
│   │   ├── StoryGame.jsx         # Interactive story display
│   │   ├── StoryLoader.jsx       # Story loading and navigation
│   │   ├── LoadingStatus.jsx     # Job status monitoring
│   │   └── ThemeInput.jsx        # Theme input component
│   ├── App.jsx
│   └── util.js                   # API configuration
└── package.json
```

### Backend (FastAPI + SQLite)
```
backend/
├── main.py                       # FastAPI application entry point
├── core/
│   ├── config.py                 # Configuration and settings
│   ├── models.py                 # Database models
│   ├── prompts.py                # AI prompts for story generation
│   └── story_generator.py        # OpenAI integration
├── routers/
│   ├── story.py                  # Story-related API endpoints
│   └── job.py                    # Job status endpoints
├── db/
│   └── database.py               # Database connection and setup
├── schemas/
│   ├── story.py                  # Pydantic schemas for stories
│   └── job.py                    # Pydantic schemas for jobs
└── mcp_server.py                 # MCP server implementation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/techwithtim/Choose-Your-Own-Adventure-AI.git
   cd Choose-Your-Own-Adventure-AI
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Create .env file in backend directory
   cat > .env << EOF
   DATABASE_URL=sqlite:///./databse.db
   API_PREFIX=/api
   DEBUG=True
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://localhost:3000,https://localhost:5173
   OPENAI_API_KEY=your_openai_api_key_here
   EOF
   ```

4. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```
   The backend will be available at `http://localhost:8000`

2. **Start the frontend development server**
   ```bash
   cd frontend
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## 🤖 MCP Integration

### What is MCP?
The Model Context Protocol (MCP) is a standard for connecting AI assistants with external tools and data sources. Our implementation allows you to interact with the Choose Your Own Adventure app using natural language through Gemini CLI.

### MCP Server Setup

1. **Install FastMCP** (if not already installed)
   ```bash
   cd backend
   source venv/bin/activate
   pip install fastmcp
   ```

2. **Configure Gemini CLI**
   
   Add the MCP server configuration to your `~/.gemini/settings.json`:
   ```json
   {
     "theme": "Atom One",
     "selectedAuthType": "oauth-personal",
     "mcpServers": {
       "adventure-game": {
         "command": "/path/to/Choose-Your-Own-Adventure-AI/backend/run_mcp_server.sh",
         "args": [],
         "env": {}
       }
     }
   }
   ```

3. **Make the MCP server script executable**
   ```bash
   chmod +x backend/run_mcp_server.sh
   ```

### Available MCP Tools

The MCP server exposes the following tools for natural language interaction:

| Tool | Description | Usage Example |
|------|-------------|---------------|
| `create_story` | Generate a new story with a theme | "Create a story about pirates" |
| `get_job_status` | Check story generation progress | "What's the status of job abc123?" |
| `get_complete_story` | Retrieve a finished story | "Get the complete story for ID 456" |
| `make_story_choice` | Make interactive story choices | "Choose option 2 in the current story" |

### Natural Language Examples

Once connected to Gemini CLI, you can use commands like:

- **"Create a new adventure story about space exploration"**
- **"Check if my story is ready"**
- **"Show me the complete story we just created"**
- **"I want to choose the first option in this story"**
- **"Generate a mystery story set in Victorian London"**

## 🛠️ API Endpoints

### Story Management
- `POST /api/stories/create` - Create a new story with a theme
- `GET /api/stories/{story_id}/complete` - Get complete story details
- `POST /api/stories/{story_id}/choice` - Make a story choice

### Job Management
- `GET /api/jobs/{job_id}` - Get job status and details

## 🎯 How It Works

1. **Story Creation**: User provides a theme → AI generates initial story setup
2. **Choice Generation**: Story presents multiple paths → User selects preferred option  
3. **Story Continuation**: AI continues the narrative based on user choice
4. **Completion**: Story reaches natural conclusion or user-defined endpoint

### AI Integration
- Uses OpenAI's GPT models for story generation
- Custom prompts ensure consistent story structure and quality
- Maintains narrative coherence across multiple story segments

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite database path | `sqlite:///./databse.db` |
| `API_PREFIX` | API route prefix | `/api` |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_ORIGINS` | CORS allowed origins | localhost variants |
| `OPENAI_API_KEY` | OpenAI API key | Required |

### CORS Configuration
The backend is configured to allow requests from common development ports:
- `http://localhost:3000` (React default)
- `http://localhost:5173` (Vite default)
- HTTPS variants of the above

## 🚀 Deployment

### Backend Deployment
The app includes Choreo configuration for cloud deployment:
- FastAPI backend with async job processing
- SQLite database (can be upgraded to PostgreSQL for production)
- Environment-based configuration

### Frontend Deployment
- Static site deployment compatible
- Vite build process for optimized production builds
- Environment-specific API URL configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) for the backend
- [React](https://reactjs.org/) and [Vite](https://vitejs.dev/) for the frontend
- [FastMCP](https://fastmcp.com/) for MCP server implementation
- [OpenAI](https://openai.com/) for AI-powered story generation
- Inspired by classic Choose Your Own Adventure books

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/techwithtim/Choose-Your-Own-Adventure-AI/issues) page
2. Create a new issue with detailed description
3. Join our community discussions

---

**Happy Storytelling!** 🎭✨
# FastMCP
