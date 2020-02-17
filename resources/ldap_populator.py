import argparse
from faker import Faker
import subprocess

# Load groups and user template
GROUPS_TEMPLATE = open('groups.template', 'r').read()
USER_TEMPLATE = open('user.template', 'r').read()

# Fill a template with values
def fill_template(template, mapping):
	res = template
	for key, value in mapping.items():
		res = res.replace("{%s}" % key, value)
	return res

def populate_ldif(users_count=5, domain_name="example.com", output_file_name="users.ldif"):
	domain, postfix = domain_name.split(".")

	groupDetailMappings = {
			"domainName": domain,
			"domainPostfix": postfix,
	}

	groups_filled_template = fill_template(GROUPS_TEMPLATE, groupDetailMappings)
	output_file.write(groups_filled_template + "\n")
	for i in range(0, users_count):
		fakeUserDetails = Faker()
		username = fakeUserDetails.user_name()
		slappasswd_cmd="slappasswd -h {MD5} -s %sldappassword" % username
		print("Exec command: %s" % slappasswd_cmd)
		userPassword = subprocess.check_output(slappasswd_cmd, shell=True).decode()[:-1]

		userDetailsMappings = {
			"username": username,
			"domainName": domain,
			"domainPostfix": postfix,
			"lastName": fakeUserDetails.last_name(),
			"givenName": fakeUserDetails.first_name(),
			"uidNumber": str(11000 + i),
			"userPassword": userPassword
		}

		user_filled_template = fill_template(USER_TEMPLATE, userDetailsMappings)
		output_file.write(user_filled_template + '\n')

	output_file.close()

	print("Copy your file to your LDAP server and run: ")
	print("'ldapadd -x -D cn=admin,dc=%s,dc=%s -W -f %s.ldif'" % (domain, postfix, output_file_name))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Populate a ldif format to be imported into LDAP server.')
	parser.add_argument('--users-count', metavar='N', dest="users_count",
							type=int, default=10,
	                    	help='Provide number of users to populate')
	parser.add_argument('--domain', metavar='domain', default="example.com", dest="domain", type=str,
	                    	help='Provide a domiain in your LDAP to populate')
	parser.add_argument('--output', metavar='<filename>', dest="output_file_name", nargs=1,
	                    	default="users",help='Provide an output file name')

	args = parser.parse_args()
	users_count = args.users_count
	output_file_name = args.output_file_name
	output_file = open(output_file_name + ".ldif", "w+")
	populate_ldif(users_count=users_count, domain_name = args.domain, output_file_name = output_file)
