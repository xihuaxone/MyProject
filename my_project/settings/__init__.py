import os
from common.config_parser import FileConfig

path = os.path.dirname(os.path.abspath(__file__))
global_config = FileConfig(os.path.join(path, 'global_config.cnf'))
