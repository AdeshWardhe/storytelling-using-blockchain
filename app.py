from flask import Flask
import state_module_2 as state
from flask import jsonify
from flask import request
from flask import render_template

from flask_socketio import SocketIO, emit

from web3 import Web3
import os
from dotenv import load_dotenv
import hashlib
import time



# -------------------- BLOCKCHAIN SETUP --------------------

load_dotenv()

# Connect to Sepolia
w3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL")))

print("Connected to Sepolia:", w3.is_connected())

private_key = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(private_key)

contract_address = os.getenv("CONTRACT_ADDRESS")

abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "_index", "type": "uint256"},
            {"internalType": "string", "name": "_hash", "type": "string"},
            {"internalType": "string", "name": "_author", "type": "string"},
            {"internalType": "uint256", "name": "_timestamp", "type": "uint256"}
        ],
        "name": "addProof",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_i", "type": "uint256"}
        ],
        "name": "getProof",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalProofs",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = w3.eth.contract(address=contract_address, abi=abi)


# -------------------- HASH FUNCTION --------------------

def generate_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


# -------------------- SAVE PROOF FUNCTION --------------------

def save_proof(index, story_text, author):
    story_hash = generate_hash(story_text)
    timestamp = int(time.time())

    nonce = w3.eth.get_transaction_count(account.address)

    tx = contract.functions.addProof(
        index,
        story_hash,
        author,
        timestamp
    ).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return tx_hash.hex()







active_users = set()
DISCUSSION_NOTES = []

STORY_OWNER = None      #This will store the Socket ID of the owner.


# app = Flask(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, cors_allowed_origins="*")


# @app.route("/test_blockchain")
# def test_blockchain():
#     test_text = "The dragon entered the city."
#     author = "Adesh"
#     index = 1

#     tx_hash = save_proof(index, test_text, author)

#     return f"Transaction sent! Hash: {tx_hash}"


@app.route("/")
def home():
    return render_template("welcome.html")


@app.route("/ui")
def ui():
    return render_template("second.html")




@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify(state.CHAIN)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

    author = data.get("author")
    text = data.get("text")

    if not author or not text:
        return jsonify({"error": "author and text are required"}), 400

    candidate = state.submit_candidate(author, text)
    return jsonify(candidate)



@app.route("/candidates", methods = ["GET"])
def get_candidates():
    return jsonify(state.CANDIDATES)



@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()

    prev_hash = data.get("prev_hash")
    candidate_hash = data.get("candidate_hash")

    success = state.vote_on_candidate(prev_hash, candidate_hash)

    if not success:
        return jsonify({"error": "vote failed"}), 400

    return jsonify({"message": "vote added"})


@app.route("/finalize", methods=["POST"])
def finalize():
    block = state.finalize_block()

    if block is None:
        return jsonify({"error": "nothing to finalize"}), 400

    return jsonify(block)


def format_candidates():
    """
    Convert internal CANDIDATES structure into UI-friendly flat list.
    """
    formatted = []

    for prev_hash, candidate_list in state.CANDIDATES.items():
        for candidate in candidate_list:
            formatted.append({
                "prev_hash": prev_hash,
                "hash": candidate["hash"],
                "author": candidate["author"],
                "text": candidate["text"],
                "votes": candidate.get("votes", 0)
            })

    return formatted


@app.route("/stories", methods=["GET"])
def get_stories():
    return jsonify(state.STORIES)



# for the scoket.io code
@socketio.on("submit_candidate")
def socket_submit_candidate(data):
    print("RECEIVED:", data)


    author = data.get("author")
    text = data.get("text")

    if not author or not text:
        return

    candidate = state.submit_candidate(author, text)

    # send updated candidates to everyone
    emit("candidates_update", format_candidates(), broadcast=True)


