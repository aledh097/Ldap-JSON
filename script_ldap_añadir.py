#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import ldap
from ldap import modlist
import getpass
import json

# Mensaje de bienvenida

print "---------------------------------------------------------------------------------------------------------------------------"
print "Script en Python que utiliza el fichero JSON como entrada y puebla el directorio LDAP con un objeto para cada alumno utilizando los ObjectClass posixAccount e inetOrgPerson."
print "---------------------------------------------------------------------------------------------------------------------------"

# Conexion con el directorio LDAP

password = getpass.getpass("Password of the administrator of the directory LDAP: ")
conexion_ldap = ldap.initialize("ldap://172.22.200.116:389/")
conexion_ldap.simple_bind_s("cn=admin,dc=apalominogarcia,dc=gonzalonazareno,dc=org",password)

uidNumber = 2000
gidNumber = 2000
contador = 0
contador2 = 0

# Lectura del fichero JSON

fichero_json = open("alumnos.json")
datos = json.load(fichero_json)

# Creamos un diccionario para introducir en el directorio LDAP

for i in datos["personas"]:
	dn="uid=%s,ou=People,dc=apalominogarcia,dc=gonzalonazareno,dc=org" % str(i["usuario"])
	dic = {}
	dic['objectclass'] = ['top','posixAccount','inetOrgPerson','ldapPublicKey']
	dic['uidNumber'] = str(uidNumber)
	dic['gidNUmber'] = str(gidNumber)
	dic['cn'] = str(i["nombre"])
	dic['sn'] = str(i["apellidos"])
	dic['mail'] = str(i['correo'])
	dic['sshPublicKey'] = str(i["clave"])
	dic['homeDirectory'] = '/home/%s' % str(i['usuario'])
	dic['loginShell'] = '/bin/bash'
	ldif = modlist.addModlist(dic)
	conexion_ldap.add_s(dn,ldif)
	uidNumber = uidNumber + 1
	contador = contador + 1

for i in datos["computers"]:
	dn="uid=%s,ou=Computers,dc=apalominogarcia,dc=gonzalonazareno,dc=org" % str(i["ipv4"])
	dic1 = {}
	dic1['objectclass'] = ['top','device','ldapPublicKey','ipHost']
	dic1['cn'] = str(i["hostname"])
	dic1['ipHostNumber'] = str(i["ipv4"])
	dic1['sshPublicKey'] = str(i["clave"])
	ldif = modlist.addModlist(dic1)
	conexion_ldap.add_s(dn,ldif)
	contador2 = contador2 + 1

print "%s usuarios insertados correctamente." % (contador)
print "%s ordenadores insertados correctamente." % (contador2)

# Desconexion con el directorio LDAP

conexion_ldap.unbind_s()

# Cerramos el fichero JSON

fichero_json.close()
