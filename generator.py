#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import config
import model

dir_path = os.path.dirname(os.path.realpath(__file__))
parser = argparse.ArgumentParser(description='Elasticsearch Config Generator')
parser.add_argument('--host', type=str, help='Set host', required=True)
parser.add_argument('--ip', type=str, help='Set ip', required=True)
parser.add_argument('--instances', type=int, help='Set Number of Instances', required=True)
parser.add_argument('--tport', type=int, help='Set Transport Port', required=True)
parser.add_argument('--hport', type=int, help='Set Http Port', required=True)
parser.add_argument('--cluster', type=str, help='Set Clusters Name', required=True)
parser.add_argument('--master', type=bool, help='Is Master', required=True)
parser.add_argument('--node', type=bool, help='Is Node Data', required=True)
parser.add_argument('--heap', type=str, help='Heap Size', required=True)
parser.add_argument('--type', type=str, help='Choose (ND|MST|QR)', required=True)
args = parser.parse_args()

if not os.path.exists(config.OUTOUT_FOLDER):
    os.mkdir(config.OUTOUT_FOLDER, 0755)

for ins in range(0, args.instances):
    # Renaming files
    es_config_folder = '{path}/elasticsearch-{ins}'.format(path=config.OUTOUT_FOLDER, ins=ins)
    node_name = '{host}-{type}.{inst}'.format(host=args.host, type=args.type, inst=ins)
    systemd_folder = '{folder}/systemd/system'.format(folder=config.OUTOUT_FOLDER)
    default_folder = '{folder}/default'.format(folder=config.OUTOUT_FOLDER)
    systemd_file = 'elasticsearch-{type}-{inst}'.format(type=args.type, inst=ins)
    # Choosing default file
    if args.type == 'ND':
        default_file = 'elasticsearch-node'
    elif args.type == 'QR':
        default_file = 'elasticsearch-query'
    elif args.type == 'MST':
        default_file = 'elasticsearch-master'
    else:
        default_file = 'elasticsearch'

    # Creating output Folder
    if not os.path.exists(es_config_folder):
        os.mkdir(es_config_folder, 0755)
        config.logger.debug('{folder} created'.format(folder=es_config_folder))

    # Getting model.
    esModel = model.get_model_es(args.cluster, args.ip, node_name, args.hport + ins,
                                 args.tport + ins, str(args.node).lower(), str(args.master).lower())

    # Create Main file
    with open(es_config_folder + '/elasticsearch.yml', 'w') as f:
        f.write(esModel)
        f.close()

    # Creating logging file
    with open(es_config_folder + '/logging.yml', 'w') as f:
        f.write(model.get_model_log())
        f.close()

    if os.path.exists(systemd_folder):
        with open('{folder}/{file}.service'.format(folder=systemd_folder, file=systemd_file), 'w') as f:
            f.write(model.get_model_systemd(ins, default_file))
            f.close()
        config.logger.info('{folder}/{file}'.format(folder=systemd_folder, file=systemd_file))

    if os.path.exists(default_folder):
        with open('{default_folder}/{default_file}'.format(default_folder=default_folder,
                                                           default_file=default_file), 'w') as f:
            f.write(model.get_model_default(args.heap))
            f.close()
        config.logger.info('{default_folder}/{default_file}'.format(default_folder=default_folder,
                                                                    default_file=default_file))
    config.logger.info('Files for {folder} created without erros'.format(folder=es_config_folder))
