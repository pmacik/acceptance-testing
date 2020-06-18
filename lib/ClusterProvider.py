import common
import subprocess
import os
from robot.api import logger

ROBOT_LIBRARY_SCOPE = 'SUITE'
AUTH_COMMAND = ''


def auth_wrap(cmd):
    return AUTH_COMMAND+' && '+cmd


def setup_cluster():
    return SetupCluster()


class SetupCluster():
    def __init__(self):
        self.provider = os.getenv("CLUSTER_PROVIDER", default='kind')
        self.base_cmd = 'bash -c'
        self.cluster_name = 'helm-acceptance-test-' + \
            os.getenv("CLUSTER_VERSION")

    def setup_cluster(self):
        global AUTH_COMMAND
        self.call_cluster_provisioner_script(f'{self.provider}_create_cluster')
        AUTH_COMMAND = self.call_cluster_provisioner_script(
            f'{self.provider}_get_cluster_auth')

    def delete_cluster(self):
        return self.call_cluster_provisioner_script(f'{self.provider}_delete_cluster')

    def get_cluster_auth(self):
        return self.call_cluster_provisioner_script(
            f'{self.provider}_get_cluster_auth')

    def call_cluster_provisioner_script(self, cmd, detach=False):
        c = f'{cmd} {self.cluster_name}'
        process = subprocess.Popen(['/bin/bash', '-c', c],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        if not detach:
            stdout = process.communicate()[0].strip().decode()
            self.rc = process.returncode
            tmp = []
            for x in stdout.split('\n'):
                logger.debug(x)
                if not x.startswith('+ '):  # Remove debug lines that start with "+ "
                    tmp.append(x)
            self.stdout = '\n'.join(tmp)
        return self.stdout
