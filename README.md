host:
nodes=>{mac}->{
                   'time':'',
                   'ip':'',
                   'port':''
              }

flow:
flow=>0:{port}->${f}


user:
user=>0:{port}->{
                    'd':'',
                    'p':'',
                    'f':
                }

yum install python-setuptools && easy_install pip
pip install shadowsocks

sudo pip install redis
sudo pip install Flask
sudo pip install requests
sudo pip install PyJWT
