## Spamfilter
**A Naive Bayesian spam classifier in Python**

This is a reimplementation of a previous spamfilter that I had written in Ruby. The original Ruby implementation can be found [here](https://github.com/avcourt/spam-filter) and contains more details regarding its design and accuracy.

Once again, I have included small training and testing directories to illustrate usage. To get reasonable accuracy, larger training sets must be used, although the accuracy was surprisngly high even with these miniscule datasets. The included emails have been preprocessed to remove the headers and footers. You can experiment and see what provides higher accuracy.

At the moment, the email directory is hardcoded and uses *nix pathnames.
