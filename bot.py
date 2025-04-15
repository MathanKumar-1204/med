import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

def simplify_response(response_text):
    # Simplify the response for a medical audience
    if len(response_text) > 300:
        response_text = response_text[:300] + "..."
    return response_text.replace("complex", "simple").replace("difficult", "easy")

def main():
    # Load environment variables
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Check if the API key is set
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY is not set in the environment variables.")
        sys.exit(1)

    try:
        # Configure the Generative AI client
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        chat = model.start_chat(history=[])
    except Exception as e:
        print(f"Error initializing GenerativeModel: {e}")
        sys.exit(1)

    history = []
    console = Console()

    console.print("[bold blue]Hi there! I'm your medical AI chatbot. Describe your symptoms or ask a question![/bold blue]")

    try:
        while True:
            prompt = input("What do you want to know? (type 'exit' to leave): ")
            if prompt.lower() == "exit":
                console.print("[bold magenta]Goodbye! Have a fantastic day![/bold magenta]")
                break
            if not prompt.strip():
                print("Input cannot be empty. Please try again.")
                continue

            # Filter inappropriate topics
            if "violence" in prompt.lower() or "scary" in prompt.lower():
                console.print("[bold red]Oops! I can't talk about that. Try asking something else![/bold red]")
                continue

            # Add user input to chat history
            history.append({"role": "user", "content": prompt})

            # Display loading spinner while processing
            with console.status("[bold green]Thinking of something helpful to say..."):
                try:
                    response = chat.send_message(prompt, stream=True)
                    response_text = ""
                    for chunk in response:
                        if chunk.text:
                            response_text += chunk.text
                except Exception as e:
                    print(f"Error during chat response: {e}")
                    continue

            response_text = simplify_response(response_text)
            # Add assistant response to chat history
            history.append({"role": "assistant", "content": response_text})
            console.print(Markdown(response_text))
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()