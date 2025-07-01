# ==============================================================================
# 10 Academy - Credit Risk Modeling - Week 5
# Task 6: Dockerfile
#
# This file is the recipe for building our application's Docker container.
# ==============================================================================

# --- Stage 1: Base Image ---
# Start from an official Python base image. 'slim' is a lightweight version.
FROM python:3.9-slim

# --- Set Environment Variables ---
# Prevents Python from writing .pyc files to disk.
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures that Python output is sent straight to the terminal without buffering.
ENV PYTHONUNBUFFERED 1

# --- Set Working Directory ---
# Create and set the working directory inside the container.
WORKDIR /app

# --- Install Dependencies ---
# Copy the requirements file first to leverage Docker's layer caching.
# If requirements.txt doesn't change, Docker won't re-run this step.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# --- Copy Application Code ---
# Copy the source code and the MLflow tracking data into the container.
COPY ./src ./src
COPY ./mlruns ./mlruns

# --- Expose Port ---
# Tell Docker that the container listens on port 8000.
EXPOSE 8000

# --- Run the Application ---
# The command to run when the container starts.
# We use uvicorn to run our FastAPI application.
# --host 0.0.0.0 makes the app accessible from outside the container.
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
