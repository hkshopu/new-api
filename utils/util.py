

def strtobool(s):
    return s.lower() in ['true', '1', 't', 'y', 'yes', 'on']

class ErrorWithArgs(Exception):
    def __init__(self, *args):
        self.args = [a for a in args]