# Execution
`afem.sh`

# Logic
We have tried to extract the words from dictcode.xml files which end with 'a' and have been marked 'feminine'.
According to Sanskrit grammar, such words are not possible.
That makes them suitable articles for examination for veracity or otherwise.
Please refer to #53 for details.

# Output
1. `afem.txt` file has suspect words in `word:dictcode` format.
2. Intermediate files are in `afem` folder. They are named `dictcode_fem.xml`.

# Programs
1. `afem.sh` mainly uses grep for getting the suspect words and sends them to `afem/dictcode_fem.xml`. After this step, it also runs `afem.py` which extracts only key1.
