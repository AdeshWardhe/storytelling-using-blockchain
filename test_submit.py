import state_module_2 as state

print("CHAIN:")
print(state.CHAIN)

print("\nCANDIDATES BEFORE:")
print(state.CANDIDATES)

state.submit_candidate("Adesh", "The hero enters the cave.")
state.submit_candidate("Alex", "A cold wind starts blowing.")

print("\nCANDIDATES AFTER:")
print(state.CANDIDATES)
