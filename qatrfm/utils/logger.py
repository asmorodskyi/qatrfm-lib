#!/usr/bin/env python3
#
# Copyright © 2019 SUSE LLC
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.


""" QaTrfm custom Logger Class

It defines a specific format of the log messages.
If LOG_COLORS=1 is exported, it will print the messages in different colors
according to it's level.
"""

import logging
import os


class QaTrfmLogger(logging.Logger):

    def __init__(self, logger_name, level="DEBUG"):
        """Initialize QaTrfmLogger Class"""
        self.colors = False
        if ('LOG_COLORS' in os.environ):
            self.colors = True
            format = "\033[37;48mqatrfm.%(levelname)s: \033[0m%(message)s"
        else:
            self.colors = False
            format = "qatrfm.%(levelname)s: %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=format)
        return super(QaTrfmLogger, self).__init__(logger_name, level)

    def info(self, msg, *args, **kwargs):
        if (self.colors):
            msg = ("\033[1;34m {}\033[0m".format(msg))
        else:
            msg = (" {}".format(msg))
        super(QaTrfmLogger, self).info(msg, *args, **kwargs)

    def success(self, msg, *args, **kwargs):
        if (self.colors):
            msg = ("\033[1;32m {}\033[0m".format(msg))
        else:
            msg = (" {}".format(msg))
        super(QaTrfmLogger, self).info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if (self.colors):
            msg = ("\033[1;31m{}\033[0m".format(msg))
        super(QaTrfmLogger, self).error(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if (self.colors):
            msg = ("\033[1;33m{}\033[0m".format(msg))
        super(QaTrfmLogger, self).warning(msg, *args, **kwargs)

    @staticmethod
    def getQatrfmLogger(name):
        return logging.getLogger(name)


logging.setLoggerClass(QaTrfmLogger)
logging.getLogger("paramiko.transport").setLevel(logging.WARNING)
logging.getLogger("paramiko.transport.sftp").setLevel(logging.WARNING)
