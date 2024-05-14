# udemy_langchain
Udemy course on langchain

I don't know what the license for this is, but the course is available on https://udemy.com/course/langchain

Make sure you create a .env file with the following vars:
OPENAI_API_KEY
PROXYCURL_API_KEY
OLLAMA_MODEL
OLLAMA_BASE_URL

## Ollama as backend

Run `docker compose up` from the root folder to start both Ollama and Open WebUI.

Run `docker compose -f docker-compose-no-gpu.yml` if you do not have a Nvidia GPU.

With the containers up, run `docker exec -it ollama ollama run <model_name>` to run a model.