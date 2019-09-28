import sys
import os
import re
import utils
from collections import defaultdict

DAY_REGEXP = r"^#\ (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\,\ (November)\ \d{1,2}\, \d{4}"
SESSION_REGEXP = r"^=Session"
PAPER_REGEXP = r"^\d{1,4}\ \d{2}\:\d{2}--\d{2}\:\d{2}\ \#\ "
POSTER_REGEXP = r"^\d{1,4}\ \# "
OTHER_REGEXP = r"^\+\ \d{2}\:\d{2}--\d{2}\:\d{2}"


pattern_day = re.compile(DAY_REGEXP)
pattern_session = re.compile(SESSION_REGEXP)
pattern_paper = re.compile(PAPER_REGEXP)
pattern_poster = re.compile(POSTER_REGEXP)
pattern_other = re.compile(OTHER_REGEXP)


dates = []
schedule = defaultdict(defaultdict)
sessions = {}
session_times = {}


def get_time_range(str_):
    r = re.compile(r"\d{2}\:\d{2}--\d{2}\:\d{2}\ ")
    return re.search(r, str_).group().strip()


def parse_order_file(orderfile):
    with open(orderfile, 'r') as in_:
        for line in in_:
            if line == '\n':
                continue
            if re.match(pattern_day, line):
                cleaned = line.replace('#', '').strip()
                day, date, year = cleaned.split(',')
                if (day, date, year) not in dates:
                    dates.append((day, date, year))
                schedule[day] = {'date': ','.join([day, date, year])}
            elif re.match(pattern_session, line):
                print(schedule)
                cleaned = line.replace('=Session ', '')
                code, name = cleaned.split(':')
                session_number = int(code[:-1])
                if re.search('poster', name.lower()):
                    is_poster = True
                exit()
            elif re.match(pattern_paper, line):
                print('PAPER', line)
            elif re.match(pattern_poster, line):
                print('POSTER', line)
            elif re.match(pattern_other, line):
                cleaned = line.replace('+ ', '')
                time_range = get_time_range(cleaned)
                title = cleaned.split(time_range)[1].strip()
                schedule[day].update({time_range: title})
            else:
                print('NOT FOUND')
                print(line)
            # exit()


if __name__ == "__main__":
    conf = sys.argv[1]
    if not os.path.exists('data/{}'.format(conf)):
        exit('No such conf like {}'.format(conf))
    parse_order_file('data/{}/proceedings/order'.format(conf))
