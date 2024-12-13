import random


def generate_local_sequence(num, min_val=0, max_val=7):
    """Generates a local random sequence given a num length and a range of numbers."""
    return "\n".join(str(random.randint(min_val, max_val)) for _ in range(num))
