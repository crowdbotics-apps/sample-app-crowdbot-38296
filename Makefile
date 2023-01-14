DB_SERVICE_NAME=postgres
API_SERVICE=api

.PHONY: help # Generate list of targets with descriptions
help:
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/ - \1 - \2/'

#--------------------------------------- DB -----------------------------------
.PHONY: db_local_seeds # Adds initial data to the system in local environment
db_local_seeds:
	@docker-compose exec $(API_SERVICE) python manage.py loaddata 000_site 000_user

.PHONY: db_stock_seeds # Adds Stock seeds to database
db_stock_seeds:
	@docker-compose run $(API_SERVICE) python manage.py loaddata 000_category
	@docker-compose run $(API_SERVICE) python manage.py loaddata 001_product

.PHONY: db_update # Updates database with fixtures
db_update:
	@docker-compose exec $(API_SERVICE) python manage.py migrate
	@make db_local_seeds
	@make db_stock_seeds

.PHONY: db_flush # Destroys and recreates database services from scratch
db_flush:
	@docker-compose kill $(DB_SERVICE_NAME)
	@docker-compose start $(DB_SERVICE_NAME)
	@sleep 10
	@make db_update

#--------------------------------------- DOCS -----------------------------------
.PHONY: doc_domain_diagrams	# Generates diagrams to be shown in documentation
doc_domain_diagrams:
	#@docker-compose run $(API_SERVICE) python manage.py graph_models stock -g -o docs/diagrams/stock.png
	@docker-compose run $(API_SERVICE) python manage.py graph_models -a -g -o docs/diagrams/system.png
