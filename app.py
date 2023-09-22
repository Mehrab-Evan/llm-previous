from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS

import organization_handle

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "<h1>Chirpent Chat is Doing great</h1>"


@app.route("/chirpent_web_chat_no_search", methods=["POST"])
def get_answer_for_chirpent():
    session_id = request.headers.get('SESSION-ID', '')
    org_url = request.headers.get('ORG-URL', '')
    user_question = request.json["user_question"]

    organization_handle.is_active(session_id, org_url, user_question)



if __name__ == '__main__':
    app.run()