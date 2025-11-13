"""
Task summarization using OpenAI Chat Completions API.

This module uses GPT-4o-mini to summarize paragraph-length task descriptions
into short phrases.
"""

import os
from openai import OpenAI


# Sample paragraph-length task descriptions
TASK_DESCRIPTIONS = [
    """I need to develop a comprehensive user authentication system for our web application 
    that includes multiple features. First, users should be able to register with their email 
    and password, with proper validation to ensure passwords are strong enough. Then, implement 
    a secure login mechanism with session management that keeps users logged in across page 
    refreshes. Additionally, add a password reset functionality that sends a secure token via 
    email, allowing users to create a new password. Finally, implement role-based access control 
    so that admin users have different permissions than regular users, and ensure all sensitive 
    routes are properly protected with authentication middleware.""",
    
    """Create a data analytics dashboard that visualizes our company's sales performance over 
    time. The dashboard should pull data from our PostgreSQL database and display interactive 
    charts showing monthly revenue trends, top-selling products by category, regional sales 
    distribution across different territories, and customer acquisition metrics. Include filters 
    that allow users to select specific date ranges, product categories, and regions to drill 
    down into the data. The visualizations should be responsive and work well on both desktop 
    and mobile devices. Also add export functionality so users can download the filtered data 
    as CSV or PDF reports for presentations and further analysis.""",
    
    """Optimize the performance of our e-commerce product search feature which is currently too 
    slow when users type in the search box. The search needs to query across multiple database 
    tables including products, categories, tags, and descriptions. Implement full-text search 
    indexing to speed up queries, add caching for frequently searched terms, and implement 
    debouncing on the frontend so we don't send a request for every keystroke. Consider adding 
    autocomplete suggestions that appear as users type, and make sure the search results are 
    ranked by relevance. Test the performance improvements to ensure search results load in 
    under 200 milliseconds even with thousands of products in the database."""
]


def summarize_task(description: str, client: OpenAI) -> str:
    """
    Summarize a paragraph-length task description into a short phrase.
    
    Args:
        description: The full task description to summarize
        client: OpenAI client instance
        
    Returns:
        A short phrase summarizing the task
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes task descriptions into short, concise phrases (3-7 words). Focus on the main action and objective."
            },
            {
                "role": "user",
                "content": f"Summarize this task description into a short phrase:\n\n{description}"
            }
        ],
        max_tokens=50,
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()


def main():
    """Main function to summarize multiple task descriptions."""
    # Initialize OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return
    
    client = OpenAI(api_key=api_key)
    
    print("Task Summarization using GPT-4o-mini")
    print("=" * 50)
    print()
    
    # Process each task description
    for i, description in enumerate(TASK_DESCRIPTIONS, 1):
        print(f"Task {i}:")
        print(f"Description: {description[:100]}...")
        print()
        
        try:
            summary = summarize_task(description, client)
            print(f"Summary: {summary}")
        except Exception as e:
            print(f"Error summarizing task: {e}")
        
        print()
        print("-" * 50)
        print()


if __name__ == "__main__":
    main()

