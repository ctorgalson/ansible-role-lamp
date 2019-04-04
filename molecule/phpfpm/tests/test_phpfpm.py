import os

import testinfra.utils.ansible_runner

import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


""" Verify services are running. """


@pytest.mark.parametrize('service,status', [
    ('apache2', 'apache2 is running'),
    ('php7.2-fpm', 'php-fpm7.2 is running'),
    ('mysql', '/usr/bin/mysqladmin'),
])
def test_running_services(host, service, status):
    s = host.run('service {} status'.format(service))

    assert status in s.stdout


""" Verify PHP files are served correctly by Apache. """


def test_php_and_apache(host):
    c = host.run('curl 127.0.0.1:80')

    assert 'PHP 7.2' in c.stdout
    assert 'lamp_db' in c.stdout
    assert 'ERROR' not in c.stdout
