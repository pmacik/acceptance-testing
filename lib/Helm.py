import os
import common
from ClusterProvider import auth_wrap

TEST_CHARTS_ROOT_DIR = os.path.abspath(os.path.dirname(
    os.path.realpath(__file__)) + '/../testdata/charts')


class Helm(common.CommandRunner):
    def get_chart_path(self, test_chart):
        provider = os.getenv("CLUSTER_PROVIDER", default='')
        if provider == '':
            return test_chart
        return f'{TEST_CHARTS_ROOT_DIR}/{provider}-{test_chart}'

    def install_test_chart(self, release_name, test_chart, extra_args):
        cmd = 'helm install '+release_name+' ' + \
            self.get_chart_path(test_chart) + ' '+extra_args
        self.run_command(auth_wrap(cmd))
