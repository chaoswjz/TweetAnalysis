import os
import re
from matplotlib import pyplot as plt
import json
import datetime as dt
import matplotlib.dates as mpldts
import csv
import pandas as pd

def count_tweets(step=1):
    # list length is the debate length plus the half hour before and after, 90 (2nd debate) or 93 (3rd debate) + 60 min
    time_count2 = [0] * (int((90 + 60) * 60 / step))
    trump2 = [0] * ((90 + 60) * 60)
    clinton2 = [0] * ((90 + 60) * 60)
    time_count3 = [0] * (int((93 + 60) * 60 / step) + 1)
    trump3 = [0] * ((93 + 60) * 60 + 1)
    clinton3 = [0] * ((93 + 60) * 60 + 1)
    #time in edt
    only_t2 = 0
    only_c2 = 0
    only_t3 = 0
    only_c3 = 0
    count_2nd_key = 0
    count_2nd_in = 0
    count_2nd_all = 0
    count_3rd_key = 0
    count_3rd_in = 0
    count_3rd_all = 0
    debate_start2 = dt.datetime.strptime('Oct 09 20:35:00 2016', '%b %d %H:%M:%S %Y')
    debate_end2 = dt.datetime.strptime('Oct 09 23:05:00 2016', '%b %d %H:%M:%S %Y')
    debate_start3 = dt.datetime.strptime('Oct 19 20:33:00 2016', '%b %d %H:%M:%S %Y')
    debate_end3 = dt.datetime.strptime('Oct 19 23:06:00 2016', '%b %d %H:%M:%S %Y')
    path = "D:/tweet/tweets"
    files = os.listdir(path)
    total = len(files)
    num = 0
    for file in files:
        num += 1
        print("progress: ", num / total)
        with open(path + '/' + file, 'r') as f:
            data = json.load(f)
            for js_dict in data:
                post_t = dt.datetime.strptime(js_dict['created_at'][4:20] + js_dict['created_at'][26:], '%b %d %H:%M:%S %Y') - dt.timedelta(hours=4)
                if post_t >= debate_start2 and post_t < debate_end2:
                    with open("2nd.txt", 'a', encoding='utf-8') as f:
                        f.write(file + '\n')
                    count_2nd_all += 1
                    ds2 = dt.datetime.strptime('Oct 09 21:05:00 2016', '%b %d %H:%M:%S %Y')
                    de2 = dt.datetime.strptime('Oct 09 22:35:00 2016', '%b %d %H:%M:%S %Y')
                    if post_t >= ds2 and post_t < de2:
                        count_2nd_in += 1
                    #regular expression to match names
                    if re.match(r'[\s\S]*(trump|donald|hillary|clinton)[\s\S]*', js_dict['text'].lower()) is not None:
                        if post_t >= ds2 and post_t < de2:
                            count_2nd_key += 1
                        time_count2[int((post_t - debate_start2).seconds / step)] += 1
                        with open("target23.txt", 'a', encoding='utf-8') as f:
                            f.write(file + '\n')
                        with open('all2ndkey_tweet.tsv', 'a', newline='', encoding="utf-8") as f:
                            twriter = csv.writer(f, delimiter='\t')
                            text = ' '.join(js_dict['text'].lower().split())
                            twriter.writerow([text, post_t])
                        if re.match(r'[\s\S]*(trump|donald)[\s\S]*', js_dict['text'].lower()) is not None:
                            trump2[(post_t - debate_start2).seconds] += 1
                            if re.match(r'[\s\S]*(hillary|clinton)[\s\S]*', js_dict['text'].lower()) is None:
                                only_t2 += 1
                                #with open('trump_tweet.tsv', 'a', newline='', encoding="utf-8") as f:
                                    #twriter = csv.writer(f, delimiter='\t')
                                    #twriter.writerow([js_dict['text'].lower(), post_t])
                        if re.match(r'[\s\S]*(hillary|clinton)[\s\S]*', js_dict['text'].lower()) is not None:
                            clinton2[(post_t - debate_start2).seconds] += 1
                            if re.match(r'[\s\S]*(trump|donald)[\s\S]*', js_dict['text'].lower()) is None:
                                only_c2 += 1
                                #with open('clinton_tweet.tsv', 'a', newline='', encoding="utf-8") as f:
                                    #cwriter = csv.writer(f, delimiter='\t')
                                    #cwriter.writerow([js_dict['text'].lower(), post_t])
                    else:
                        print(file + ' does not contain keyword')
                if post_t >= debate_start3 and post_t <= debate_end3:
                    ds3 = dt.datetime.strptime('Oct 19 21:03:00 2016', '%b %d %H:%M:%S %Y')
                    de3 = dt.datetime.strptime('Oct 19 22:36:00 2016', '%b %d %H:%M:%S %Y')
                    count_3rd_all += 1
                    if post_t >= ds3 and post_t < de3:
                        count_3rd_in += 1
                    #regular expression to match names
                    if re.match(r'[\s\S]*(trump|donald|hillary|clinton)[\s\S]*', js_dict['text'].lower()) is not None:
                        if post_t >= ds3 and post_t < de3:
                            count_3rd_key += 1
                        time_count3[int((post_t - debate_start3).seconds / step)] += 1
                        with open("target23.txt", 'a', encoding='utf-8') as f:
                            f.write(file + '\n')
                        if re.match(r'[\s\S]*(trump|donald)[\s\S]*', js_dict['text'].lower()) is not None:
                            trump3[(post_t - debate_start3).seconds] += 1
                            with open('trump_tweet.tsv', 'a', newline='', encoding="utf-8") as f:
                                twriter = csv.writer(f, delimiter='\t')
                                text = ' '.join(js_dict['text'].lower().split())
                                twriter.writerow([text, post_t])
                            if re.match(r'[\s\S]*(hillary|clinton)[\s\S]*', js_dict['text'].lower()) is None:
                                only_t3 += 1
                        if re.match(r'[\s\S]*(hillary|clinton)[\s\S]*', js_dict['text'].lower()) is not None:
                            clinton3[(post_t - debate_start3).seconds] += 1
                            with open('clinton_tweet.tsv', 'a', newline='', encoding="utf-8") as f:
                                cwriter = csv.writer(f, delimiter='\t')
                                text = ' '.join(js_dict['text'].lower().split())
                                cwriter.writerow([text, post_t])
                            if re.match(r'[\s\S]*(trump|donald)[\s\S]*', js_dict['text'].lower()) is None:
                                only_c3 += 1
                    else:
                        print(file + ' does not contain keyword')

    #tc = np.array(time_count)
    #t = np.array(trump)
    #c = np.array(clinton)
    #np.save("tc.npy", tc)
    #np.save("t.npy", t)
    #np.save("c.npy", c)
    print("only about trump in second debate: ", only_t2)
    print("only about clinton in second debate: ", only_c2)
    print("only about trump in third debate: ", only_t3)
    print("only about clinton in third debate: ", only_c3)
    print("30 before/after 2nd debate: ", count_2nd_all)
    print("2nd debate during: ", count_2nd_in)
    print("2nd debate with key: ", count_2nd_key)
    print("30 before/after 3rd debate: ", count_3rd_all)
    print("3rd debate during: ", count_3rd_in)
    print("3rd debate with key: ", count_3rd_key)
    return trump2, clinton2, time_count2, trump3, clinton3, time_count3

