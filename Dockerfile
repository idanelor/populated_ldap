FROM osixia/openldap:1.3.0

EXPOSE 389

ARG ldap_domain="example.com"
ARG ldap_organization="Example Inc."
ARG ldap_admin_password="admin"
ARG ldap_users_count="25"

ENV LDAP_DOMAIN $ldap_domain
ENV LDAP_ORGANISATION $ldap_organization
ENV LDAP_ADMIN_PASSWORD $ldap_admin_password
ENV LDAP_USER_COUNT $ldap_users_count

RUN apt update -y
RUN apt-get install -y python3 python3-pip

COPY resources/ .
RUN pip3 install -r requirements.txt
 
CMD ./init_and_populate.sh
