# cleanmymac
A simple command line tool to clean old stuff from your mac

# documentation
http://cleanmymac.readthedocs.org/en/latest/

# usage
```bash
$ cleanmymac -h
usage: cleanmymac [-h] [-u] [-d] [-q] [-l] [-s] [-c CONFIG] [-t TARGETS_PATH]
                  [TARGETS [TARGETS ...]]

cleanmymac v0.1.5, a simple utility designed to help clean your mac from
old/unwanted stuff

positional arguments:
  TARGETS               the list of targets to execute. Execute all if not
                        specified.

optional arguments:
  -h, --help            show this help message and exit
  -u, --update          update the target if applicable
  -d, --dry_run         describe the actions to be performed, do not execute
                        them
  -q, --quiet           run in quiet mode
  -l, --list            list registered cleanup targets
  -s, --stop_on_error   stop execution when first error is detected
  -c CONFIG, --config CONFIG
                        specify the configuration path
  -t TARGETS_PATH, --targets_path TARGETS_PATH
                        specify extra yaml defined targets path
```

a typical usage pattern is: 

```bash
$ cleanmymac
```


# installation
clone the repository locally and issue

```bash
python setup.py install
```

# configuration

the *cleanmymac* utility accepts a configuration file by specifying the *-c* option. If not specified the 
file is assumed to be at the following location **~/.cleanmymac.yaml**

the global configuration can be used (for now) to pass specific env vars to shell commands, for example 
assume that *anaconda* is not in the main path:

```yaml
anaconda: {
  env: {
    PATH: '~/anaconda/bin',
  },
}
```

# extensibility

one can add more *cleanup targets* either by installing them as python classes registered to the following
entry-point: **cleanmymac.target** like this (in setup.py):

```python
entry_points={
    # ....
    'cleanmymac.target': [
        'my_target_name = my.python.package.MyTargetClass'
    ]
    # ...
}
```

alternatively for shell based commands simply create yaml files with the following schema:

```yaml
type: 'cmd'
args: {
  update_commands: [
    'brew update',
    'brew outdated | brew upgrade'
  ],
  clean_commands: [
    'brew cleanup'
  ]
}
```

or for cleaning up directories (removing all but the latest version):

```yaml
type: 'dir'
args: [
  { dir: '/usr/local/texlive/',
  pattern: '\d+' },
]
```

**note**: see the *cleanmymac.builtins* module for more details

and point *cleanmymac* to the folder where the yaml files reside with the *-t* command line option

# builtin targets

to see a list of builtin targets run:
```bash
$ cleanmymac -l
```

currently the following are supported:
 * homebrew
 * java jdk
 * texlive
 * anaconda

# disclaimer

I created this utility in the hope that others may find it useful, as I found it annoying to always remember 
how and what to clean from my mac. This is work in progress, so use at your own risk!