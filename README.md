# AI Generated Git Commits!

A simple script for generating git commits with AI.

Commits are prefaced with either:
- `chore:` for dev related tasks
- `feat:` for feature related tasks
- `bug:` for bug related tasks

Will call:
- `git add .`
- `git commit -m '...'` 

1. Create an alias in your bash config (mine is `gcm`) & link to `main.py`
2. Install openai
3. Voila
