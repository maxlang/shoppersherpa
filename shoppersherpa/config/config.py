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

    def __init__(self, debug=False):
        self.debug = debug
        if debug:
            logger.debug("config in debug mode")
        self.loadConfig()

    def loadConfig(self):
        logger.debug("loading config")
        self.config = dict()

        # set up view directory
        self.curDir = os.path.dirname(os.path.realpath(__file__))
        logger.debug("config dir: %s", self.curDir)

        #self.configDir Name= "config"

        configmodefile = open(os.path.join(self.curDir, "configmode.txt"))
        mode = configmodefile.readline()
        configfilename = "{0}.yml".format(mode.strip())
        configFile = os.path.join(self.curDir, 'yml', configfilename)
        if os.path.isfile(configFile):
            self.configFile = configFile
            with open(configFile, 'r') as configFileHandle:
                self.config.update(yaml.load(configFileHandle))
        else:
            raise ("can't find config file: {0}".format(configFile))

    def __len__(self):
        return len(self.config)

    def __getitem__(self, key):
        logger.debug("getting config value: " + str(key))
        if self.debug:
            self.loadConfig()
        return self.config[key]

    def __iter__(self):
        return iter(self.config)

masterConfig = Config()
pass
