import cProfile
import string
import time
from line_profiler import profile
import ahocorasick
import string
import pstats
"""In order to run the tests simply run

LINE_PROFILE=1 python -m pytest -n 4 a9number_v3_updated_multithread.py

In order to see the profiling, you need to add the option -s
"""
punctuation_to_remove = string.punctuation.replace('-', '').replace("'","").replace(":","") + "“”«_»"
trans_table = str.maketrans(punctuation_to_remove, ' ' * len(punctuation_to_remove))

import threading
import queue
from line_profiler import profile
import string
punctuation_to_remove = string.punctuation.replace('-', '').replace("'", '').replace(":", '') + "“”«_»"
trans_table = str.maketrans(punctuation_to_remove, ' ' * len(punctuation_to_remove))
def count_occurrences_worker(word_list, text_words, start_index, end_index, result_queue):
    count = 0
    word_length = len(word_list)
    if "left" in word_list:
       print(text_words[start_index:end_index])

    for i in range(start_index, end_index - word_length + 1):
        # Check if the current slice of text_words matches the word_list

        if text_words[i:i + word_length] == word_list:
            count += 1
        
    
    # Put the count in the queue
    result_queue.put(count)
num_threads=4
@profile
def count_occurrences_in_text(word, text):
    if len(text)>len(word)*10 :
        num_threads=4
    else :
        num_threads=1
    normalized_text = text.translate(trans_table).lower()
    normalized_word = word.translate(trans_table).lower()
    text_words = normalized_text.replace(":"," : ").replace("'''","").replace("''","").split()
    word_list = normalized_word.split()
    text_length = len(text_words)
    chunk_size = text_length // num_threads
    result_queue = queue.Queue()
    merge=0
    threads = []
    for i in range(num_threads):
        start_index = i * chunk_size + merge
        merge = 0
        if i == num_threads - 1:
            end_index = text_length+merge 

        else:
            end_index = (i + 1) * chunk_size + merge
            while (end_index +merge) < text_length and text_words[end_index] in word_list[-1]:
                end_index += 1
                merge=+1
                print(text_words[end_index+merge])

        
        thread = threading.Thread(target=count_occurrences_worker, args=(word_list, text_words, start_index, end_index, result_queue))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    total_count = 0
    while not result_queue.empty():
        total_count += result_queue.get()
    return total_count

