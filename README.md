This repo is a playground to explore similarity search, semantic search, and recommendations powered by embeddings.
It comes with data from Maven courses, and the steps below will set you up with a database with course embeddings that you can use to explore how embeddings work.

Prerequisites: 
- [pyenv](https://github.com/pyenv/pyenv) to manage Python versions
- [poetry](https://python-poetry.org/) for package management
- [Docker](https://docs.docker.com/get-started/get-docker/) for the Postgres installation
- [OpenAI](https://platform.openai.com/docs/overview) API keys or keys to another embedding model


Once those are ready, run these steps:

1. Clone this repo:  
`git clone git@github.com:shreyansb/embedding_recs.git`
3. Enter the directory:  
`cd embeddings_recs`
4. Install dependencies:  
`poetry install`
5. Build the Docker image:  
`docker build -t postgres:16-pgvector .`
6. Start the Docker image:  
`docker run --name postgres16_pgvector -e POSTGRES_PASSWORD=password -p 5433:5432 -d postgres:16-pgvector`
7. Setup pgvector:  
`psql -h localhost -p 5433 -U postgres -W -c "CREATE EXTENSION IF NOT EXISTS vector;"`
8. Run database migrations to set up the `courses` table:  
`alembic upgrade head`
9. Load courses into the database:  
`python load_courses.py`
10. Add an OpenAI API key to a .env file:  
`echo "OPENAI_API_KEY=your-key-here" >> .env`
11. Go into ipython:  
`poetry run ipython`
12. Get embeddings for all courses:  
`import courses; courses.embed_all_courses()`
13. Run a query:  
`courses.find_courses_by_query("head of engineering")`
14. Find similar courses:  
`courses.find_similar_courses(1)`
