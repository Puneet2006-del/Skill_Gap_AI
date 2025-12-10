# RESUME WORD COUNTER
import re
from collections import Counter

text = input("Enter your resume paragraph:\n")

words = re.findall(r"\b\w+\b", text.lower())

total_words = len(words)
unique_words = len(set(words))

word_counts = Counter(words)
most_common_word, frequency = word_counts.most_common(1)[0]

print("\nResume Word Count Result")
print("------------------------")
print(f"Total words: {total_words}")
print(f"Unique words: {unique_words}")
print(f"Most repeated word: '{most_common_word}' (appears {frequency} times)")
