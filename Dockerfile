FROM python:3.8

ARG DOCKERIMAGEID
ENV DOCKER_IMAGE_ID $DOCKERIMAGEID
# Set the working directory
COPY . /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code
#COPY .. .

# Expose the default port for the application.
EXPOSE 80

# Run the application.
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
