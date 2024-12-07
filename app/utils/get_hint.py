"NOTE: This is inspired by the bulls and cows game!"

"""
You are playing the Bulls and Cows game with your friend.

You write down a secret number and ask your friend to guess what the number is. When your friend makes a guess, you provide a hint with the following info:

The number of "bulls", which are digits in the guess that are in the correct position.
The number of "cows", which are digits in the guess that are in your secret number but are located in the wrong position. Specifically, the non-bull digits in the guess could be rearranged such that they become bulls.
Given the secret number 'secret' and your friend's guess 'guess', return the hint for your friend's guess.

The hint should be formatted as "xAyB", where x is the number of bulls and y is the number of cows. Note that both secret and guess may contain duplicate digits.
"""

from collections import Counter
# Time: O(n)
# Input + Auxiliary + Output Space: O(n) + O(1) + O(1) as the string won't be that large
def get_hint(secret: str, guess: str):
    frequencies_of_secret = Counter(secret) # Time: O(n)
    frequencies_of_guess = Counter(guess) # Time: O(n)
    bulls = 0
    cows = 0

    for i in range(len(secret)): # Time: O(n)
        # Are the values the same at this index? If so bull += 1
        if secret[i] == guess[i]:
            bulls += 1
            frequencies_of_secret[secret[i]] -= 1
            frequencies_of_guess[secret[i]] -= 1

            # Delete the key if the frequency went below 1
            if frequencies_of_secret[secret[i]] <= 0:
                del frequencies_of_secret[secret[i]]
            if frequencies_of_guess[secret[i]] <= 0:
                del frequencies_of_guess[secret[i]]
    # Look for cows!
    for key in frequencies_of_secret: # Time: O(n)
        if key in frequencies_of_guess:
            cows += min(frequencies_of_secret[key], frequencies_of_guess[key])

    # return "".join([str(bulls), "A", str(cows), "B"])
    return [bulls, cows]