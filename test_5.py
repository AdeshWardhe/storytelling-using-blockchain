import state_module_2 as state

# Submit two candidates
c1 = state.submit_candidate("Adesh", "The hero enters the cave.")
c2 = state.submit_candidate("Alex", "A monster appears.")

# Get prev_hash
prev_hash = state.CHAIN[-1]["hash"]

print("Before voting:")
print(state.CANDIDATES)

# Vote
state.vote_on_candidate(prev_hash, c2["hash"])
state.vote_on_candidate(prev_hash, c2["hash"])
state.vote_on_candidate(prev_hash, c1["hash"])

print("\nAfter voting:")
print(state.CANDIDATES)
