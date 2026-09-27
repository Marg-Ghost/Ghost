# Ghost AI

Ghost is an experimental, local-first AI assistant. It combines a small browser chat interface with a FastAPI service, Ollama for local language-model inference, and ChromaDB (=Vector database) for retrieving stored Info about you or any Information.

## Features

- Chat through a browser-based interface.
- Retrieve relevant notes from long-term memory for a prompt.
- Keep a bounded buffer of recent user messages and summarize older messages for storage.
- Add notes manually through the API.
- Run the web interface and AI service as separate Docker Compose services.

## Architecture

```text
Browser (localhost:4100)
		-> Web API (FastAPI)
				-> Core API (FastAPI, localhost:4000)
						-> Ollama (qwen2.5:1.5b)
						-> ChromaDB and JSON-backed memory data
```

The web service forwards chat requests to the core service. The core queries ChromaDB for relevant stored notes and sends the resulting context to Ollama.

## Run with Docker Compose

Prerequisites:

- Docker Desktop (or Docker Engine) with the Compose plugin.
- [Ollama](https://ollama.com/) installed and running on the host.

Pull the model used by the core service:

```powershell
ollama pull qwen2.5:1.5b
```

From the repository root, build and start both services:

```powershell
docker compose up --build
```

Then open:

- Web interface: <http://localhost:4100>
- Core API documentation: <http://localhost:4000/docs>

Stop the services with `Ctrl+C`, or run `docker compose down` in another terminal.

## Python dependencies

Dependencies are listed per service because each container has its own environment:

- Core: `core/requirements.txt`
- Web API: `clients/web/ai_interface/requirements.txt`

The Dockerfiles install the matching list automatically. The project currently targets Python 3.11 in its Docker images.

## API

The core API provides:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/chat` | Send a chat message and receive a response. |
| `POST` | `/manual-entry` | Summarize and store supplied text as memory entries. |
| `GET` | `/memory/short` | Read the recent-message buffer. |
| `GET` | `/memory/long` | Read stored long-term memory entries. |

Example chat request:

```json
{
	"role": "user",
	"content": "What notes do you have about C pointers?"
}
```

## Repository layout

```text
clients/
	terminal/                 Experimental terminal client
	web/ai_interface/         Browser UI and web API
core/                       Chat, retrieval, and memory service
	data/                     Seed memory data and loading helpers
docker-compose.yml           Local multi-service setup
```

`core/eyes.py` is a standalone camera experiment; it is not part of the Docker Compose application and has separate system dependencies.

## Current limitations

Ghost is a learning project, not a production-ready service. The Compose setup does not mount persistent volumes for ChromaDB or runtime memory changes, so removing/recreating containers can discard data written inside them. The APIs have no authentication, and the web API allows requests from any origin; keep the services on a trusted machine and do not expose their ports publicly. The bundled memory JSON is sample data and should be reviewed or replaced before use with personal data.

Useful next steps for making the project more robust are persistent Docker volumes, automated tests, and configuration for the model and service URLs.