# 2nd debate plot
def plot_line2(title, lst1, lst2=None, step=1):
    # d_s = dt.datetime.strptime('Oct 19 21:05:00 2016', '%b %d %H:%M:%S %Y')
    debate_start = dt.datetime.strptime('Oct 09 20:35:00 2016', '%b %d %H:%M:%S %Y')
    debate_end = dt.datetime.strptime('Oct 09 23:05:00 2016', '%b %d %H:%M:%S %Y')
    delta = dt.timedelta(seconds=step)
    x = mpldts.drange(debate_start, debate_end, delta)
    fig = plt.figure(figsize=(60, 1))
    ax = plt.gca()
    ax.plot_date(x, lst1, "g", linewidth=1)
    plt.axvline(dt.datetime.strptime('Oct 09 21:05:00 2016', '%b %d %H:%M:%S %Y'), linestyle='dashed', c='black')
    plt.axvline(dt.datetime.strptime('Oct 09 22:35:00 2016', '%b %d %H:%M:%S %Y'), linestyle='dashed', c='black')
    plt.xlabel("time(8:35-11:05 Oct 09, 2016 edt)")
    plt.ylabel("num of tweets")
    plt.title(title)
    date_format = mpldts.DateFormatter("%H:%M:%S")
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    # plt.savefig(filename)
    plt.show()

