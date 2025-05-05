#!/bin/bash
# Ensure .venv exists, or create it
if [ ! -d ".venv" ]; then
    echo ".venv directory not found. Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        exit 1
    fi
fi

# Check if the .venv virtual environment is active by checking the VIRTUAL_ENV variable and if it contains ".venv"
if [[ "$VIRTUAL_ENV" == *".venv"* ]]; then
  # .venv is active, so deactivate it and then reactivate it
  echo ".venv is currently active. Deactivating and reactivating..."
  deactivate
  source .venv/bin/activate # Activate .venv
  if [[ "$VIRTUAL_ENV" == *".venv"* ]]; then
    echo ".venv deactivated and reactivated successfully."
  else
    echo "Failed to reactivate .venv."
    exit 1
  fi
elif [[ -n "$VIRTUAL_ENV" ]]; then
    echo "A different virtual environment ($VIRTUAL_ENV) is active.  Deactivating it first."
    deactivate
    source .venv/bin/activate
     if [[ "$VIRTUAL_ENV" == *".venv"* ]]; then
        echo ".venv activated successfully."
     else
        echo "Failed to activate .venv"
        exit 1
     fi
else
  # No virtual environment is active, so activate .venv
  echo ".venv is not active. Activating..."
  source .venv/bin/activate # Activate .venv
  if [[ "$VIRTUAL_ENV" == *".venv"* ]]; then
    echo ".venv activated successfully."
  else
    echo "Failed to activate .venv."
    exit 1
  fi
fi