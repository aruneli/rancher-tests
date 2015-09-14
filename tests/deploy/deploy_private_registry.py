import argparse
import logging
import os
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
from digitalocean import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='target version')
    parser.add_argument('-n', help='count of nodes')
    parser.add_argument('-apitoken', help='digital ocean api token')
    args = parser.parse_args()
    logger.info(args)
    deploy_private_registry(args.t, args.n, args.apitoken)


def deploy_private_registry(server_version, num_no_nodes, token):
    delete_ssh_keys(token)
    # sshKey = open(os.path.expanduser('~/.ssh/id_rsa.pub')).read()
    # print sshKey
    # rancher_server_droplet = Droplet(token=token,
    #                                               name='RancherServerTest',
    #                                               region='nyc2',  # New York 2
    #                                               image='ubuntu-14-04-x64',  # Ubuntu 14.04 x64
    #                                               size_slug='512mb',  # 512MB
    #                                               backups=True, private_networking=True,
    #                                               ssh_keys=[sshKey])
    #
    # rancher_host1_droplet = Droplet(token=token,
    #                                              name='RancherHost1Test',
    #                                              region='nyc2',  # New York 2
    #                                              image='ubuntu-14-04-x64',  # Ubuntu 14.04 x64
    #                                              size_slug='512mb',  # 512MB
    #                                              backups=True, private_networking=True,
    #                                              ssh_keys=[sshKey])
    #
    # rancher_host2_droplet = Droplet(token=token,
    #                                              name='RancherHost2Test',
    #                                              region='nyc2',  # New York 2
    #                                              image='ubuntu-14-04-x64',  # Ubuntu 14.04 x64
    #                                              size_slug='512mb',  # 512MB
    #                                              backups=True, private_networking=True,
    #                                              ssh_keys = [sshKey])
    #
    # droplets = [rancher_server_droplet, rancher_host1_droplet, rancher_host2_droplet]
    #
    # for droplet in droplets:
    #     droplet.create()


def shutdown_droplets(token):
    manager = Manager(token=token)
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        droplet.shutdown()


def delete_ssh_keys(token):
    SSHKey.destroy()


def delete_droplets(token):
    manager = Manager(token=token)
    my_droplets = manager.get_all_droplets()
    for droplet in my_droplets:
        droplet.destroy()


def status_droplets(droplet):
    actions = droplet.get_actions()
    for action in actions:
        action.load()
    # Once it shows complete, droplet is up and running
    print action.status


if __name__ == '__main__':
    main()
