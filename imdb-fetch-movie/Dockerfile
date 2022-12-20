
# Dockerfile - blueprint for building images
# Image - template for containers
# - docker build -t (tag) python-imdb
# - docker run -t i (interactive mode)
# Container - running process
FROM python:3.8

# add this file to the image
ADD main.py .

# dependencies
RUN pip install requests beautifulsoup4

# run this in the cmd line
CMD [ "python", "./main.py" ]


