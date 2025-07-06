# LangGraph Agent with FastAPI Integration

This project integrates a LangGraph agent with a FastAPI backend, providing intelligent routing between RAG (Retrieval-Augmented Generation), web search, and direct answering capabilities.

## Features

- **Intelligent Routing**: The agent automatically decides whether to use RAG, web search, or direct answering
- **RAG Integration**: Searches through uploaded documents using Chroma vector store
- **Web Search**: Uses Tavily for up-to-date information
- **Session Management**: Maintains conversation history across requests
- **Document Management**: Upload, list, and delete documents
- **Smart Chat Endpoint**: Uses LangGraph agent for intelligent responses

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the `api` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  # For web search functionality
```

### 3. Initialize the Database

The database tables will be created automatically when you first run the application.

## API Endpoints

### Chat Endpoint

#### LangGraph Agent Chat (`/chat`)
Uses the intelligent LangGraph agent with routing capabilities for all queries.

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What's the latest news about AI?",
    "session_id": "user-123",
    "model": "gpt-4o-mini"
  }'
```

The agent will automatically:
- Route simple questions to direct answering
- Route document queries to RAG search
- Route current events to web search
- Route greetings to direct responses

### Document Management

#### Upload Document (`/upload-doc`)
```bash
curl -X POST "http://localhost:8000/upload-doc" \
  -F "file=@your_document.pdf"
```

#### List Documents (`/list-docs`)
```bash
curl -X GET "http://localhost:8000/list-docs"
```

#### Delete Document (`/delete-doc`)
```bash
curl -X POST "http://localhost:8000/delete-doc" \
  -H "Content-Type: application/json" \
  -d '{"file_id": 1}'
```

## Running the Application

### Development Server
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server
```bash
cd api
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Testing

### Test the Agent
```bash
cd api
python test_agent.py
```

### Interactive Testing
```bash
cd api
python langgraph_agent.py
```

## Agent Architecture

The LangGraph agent consists of four main nodes:

1. **Router Node**: Decides how to handle the query
   - `end`: For greetings/small talk
   - `rag`: For knowledge base queries
   - `answer`: For direct questions

2. **RAG Node**: Searches the document knowledge base

3. **Web Search Node**: Performs web searches using Tavily

4. **Answer Node**: Generates the final response

## File Structure

```
api/
├── main.py              # FastAPI application with endpoints
├── langgraph_agent.py   # LangGraph agent definition
├── nodes.py             # Agent node implementations
├── tools.py             # RAG and web search tools
├── pydantic_models.py   # API request/response models
├── db_utils.py          # Database operations
├── chroma_utils.py      # Chroma vector store operations
├── test_agent.py        # Agent testing script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Usage Examples

### Example 1: Simple Question
```json
{
  "question": "What is the capital of France?",
  "session_id": "user-123"
}
```
**Route**: `answer` (direct response)

### Example 2: Document Query
```json
{
  "question": "What does the uploaded PDF say about machine learning?",
  "session_id": "user-123"
}
```
**Route**: `rag` → `answer` (if sufficient) or `rag` → `web` → `answer` (if insufficient)

### Example 3: Current Events
```json
{
  "question": "What's the latest news about AI developments?",
  "session_id": "user-123"
}
```
**Route**: `rag` → `web` → `answer` (web search for current information)

### Example 4: Greeting
```json
{
  "question": "Hello, how are you?",
  "session_id": "user-123"
}
```
**Route**: `end` (direct response)

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure `OPENAI_API_KEY` is set
2. **Tavily Errors**: Set `TAVILY_API_KEY` for web search functionality
3. **Chroma Issues**: The vector store is automatically created in `./chroma_db`
4. **Database Errors**: SQLite database is created automatically

### Logs

Check `app.log` for detailed application logs.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. 