.PHONY: all install setup preprocess train inference clean help

all: preprocess train

preprocess:
	@echo "Running preprocessing..."
	@python src/preprocess.py
	@echo "Preprocessing completed."

train:
	@echo "Running training..."
	@python src/train.py
	@echo "Training completed."

inference:
	@echo "Running inference..."
	@python src/inference.py
	@echo "Inference completed."

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt
	@echo "Dependencies installed."

setup:
	@echo "Setting up directories..."
	@mkdir -p logs
	@mkdir -p data/raw
	@mkdir -p model
	@echo "Directory structure ready."

clean:
	@echo "Cleaning up..."
	@rm -rf logs/*.log
	@rm -rf __pycache__ src/__pycache__ mlruns model data
	@echo "Cleanup complete."

help:
	@echo "Available targets:"
	@echo "  all        : Run preprocessing and training (default)"
	@echo "  preprocess : Run preprocessing step"
	@echo "  train      : Run training step"
	@echo "  inference  : Run inference step"
	@echo "  install    : Install Python dependencies"
	@echo "  setup      : Create necessary directories"
	@echo "  clean      : Remove generated files"
	@echo "  help       : Show this help message"

.DEFAULT_GOAL := all
