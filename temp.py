import os
import logging
import tempfile


logger = logging.getLogger(__name__)


class TemporaryDirectory(object):
    def __init__(self):
        self.dir = tempfile.mkdtemp()
        logger.info('created directory ' + self.dir)

    def __enter__(self):
        return self.dir

    def __exit__(self, *args, **kwargs):
        logger.info('removing directory ' + self.dir)
        os.rmdir(self.dir)
        logger.info('removed directory ' + self.dir)


def get_temp_file_name():
    return tempfile._get_candidate_names().__next__()


class TemporaryFile(object):
    def __init__(self, temp_dir, extension):
        self.file = os.path.join(temp_dir, '%s.%s' % (get_temp_file_name(), extension))
        logger.info('created file ' + self.file)

    def __enter__(self):
        return self.file

    def __exit__(self, *args, **kwargs):
        logger.info('removing file ' + self.file)
        os.remove(self.file)
        logger.info('removed file ' + self.file)


class StandaloneTemporaryFile(object):
    def __init__(self, extension):
        self.dir = TemporaryDirectory()
        self.file = TemporaryFile(self.dir.__enter__(), extension)

    def __enter__(self):
        return self.file.__enter__()

    def __exit__(self, *args, **kwargs):
        # ディレクトリを空にしてから削除する必要がある
        self.file.__exit__(*args, **kwargs)
        self.dir.__exit__(*args, **kwargs)
