# 1. Start with a foundation
FROM python:3.11-slim

# 2. Set up a "workshop" folder inside the container
WORKDIR /app

# 3. Copy just the "shopping list" first
COPY requirements.txt .

# 4. Install the "tools" from the shopping list
RUN pip install -r requirements.txt

# 5. Copy the rest of our project
COPY main.py .

# 6. The one command to run when the container starts
CMD ["python3", "main.py"]