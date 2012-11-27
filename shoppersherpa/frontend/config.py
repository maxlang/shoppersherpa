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
# TODO: add functions so dict items can be accessed like attributes (nicer)
# see bottle.config and bottle's configdict
class Config(collections.Mapping):
    def __init__(self,debug=False):
        self.debug=debug
        if debug:
            logger.debug("config in debug mode")
        self.loadConfig()

    def loadConfig(self):
        logger.debug("loading config")
        self.config = dict()

        # set up view directory
        self.curDir = os.path.dirname(os.path.realpath(__file__))
        logger.debug("frontend dir: %s", self.curDir)

        self.configDirName = "config"

        self.configDir = os.path.join(self.curDir, self.configDirName)
        self.configFiles = []
        for f in os.listdir(self.configDir):
            configFile = os.path.join(self.configDir, f)
            if os.path.isfile(configFile):
                self.configFiles.append(configFile)
                with open(configFile, 'r') as configFileHandle:
                    self.config.update(yaml.load(configFileHandle))

        # setup like this should probably be moved out
        # we can change config to a MutableMapping and set computed config
        # values on a global instance
        # that said, some config will have to be per request - eg for flighting
        self.config['viewDir'] = os.path.join(self.curDir, self.config['viewDirName'])
        logger.debug("view dir: %s", self.config['viewDir'])

        self.config['staticDir'] = os.path.join(self.curDir, self.config['staticDirName'])
        logger.debug("static dir: %s", self.config['staticDir'])

    def __len__(self):
        return len(self.config)

    def __getitem__(self, key):
        logger.debug("getting config value: " + str(key))
        if self.debug:
            self.loadConfig()
        return self.config[key]

    def __iter__(self):
        return iter(self.config)