# For the third debate plot
def plot_line(title, lst1, lst2=None, step=1):
    if lst2 is None:
        #d_s = dt.datetime.strptime('Oct 19 21:05:00 2016', '%b %d %H:%M:%S %Y')
        debate_start = dt.datetime.strptime('Oct 19 20:33:00 2016', '%b %d %H:%M:%S %Y')
        debate_end = dt.datetime.strptime('Oct 19 23:06:00 2016', '%b %d %H:%M:%S %Y')
        delta = dt.timedelta(seconds=step)
        x = mpldts.drange(debate_start, debate_end, delta)
        fig = plt.figure(figsize=(60, 1))
        ax = plt.gca()
        ax.plot_date(x, lst1, "g", linewidth=1)
        plt.axvline(dt.datetime.strptime('Oct 19 21:03:00 2016', '%b %d %H:%M:%S %Y'), linestyle='dashed', c='black')
        plt.axvline(dt.datetime.strptime('Oct 19 22:36:00 2016', '%b %d %H:%M:%S %Y'), linestyle='dashed', c='black')
        plt.xlabel("time(20:33-23:06 Oct 19, 2016 edt)")
        plt.ylabel("num of tweets")
        plt.title(title)
        date_format = mpldts.DateFormatter("%H:%M:%S")
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        #plt.savefig(filename)
        plt.show()
    else:
        debate_start = dt.datetime.strptime('Oct 19 20:33:00 2016', '%b %d %H:%M:%S %Y')
        debate_end = dt.datetime.strptime('Oct 19 23:06:00 2016', '%b %d %H:%M:%S %Y')
        delta = dt.timedelta(seconds=1)
        x = mpldts.drange(debate_start, debate_end, delta)
        fig = plt.figure(figsize=(60, 1))
        ax = plt.gca()
        ax.plot_date(x, lst1, "r", linewidth=1)
        ax.plot_date(x, lst2, "b", linewidth=1)
        plt.axvline(dt.datetime.strptime('Oct 19 21:03:00 2016', '%b %d %H:%M:%S %Y'), linestyle='dashed', c='black')
        plt.axvline(dt.datetime.strptime('Oct 19 22:36:00 2016', '%b %d %H:%M:%S %Y'), linestyle='dashed', c='black')
        plt.xlabel("time(20:33-23:06 Oct 19, 2016 edt)")
        plt.ylabel("num of tweets")
        plt.title(title)
        date_format = mpldts.DateFormatter("%H:%M:%S")
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        #plt.savefig(filename)
        plt.show()

