import sys
import os
import re
import utils
from collections import defaultdict
from datetime import datetime

DAY_REGEXP = r"^#\ (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\,\ (November)\ \d{1,2}\, \d{4}"
SESSION_REGEXP = r"^=Session"
PAPER_REGEXP = r"^\d{1,4}\ \d{2}\:\d{2}--\d{2}\:\d{2}\ \#\ "
TACL_PAPER_REGEXP = r"^\d{1,4}/TACL\ \d{2}\:\d{2}--\d{2}\:\d{2}\ \#\ "
POSTER_REGEXP = r"^\d{1,4}\ \# "
OTHER_REGEXP = r"^\+\ \d{2}\:\d{2}--\d{2}\:\d{2}"


pattern_day = re.compile(DAY_REGEXP)
pattern_session = re.compile(SESSION_REGEXP)
pattern_paper = re.compile(PAPER_REGEXP)
pattern_tacl_paper = re.compile(TACL_PAPER_REGEXP)
pattern_poster = re.compile(POSTER_REGEXP)
pattern_other = re.compile(OTHER_REGEXP)


dates = []
schedule = defaultdict(list)
sessions = defaultdict(list)


def get_time_range(str_):
    r = re.compile(r"\d{2}\:\d{2}--\d{2}\:\d{2}\ ")
    return re.search(r, str_).group().strip()


parent_session = None
current_session = None


def parse_order_file(orderfile):
    with open(orderfile, 'r') as in_:
        for line in in_:
            if line == '\n':
                continue

            if re.match(pattern_day, line):
                cleaned = line.replace('#', '').strip()
                # day, date, year = cleaned.split(',')
                dobj = datetime.strptime(cleaned, '%A, %B %d, %Y')#.date()
                if dobj not in dates:
                    dates.append(dobj)
                schedule[dobj] = []

            elif re.match(pattern_session, line):  # parallel session
                cleaned = line.replace('=Session ', '')
                code, name = cleaned.split(':')
                par_session = utils.ParallelSession(code, name)
                parent_session.add_parallel_session(par_session)
                current_session = par_session

            elif re.match(pattern_paper, line):   # paper
                id_time_str, title = line.strip().split(" # ")
                paper_id, time_range = id_time_str.split()
                paper_id = int(paper_id)
                time_range = time_range.strip()
                paper = utils.Paper(title, paper_id, code, time_range)
                current_session.add_paper(paper)

            elif re.match(pattern_tacl_paper, line):   # paper
                id_time_str, title = line.strip().split(" # ")
                paper_id, time_range = id_time_str.split()
                paper_id = int(paper_id.replace('/TACL', ''))
                time_range = time_range.strip()
                paper = utils.Paper(title, paper_id, code, time_range)
                current_session.add_paper(paper)

            elif re.match(pattern_poster, line):  # poster
                paper_id, title = line.strip().split(" # ")
                paper_id = int(paper_id)
                paper = utils.Poster(title, paper_id, code)
                current_session.add_poster(paper)

            elif re.match(pattern_other, line):  # session and others
                cleaned = line.replace('+ ', '')
                time_range = get_time_range(cleaned)
                title = cleaned.split(time_range)[1].strip()
                if re.search('poster', title.lower()) or re.search('demo', title.lower()):
                    session_code,  session_title = title.strip('Poster & Demo Session ').split(':')
                    s = utils.PosterSession(session_title, time_range)
                    current_session = s
                    parent_session.add_poster_session(s)
                elif re.search('Session', title):
                    session_code, session_title = int(title.split()[1]), 'Session'
                    s = utils.Session(session_code, session_title, time_range)
                    parent_session = s
                else:
                    s = title
                schedule[dobj].append((time_range, s))
            else:
                pass
                #print('NOT FOUND')
                #print(line)
    return schedule


def process_time_range(tr):
    st, end = tr.split('--')
    return "{} & -- & {} ".format(st, end)


