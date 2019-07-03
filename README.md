# Gorra

Gorra is a modular endpoint checker with support for EOSio blockchains monitoring.
The eos module allows monitoring of multiples blockproducers and multiples sidechains.


## Configuration
add the endpoints , blockproducers, time range and telegram bots information to config.yml

## Docker
```
git clone  https://github.com/notchxor/gorra.git
cd gorra
docker build -t gorra .
docker run --name gorra --restart always -d gorra 
```

## Installation

```
git clone  https://github.com/notchxor/gorra.git
cd gorra  
python3 -m venv env  
source env/bin/activate  
pip3 install --editable .  
gorra monitor  
```
