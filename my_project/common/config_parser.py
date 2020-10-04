from configparser import ConfigParser


class FileConfig(ConfigParser):
    def __init__(self, file_path, *args, **kwargs):
        super(FileConfig, self).__init__(*args, **kwargs)
        self.read(file_path)

    @property
    def get_config(self):
        _config = {}
        for sec in self.sections():
            _config[sec] = self.section(sec)

        return _config

    def get_section(self, section):
        return {k: v for k, v in self.items(section)}
