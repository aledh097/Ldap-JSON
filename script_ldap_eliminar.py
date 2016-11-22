#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import getpass
import json

password = getpass.getpass("Password of the administrator of the directory LDAP: ")

# Lectura del fichero JSON
fichero_json = open("alumnos.json")
datos = json.load(fichero_json)


for i in datos["personas"]:
	rm_usuarios = 'ldapdelete -x -D "cn=admin,dc=apalominogarcia, dc=gonzalonazareno,dc=org" -h 172.22.200.116 -p 389 -w %s "uid=%s,ou=People,dc=apalominogarcia,dc=gonzalonazareno,dc=org"' % (password,str(i["usuario"]))
	os.system(rm_usuarios)

for i in datos["computers"]:
	rm_ordenadores = 'ldapdelete -x -D "cn=admin,dc=apalominogarcia, dc=gonzalonazareno,dc=org" -h 172.22.200.116 -p 389 -w %s "uid=%s,ou=computers,dc=apalominogarcia,dc=gonzalonazareno,dc=org"' % (password,str(i["ipv4"]))
	os.system(rm_ordenadores)

print "Usuarios eliminados correctamente"
print "Ordenadores eliminados correctamente"
