# Install python and compiled modules for project
class python ($project_path){
  case $operatingsystem {
    ubuntu: {
      package {
        ["python2.6-dev", "python2.6", "python-imaging", "python-wsgi-intercept", "python-pip"]:
          ensure => installed,
      }
      exec { "virtualenvwrapper":
        command => "pip install virtualenv virtualenvwrapper",
        require => Package['python-pip'],
      }

      exec { "pip-install-compiled":
        command => "pip install -r $project_path/requirements/compiled.txt",
        require => Package['python-pip'],
      }

      exec { "pip-install-development":
        command => "pip install -r $project_path/requirements/dev.txt",
        require => Package['python-pip'],
      }
    }
  }
}
