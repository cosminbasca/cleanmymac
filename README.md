# cleanmymac
A simple command line tool to clean old stuff from your mac

# usage
```bash
$ cleanmymac -h
  usage: cleanmymac [-h] [-u] [-d] [-v] [-c CONFIG] [-t TARGETS_PATH]
  
  cleanmymac v0.0.5, a simple utility designed to help clean your mac from
  old/unwanted stuff
  
  optional arguments:
    -h, --help            show this help message and exit
    -u, --update          update the target if applicable
    -d, --dry_run         describe the actions to be performed, do not execute
                          them
    -v, --verbose         run in verbose mode
    -c CONFIG, --config CONFIG
                          specify the configuration path
    -t TARGETS_PATH, --targets_path TARGETS_PATH
                          specify extra yaml defined targets path
```

a typical usage pattern is: 

```bash
$ cleanmymac -v
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
entry-point: **cleanmymac.target*** like this (in setup.py):

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
update_commands: []
clean_commands: []
```

and point *cleanmymac* to the folder where the yaml files reside with the *-t* command line option

# disclaimer

I created this utility in the hope that others may find it useful, as I found it annoying to always remember 
how and what to clean from my mac. This is work in progress, so use at your own risk!