# Populated LDAP
## A tool leveraging faker and osixia/docker-openldap to generate a fake records to be imported in ldap directly to docker
Simply start by

```
docker run --name populated_ldap --detach -p 389:389 -e "LDAP_DOMAIN=example.com" -e "LDAP_ORGANISATION=Example Inc." -e "LDAP_USER_COUNT=100" -e "LDAP_ADMIN_PASSWORD=admin" idanelor/populated_ldap:lts 
```

For see the users either start the osixia/docker-openldap

```
docker run --name phpldapadmin-service -p 9999:443 --hostname phpldapadmin-service --link populated_ldap:ldap-host --env PHPLDAPADMIN_LDAP_HOSTS=ldap-host  --detach osixia/phpldapadmin:0.7.1
```

Browse to "https://localhost:9999" and connect with
```"cn=admin,dc=example,dc=com"``` and selected password (```admin``` by default)

##### Note: If your domain is foo.my.app.com than admin will be acordingly, ```cn=admin,dc=foo,dc=my,dc=app,dc=com```

Populated users can be either found in https://localhost:9999 or by running
``` docker logs populated_ldap ```
Any questions, just reach out.