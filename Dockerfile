FROM python:3.9
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
COPY . .
CMD python -m streamlit run Home.py --server.enableWebsocketCompression true