"""
REWARD MODEL ON YOUR LAPTOP - Complete Working Example
========================================================

This script shows how to use a pre-trained reward model from Hugging Face
to score and rank multiple responses on your laptop (CPU or GPU).

Model: OpenAssistant/reward-model-deberta-v3-base
- Size: ~500MB
- Runs on: CPU (no GPU needed!)
- RAM: 2-4GB recommended
- Speed: ~1 second per response on CPU

"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List, Tuple
import time

print("=" * 70)
print("REWARD MODEL SCORING - Laptop Friendly")
print("=" * 70)

# ============================================================================
# STEP 1: Load the Reward Model
# ============================================================================
print("\nLoading reward model...")
print("(First run will download ~500MB, then cached locally)")

MODEL_NAME = "OpenAssistant/reward-model-deberta-v3-base"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Set to evaluation mode
model.eval()

print(f"✓ Model loaded: {MODEL_NAME}")
print(f"✓ Device: {'GPU' if torch.cuda.is_available() else 'CPU'}")


# ============================================================================
# STEP 2: Define Function to Score Responses
# ============================================================================

def score_response(prompt: str, response: str) -> float:
    """
    Score a single prompt-response pair.

    Args:
        prompt: The question or instruction
        response: The generated response to score

    Returns:
        float: Reward score (higher = better, typically -2 to +2)
    """
    # Format: Some models expect specific format
    # DeBERTa models typically just concatenate
    text = f"{prompt}\n\n{response}"

    # Tokenize
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,  # Keep it short for speed
        padding=True
    )

    # Get score
    with torch.no_grad():
        outputs = model(**inputs)
        score = outputs.logits[0][0].item()

    return score


def rank_responses(prompt: str, responses: List[str]) -> List[Tuple[str, float]]:
    """
    Score multiple responses and return them ranked.

    Args:
        prompt: The question or instruction
        responses: List of responses to rank

    Returns:
        List of (response, score) tuples, sorted by score (best first)
    """
    scored_responses = []

    for i, response in enumerate(responses, 1):
        print(f"  Scoring response {i}/{len(responses)}...", end=" ")
        score = score_response(prompt, response)
        scored_responses.append((response, score))
        print(f"✓ Score: {score:+.4f}")

    # Sort by score (descending)
    scored_responses.sort(key=lambda x: x[1], reverse=True)

    return scored_responses


# ============================================================================
# STEP 3: Example Usage - Rank Multiple Responses
# ============================================================================

print("\n" + "=" * 70)
print("EXAMPLE 1: Ranking Multiple Responses")
print("=" * 70)

prompt = "How do I learn Python programming?"

responses = [
    "Start with the basics: learn syntax, practice daily, build small projects, "
    "use free resources like Python.org and freeCodeCamp. Consistency is key!",

    "Python is hard. You need years of experience.",

    "Learn Python by taking online courses, reading documentation, practicing "
    "coding challenges, and building real projects. Join Python communities for help.",

    "Just Google it.",

    "I recommend starting with 'Automate the Boring Stuff with Python' book, "
    "then doing Python exercises on sites like LeetCode and HackerRank."
]

print(f"\nPrompt: \"{prompt}\"")
print(f"\nScoring {len(responses)} responses...")

start_time = time.time()
ranked = rank_responses(prompt, responses)
elapsed = time.time() - start_time

print(f"\n⏱️  Total time: {elapsed:.2f} seconds")
print(f"⚡ Average: {elapsed / len(responses):.2f} sec/response")

print("\n" + "=" * 70)
print("RANKING RESULTS (Best to Worst)")
print("=" * 70)

for rank, (response, score) in enumerate(ranked, 1):
    print(f"\n#{rank} - Score: {score:+.4f}")
    print(f"   {response[:100]}...")

# ============================================================================
# STEP 4: Example 2 - Quick Quality Check
# ============================================================================

print("\n\n" + "=" * 70)
print("EXAMPLE 2: Quick Quality Check")
print("=" * 70)

test_cases = [
    ("What is 2+2?", "2+2 equals 4."),
    ("What is 2+2?", "I don't know, maybe 5?"),
    ("Explain gravity simply", "Gravity is the force that pulls objects toward Earth."),
    ("Explain gravity simply", "Gravity is complicated quantum physics stuff."),
]

print("\nComparing good vs bad responses:\n")

for prompt, response in test_cases:
    score = score_response(prompt, response)
    quality = "✓ GOOD" if score > 0 else "✗ BAD"
    print(f"{quality:8} Score: {score:+.4f} | {response[:60]}...")

# ============================================================================
# STEP 5: Example 3 - Your Own Prompts
# ============================================================================

print("\n\n" + "=" * 70)
print("EXAMPLE 3: Try Your Own!")
print("=" * 70)

# You can modify these!
my_prompt = "How do I make scrambled eggs?"

my_responses = [
    "Crack 2-3 eggs into a bowl, whisk with salt and pepper. Heat butter in a pan "
    "over medium heat. Pour in eggs, gently stir with spatula until just set. Serve hot.",

    "Put eggs in pan and cook them.",

    "First, crack your eggs into a bowl. Add a splash of milk, salt, and pepper. "
    "Whisk thoroughly. Heat a non-stick pan with butter over medium-low heat. "
    "Pour in eggs and cook slowly, stirring gently, until soft curds form.",
]

print(f"\nYour Prompt: \"{my_prompt}\"")
print(f"\nRanking {len(my_responses)} responses...\n")

my_ranked = rank_responses(my_prompt, my_responses)

print("\nYOUR RESULTS:")
for rank, (response, score) in enumerate(my_ranked, 1):
    print(f"\n#{rank} - Score: {score:+.4f}")
    print(f"   {response[:80]}...")

# ============================================================================
# UNDERSTANDING SCORES
# ============================================================================

print("\n\n" + "=" * 70)
print("UNDERSTANDING REWARD SCORES")
print("=" * 70)

print("""
Score Range: Typically -2 to +2 (but can vary)

 +1.5 to +2.0  → Excellent response
 +0.5 to +1.5  → Good response
 -0.5 to +0.5  → Mediocre response
 -1.5 to -0.5  → Poor response
 -2.0 to -1.5  → Very poor response

Key Points:
✓ Higher score = Better response
✓ Scores are RELATIVE (compare responses to each other)
✓ Not absolute quality measures
✓ Best used for ranking, not absolute judgment

Tips:
• Compare multiple responses to the same prompt
• Look for largest score differences
• Scores > 0 generally indicate helpful responses
• Scores < 0 generally indicate unhelpful responses
""")

# ============================================================================
# SAVING RESULTS
# ============================================================================

print("\n" + "=" * 70)
print("SAVING RESULTS (Optional)")
print("=" * 70)

# Save results to file
with open('reward_scores.txt', 'w') as f:
    f.write("REWARD MODEL SCORING RESULTS\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Prompt: {my_prompt}\n\n")

    for rank, (response, score) in enumerate(my_ranked, 1):
        f.write(f"#{rank} - Score: {score:+.4f}\n")
        f.write(f"   {response}\n\n")

print("✓ Results saved to 'reward_scores.txt'")

print("\n" + "=" * 70)
print("DONE! You can now:")
print("=" * 70)
print("""
1. Modify the prompts and responses above
2. Use score_response() to score individual responses  
3. Use rank_responses() to rank multiple responses
4. Integrate into your own projects!

The model is now cached locally. Future runs will be much faster!
""")

print("=" * 70)