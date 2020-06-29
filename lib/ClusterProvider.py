import common
import os
from robot.api import logger

ROBOT_LIBRARY_SCOPE = 'SUITE'
AUTH_COMMAND = ''

def auth_wrap(cmd):
    return AUTH_COMMAND+' && '+cmd

class ClusterProvider(common.CommandRunner):
    def __init__(self):
        self.provider = os.getenv("CLUSTER_PROVIDER", default='kind')
        self.cluster_name = 'helm-acceptance-test-' + os.getenv("CLUSTER_VERSION")

    def create_test_cluster_with_kubernetes_version(self, kube_version):
        global AUTH_COMMAND
        self.call_cluster_provisioner_function('setup_cluster', self.cluster_name)
        AUTH_COMMAND = self.call_cluster_provisioner_function('get_cluster_auth', kube_version)

    def wait_for_cluster(self):
        return self.call_cluster_provisioner_function('wait_for_cluster')

    def delete_test_cluster(self):
        return self.call_cluster_provisioner_function('delete_cluster')

    def cleanup_all_test_clusters(self):
        return self.call_cluster_provisioner_function('cleanup_all_test_clusters')

    def get_cluster_auth(self):
        return self.call_cluster_provisioner_function('get_cluster_auth')

    def call_cluster_provisioner_function(self, func, args=''):
        c = f'{self.provider}_{func} {self.cluster_name} {args}'
        self.run_command(c)
        return self.stdout