def test_count_occurrences_in_text():
    text = """Georges is my name and I like python. Oh ! your name is georges? And you like Python!
Yes is is true, I like PYTHON
and my name is GEORGES"""
    # test with a little text.
    assert 3 == count_occurrences_in_text("Georges", text)
    assert 3 == count_occurrences_in_text("GEORGES", text)
    assert 3 == count_occurrences_in_text("georges", text)
    assert 0 == count_occurrences_in_text("george", text)
    assert 3 == count_occurrences_in_text("python", text)
    assert 3 == count_occurrences_in_text("PYTHON", text)
    assert 2 == count_occurrences_in_text("I", text)
    assert 0 == count_occurrences_in_text("n", text)
    assert 1 == count_occurrences_in_text("true", text)
    # regard ' as text:
    assert 0 == count_occurrences_in_text("maley", "John O'maley is my friend")

    # Test it but with a BIG length file.
    text = """The quick brown fox jump over the lazy dog.The quick brown fox jump over the lazy dog.""" * 500
    text += """The quick brown fox jump over the lazy dog.The quick brown Georges jump over the lazy dog."""
    text += """esrf sqfdg sfdglkj sdflgh sdflgjdsqrgl """ * 4000
    text += """The quick brown fox jump over the lazy dog.The quick brown fox jump over the lazy python."""
    text += """The quick brown fox jump over the lazy dog.The quick brown fox jump over the lazy dog.""" * 500
    text += """The quick brown fox jump over the lazy dog.The quick brown Georges jump over the lazy dog."""
    text += """esrf sqfdg sfdglkj sdflgh sdflgjdsqrgl """ * 4000
    text += """The quick brown fox jump over the lazy dog.The quick brown fox jump over the lazy python."""
    text += """The quick brown fox jump over the lazy dog.The quick brown fox jump over the lazy dog.""" * 500
    text += """The quick brown fox jump over the lazy dog.The quick brown Georges jump over the lazy dog."""
    text += """esrf sqfdg sfdglkj sdflgh sdflgjdsqrgl """ * 4000
    text += """The quick brown fox jump over the lazy dog.The quick brown fox jump over the lazy python."""
    text += """The quick brown fox jump over the true lazy dog.The quick brown fox jump over the lazy dog."""
    text += """The quick brown fox jump over the lazy dog.The quick brown fox jump over the lazy dog.""" * 500
    text += """ I vsfgsdfg sfdg sdfg sdgh sgh I sfdgsdf"""
    text += """The quick brown fox jump over the lazy dog.The quick brown fox jump over the lazy dog.""" * 500

    assert 3 == count_occurrences_in_text("Georges", text)
    assert 3 == count_occurrences_in_text("GEORGES", text)
    assert 3 == count_occurrences_in_text("georges", text)
    assert 0 == count_occurrences_in_text("george", text)
    assert 3 == count_occurrences_in_text("python", text)
    assert 3 == count_occurrences_in_text("PYTHON", text)
    assert 2 == count_occurrences_in_text("I", text)
    assert 0 == count_occurrences_in_text("n", text)
    assert 1 == count_occurrences_in_text("true", text)
    assert 1 == count_occurrences_in_text(
        "'reflexion mirror'", "I am a senior citizen and I live in the Fun-Plex 'Reflexion Mirror' in Sopchoppy, Florida"
    )
    assert 1 == count_occurrences_in_text(
        "reflexion mirror", "I am a senior citizen and I live in the Fun-Plex (Reflexion Mirror) in Sopchoppy, Florida"
    )
    assert 1 == count_occurrences_in_text("reflexion mirror", "Reflexion Mirror\" in Sopchoppy, Florida")
    assert 1 == count_occurrences_in_text(
        "reflexion mirror", "I am a senior citizen and I live in the Fun-Plex «Reflexion Mirror» in Sopchoppy, Florida"
    )
    assert 1 == count_occurrences_in_text(
        "reflexion mirror",
        "I am a senior citizen and I live in the Fun-Plex \u201cReflexion Mirror\u201d in Sopchoppy, Florida"
    )
    assert 1 == count_occurrences_in_text(
        "legitimate", "who is approved by OILS is completely legitimate: their employees are of legal working age"
    )
    assert 0 == count_occurrences_in_text(
        "legitimate their", "who is approved by OILS is completely legitimate: their employees are of legal working age"
    )
    assert 1 == count_occurrences_in_text(
        "get back to me", "I hope you will consider this proposal, and get back to me as soon as possible"
    )
    assert 1 == count_occurrences_in_text(
        "skin-care", "enable Delavigne and its subsidiaries to create a skin-care monopoly"
    )
    assert 1 == count_occurrences_in_text(
        "skin-care monopoly", "enable Delavigne and its subsidiaries to create a skin-care monopoly"
    )
    assert 0 == count_occurrences_in_text(
        "skin-care monopoly in the US", "enable Delavigne and its subsidiaries to create a skin-care monopoly"
    )
    assert 1 == count_occurrences_in_text("get back to me", "When you know:get back to me")
    assert 1 == count_occurrences_in_text(
        "don't be left", """emergency alarm warning.
Don't be left unprotected. Order your SSSS3000 today!"""
    )
    assert 1 == count_occurrences_in_text(
        "don", """emergency alarm warning.
Don't be left unprotected. Order your don SSSS3000 today!"""
    )
    assert 1 == count_occurrences_in_text("take that as a 'yes'", "Do I have to take that as a 'yes'?")
    assert 1 == count_occurrences_in_text("don't take that as a 'yes'", "I don't take that as a 'yes'?")
    assert 1 == count_occurrences_in_text("take that as a 'yes'", "I don't take that as a 'yes'?")
    assert 1 == count_occurrences_in_text("don't", "I don't take that as a 'yes'?")
    assert 1 == count_occurrences_in_text("attaching my c.v. to this e-mail", "I am attaching my c.v. to this e-mail.")
    assert 1 == count_occurrences_in_text("Linguist", "'''Linguist Specialist Found Dead on Laboratory Floor'''")
    assert 1 == count_occurrences_in_text(
        "Linguist Specialist", "'''Linguist Specialist Found Dead on Laboratory Floor'''"
    )
    assert 1 == count_occurrences_in_text(
        "Laboratory Floor", "'''Linguist Specialist Found Dead on Laboratory Floor'''"
    )
    assert 1 == count_occurrences_in_text("Floor", "'''Linguist Specialist Found Dead on Laboratory Floor'''")
    assert 1 == count_occurrences_in_text("Floor", "''Linguist Specialist Found Dead on Laboratory Floor''")
    assert 1 == count_occurrences_in_text("Floor", "__Linguist Specialist Found Dead on Laboratory Floor__")
    assert 1 == count_occurrences_in_text("Floor", "'''''Linguist Specialist Found Dead on Laboratory Floor'''''")
    assert 1 == count_occurrences_in_text("Linguist", "'''Linguist Specialist Found Dead on Laboratory Floor'''")
    assert 1 == count_occurrences_in_text("Linguist", "''Linguist Specialist Found Dead on Laboratory Floor''")
    assert 1 == count_occurrences_in_text("Linguist", "__Linguist Specialist Found Dead on Laboratory Floor__")
    assert 1 == count_occurrences_in_text("Linguist", "'''''Linguist Specialist Found Dead on Laboratory Floor'''''")


