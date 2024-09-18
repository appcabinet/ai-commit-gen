import os
import subprocess
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8')

def get_git_diff():
    output, _ = run_command("git diff --cached")
    return output

def generate_commit_message(diff):
    prompt = f"""
Based on the following git diff, generate a concise and descriptive commit message:

{diff}

The commit message should start with either 'feat:' for new features, 'chore:' for maintenance tasks, or 'bug:' for bug related fixes.
Limit the message to 50 characters for the subject line.
"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates git commit messages."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

def main():
    # Stage all changes
    run_command("git add .")

    # Get the diff of staged changes
    diff = get_git_diff()

    if not diff:
        print("No changes to commit.")
        return

    # Generate commit message
    commit_message = generate_commit_message(diff)

    # Commit changes
    output, error = run_command(f'git commit -m "{commit_message}"')

    if error:
        print(f"Error committing changes: {error}")
    else:
        print(f"Changes committed successfully with message: {commit_message}")

if __name__ == "__main__":
    main()

