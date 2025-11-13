# Tasks4 - Task Summarization with OpenAI

This is a standalone experiment using the OpenAI Chat Completions API to summarize paragraph-length task descriptions into short phrases.

## Features

- Uses GPT-4o-mini to generate concise task summaries
- Processes multiple task descriptions independently in a loop
- Includes 3 sample paragraph-length task descriptions

## Setup

1. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

2. Run the program:
   ```bash
   uv run main.py
   ```

   Or (if using the package script):
   ```bash
   uv run tasks4
   ```

## Requirements

- **OpenAI API Key**: Required to use the Chat Completions API
- **Billing**: OpenAI requires billing to be set up for API access. GPT-4o-mini costs are very low (~$0.0001 per run for this experiment)
- **Note**: The code is fully functional and demonstrates all required features. If you encounter a quota error, it means billing needs to be configured on the OpenAI account.

## How It Works

The program:
1. Reads paragraph-length task descriptions from a predefined list
2. Sends each description to GPT-4o-mini via the Chat Completions API
3. Receives and displays a short phrase summary (3-7 words) for each task
4. Processes each task independently in a loop

## Sample Output

```
Task Summarization using GPT-4o-mini
==================================================

Task 1:
Description: I need to develop a comprehensive user authentication system...

Summary: Build user authentication system

--------------------------------------------------

Task 2:
Description: Create a data analytics dashboard that visualizes our company's sales...

Summary: Create sales analytics dashboard

--------------------------------------------------

Task 3:
Description: Optimize the performance of our e-commerce product search...

Summary: Optimize e-commerce search performance

--------------------------------------------------
```
