Multiple K8s manifests may be stored in a single YAML file using the "`---`" separator. `kup` unpacks such manifests into separate "`${kind}/${name}.yaml`" files.

```
usage: kup [-h] [-d DIRECTORY] [files ...]

positional arguments:
  files                 Input files containing multiple manifests to unpack.
                        If none specified, manifests are read from stdin.

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory to unpack into (default: .)
```

## Install
Setup and activate a new virtualenv if needed:
```
python3 -m venv $HOME/.virtualenvs/kup
source $HOME/.virtualenvs/kup/bin/activate
```
Clone and install:
```
git clone https://github.com/ivc/kup
pip3 install ./kup
```
