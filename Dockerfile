FROM python:3.9-slim-buster

# Install Firefox and other dependencies
RUN apt-get update && apt-get install -y firefox-esr xvfb

# Install Python packages
RUN pip install selenium

# Install xvfb and xauth packages
RUN apt-get install -y xvfb xauth curl

# Add non root selenium user
RUN useradd selenium

RUN mkdir -p /.cache/selenium && mkdir -p /.mozilla
RUN chown -R selenium:selenium /.cache && chmod -R 777 /.cache && \
    chown -R selenium:selenium /.mozilla && chmod -R 777 /.mozilla


RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

USER selenium

# Copy Python script
COPY app.py .

# Run script with xvfb
CMD ["xvfb-run", "--server-args='-screen 0 1024x768x24'", "--auto-servernum", "python", "app.py"]
