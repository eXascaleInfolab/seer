# Use a Python 3.6 base image
FROM python:3.6-slim

# Install Git and Git LFS
RUN apt-get update

# Install Python packages
RUN python -m pip install --upgrade pip

RUN python -m pip install numpy pandas matplotlib && \
    python -m pip install https://files.pythonhosted.org/packages/86/9f/be0165c6eefd841e6928e54d3d083fa174f92d640fdc52f73a33dc9c54d1/tensorflow-1.4.0-cp36-cp36m-manylinux1_x86_64.whl && \
    python -m pip install sugartensor==1.0.0.2 && \
    python -m pip install  sklearn && \
    python -m pip install  future && \
    python -m pip install torch && \
    python -m pip install  scipy && \
    python -m pip install toml  && \
    python -m pip install  torchvision && \
    python -m pip install   wfdb && \
    python -m pip install  lshashpy3


RUN python -m pip install flask

# Set the working directory
WORKDIR /app

COPY gan /app/gan
COPY hashing /app/hashing
COPY graph /app/gaph
COPY config.toml /app
COPY run_pretrained.py /app
COPY html_connection.py /app

EXPOSE 80
# Set the default command
CMD ["python", "html_connection.py"]