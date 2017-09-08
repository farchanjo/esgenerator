#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger("Generator")
dir_path = os.path.dirname(os.path.realpath(__file__))

# Setting Variables
OUTOUT_FOLDER = '/Users/fabricio/1/es'
