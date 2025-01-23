# AI-Powered Product Search Engine

A sophisticated product search engine that combines local database search with AI-powered recommendations and external content integration. The system uses semantic search, vector embeddings, and a workflow-based architecture to provide intelligent product recommendations.

## Features

- **Semantic Search**: Uses FAISS and Sentence Transformers for intelligent product matching
- **External Content Integration**: Fallback to web content using Exa API when local results aren't sufficient
- **AI-Powered Recommendations**: Integrates with Mistral LLM for intelligent product suggestions
- **Interactive UI**: Built with Streamlit for a seamless user experience
- **Workflow-Based Architecture**: Uses LangGraph for structured processing pipeline

## Technology Stack

- **Backend Framework**: Python
- **Vector Search**: FAISS
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM Integration**: Ollama (Mistral)
- **External Search**: Exa API
- **UI**: Streamlit
- **Workflow Management**: LangGraph

## Prerequisites

- Python 3.8+
- Virtual environment manager
- Ollama installed locally
- Exa API key (optional, for external search)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Exa API key if you want external search capability

## Project Structure

```
.
├── data/
│   └── products.csv         # Local product database
├── src/
│   ├── app.py              # Streamlit application
│   ├── search_engine.py    # Search engine implementation
│   └── workflow.py         # LangGraph workflow definition
├── requirements.txt        # Project dependencies
└── .env                   # Environment variables
```

## Components

### Search Engine
The search engine (`search_engine.py`) provides two-tier search capabilities:
- Primary: Local vector search using FAISS
- Fallback: External content search using Exa API

Reference: 
```python:search_engine.py
startLine: 7
endLine: 64
```

### Workflow System
The workflow system (`workflow.py`) orchestrates the search and recommendation process:
- Manages state transitions
- Coordinates between search and chatbot components
- Handles message processing

Reference:
```python:workflow.py
startLine: 16
endLine: 64
```

### User Interface
The Streamlit interface (`app.py`) provides:
- Search input field
- Real-time result updates
- Formatted display of both local and external results

Reference:
```python:app.py
startLine: 6
endLine: 58
```

## Usage

1. Start the application:
```bash
streamlit run src/app.py
```

2. Enter your search query in the text input field
3. View results, which may include:
   - Local product matches
   - External content (if enabled)
   - AI-powered recommendations

## Configuration

The system can be configured through several parameters:

- `top_k`: Number of search results to return (default: 5)
- `distance_threshold`: Relevance threshold for local results (default: 1.5)
- `model_name`: Sentence transformer model (default: 'all-MiniLM-L6-v2')

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## Acknowledgments

- FAISS by Facebook Research
- Sentence Transformers by UKPLab
- Exa API for external content search
- LangGraph and LangChain communities
