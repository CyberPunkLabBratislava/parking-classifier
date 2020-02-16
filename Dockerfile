FROM python:3.7

# Copy files
COPY src src
# COPY setup.py .
COPY requirements.txt .
COPY parkingspots.csv .
COPY model model

# Install app dependencies
RUN python -m venv .
RUN /bin/bash -c "source bin/activate"
# RUN python setup.py bdist_wheel
# RUN pip install dist/*
RUN pip install -r requirements.txt
EXPOSE 5000
CMD uwsgi --module src.__main__:app --http :5000