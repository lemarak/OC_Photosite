# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /PhotoSite

# Install dependencies
COPY Pipfile Pipfile.lock /PhotoSite/
RUN pip install pipenv && pipenv install --deploy --system

# # copy entrypoint.sh
# COPY ./entrypoint.sh .

# Copy project
COPY . /PhotoSite/

# # run entrypoint.sh
# ENTRYPOINT ["./entrypoint.sh"]