"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    new = []
    for i in paragraphs:
        if select(i):
            new.append(i)

    if k >= len(new):
        return ''
    else:
        return new[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def select(p):
        for i in topic:
            if i in split(remove_punctuation(lower(p))):
                return True
        return False
    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    if typed_words == []:
        return 0.0
    elif len(typed_words) == len(reference_words):
        i = 0
        for n in range(len(typed_words)):
            if typed_words[n] == reference_words[n]:
                i += 1
        return i / len(typed_words) * 100
    elif len(typed_words) > len(reference_words):
        i = 0
        for n in range(len(reference_words)):
            if typed_words[n] == reference_words[n]:
                i += 1
        return i / len(typed_words) * 100
    else:
        i = 0
        for n in range(len(typed_words)):
            if typed_words[n] == reference_words[n]:
                i += 1
        return i / len(typed_words) * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    if typed == '':
        return 0.0
    else:
        return len(typed) / 5 * 60 / elapsed
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    d = {}
    if user_word in valid_words:
        return user_word
    else:
        for word in valid_words:
            if diff_function(user_word, word, limit) > limit:
                None
            elif diff_function(user_word, word, limit) in d:
                None
            else:
                d[diff_function(user_word, word, limit)] = word
        if d == {}:
            return user_word
        else:
            return d[min(d)]
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6

    """def helper(start, goal, limit, result):
        if result > limit:
            return limit
        elif start == '' or goal == '':
            return max(len(start), len(goal))
        elif start[0] == goal[0]:
            return helper(start[1:], goal[1:], limit, result)
        else:
            return 1 + helper(start[1:], goal[1:], limit, result + 1)

    return helper(start, goal, limit, 0)"""

    if limit == -1:
        return 0
    elif start == '' or goal == '':
        return max(len(start), len(goal))
    elif start[0] == goal[0]:
        return swap_diff(start[1:], goal[1:], limit)
    else:
        return 1 + swap_diff(start[1:], goal[1:], limit - 1)
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""


    if limit == -1: # Fill in the condition
        # BEGIN
        return 0
        # END

    elif start == '' or goal == '': # Feel free to remove or add additional cases
        # BEGIN
        return max(len(start), len(goal))
        # END
    elif start[0] == goal[0]:
        return edit_diff(start[1:], goal[1:], limit)

    else:
        add_diff = edit_diff(goal[0] + start, goal, limit - 1) + 1  # Fill in these lines
        remove_diff = edit_diff(start[1:], goal, limit - 1) + 1
        substitute_diff = edit_diff(goal[0] + start[1:], goal, limit - 1) + 1
        # BEGIN
    return min(add_diff, remove_diff, substitute_diff)
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    n = 0
    for i in range(len(typed)):
        if typed[i] == prompt[i]:
            n += 1
        else:
            break
    rate = n / len(prompt)
    send({'id': id, 'progress': rate})
    return rate
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    l = []
    for i in range(n_players):
        l.append([])

    for n in range(n_words):
        fast_word = []

        for i in range(n_players):
            fast_word.append(elapsed_time(word_times[i][n + 1]) - elapsed_time(word_times[i][n]))
        fast = min(fast_word)

        for i in range(n_players):
            if abs(fast_word[i] - fast) < margin:
                l[i].append(word(word_times[0][n + 1]))
    return l
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
