import math
import os
import re
from collections import Counter


class Spamfilter:
    """A naive Bayesian spam filter"""

    def __init__(self, training_dir):
        """ inits Spamfilter with training data
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        print("Training filter with known ham ...")
        self.ham_table = dict(Counter(dir_tokens(training_dir + "ham/")))
        print("Training filter with known spam...")
        self.spam_table = dict(Counter(dir_tokens(training_dir + "spam/")))
        self.uniq_h_toks = len(self.ham_table)
        self.uniq_s_toks = len(self.spam_table)
        self.total_h_toks = sum(self.ham_table.values())
        self.total_s_toks = sum(self.spam_table.values())
        self.tok_arr = sorted(
            list(self.ham_table.keys()) + list(self.spam_table.keys())
        )
        self.freq_tab = self.create_frequency_table()
        self.file_count = 0
        self.count_spam = 0
        self.count_ham = 0
        self.spam_list = []
        self.ham_list = []

    def create_frequency_table(self):
        """ Generates token frequency table from training emails
        :return:  dict{k,v}:  spam/ham frequencies
        k = (str)token, v = {spam_freq: , ham_freq:, prob_spam:, prob_ham:}
        """
        freq_table = {}
        for tok in self.tok_arr:
            entry = {}
            s_freq = self.spam_table.get(tok, 0)
            entry["spam_freq"] = s_freq
            h_freq = self.ham_table.get(tok, 0)
            entry["ham_freq"] = h_freq
            s_prob = (s_freq + 1 / float(self.uniq_s_toks)) / (self.total_s_toks + 1)
            entry["prob_spam"] = s_prob
            h_prob = (h_freq + 1 / float(self.uniq_h_toks)) / (self.total_h_toks + 1)
            entry["prob_ham"] = h_prob
            freq_table[tok] = entry
        return freq_table

    def prob_spam(self, token):
        """calculates the probability that 'token' is found in spam emails

        :param token: (str)
        :return: (float) probability 'token' is spam based on training emails
        """
        val = self.freq_tab.get(token)
        if val is not None:
            return val["prob_spam"]
       
        return (1.0 / self.uniq_s_toks) / (self.total_s_toks + 1)

    def prob_ham(self, token):
        """calculates the probability that 'token' is found in ham emails

        :param token: (str)
        :return: (float) probability 'token' is ham based on training emails
        """
        val = self.freq_tab.get(token)
        if val is not None:
            return val["prob_ham"]
    
        return (1.0 / self.uniq_h_toks) / (self.total_h_toks + 1)

    def prob_msg_spam(self, filepath):
        """Calculates the probability that a message is spam

        :param filepath: (str) path of email
        :return: (float) probability message is spam
        """
        toks = file_tokens(filepath)
        sm = 0
        for tok in toks:
            sm += math.log10(self.prob_spam(tok))
        return sm

    def prob_msg_ham(self, filepath):
        """Calculates the probability that a message is ham

        :param filepath: (str) path of email
        :return: (float) probability message is ham
        """
        toks = file_tokens(filepath)
        sm = 0
        for tok in toks:
            sm += math.log10(self.prob_ham(tok))
        return sm

    def classify(self, filepath):
        """classifies a file as spam or ham based on training data

        :param filepath:
        :return: (boolean) True->spam, False->ham
        """
        self.file_count += 1
        if self.prob_msg_spam(filepath) > self.prob_msg_ham(filepath):
            self.count_spam += 1
            self.spam_list.append(filepath)
            return True
        else:
            self.count_ham += 1
            self.ham_list.append(filepath)
            return False

    def classify_all(self, dir_path, known_type="spam"):
        """Classifies all emails in a testing directory and maintains count of errors

        :param dir_path: path of testing directory
        :param known_type: str: the known type of testing directory
        """
        self.ham_list = []
        self.spam_list = []
        self.file_count = 0
        self.count_spam = 0
        self.count_ham = 0
        print("\nClassifying all emails found in directory: ./" + dir_path)

        try:
            for f in os.listdir(dir_path):
                self.classify(dir_path + f)
                if known_type == "spam":
                    correct = self.count_spam / float(self.file_count)
                else:
                    correct = self.count_ham / float(self.file_count)

            print("Total spam:{:8d}".format(self.count_spam))
            print("Total ham: {:8d}".format(self.count_ham))
            print("Correctly classified: {:6.2f}%".format(correct * 100))
        except FileNotFoundError as e:
            print("ERROR: classify_all() failed " + str(e))

    def clean_table(self, min_freq):
        """Removes entries from frequency table if they are deemed poor indicators.
        or if combined spam/ham frequency is below 'min_freq'

        :param min_freq: if total token count below threshold, delete from table
        """
        rm_keys = []
        for k, v in self.freq_tab.items():
            if (
                v["spam_freq"] + v["ham_freq"] < min_freq
                or 0.45 < (v["prob_spam"] / (v["prob_spam"] + v["prob_ham"])) < 0.55
            ):
                rm_keys.append(k)
        for k in rm_keys:
            print("deleting " + str(k) + " from freq table in clean()")
            del self.freq_tab[k]

    def print_table_info(self):
        """ Print training info:
            - unique tokens in ham and spam, number of emails in training set"""
        print("\n=======================================")
        print("TRAINING AND FREQUENCY TABLE INFO")
        print("=======================================")
        print("Unique tokens in spam messages:{:8d}".format(len(self.spam_table)))
        print("Unique tokens in ham messages: {:8d}".format(len(self.ham_table)))
        print("Unique tokens in ALL messages: {:8d}".format(len(self.freq_tab)))
        print("Num spam e-mails:{:22d}".format(len(os.listdir("emails/testing/spam/"))))
        print("Num ham e-mails: {:22d}".format(len(os.listdir("emails/testing/ham/"))))


def tokens(text, tok_size=3):
    """ Returns a list of all substrings contained in 'text' of size 'tok_size'

    :param text: (string) text to tokenize
    :param tok_size: length of substrings
    :return: (list) tokens of 'text'
    """
    return [text[i : i + tok_size] for i in range(len(text) - tok_size + 1)]


def clean_split(in_str):
    """ Removes all non-alphanum chars and splits string at whitespace, downcase

    :param in_str: (str) target string
    :return: (list) cleaned strings
    """
    return re.sub(r"[^\s\w]|_", "", in_str).lower().split()


def file_tokens(filepath):
    """ tokenizes all strings contained in 'filepath' after removing \
     all non-alphanum chars and splitting strings at whitespace

    :param filepath: path of target file
    :return: list of tokens
    """
    toks = []
    try:
        with open(filepath, encoding="utf8", errors="ignore") as fp:
            for line in fp:
                words = clean_split(line)
                toks.extend(words)
    except FileNotFoundError as e:
        print("Error:" + str(e))
    return [x for x in toks if len(x) < 10]


def dir_tokens(dir_path):
    """ tokenizes all files contained in 'dir_path'

    :param dir_path: directory containing files to be tokenized
    :return: list of tokens
    """
    dir_toks = []
    try:
        filenames = os.listdir(dir_path)
        for f in filenames:
            dir_toks.extend(file_tokens(dir_path + f))
    except FileNotFoundError as e:
        print("Error:" + str(e))
    return dir_toks


if __name__ == "__main__":
    spamfilter = Spamfilter("emails/training/")
    spamfilter.print_table_info()
    spamfilter.classify_all("emails/testing/spam/", "spam")
    spamfilter.classify_all("emails/testing/ham/", "ham")