# For revisit very quickly
def tweets(step=1):
    only_t2 = 0
    only_c2 = 0
    count_2nd_in = 0
    time_count = [0] * int(((90 + 60) * 60 / step))  # number is the second of the duration
    trump = [0] * ((90 + 60) * 60)  # number is the second of the duration
    clinton = [0] * ((90 + 60) * 60)  # number is the second of the duration
    # time in edt
    debate_start = dt.datetime.strptime('Oct 09 20:35:00 2016', '%b %d %H:%M:%S %Y')
    debate_end = dt.datetime.strptime('Oct 09 23:05:00 2016', '%b %d %H:%M:%S %Y')
    path = "D:/tweet/tweets/"
    names = set()
    with open("target23.txt", 'r') as f:
        line = f.readline().strip()
        while line:
            names.add(line)
            line = f.readline().strip()
    total = len(names)
    num = 0
    for file in names:
        num += 1
        print("progress: ", num / total)
        with open(path + '/' + file, 'r') as f:
            data = json.load(f)
            for js_dict in data:
                post_t = dt.datetime.strptime(js_dict['created_at'][4:20] + js_dict['created_at'][26:],
                                              '%b %d %H:%M:%S %Y') - dt.timedelta(hours=4)
                if post_t >= debate_start and post_t < debate_end:
                    # regular expression to match names
                    if re.match(r'[\s\S]*(trump|donald|hillary|clinton)[\s\S]*', js_dict['text'].lower()) is not None:
                        time_count[int((post_t - debate_start).seconds / step)] += 1
                        ds2 = dt.datetime.strptime('Oct 09 21:05:00 2016', '%b %d %H:%M:%S %Y')
                        de2 = dt.datetime.strptime('Oct 09 22:35:00 2016', '%b %d %H:%M:%S %Y')
                        if post_t >= ds2 and post_t <= de2:
                            count_2nd_in += 1
                        if re.match(r'[\s\S]*(trump|donald)[\s\S]*', js_dict['text'].lower()) is not None:
                            trump[(post_t - debate_start).seconds] += 1
                            with open('trump_tweet.tsv', 'a',newline='', encoding="utf-8") as f:
                                twriter = csv.writer(f, delimiter='\t')
                                text = ' '.join(js_dict['text'].lower().split())
                                twriter.writerow([text, post_t])
                            if re.match(r'[\s\S]*(hillary|clinton)[\s\S]*', js_dict['text'].lower()) is None:
                                only_t2 += 1
                        if re.match(r'[\s\S]*(hillary|clinton)[\s\S]*', js_dict['text'].lower()) is not None:
                            clinton[(post_t - debate_start).seconds] += 1
                            with open('clinton_tweet.tsv', 'a', newline='', encoding="utf-8") as f:
                                cwriter = csv.writer(f, delimiter='\t')
                                text = ' '.join(js_dict['text'].lower().split())
                                cwriter.writerow([text, post_t])
                            if re.match(r'[\s\S]*(trump|donald)[\s\S]*', js_dict['text'].lower()) is None:
                                only_c2 += 1
                    else:
                        print(file + ' does not contain keyword')

    #tc = np.array(time_count)
    #t = np.array(trump)
    #c = np.array(clinton)
    #np.save("tc.npy", tc)
    #np.save("t.npy", t)
    #np.save("c.npy", c)
    print("only about trump in second debate: ", only_t2)
    print("only about clinton in second debate: ", only_c2)
    print("2nd debate during: ", count_2nd_in)
    return trump, clinton, time_count

