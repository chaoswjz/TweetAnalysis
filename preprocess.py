import csv
import re
import argparse

def removeURL(text: str) -> str:
    text = text.strip('\n').strip('\t')
    pattern = re.compile(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*")
    match = re.search(pattern, text)
    return text if match is None else text[:match.start()] + text[match.end():]

def removeMention(text: str) -> str:
    text = text.strip('\n').strip('\t')
    pattern = re.compile(r"@[^ ,.!?\"]+")
    match = re.findall(pattern, text)
    ans = []
    for word in text.split():
        if word in match:
            continue
        else:
            ans.append(word.strip('\n').strip('\t'))
    return ' '.join(ans)

def output(file: str, text: str, label: int):
    with open(file, "a+", encoding="utf-8") as csv_f:
        csv_writer = csv.writer(csv_f, delimiter=',')
        csv_writer.writerow([text, label])

def preprocessing(file: str):
    outfile = file.split('.')[0] + "_out.csv"
    with open(outfile, "w", encoding="utf-8") as csv_out:
        fields = ['tweet', 'code']
        csv_writer = csv.writer(csv_out, delimiter=',')
        csv_writer.writerow(fields)
    with open(file, "r", encoding="utf-8") as csv_in:
        csv_reader = csv.reader(csv_in, delimiter=',')
        for i, row in enumerate(csv_reader):
            if i == 0: continue
            text = row[1].lower()
            text = removeURL(text)
            text = removeMention(text)
            output(outfile, text, row[2])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, nargs='*')
    files = parser.parse_args().file
    for f in files:
        preprocessing(f)
