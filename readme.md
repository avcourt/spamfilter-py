## Spamfilter
**A Naive Bayesian spam classifier in Python**

This is a reimplementation of my previous spamfilter that I had written in Ruby.

Once again, I have included small training and testing directories to illustrate usage. To get reasonable accuracy, larger training sets must be used, although the accuracy was surprisngly high even with these miniscule datasets. The included emails have been preprocessed to remove the headers and footers. You can experiment and see what provides higher accuracy.

At the moment, the email directory is hardcoded and uses *nix pathnames.
