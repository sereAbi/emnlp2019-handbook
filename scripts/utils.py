import re


class Session:

    def __init__(self, code, name, time_range, is_poster):
        self.code = code
        self.name = name.strip()
        self.timerange = time_range
        self.is_poster = is_poster
        self.papers = []
        self.parallels = []

    def add_poster(self, poster):
        self.papers.append(poster)

    def add_parallel(self, parallelsession):
        self.parallels.append(parallelsession)

    def __str__(self):
        if self.is_poster:
            return "Poster & Demo session {}: {}".format(self.code, self.name)
        else:
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

class Paper:
    def __init__(self, title, id_, sessioncode, time_range):
        self.title = title
        self.id_ = id_
        self.sessioncode = sessioncode
        self.time_range = time_range

    def __str__(self):
        return "{} {} {}".format(self.time_range, self.id_, self.title)


class Poster:

    def __init__(self, title, id_, sessioncode):
        self.title = title
        self.id_ = id_
        self.sessioncode = sessioncode

    def __str__(self):
        return "{} {}".format(self.id_, self.title)