def build_overview(schedule, outdir, conf):
    for date, sched in sorted(schedule.items()):
        with open('{}/{}-overview.tex'.format(os.path.join(outdir, conf), date.strftime("%A")), 'w') as out:
            out.write('\\section*{Overview}\n')
            out.write('\\renewcommand{\\arraystretch}{1.2}\n')
            out.write('\\begin{SingleTrackSchedule}\n')
            for time_range, event in sched:
                if isinstance(event, str):
                    out.write("{} & \\bfseries{{ {} }} \\\\".format(process_time_range(time_range), event))
                elif isinstance(event, utils.Session):
                    if event.parallels:
                        out.write("{}".format(process_time_range(time_range)))
                        out.write(" & \\begin{tabular}{|p{0.9in}|p{0.9in}|p{0.9in}|p{0.9in}|} \n")
                        out.write("\multicolumn{{4}}{{l}}{{\\bfseries {}}}\\\\ \n \\hline ".format(event))
                        out.write(' & '.join([p.get_desc() for p in event.parallels]) + '\\\\')
                        out.write(' & '.join(['\emph{LOCATION}' for _ in event.parallels]) + '\\\\')
                        out.write('  \\hline\\end{tabular} \\\\')
                    else:
                        out.write("{} & \\bfseries{{ {} }} \\\\".format(process_time_range(time_range), event))
            out.write('\\end{SingleTrackSchedule}')
            out.write('\\clearpage')

        print('Done: {}/{}-overview.tex'.format(os.path.join(outdir, conf), date.strftime("%A")))


def build_session_overview(schedule, outdir, conf):
    for date, sched in sorted(schedule.items()):
        for time_range, event in sched:
            # print(time_range, event)
            paper_times = {}
            times = defaultdict(list)
            if isinstance(event, utils.Session):
                parallel_sessions = event.parallels
                poster_session = event.poster_session

                with open('{}/{}-parallel-session-{}.tex'.format(os.path.join(outdir, conf), date.strftime("%A"), event.code), 'w') as out:
                    out.write('\\clearpage\n')
                    out.write('\\setheaders{{Session {} }}{{\\daydateyear}}\n'.format(event.code))
                    out.write('\\begin{{FourSessionOverview}}{{Session {}}}{{\daydateyear}}\n'.format(event.code))
                    for ps in parallel_sessions:
                        out.write('{{{}}}\n'.format(ps.name))

                        for paper in ps.papers:
                            paper_times[paper.id_] = paper.get_start_time()
                            times[paper.get_start_time()].append(paper.id_)

                    fl = False
                    for time, list_ in sorted(times.items()):
                        if fl:
                            out.write('\\midrule\n')
                        out.write(' \\marginnote{{\\rotatebox{{90}}{{ {} }}[2mm]\n'.format(time))
                        out.write(' & '.join(['\\papertableentry{{{}-{}}} '.format(conf, id_) for id_ in list_]))
                        out.write('\\\\\n')
                        fl = True
                    out.write('\\end{FourSessionOverview}\n')

                    out.write("{{\\large {{\\bf Poster tracks}} \\hfill {{{}}} \\\\ \\\\ \n".format(poster_session.time_range))
                    out.write("\\vspace{0.3em} \n")
                    out.write("{{\\bf Track E}}: {{\\it {} }} \\hfill \\TrackELoc \n".format(poster_session.name))

                    out.write('\\newpage\n')
                    out.write('\\section*{{Parallel Session {}}}\n'.format(event.code))

                # for pn in range(num_papers):
                #     if pn > 0:
                #         out.write(' \\midrule')
                #     out.write('  \\marginnote{{\\rotatebox{{90}}{{}}[2mm]'.format(paper_times[pn]))

        # print('{}/{}-parallel-session-{}.tex'.format(os.path.join(outdir, conf), date.strftime("%A")))
        pass


if __name__ == "__main__":
    conf = sys.argv[1]
    if not os.path.exists('data/{}'.format(conf)):
        exit('No such conf like {}'.format(conf))
    schedule = parse_order_file('data/{}/proceedings/order'.format(conf))
    # build_overview(schedule, 'auto', conf)
    build_session_overview(schedule, 'auto', conf)
    # for time_range_a, event_list in sorted(schedule.items()):
    #     print(time_range_a, type(event_list))
    #     for time_range, event in event_list:
    #         if isinstance(event, utils.Session):
    #             print('Session', event.code)
    #             if event.parallels:
    #                 for p in event.parallels:
    #                     print(p.code, p.papers)
    #             if event.poster_session:
    #                 print("{}E".format(event.code), event.poster_session.posters)

        #             for pp in p.papers:
        #                 print(pp)
        #     else:  # poster
        #         for p in event.papers:
        #             print(p)