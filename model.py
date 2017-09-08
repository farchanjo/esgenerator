#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config


def get_model_es(cluster_name, networkIp, nodeName, httpPort,
                 transportPort, isData='true', isMaster='true'):
    output = ''
    with open(config.dir_path + '/esconfigmodel') as esModel:
        for line in esModel:
            output += line.format(clustername=cluster_name, isData=isData, nodeName=nodeName,
                                  transportPort=transportPort, httpPort=httpPort,
                                  isMaster=isMaster, networkIp=networkIp)
        esModel.close()
    return output


def get_model_log():
    output = ''
    with open(config.dir_path + '/esloggingmodel') as esLogModel:
        for line in esLogModel:
            output += line
        esLogModel.close()
    return output
