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
conexion_ldap = ldap.initialize("ldap://localhost:389/")
conexion_ldap.simple_bind_s("cn=admin,dc=apalominogarcia,dc=gonzalonazareno,dc=org",password)

uidNumber = 2000
gidNumber = 2000
contador = 0

# Lectura del fichero JSON

alumnos_2ASIR = open("alumnos.json")
datos = json.load(alumnos_2ASIR)

# Creamos un diccionario para introducir en el directorio LDAP

for i in datos["personas"]:
	dn="uid=%s,dc=apalominogarcia,dc=gonzalonazareno,dc=org" % str(i["usuario"])
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

print "%s Usuarios insertados correctamente." % (contador)

# Desconexion con el directorio LDAP

conexion_ldap.unbind_s()

# Cerramos el fichero JSON

alumnos_2ASIR.close()
