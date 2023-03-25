FROM python:3.9

ENV PORT=8578

EXPOSE $PORT

WORKDIR /zeitgeist-streamlit-app

COPY . .

RUN pip install -r requirements.txt

CMD sh setup.sh && streamlit run main.py
