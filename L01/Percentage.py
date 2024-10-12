import matplotlib.pyplot as plt
from collections import Counter

def percentage(S, letter):

    S = S.upper()

    letter = letter.upper()

    total_letters = len([char for char in S if char.isalpha()])

    letter_count = S.count(letter)

    if total_letters == 0:
        return 0

    return (letter_count / total_letters) * 100


def plot_percentage(S):

    S = S.upper()
    letter_counts = Counter([char for char in S if char.isalpha()])
    total_letters = sum(letter_counts.values())

    letters = sorted(letter_counts.keys())
    percentages = [(letter_counts[char] / total_letters) * 100 for char in letters]

    plt.bar(letters, percentages)
    plt.xlabel('Letters')
    plt.ylabel('Percentage')
    plt.show()


S = "GAGNIUC"
letter = "G"
print(percentage(S, letter))

plot_percentage(S)
