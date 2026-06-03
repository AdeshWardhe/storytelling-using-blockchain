import os
import json
import hashlib
from pathlib import Path
from helper import now_iso, compute_hash

'''
os → lets us read environment variables (like AWS file paths)

json → lets us read and write state.json

Path → helps us check if a file exists

helpers → we reuse timestamp + hashing from Module 1

'''

STATE_FILE = os.environ.get('STATE_FILE', 'state.json')

CHAIN = []         
CANDIDATES = {}   
STORIES = []   # list of completed stories
'''
Why move from candidate to chain?

CANDIDATES are provisional — multiple and changeable.

CHAIN is the official record/ history. Once a candidate is chosen, it must be fixed and recorded in CHAIN — that’s how a story grows one accepted block at a time.
'''


'''
What it does: if CHAIN is empty, it creates the first block (index 0), computes its hash and adds it to CHAIN.

Why: Every blockchain needs a starting block. This guarantees the chain always has at least one block.
'''
def create_genesis_if_missing():
    if CHAIN:
        return
    genesis = {
        'index': 0,
        'author': 'system',
        'text': 'Genesis',
        'timestamp': now_iso(),
        'prev_hash': '0'
    }
    genesis['hash'] = compute_hash(genesis)
    CHAIN.append(genesis)

def load_state_from_file():
    """
    Try to load state from STATE_FILE.
    Returns tuple (chain, candidates) or (None, None) if file missing or unreadable.
    """
    p = Path(STATE_FILE)
    if not p.exists():
        return None, None
    try:
        with p.open('r', encoding='utf-8') as f:
            state = json.load(f)
        chain = state.get('chain', [])
        candidates = state.get('candidates', {})
        stories = state.get("stories", [])
        return chain, candidates, stories
    except Exception as e:
        # Print error so you can debug issues with state.json
        print("Error loading state:", e)
        return None, None

def initialize_state():
    global CHAIN, CANDIDATES, STORIES

    chain, candidates, stories = load_state_from_file()

    if chain is not None:
        CHAIN = chain
        CANDIDATES = candidates or {}
        STORIES = stories or []
        print(f"Loaded chain with {len(CHAIN)} blocks")
        print(f"Loaded {len(STORIES)} archived stories")
    else:
        create_genesis_if_missing()
        STORIES = []
        print("No saved state found — created genesis block.")


# Run initialization on import so other modules can 'import state' and get ready structures
initialize_state()

# MODULE 3: Save state function
def save_state():
    state = {
        "chain": CHAIN,
        "candidates": CANDIDATES,
        "stories": STORIES
    }

    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        print(f"State saved to {STATE_FILE}")
    except Exception as e:
        print("Error saving state:", e)


# MODULE 4: Submit candidate function

def submit_candidate(author, text):
    #get the last block from the chain
    last_block = CHAIN[-1]

    new_index = last_block['index'] + 1
    previous_hash = last_block["hash"]
    current_time = now_iso()

    candidate = {
    "index": last_block["index"] + 1,
    "author": author,
    "text": text,
    "timestamp": now_iso(),
    "prev_hash": last_block["hash"],
    "votes": 0
}

    candidate_hash = compute_hash(candidate)
    candidate["hash"] = candidate_hash

    # Step 5: store candidate in CANDIDATES
    if previous_hash in CANDIDATES:
        CANDIDATES[previous_hash].append(candidate)
    else:
        CANDIDATES[previous_hash] = []
        CANDIDATES[previous_hash].append(candidate)

    # Step 6: save everything to file
    save_state()

    # Step 7: return the candidate (optional but useful)
    return candidate






# MODULE 5: Vote for candidate function

def vote_on_candidate(prev_hash, candidate_hash, voter_id):
    if prev_hash not in CANDIDATES:
        print("No candidates found for this block.")
        return False

    candidates_list = CANDIDATES[prev_hash]

    for candidate in candidates_list:
        if candidate["hash"] == candidate_hash:

            # 🚫 prevent double voting
            voters = candidate.setdefault("voters", [])

            if voter_id in voters:
                print("User already voted.")
                return False

            # ✅ allow vote
            candidate["votes"] += 1
            voters.append(voter_id)

            save_state()
            print("Vote added successfully.")
            return True

    print("Candidate not found.")
    return False


# MODULE 6: Choose winning candidate function

def finalize_block():

    last_block = CHAIN[-1]
    last_hash = last_block["hash"]

    # No candidates
    if last_hash not in CANDIDATES:
        print("No candidates to finalize.")
        return None

    candidates_list = CANDIDATES[last_hash]

    if len(candidates_list) == 0:
        print("Candidate list is empty.")
        return None

    # 1️⃣ Find maximum votes
    max_votes = 0
    for c in candidates_list:
        if c["votes"] > max_votes:
            max_votes = c["votes"]

    # 2️⃣ Find all candidates with max votes
    top_candidates = []
    for c in candidates_list:
        if c["votes"] == max_votes:
            top_candidates.append(c)

    # 3️⃣ Tie → reset votes
    if len(top_candidates) > 1:
        print("Tie detected. Resetting votes.")
        reset_votes(last_hash)
        return None

    # 4️⃣ Clear winner
    winner = top_candidates[0]

    # 5️⃣ Create final block
    final_block = {
        "index": winner["index"],
        "author": winner["author"],
        "text": winner["text"],
        "timestamp": winner["timestamp"],
        "prev_hash": winner["prev_hash"]
    }

    final_block["hash"] = compute_hash(final_block)

    # 6️⃣ Add to chain
    CHAIN.append(final_block)

    # 7️⃣ Remove used candidates
    del CANDIDATES[last_hash]

    # 8️⃣ Save state
    save_state()

    print("Block finalized and added to chain.")
    return final_block

def reset_votes(prev_hash):
    if prev_hash not in CANDIDATES:
        return

    for candidate in CANDIDATES[prev_hash]:
        candidate["votes"] = 0
        candidate["voters"] = []

    save_state()




def start_new_story(author, title):
    global CHAIN, CANDIDATES, STORIES

    # ✅ Archive old story
    if CHAIN:
        STORIES.append({
            "ended_at": now_iso(),
            "chain": CHAIN
        })

    genesis = {
        "index": 0,
        "author": author,
        "text": title,
        "timestamp": now_iso(),
        "prev_hash": "0"
    }

    # ✅ Use SAME hashing logic as rest of the chain
    genesis["hash"] = compute_hash(genesis)

    CHAIN = [genesis]
    CANDIDATES = {}

    save_state()
    return CHAIN



