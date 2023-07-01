FROM python:3.9

ENV PORT=80

EXPOSE $PORT

WORKDIR /zeitgeist-streamlit-app

COPY . .

RUN pip install -r requirements.txt

CMD sh setup.sh && streamlit run main.py --server.enableWebsocketCompression=false
