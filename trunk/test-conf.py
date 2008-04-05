# Generates the default configuration file

import sys
sys.path.append('lib')
import config

c = config.Config()
c.save_settings()
