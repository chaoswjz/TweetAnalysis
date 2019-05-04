import csv

if __name__ == "__main__":
    with open("Clinton2500.csv", "r", encoding="utf-8") as f:
        r = csv.reader(f)
        with open("Clinton2500.tsv", "a", newline = '', encoding="utf-8") as f2:
            w = csv.writer(f2, delimiter='\t')
            for line in r:
                if line[1] != "4":
                    w.writerow([line[0].strip('\n').replace('\n', '. '), line[1]])

'''
if __name__ == "__main__":
    with open("Clinton2500.tsv", "r", encoding="utf-8") as f:
        r = csv.reader(f, delimiter='\t')
        with open("ctrain.txt", "a", newline = '', encoding="utf-8") as f2:
            for line in r:
                f2.write(line[0] + '\n')
    with open("Trump2500.tsv", "r", encoding="utf-8") as f:
        r = csv.reader(f, delimiter='\t')
        with open("ttrain.txt", "a", newline = '', encoding="utf-8") as f2:
            for line in r:
                f2.write(line[0] + '\n')
'''