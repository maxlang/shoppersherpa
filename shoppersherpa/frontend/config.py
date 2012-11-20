# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 02:27:49 2012

@author: Max Lang
"""
from shoppersherpa import logging
import os
import yaml
import collections

logger = logging.getLogger(__name__)


#TODO: we should move config to be project wide, rather than just for frontend
class Config(collections.Mapping):
    def __init__(self):
        self.config = dict()

        # set up view directory
        curDir = os.path.dirname(os.path.realpath(__file__))
        logger.debug("frontend dir: %s", curDir)

        configDirName = "config"

        configDir = os.path.join(curDir, configDirName)
        for f in os.listdir(configDir):
            configFile = os.path.join(configDir,f)
            if os.path.isfile(configFile):
                self.config.update(yaml.load(file(configFile,'r')))

        # setup like this should probably be moved out
        # we can change config to a MutableMapping and set computed config
        # values on a global instance
        # that said, some config will have to be per request - eg for flighting
        self['viewDir'] = os.path.join(curDir, self['viewDirName'])
        logger.debug("view dir: %s", self['viewDir'])

        self['staticDir'] = os.path.join(curDir, self['staticDirName'])
        logger.debug("static dir: %s", self['staticDir'])

    def __len__(self):
        return len(self.config)

    def __getitem__(self, key):
        return self.config[key]

    def __iter__(self):
        return iter(self.config)

# global config
config = Config()