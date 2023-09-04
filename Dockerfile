# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

#Environment variables must be redefined at run time
ARG BOT_TOKEN
ENV BOT_TOKEN=${BOT_TOKEN}
ARG CHANNEL_ID
ENV CHANNEL_ID=${CHANNEL_ID}
ARG LOGGER_ID
ENV LOGGER_ID=${LOGGER_ID}
ARG API_KEY
ENV API_KEY=${API_KEY}


# Command to run your python program
CMD ["python3", "bot.py"]
