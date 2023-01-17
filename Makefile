DB_SERVICE_NAME=postgres
API_SERVICE=app

.PHONY: help # Generate list of targets with descriptions
help:
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/ - \1 - \2/'

#--------------------------------------- DB -----------------------------------
.PHONY: db_local_seeds # Adds initial data to the system in local environment
db_local_seeds:
	@docker-compose run $(API_SERVICE) python manage.py loaddata 000_site 000_user

.PHONY: db_application_seeds # Adds Application seeds to database
db_application_seeds:
	@docker-compose run $(API_SERVICE) python manage.py loaddata 001_plan 002_application 003_subscription_history

.PHONY: db_update # Updates database with fixtures
db_update:
	@docker-compose run $(API_SERVICE) python manage.py migrate
	@make db_local_seeds
	@make db_application_seeds

.PHONY: db_flush # Destroys and recreates database services from scratch
db_flush:
	@docker-compose kill $(DB_SERVICE_NAME)
	@docker-compose start $(DB_SERVICE_NAME)
	@sleep 10
	@make db_update

#--------------------------------------- DOCS -----------------------------------
.PHONY: doc_domain_diagrams # Generates diagrams to be shown in documentation
doc_domain_diagrams:
	@docker-compose run $(API_SERVICE) python manage.py graph_models -a -g -o docs/diagrams/system.png
	@docker-compose run $(API_SERVICE) python manage.py graph_models applications -g -o docs/diagrams/applications.png
