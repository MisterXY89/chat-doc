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

from chat_doc.app.utils import generate_chat_id, hf_inference, update_chat_history

# Create a Blueprint
routes_blueprint = Blueprint("routes_blueprint", __name__)


@routes_blueprint.route("/")
def home():
    chat_id = generate_chat_id(request)
    return render_template("index.html", chat_id=chat_id)


@routes_blueprint.route("/chat")
def chat():
    chat_id = generate_chat_id(request)
    return render_template("chat.html", chat_id=chat_id)


# call hf inference endpoint, extract answer and return it
@routes_blueprint.route("/api/ask")
def chat_doc():
    chat_id = request.args.get("chat_id")
    history = request.args.get("history")
    question = request.args.get("question")

    answer = hf_inference(question, history)
    # chat-id is our identifier to the text
    update_chat_history(chat_id, question, answer)

    return jsonify(answer=answer)
