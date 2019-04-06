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

The role itself only provides a single variable (see **Role Variables**
below) that are used to determine which roles to run (by default, we run
`weareinteractive.apt`, `ctorgalson.files`, `geerlingguy.mysql`,
`geerlingguy.apache`, `geerlingguy.php`, and `geerlingguy.composer`).

## Requirements

This role has no special requirements.

## Role Variables

| Variable name     | Default value | Description |
|-------------------|---------------|-------------|
| `lamp_configure`  | `['apt', 'files', 'mysql', 'apache', 'php', 'composer']` | A list 'AMP' items to configure. Possible values include `apache`, `apt`, `files`, `fpm`, `mysql`, `php`, and `composer` |

## Dependencies

This role includes several Galaxy roles as dependencies. For details on how
to configure them, see each role's specific documentation:

- [weareinteractive.apt](https://galaxy.ansible.com/weareinteractive/apt)
- [ctorgalson.files](https://galaxy.ansible.com/ctorgalson/files)
- [geerlingguy.mysql](https://galaxy.ansible.com/geerlingguy/mysql)
- [geerlingguy.apache](https://galaxy.ansible.com/geerlingguy/apache)
- [geerlingguy.php](https://galaxy.ansible.com/geerlingguy/php)
- [geerlingguy.composer](https://galaxy.ansible.com/geerlingguy/composer)
- [geerlingguy.apache-php-fpm](https://galaxy.ansible.com/geerlingguy/apachei-php-fpm)

## Example Playbook

## Role Use

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

3. To exclude certain dependencies from execution, see **Role
   Variables**, above.

4. Becuase the roles are declared _as dependencies_, they must all be
   installed/present. If you don't use many/most of the dependencies,
   this role may not be suitable for your use.

## Example

    - hosts: all
      vars:
        # ctorgalson.files vars.
        files_files:
          - path: "/var/www/lamp/web"
            state: directory
            owner: "jenkins"
            group: "www-data"
            mode: "ug=rwx,o=rx"

        # ctorgalson.lamp var.
        lamp_configure:
          - apt
          - files
          - mysql
          - apache
          - php

        # geerlingguy.apache vars.
        apache_remove_default_vhost: true
        apache_mods_enabled:
          - "expires.load"
          - "headers.load"
          - "rewrite.load"
        apache_vhosts:
          - servername: "lamp"
            documentroot: "/var/www/lamp/web"

        # geerlingguy.composer vars.
        composer_home_path: "/home/{{ app_owner }}/.composer"
        composer_home_owner: "{{ app_owner }}"
        composer_home_group: "{{ app_owner }}"

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
