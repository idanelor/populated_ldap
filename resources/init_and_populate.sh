#!/bin/bash

python3 ldap_populator.py --domain $LDAP_DOMAIN --users-count $LDAP_USER_COUNT
DOMAIN_DN=`python3 -c "print('dc='+ '$LDAP_DOMAIN'.replace('.',',dc='))"`
(sleep 10; ldapadd -x -D "cn=admin,$DOMAIN_DN" -w $LDAP_ADMIN_PASSWORD -f users.ldif) & 
echo -e "Users are:"
cat users.ldif
/usr/bin/python3 -u /container/tool/run