@socketio.on("vote")
def socket_vote(data):
    prev_hash = data.get("prev_hash")
    candidate_hash = data.get("candidate_hash")
    voter_id = request.sid

    success = state.vote_on_candidate(prev_hash, candidate_hash, voter_id)

    if success:
        emit("candidates_update", format_candidates(), broadcast=True)
    else:
        emit("vote_rejected", {"message": "You already voted"}, to=request.sid)


# @socketio.on("finalize")
# def socket_finalize():
#     block = state.finalize_block()

#     if block is None:
#         emit("finalize_failed", {
#             "reason": "tie_reset"
#         }, broadcast=True)
#         emit("candidates_update", format_candidates(), broadcast=True)
#         return

#     emit("chain_update", state.CHAIN, broadcast=True)
#     emit("candidates_update", format_candidates(), broadcast=True)



@socketio.on("finalize")
def socket_finalize():
    block = state.finalize_block()

    if block is None:
        emit("finalize_failed", {
            "reason": "tie_reset"
        }, broadcast=True)
        emit("candidates_update", format_candidates(), broadcast=True)
        return

    # 🔥 ADD THIS
    tx_hash = save_proof(
        index=block["index"],
        story_text=block["text"],
        author=block["author"]
    )
    print("Blockchain TX:", tx_hash)

    emit("chain_update", state.CHAIN, broadcast=True)
    emit("candidates_update", format_candidates(), broadcast=True)



# @socketio.on("connect")
# def handle_connect():
#     active_users.add(request.sid)
#     emit("presence_update", len(active_users), broadcast=True)

@socketio.on("connect")
def handle_connect():
    global STORY_OWNER

    print("USER CONNECTED:", request.sid)

    active_users.add(request.sid)

    if STORY_OWNER is None:
        STORY_OWNER = request.sid
        print("STORY OWNER SET TO:", STORY_OWNER)
        emit("story_owner", {"owner": STORY_OWNER}, broadcast=True)

    emit("presence_update", len(active_users), broadcast=True)




@socketio.on("add_note")
def handle_add_note(data):
    text = data.get("text")

    if not text:
        return

    DISCUSSION_NOTES.append(text)

    emit("notes_update", DISCUSSION_NOTES, broadcast=True)




# The correct way to handle the ghost shadows
@socketio.on('mouse_move')
def handle_mouse_move(data):
    # data is a dictionary: {'x': 100, 'y': 200, 'username': 'Adesh'}
    emit('show_mouse', {
        'id': request.sid, # The unique ID of the person moving their mouse
        'x': data.get('x'),
        'y': data.get('y'),
        'username': data.get('username', 'Guest')
    }, broadcast=True, include_self=False) # Broadcast=True sends it to everyone

# Remove the shadow when a user leaves


@socketio.on("disconnect")
def handle_disconnect():
    global STORY_OWNER

    # remove user from presence
    active_users.discard(request.sid)

    if request.sid == STORY_OWNER:
        STORY_OWNER = None
        emit("story_owner", {"owner": None}, broadcast=True)


    emit("presence_update", len(active_users), broadcast=True)

    # remove ghost cursor
    emit("remove_mouse", request.sid, broadcast=True)



@socketio.on('mouse_leave')
def handle_mouse_leave():
    emit('hide_mouse', request.sid, broadcast=True, include_self=False)

# if __name__ == "__main__":
#     app.run(debug=True)


@socketio.on("new_story")
def socket_new_story(data):
    global STORY_OWNER

    # block non-owners
    if STORY_OWNER is not None and request.sid != STORY_OWNER:
        emit(
            "not_owner",
            {"message": "Only the story owner can start a new story."},
            to=request.sid
        )
        return

    author = data.get("author", "System")
    title = data.get("title", "Genesis")

    # assign owner
    STORY_OWNER = request.sid

    # ✅ delegate everything to state layer
    state.start_new_story(author, title)

    # notify everyone
    
    emit("chain_update", state.CHAIN, broadcast=True)
    emit("candidates_update", [], broadcast=True)



if __name__ == "__main__":
    socketio.run(app, debug=True)