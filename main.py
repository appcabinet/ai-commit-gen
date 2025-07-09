import os
import subprocess
import openai
from dotenv import load_dotenv

load_dotenv()

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
Given the following git diff, generate a clear, concise commit message.

{diff}

Requirements:
- Begin with one of: 'feat:' (new feature), 'chore:' (maintenance), or 'bug:' (bug fix).
- Use an imperative, present-tense verb.
- Subject line must be 50 characters or fewer.
- Summarize the main change; do not include details or explanations.
"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert level software engineer, with a clear understanding of how to write succinct, informative git commit messages."},
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

