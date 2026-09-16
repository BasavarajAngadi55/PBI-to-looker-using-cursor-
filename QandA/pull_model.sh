#!/usr/bin/env bash
# Pull the latest Google Gemma model into local Ollama for QandA.
set -euo pipefail

MODEL="${QANDA_OLLAMA_MODEL:-gemma3:latest}"

echo "Pulling Ollama model: ${MODEL}"
ollama pull "${MODEL}"
echo "Done. Listed models:"
ollama list | head -20
echo
echo "Test: ollama run ${MODEL} \"Say ready\""
