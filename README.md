# Ansible Role LAMP

[![Build Status](https://travis-ci.org/ctorgalson/ansible-role-lamp.svg?branch=master)](https://travis-ci.org/ctorgalson/ansible-role-lamp)

This role sets up the AMP part of a LAMP stack using geerlingguy.* roles.

The role does not provide any defaults, tasks, or vars. All roles are
included as dependencies in `meta/main.yml`. The reason for this is
Ansible's odd variable inheritance with included roles. In this kind of
setup:

- variables from `defaults/main.yml` are never seen by the dependent roles,
- variables from `vars/main.yml` are not easily overriden from the
  parent role or playbooks that call it.

But with this setup, it is possible to provide variables:

- from the calling playbook (see `molecule/default/playbook.yml`),
- using group variables (see `molecule/default/group_vars/`).

This means that for LAMP setups where the set and order of roles defined
in `dependencies` (in `meta/main.yml`) is acceptable, this role provides
a way to quickly setup the AMP part of the stack on an Ubuntu server
(tested on Xenial, but should work elsewhere).

## Requirements

This role has no special requirements.

## Role Variables

This role provides no variables of its own.

## Dependencies

This role includes several Galaxy roles as dependencies. For details on how
to configure them, see each role's specific documentation:

- [weareinteractive.apt](https://galaxy.ansible.com/weareinteractive/apt)
- [geerlingguy.mysql](https://galaxy.ansible.com/geerlingguy/mysql)
- [geerlingguy.apache](https://galaxy.ansible.com/geerlingguy/apache)
- [geerlingguy.php](https://galaxy.ansible.com/geerlingguy/php)
- [geerlingguy.apache-php-fpm](https://galaxy.ansible.com/geerlingguy/apachei-php-fpm)

## Example Playbook

### Notes

1. Many of the variables shown here could be stored in `group_vars/`
   and/or `host_vars/`--especially when provisioning multiple
   servers! (see `molecule/default` for a working example)--and are
   only included to provide an all-in-one-place look at what's needed
   to use the role in a playbook.

   If the variables were stored elsewhere, this playbook could be as
   simple as:

   ```
   - hosts: all
     roles:
       - role: ansible-role-lamp
   ```
2. This playbook _only_ handles setting up Apache, MySql and PHP.
   Other server configuration tasks such as security setup and
   even creating the vhost directory need to be handled by other tasks
   or roles in your playbooks.

3. Though `geerlingguy.apache-php-fpm` is listed as a dependency, it
   relies on variables in `geerlingguy.php` to be configured and
   enabled. This means it's possible to configure a server to run
   php-cgi (i.e. and _not_ php-fpm) with this role.

### Example

    - hosts: all
      vars:
        # geerlingguy.apache vars.
        apache_remove_default_vhost: true
        apache_mods_enabled:
          - "expires.load"
          - "headers.load"
          - "rewrite.load"
        apache_vhosts:
          - servername: "lamp"
            documentroot: "/var/www/lamp/web"

        # geerlingguy.mysql vars.
        mysql_packages:
          - "mariadb-client"
          - "mariadb-server"
          - "python-mysqldb"
        mysql_root_password: "lamp_root_password"
        mysql_databases:
          - name: "lamp_db"
            encoding: "utf8"
            collation: "utf8_general_ci"
        mysql_users:
          - name: "lamp_user"
            host: "localhost"
            password: "lamp_user_password"
            priv: "lamp_db.*:ALL

        # geerlingguy.php vars.
        php_default_version_debian: "7.2"
        php_install_recommends: "no"
        php_date_timezone: "UTC"
        php_post_max_size: "64M"
        php_error_reporting: "E_ALL & ~E_DEPRECATED & ~E_STRICT"
        php_display_errors: "Off"
        php_display_startup_errors: "On"
        php_packages:
          - "libpcre3-dev"
          - "php{{ php_default_version_debian }}-cli"
          - "php{{ php_default_version_debian }}-common"
          - "php{{ php_default_version_debian }}-curl"
          - "php{{ php_default_version_debian }}-dev"
          - "php{{ php_default_version_debian }}-gd"
          - "php{{ php_default_version_debian }}-imap"
          - "php{{ php_default_version_debian }}-json"
          - "php{{ php_default_version_debian }}-mbstring"
          - "php{{ php_default_version_debian }}-mysql"
          - "php{{ php_default_version_debian }}-opcache"
          - "php{{ php_default_version_debian }}-pdo"
          - "php{{ php_default_version_debian }}-xml"
          - "php{{ php_default_version_debian }}-zip"
          - "php-sqlite3"
          - "php-apcu"
          - "php-redis"
          - "libapache2-mod-php{{ php_default_version_debian }}"

        # weareinteractive.apt vars.
        apt_repositories:
          - repo: "ppa:ondrej/php"
            codename: xenial
            update_cache: true
          - repo: "ppa:ondrej/apache2"
            codename: xenial
            update_cache: true

      roles:
        - role: ansible-role-lamp

## License

GPLv2
