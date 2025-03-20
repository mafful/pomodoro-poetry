.DEFAULT_TARGET := help

ENV_FILE = .env

include $(ENV_FILE)
export

# Define the Compose file
COMPOSE_DEV := ./docker-compose-dev.yaml
DOCKER_COMPOSE_FILE := $(COMPOSE_DEV)

print:
	@echo "Using DOCKER_COMPOSE_FILE=$(DOCKER_COMPOSE_FILE)"

#=============== Python-specific clean ======
clean: ## Clean Python temporary files and logs
	@echo "Cleaning up Python directories..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +
	find . -name "*.log" -delete
	find . -name "*.log.*" -delete
	find . -name ".ruff_cache" -type d -exec rm -r {} +


#=============== SQLite db ==================
# Python-specific run
create_db:  ## Create SQLite db
	@echo "Create SQLite database..."
	python -m SQLite_db.DB_create_SQLITE_db
	@echo "Database successfully created"

add_data_to_db: ## Add data in db
	@echo  "Adding data to database..."
	python -m SQLite_db.DB_data_add
	@echo "Data successfully added to the database"

select_from_db: ## Select data from db
	python  -m SQLite_db.DB_data_select

update_db: ## Update data from db
	python  -m SQLite_db.DB_data_update

delete_db: ## Delete data from db
	python  -m SQLite_db.DB_data_delete


#=============== Postrgers server ===============
migrate: ## Upgrade the database to the latest revision
	poetry run alembic upgrade head

downgrade: ## Downgrade the database by one revision
	poetry run alembic downgrade -1

makemigration: ## Generate a new migration (make makemigration msg="описание изменений")
	@echo "Current directory: $(shell pwd)"
	@if [ ! -d "alembic/versions" ]; then \
		echo "Creating alembic/versions directory"; \
		mkdir -p alembic/versions; \
	fi
	poetry run alembic revision --autogenerate -m "$(MSG)"


#=============== Docker Compose ===============
up: down ## Start containers using Docker Compose. This will first stop and remove existing containers before starting new ones.
	@echo "Starting containers using Docker Compose file: $(DOCKER_COMPOSE_FILE)..."
	@docker-compose --project-directory . --env-file $(ENV_FILE) -f $(DOCKER_COMPOSE_FILE) up -d

down: ## Stop and remove containers, networks, and volumes defined in the Docker Compose file.
	@echo "Stopping and removing containers using Docker Compose file: $(DOCKER_COMPOSE_FILE)..."
	docker-compose --project-directory . --env-file $(ENV_FILE) -f $(DOCKER_COMPOSE_FILE) down

restart: down up ## Restart containers by stopping and then starting them again.
	@echo "Restarted containers using Docker Compose file: $(DOCKER_COMPOSE_FILE)."

logs: ## Display and follow the logs for containers defined in the Docker Compose file.
	@echo "Displaying logs for containers defined in Docker Compose file: $(DOCKER_COMPOSE_FILE)..."
	@docker-compose --project-directory . --env-file $(ENV_FILE) -f $(DOCKER_COMPOSE_FILE) logs -f

ps: ## Check the status of containers defined in the Docker Compose file.
	@echo "Checking status of containers defined in Docker Compose file: $(DOCKER_COMPOSE_FILE)..."
	@docker-compose --project-directory . --env-file $(ENV_FILE) -f $(DOCKER_COMPOSE_FILE) ps

clean_docker: down ## Clean up Docker resources, including volumes and orphaned containers.
	@echo "Cleaning up resources defined in Docker Compose file: $(DOCKER_COMPOSE_FILE)..."
	@docker-compose --project-directory . --env-file $(ENV_FILE) -f $(DOCKER_COMPOSE_FILE) down --volumes --remove-orphans
	@echo "Pruning unused Docker volumes..."
	@docker volume prune -a -f

#=============== FastAPI server ===============
run: ## Start the FastAPI development server
	@echo "Starting FastAPI server..."
	poetry run uvicorn main:app --host 127.0.0.1 --port 8001 --reload --env-file .env

stop: ## Stop the running Uvicorn server (equivalent to Ctrl+C)
	@echo "Sending SIGINT to uvicorn..."
	pkill -15 -f "uvicorn"


#=============== Help =========================
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: $(shell awk -F ':.*?## ' '/^[a-zA-Z0-9_-]+:.*?## / {print $$1}' $(MAKEFILE_LIST))