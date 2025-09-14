import os

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.google import Gemini
from agno.tools.postgres import PostgresTools
from agno.tools.reasoning import ReasoningTools
from dotenv import load_dotenv

db_url = "postgresql://postgres:admin@localhost:5432/data_enrichment"  # Replace with your own connection string


# Load environment variables
load_dotenv()


def main():
    # Initialize PostgresTools with connection details
    postgres_tools = PostgresTools(
        host="localhost",
        port=5432,
        db_name="data_enrichment",
        user="postgres",
        password="admin",
    )
    # Create an agent with Gemini model, web search, and database querying capabilities
    agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
        tools=[ReasoningTools(), postgres_tools],
        instructions=[
            "You are a helpful daily report agent with database querying capabilities.",
            "You can query the PostgreSQL database for data analysis and reporting.",
            "When querying the database, use the available PostgresTools to run SQL queries.",
            "Keep your responses concise and focused.",
        ],
        markdown=True,
        add_history_to_context=True,
        num_history_runs=3,
        db=PostgresDb(db_url=db_url),
    )

    print("🤖 Daily Report Agent is ready!")
    print(
        "You can ask me questions about data in your database and I'll help you with daily tasks and information gathering."
    )
    print(
        "\nExample: 'Show me the latest records from my database' or 'What's the latest news about AI?' or 'Help me analyze my data'"
    )

    # Example interaction
    try:
        # response = agent.run("Hello! Can you tell me what day it is today?")
        # print(f"\nAgent Response: {response.content}")
        agent.cli_app(
            input="Hello! Can you explore my database and show me what tables are available?",
            stream=True,
            session_id="123",
        )
    except Exception as e:
        print(
            f"Note: Agent setup complete, but you'll need to set GOOGLE_API_KEY environment variable to run it. Error: {e}"
        )


if __name__ == "__main__":
    main()
