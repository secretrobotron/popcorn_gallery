Popcorn Gallery
===============

Django app to power the Popcorn Maker! http://mozillapopcorn.org/

The Project structure is based on Mozilla Playdoh http://playdoh.readthedocs.org/en/latest/index.html


Getting the source code
=======================

Clone the repository and its dependencies:

    git clone --recursive git@github.com:alfredo/popcorn_gallery.git


Setup the application
=====================

The recommended setup is using vagrant and virtual box, you can get them from:

- Virtualbox: https://www.virtualbox.org/wiki/Downloads
- Vagrant: http://vagrantup.com/

This will keep the code living in your filesystem but the application running inside a VM.

Once you've installed vagrant, from the root of the repository copy the local vagrant settings.

    cp vagrantconfig_local.yaml-dist vagrantconfig_local.yaml

Edit ``vagrantconfig_local.yaml`` if you want to change any of the defaults.

Now we are ready to provision the machine run.

    vagrant up

This will take a few minutes, so go on and reward yourself with a nice cup of tea!


Update the local settings file
==============================

Amend ``popcorn_gallery/settings/local.py``  with your details:

- ADMINS: Add your email address and name.
- SECRET_KEY
- HMAC_KEYS: Uncomment or add your own key.


Preapare the static assets
==========================

Because the project is has a lot of media that needs to be served the files need to be collected and prepared.

SSH into the virtualbox:

    vagrant ssh

Run from te root of the project:

    fab collectstatic


Add a host alias
================

This is done so ou can access the application via: http://local.mozillapopcorn.org

Add to /etc/hosts in your local machine:

    33.33.33.11 local.mozillapopcorn.org

Now the application should be available at:

    http://local.mozillapopcorn.org


Runing the test suite
=====================

SSH into the virtualbox:

    vagrant ssh

And run the test suite:

    fab test


Picking up development server updates
=====================================

The development server provisioning is done via Puppet http://puppetlabs.com/ to pick up the latest changes once you updated the project run:

    vagrant provision


Speed up the server
===================

At the moment the wsgi application is served via apache, which it's a bit hacky in order to pick up the file changes and reload automaticaly.

If you want to speed up the application you could try stop apache and run the application via the development server.

NGINX is proxy-passing the port 8000 to 80 and serving most of the static files.

SSH into the virtual box:

    vagrant ssh

Stop apache:

    sudo /etc/init.d/apache2 stop

Run the development server

    python manage.py runserver

