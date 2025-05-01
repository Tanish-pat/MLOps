# Makefile for ETL Pipeline Project

.PHONY: run install setup clean

run: setup
	@echo "Starting ETL Pipeline..."
	@cd src && python -c "from validate import validate_data; from extract import extract_data; df=extract_data(); [validate_data(d) for d in df.values()]"
	@cd src && python etl_pipeline.py
	@echo "ETL process completed!"

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt  # Ensure you have a requirements.txt file
	@echo "Dependencies installed."

setup:
	@echo "Setting up directories..."
	@mkdir -p logs
	@mkdir -p data/raw
	@echo "Directory structure ready."

clean:
	@echo "Cleaning up..."
	@rm -rf logs/*.log
	@echo "Cleanup complete."

help:
	@echo "Available targets:"
	@echo "  run     	: Execute the ETL pipeline (default)"
	@echo "  install 	: Install Python dependencies"
	@echo "  setup   	: Create required directories"
	@echo "  clean   	: Remove generated files"
	@echo "  test    	: Run Validation Test"
	@echo "  check-env     : Check Environment"
	@echo "  help    	: Show this help message"

test: setup
	@echo "Running data validation..."
	@cd src && python -c "from validate import validate_data; from extract import extract_data; df=extract_data(); exit(0 if all(validate_data(d) for d in df.values()) else 1)"
	@echo "Data validation completed."

check-env:
	@echo "Checking environment..."
	@test -f .env || (echo "Error: .env file missing"; exit 1)
	@test -n "$$(grep MONGO_URI .env)" || (echo "Error: MONGO_URI not set in .env"; exit 1)
	@echo "Environment check passed."

.DEFAULT_GOAL := run