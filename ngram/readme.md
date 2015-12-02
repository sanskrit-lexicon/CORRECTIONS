# ngrams

`python ngram.py <dictcode> <n>`

e.g.

`python ngram.py MW 2` would give words in other dictionaries which have 2 letter chunks which are not found in MW.

# Logic

This method would use the following logic.

1. Word should not be member of the base dictionary.

2. Word should have at least one 'ngram' which is not found in any 'ngram' of base dictionary.

3. Word should be found only in one dictionary.

4. Word should not have 'rCC' pattern or should not have a[mMH] pattern.

