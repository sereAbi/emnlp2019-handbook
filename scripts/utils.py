import re


class Session:

    def __init__(self, code, name, time_range):
        self.code = code
        self.name = name.strip()
        self.timerange = time_range
        self.parallels = []
        self.poster_session = None

    def add_parallel_session(self, parallelsession):
        self.parallels.append(parallelsession)

    def add_poster_session(self, postersession):
        self.poster_session = postersession

    def __str__(self):
        return "Session {}".format(self.code)


class ParallelSession:

    def __init__(self, code, name):
        self.code = code
        self.name = name.strip()
        self.parent = None
        self.chair = None
        self.papers = []
        self.get_parent()


    def get_parent(self):
        if re.search('[A-Z]{1}$', self.code):
            self.parent = self.code[:-1]

    def add_paper(self, paper):
        self.papers.append(paper)

    def __str__(self):
        return "Session {}: {}".format(self.code, self.name)

    def get_desc(self):
        return self.name


class PosterSession:
    def __init__(self, name, time_range):
        self.name = name
        self.posters = []
        self.time_range = time_range

    def add_poster(self, poster):
        self.posters.append(poster)


class Paper:
    def __init__(self, title, id_, sessioncode, time_range):
        self.title = title
        self.id_ = id_
        self.sessioncode = sessioncode
        self.time_range = time_range

    def __str__(self):
        return "{} {} {}".format(self.time_range, self.id_, self.title)

    def get_start_time(self):
        return self.time_range.split('--')[0]


class Poster:

    def __init__(self, title, id_, sessioncode):
        self.title = title
        self.id_ = id_
        self.sessioncode = sessioncode

    def __str__(self):
        return "{} {}".format(self.id_, self.title)