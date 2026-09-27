from flask import Flask, jsonify, request
from flask_cors import CORS
from chatbot_bridge import ChatbotBridge


app = Flask(__name__)
CORS(app)


# =========================================================
# CHATBOT SESSIONS
# =========================================================

chatbot_sessions = {}


def get_chatbot_session(user_id):

    if user_id not in chatbot_sessions:
        chatbot_sessions[user_id] = ChatbotBridge()

    return chatbot_sessions[user_id]


# =========================================================
# HOME
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "message": "DPredicto backend is running"
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "success": True,
        "message": "Backend connected successfully"
    })


# =========================================================
# START CHAT
# =========================================================

@app.route("/api/chat/start", methods=["POST"])
def start_chat():

    data = request.get_json() or {}

    user_id = data.get("user_id")

    if not user_id:

        return jsonify({
            "success": False,
            "message": "User ID is required"
        }), 400

    chatbot_sessions[user_id] = ChatbotBridge()

    result = chatbot_sessions[user_id].start()

    return jsonify(result), 200


# =========================================================
# INITIAL SYMPTOM MESSAGE
# =========================================================

@app.route("/api/chat/message", methods=["POST"])
def chat_message():

    data = request.get_json() or {}

    user_id = data.get("user_id")
    message = data.get("message", "").strip()

    if not user_id:

        return jsonify({
            "success": False,
            "message": "User ID is required"
        }), 400

    if not message:

        return jsonify({
            "success": False,
            "message": "Message is required"
        }), 400

    chatbot = get_chatbot_session(user_id)

    result = chatbot.send_message(message)

    # -----------------------------------------------------
    # DEBUG
    # -----------------------------------------------------

    print("\n========================================")
    print("INITIAL CHAT RESPONSE")
    print("========================================")
    print(result)
    print("========================================\n")

    return jsonify(result), 200


# =========================================================
# QUESTION FORM ANSWERS
# =========================================================

@app.route("/api/chat/answers", methods=["POST"])
def chat_answers():

    data = request.get_json() or {}

    user_id = data.get("user_id")
    answers = data.get("answers")

    if not user_id:

        return jsonify({
            "success": False,
            "message": "User ID is required"
        }), 400

    if not isinstance(answers, list):

        return jsonify({
            "success": False,
            "message": "Answers must be a list"
        }), 400

    chatbot = get_chatbot_session(user_id)

    # -----------------------------------------------------
    # SEND ANSWERS TO CHATBOT
    # -----------------------------------------------------

    result = chatbot.send_batch_answers(answers)

    # -----------------------------------------------------
    # DEBUG - IMPORTANT
    # -----------------------------------------------------

    print("\n========================================")
    print("FORM ANSWERS RECEIVED")
    print("========================================")
    print("User ID:")
    print(user_id)

    print("\nAnswers:")
    print(answers)

    print("\nCHATBOT RESULT:")
    print(result)

    print("\nPossible Conditions:")
    print(result.get("possible_conditions"))

    print("\nFinal Prediction:")
    print(result.get("prediction"))

    print("\nFinished:")
    print(result.get("finished"))

    print("========================================\n")

    return jsonify(result), 200


# =========================================================
# START SERVER
# =========================================================
if __name__ == "__main__":
    print("Starting DPredicto Flask backend...")
    print("Backend running at http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False, port=5000)
