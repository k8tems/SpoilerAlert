import os
import tempfile


class TemporaryDirectory(object):
    def __init__(self):
        self.dir = tempfile.mkdtemp()

    def __enter__(self):
        return self.dir

    def __exit__(self, *args, **kwargs):
        os.rmdir(self.dir)


def get_temp_file_name():
    return tempfile._get_candidate_names().__next__()


class TemporaryFile(object):
    def __init__(self, temp_dir, extension):
        self.file = os.path.join(temp_dir, '%s.%s' % (get_temp_file_name(), extension))

    def __enter__(self):
        return self.file

    def __exit__(self, *args, **kwargs):
        os.remove(self.file)


class StandaloneTemporaryFile(object):
    def __init__(self, extension):
        self.dir = TemporaryDirectory()
        self.file = TemporaryFile(self.dir.__enter__(), extension)

    def __enter__(self):
        return self.file.__enter__()

    def __exit__(self, *args, **kwargs):
        self.file.__exit__(*args, **kwargs)
        self.dir.__exit__(*args, **kwargs)
