whoisd: whois daemon
==========================

Este daemon recebe as requisições no protolo whois, e as direciona ao SIGI[1]
por meio da API em /whois. Requer Python 3 e eventualmente vai evoluir para
encaminhar consultas no formato RDAP.

This daemon receives whois requests and forwards it to SIGI[1] through the
/whois API. Requires Python 3 and eventually will evolve to support RDAP
backends.

Instalação
---------------

 virtualenv --python python3 whoisd_env
 cd whoisd_env
 git clone https://github.com/interlegis/whoisd.git whoisd
 source bin/activate
 pip install -r whoisd/requirements/requirements.txt
 python whoisd/whoisd.py

Detalhes
---------------

TODO: Escrever algo aqui...


[1]:https://github.com/interlegis/sigi

Copyright (c) 2016 Interlegis