# draw who's giving a speech in the time-count figure
def plot_speech(speecher, time_count, step = 1, path = None):
    d_s = dt.datetime.strptime('Oct 19 21:03:00 2016', '%b %d %H:%M:%S %Y')
    debate_start = dt.datetime.strptime('Oct 19 20:33:00 2016', '%b %d %H:%M:%S %Y')
    debate_end = dt.datetime.strptime('Oct 19 23:06:00 2016', '%b %d %H:%M:%S %Y')
    delta = dt.timedelta(seconds=step)
    x = mpldts.drange(debate_start, debate_end, delta)
    fig = plt.figure(figsize=(60, 1))
    ax = plt.gca()
    ax.plot_date(x, time_count, "g", linewidth=1)
    plt.axvline(dt.datetime.strptime('Oct 19 21:03:00 2016', '%b %d %H:%M:%S %Y'), linestyle='dashed', c='black')
    plt.axvline(dt.datetime.strptime('Oct 19 22:36:00 2016', '%b %d %H:%M:%S %Y'), linestyle='dashed', c='black')
    if not path is None:
        df = pd.read_csv(path, skiprows=1)
        t = []
        c = []
        slot = []
        last_name = ""
        for i in range(len(df)):
            if len(slot) == 0:
                if df.iloc[i][0] == "Hillary Clinton" or df.iloc[i][0] == "Donald J. Trump":
                    time = d_s + (dt.datetime.strptime(df.iloc[i][2], "%H:%M:%S") - dt.datetime.strptime("00:02:20",
                                                                                                         "%H:%M:%S"))
                    time = time - dt.timedelta(seconds=(time.second % step)) + dt.timedelta(seconds=3)
                    slot.append(time)
                    last_name = df.iloc[i][0]
            elif len(slot) == 1:
                time = d_s + (dt.datetime.strptime(df.iloc[i][2], "%H:%M:%S") - dt.datetime.strptime("00:02:20",
                                                                                                     "%H:%M:%S")) - dt.timedelta(
                    seconds=1)
                if time.second % step > 0:
                    time = time - dt.timedelta(seconds=(time.second % step)) + dt.timedelta(seconds=step)+ dt.timedelta(seconds=3)
                else:
                    time = time - dt.timedelta(seconds=(time.second % step))+ dt.timedelta(seconds=3)
                slot.append(time)
                if last_name == "Hillary Clinton":
                    c.append(slot)
                    slot = []
                elif last_name == "Donald J. Trump":
                    t.append(slot)
                    slot = []
                if df.iloc[i][0] == "Hillary Clinton" or df.iloc[i][0] == "Donald J. Trump":
                    time = d_s + (dt.datetime.strptime(df.iloc[i][2], "%H:%M:%S") - dt.datetime.strptime("00:02:20",
                                                                                                         "%H:%M:%S"))
                    time = time - dt.timedelta(seconds=(time.second % step))+ dt.timedelta(seconds=3)
                    slot.append(time)
                    last_name = df.iloc[i][0]
        if speecher == "Trump":
            for i in range(len(t)):
                plt.axvspan(t[i][0], t[i][1], facecolor='#FFC0CB', alpha=1)
        elif speecher == "Clinton":
            for i in range(len(c)):
                plt.axvspan(c[i][0], c[i][1], facecolor='#AFEEEE', alpha=1)
    plt.xlabel("time(8:33-11:06 Oct 19, 2016 edt)")
    plt.ylabel("num of tweets")
    plt.title(speecher)
    date_format = mpldts.DateFormatter("%H:%M:%S")
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    plt.show()


def main():
    if not os.path.exists("target23.txt"):
        trump2, clinton2, time_count2, trump3, clinton3, time_count3 = count_tweets()
    else:
        trump2, clinton2, time_count2 = tweets(1)
    count_num2 = 0
    for i in range(len(time_count2)):
        count_num2 += time_count2[i]

    trump_num2 = 0
    for i in range(len(trump2)):
        trump_num2 += trump2[i]

    clinton_num2 = 0
    for i in range(len(clinton2)):
        clinton_num2 += clinton2[i]

    count_num3 = 0
    for i in range(len(time_count3)):
        count_num3 += time_count3[i]

    trump_num3 = 0
    for i in range(len(trump3)):
        trump_num3 += trump3[i]

    clinton_num3 = 0
    for i in range(len(clinton3)):
        clinton_num3 += clinton3[i]

    print("num of tweets about trump in 2nd debate: ", trump_num2)
    print("num of tweets about clinton in 2nd debate: ", clinton_num2)
    print("num of tweets has keyword during debate in 2nd debate: ", count_num2)

    print("num of tweets about trump in 3rd debate: ", trump_num3)
    print("num of tweets about clinton in 3rd debate: ", clinton_num3)
    print("num of tweets has keyword during debate in 3rd debate: ", count_num3)

    #plot_line('tweets about trump(red) and clinton(blue) over time', 'trumpclinton.png', trump, clinton)
    #time_count2 = [0] * (int((90 + 60) * 60))
    plot_line2('total tweets over time', time_count2, None, 1)
    plot_line2('total tweets over time', trump2, None, 1)
    plot_line2('total tweets over time', clinton2, None, 1)
    plot_line('total tweets over time', time_count3, None, 1)
    plot_line('total tweets over time', trump3, clinton3, 1)
    #plot_speech("Clinton", time_count, 10, "3rd.csv")
    #plot_speech("Trump", time_count, 10, "3rd.csv")


if __name__ == "__main__":
    main()