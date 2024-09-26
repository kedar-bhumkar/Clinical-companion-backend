# AI-Powered Healthcare Assistant

## Overview

This project implements an AI-powered healthcare assistant using FastAPI, OpenAI's GPT models, and custom tools for patient data management. The system is designed to provide intelligent responses to healthcare-related queries, assist with patient data retrieval, and automate certain aspects of healthcare management.

## Key Features

- **AI Chat Interface**: Utilizes OpenAI's GPT models for natural language understanding and generation.
- **Patient Data Management**: Includes mock data generation for patient information, including vitals, allergies, medications, and more.
- **Configurable Actions**: Uses YAML configuration files to define system and user intents, allowing for flexible interaction patterns.
- **Auto-population**: Capability to automatically populate forms based on patient data and AI-generated responses.
- **Multi-model Support**: Can switch between different AI models (OpenAI, LMStudio, OpenRouter, Groq) based on configuration.

## Project Structure

- `api.py`: FastAPI application setup and endpoint definitions.
- `bot_agent_with_memory_api_ready.py`: Implements the AI agent with memory capabilities.
- `constants.py`: Defines constant values used throughout the application.
- `dto.py`: Data Transfer Object definitions for patient data retrieval.
- `mock_data.py`: Generates mock patient data for testing and development.
- `pydantic_models.py`: Pydantic models for request/response validation.
- `service.py`: Core business logic for handling messages and configuring the system.
- `shared.py`: Implements a singleton for shared data across modules.
- `util.py`: Utility functions for configuration loading, token counting, etc.

## Configuration

The system uses YAML files for configuration:

- `config/config.yaml`: API keys and model preferences for different AI providers.
- `config/action.yaml`: Defines system and user intents for different pages/scenarios.

## Setup and Running

1. Install dependencies:
   ```
   pip install fastapi pydantic openai langchain tiktoken pyyaml
   ```

2. Set up your environment variables or update the `config/config.yaml` file with your API keys.

3. Run the FastAPI application:
   ```
   uvicorn api:app --reload
   ```

## API Endpoints

- `GET /`: Health check endpoint.
- `POST /chat`: Main chat endpoint for interacting with the AI assistant.
- `POST /config`: Endpoint for retrieving configuration options.

## Customization

- Add new patient data functions in `mock_data.py` and `dto.py`.
- Extend the action configurations in `config/action.yaml` for new use cases.
- Modify prompts and system behaviors in the YAML configuration files.

## Note

This project uses mock data for demonstration purposes. In a production environment, ensure proper data security measures are in place and replace mock data with actual patient data retrieval mechanisms.

## License

[Add your chosen license here]

