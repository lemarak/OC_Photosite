# Pull base image
FROM python:3.8

# Set work directory
WORKDIR /PhotoSite

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install dependencies
COPY Pipfile Pipfile.lock /PhotoSite/
RUN pip install pipenv && pipenv install --deploy --system

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod 755 /PhotoSite/entrypoint.sh

# Copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/PhotoSite/entrypoint.sh"]