SAMPLE_TEXT_FOR_BENCH = """
A Suggestion Box Entry from Bob Carter

Dear Anonymous,

I'm not quite sure I understand the concept of this 'Anonymous' Suggestion Box. If no one reads what we write, then how will anything ever
change?

But in the spirit of good will, I've decided to offer my two cents, and hopefully Kevin won't steal it! (ha, ha). I would really like to
see more varieties of coffee in the coffee machine in the break room. 'Milk and sugar', 'black with sugar', 'extra sugar' and 'cream and su
gar' don't offer much diversity. Also, the selection of drinks seems heavily weighted in favor of 'sugar'. What if we don't want any suga
r?

But all this is beside the point because I quite like sugar, to be honest. In fact, that's my second suggestion: more sugar in the office.
Cakes, candy, insulin, aspartame... I'm not picky. I'll take it by mouth or inject it intravenously, if I have to.

Also, if someone could please fix the lock on the men's room stall, that would be helpful. Yesterday I was doing my business when Icarus ne
arly climbed into my lap.

So, have a great day!

Anonymously,
Bob Carter
"""


def doit():
    """
    Run count_occurrences_in_text on a few examples
    """
    i = 0
    for x in range(400):
        i += count_occurrences_in_text("word", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("sugar", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("help", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("heavily", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("witfull", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("dog", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("almost", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("insulin", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("attaching", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("asma", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("neither", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("won't", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("green", SAMPLE_TEXT_FOR_BENCH)
        i += count_occurrences_in_text("parabole", SAMPLE_TEXT_FOR_BENCH)
    return i


def test_profile():
    with cProfile.Profile() as pr:
        assert doit() == 2000
        pr.print_stats()

# def test_profile():
#     assert doit() == 2000

# def profile_and_save_stats():
#     """
#     Profiles the `test_profile()` function and collects the profiling data.
#     Returns the timing data.
#     """
#     # Number of runs
#     num_runs = 10
#     total_time_in_function = 0
#     for run in range(num_runs):
#         profiler = cProfile.Profile()
#         profiler.enable()
#         test_profile()
#         profiler.disable()
#         stats_obj = pstats.Stats(profiler)
#         stats_obj.strip_dirs().sort_stats('cumulative')

#         for function, (ncalls, tottime, primetime, cumtime, callers) in stats_obj.stats.items():
#             if function == ('a9number_v3_updated.py', 12, 'count_occurrences_in_text'):
#                 # Add the cumulative time for the function
#                 total_time_in_function += cumtime
#                 break
#                 # Iterate through the stats and save the function name and cumulative time
#         # timing_data = []
#         # for function, (ncalls, tottime, primetime, cumtime, callers) in stats_obj.stats.items():
#         #     timing_data.append({
#         #         'function': function,
#         #         'total_time': cumtime
#         #     })
#     avg_time_in_function = total_time_in_function / num_runs
#     return avg_time_in_function
# avg_time = profile_and_save_stats()
# print(f"Average total time in function 'count_occurrences_in_text' over {10} runs: {avg_time} seconds")

test_profile()