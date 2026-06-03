# test_helpers.py
from helper import now_iso, compute_hash
b = {'index':0,'author':'system','text':'Genesis','timestamp':now_iso(),'prev_hash':'0'}
print("Block:", b)
print("Computed hash:", compute_hash(b))

import state_module_2 as state
print("frmo module 2")
print("CHAIN length:", len(state.CHAIN))
print("GENESIS block:", state.CHAIN[0])
print("CANDIDATES keys:", list(state.CANDIDATES.keys()))