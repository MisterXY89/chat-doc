"""
Contains all the routes for the app
"""

from flask import (
    Blueprint,
    Response,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

import chat_doc.rag.main as rag
from chat_doc.app.utils import generate_chat_id, hf_inference, update_chat_history

# Create a Blueprint
routes_blueprint = Blueprint("routes_blueprint", __name__)


@routes_blueprint.route("/")
def home():
    chat_id = generate_chat_id(request)
    return render_template("index.html", chat_id=chat_id, title="Home")


@routes_blueprint.route("/chat")
def chat():
    chat_id = generate_chat_id(request)
    return render_template("chat.html", chat_id=chat_id, title="Chat")


# call hf inference endpoint, extract answer and return it
@routes_blueprint.route("/api/ask", methods=["POST"])
def chat_doc():
    # read post data
    print(request.json)
    chat_id = request.json["chat_id"]
    history = request.json["history"]
    question = request.json["question"]

    icd_matches = rag.retrieve(question)

    print("chat_id", chat_id)
    print("history", history)
    print("question", question)

    answer = hf_inference(question, history, icd_match=icd_matches[0]["text"])
    update_chat_history(chat_id, question, answer)

    return jsonify(
        answer=answer,
        icd_matches=icd_matches,
    )


# retrive best matches from rag (ICD)
@routes_blueprint.route("/api/retrieve", methods=["POST"])
def rag_retrieve():
    print(request.json)
    query = request.json["query"]

    print("query", query)

    matches = rag.retrieve(query)
    return jsonify(
        matches=matches,
    )
