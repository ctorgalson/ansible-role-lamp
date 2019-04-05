import os

import testinfra.utils.ansible_runner

import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


""" Verify Apache packages are present. """


@pytest.mark.parametrize('package', [
    'expires_module',
    'headers_module',
    'rewrite_module',
])
def test_apache_packages(host, package):
    p = host.run('apache2ctl -M')

    assert package in p.stdout


""" Verify MySQL users and databses. """


@pytest.mark.parametrize('user,password,command,output', [
    (
      'root',
      'lamp_root_password',
      'SELECT USER()',
      'root@localhost'
    ),
    (
      'root',
      'lamp_root_password',
      'SELECT * FROM mysql.user',
      'lamp_user'
    ),
    (
      'lamp_user',
      'lamp_user_password',
      'SHOW DATABASES',
      'lamp_db'
    ),
])
def test_mysql_root_login(host, user, password, command, output):
    m = host.run(
      'mysql -u {u} -p{p} -e "{e}"'.format(
        u=user,
        p=password,
        e=command
      )
    )

    assert output in m.stdout


""" Verify PHP version. """


def test_php_version(host):
    v = host.run('php --version')

    assert 'PHP 7.0' in v.stdout


""" Verify PHP packages are present. """


@pytest.mark.parametrize('package', [
    'Core',
    'curl',
    'gd',
    'imap',
    'json',
    'mbstring',
    'mysql',
    'pcre',
    'PDO',
    'pdo_mysql',
    'xml',
    'zip',
])
def test_php_packages(host, package):
    p = host.run('php -m')

    assert package in p.stdout


""" Verify services are running. """


@pytest.mark.parametrize('service,status', [
    ('apache2', 'apache2 is running'),
    ('mysql', '/usr/bin/mysqladmin'),
])
def test_running_services(host, service, status):
    s = host.run('service {} status'.format(service))

    assert status in s.stdout


""" Verify PHP files are served correctly by Apache. """


def test_php_and_apache(host):
    c = host.run('curl lamp:80')

    assert 'PHP 7.0' in c.stdout
    assert 'lamp_db' in c.stdout
    assert 'ERROR' not in c.stdout
