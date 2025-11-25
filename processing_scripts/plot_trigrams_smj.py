
import matplotlib.pyplot as plt

trigrams = "/home/hiovain/Desktop/code_test/trigrams-smj.txt"

with open(trigrams) as tgrams:
    counts = []
    for r in tgrams:
        rivi = r.replace("\n","")
        columns = rivi.split("\t")
        counts.append(int(columns[1]))
    print(counts)

# Not optimal...
plt.hist(counts, bins = 10)
plt.show()

