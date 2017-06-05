__author__ = 'songtao'
# -*- coding: utf-8 -*-

import os
import ldap
import ConfigParser

#格式化数据
import ldap.modlist as modlist

class LdapUserManage(object):
    """
    """
    def __init__(self,username):
        cur_path = os.path.abspath(os.path.dirname(__file__))
        config = ConfigParser.ConfigParser()
        config.read('%s/ldap.conf' % cur_path)
        self.uri = config.get('ldap','server')
        self.base = config.get('ldap','base')
        self.bind = config.get('ldap','admin')
        self.passwd = config.get('ldap','admin_pass')
        self.username = username
        try:
            self.l = ldap.initialize(self.uri)
            self.l.protocol_version = ldap.VERSION2
            self.l.bind(self.bind,self.passwd)
        except ldap.LDAPError, e:
            print e

    def usradd(self,usergroup):
        """
        dn example: dn = "ou=sa,dc=my-domain,dc=com"
        """
        dn =("cn=%s,%s" % (usergroup,self.base))
        attrs = {}
        attrs['cn'] = self.username
        attrs['uid'] = self.username
        attrs['objectclass'] = ['top','person','inetOrgPerson','posixAccount','vpseeAccount']
        ldif = modlist.addModlist(attrs)
        self.l.add_s(dn,ldif)
        pass

    def userdel(self):
        deletedn = ("cn=%s," + self.base) %self.username
        self.l.delete_s(deletedn)

    def activeuser(self):
        pass

    def searchuser(self):
        searchscope = ldap.SCOPE_SUBTREE
        searchfiler = "uid=*" + self.username + "*"
        resultid = self.l.search(self.base,searchscope,searchfiler,None)
        result_set = []
        while True:
            result_type, result_data = self.l.result(resultid,0)
            if result_data==[]:
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
        return result_set[0][0][1]['cn']



def main():
    username = 'songtao'
    result = LdapUserManage(username)
    a=result.searchuser()
    print a

if __name__ == '__main__':
    main()


# cur_path = os.path.abspath(os.path.dirname(__file__))
#
# config = ConfigParser.ConfigParser()
# config.read('%s/ldap.conf' % cur_path)
#
# LDAP_HOST = config.get('ldap','ldap_host')
# LDAP_BASE = config.get('ldap','ldap_base')
# LDAP_BIND = config.get('ldap','admin_cn')
# LDAP_PASS = config.get('ldap','admin_pass')
# # LDAP_HOST = config.get('ldap','ldap_host')
# # LDAP_HOST = config.get('ldap','ldap_host')
#
#
#
#
#
#
# def ldap_add(firstname, lastname, username):
#     l = ldap.initialize(LDAP_HOST)
#     l.protocol_version = ldap.VERSION3
#     l.simple_bind(LDAP_BIND, LDAP_PASS)
#
#     cn = firstname + ' ' + lastname
#     addDN = "cn=%s,ou=People,dc=vpsee,dc=com" % cn
#     attrs = {}
#     attrs['objectclass'] = ['top','person','inetOrgPerson','posixAccount','vpseeAccount']
#     attrs['cn'] = cn
#     attrs['givenName'] = firstname
#     attrs['homeDirectory'] = '/home/people/%s' % username
#     attrs['loginShell'] = '/bin/bash'
#     attrs['sn'] = lastname
#     attrs['uid'] = username
#     attrs['uidNumber'] = ldap_newuid()
#     attrs['gidNumber'] = ldap_getgid()
#     attrs['active'] = 'TRUE'
#     ldif = modlist.addModlist(attrs)
#     l.add_s(addDN, ldif)
#     l.unbind_s()
#
#
# def ldap_getcn(username):
#     try:
#         l = ldap.initialize(LDAP_HOST)
#         l.protocol_version = ldap.VERSION3
#         l.simple_bind(LDAP_BIND, LDAP_PASS)
#
#         searchScope = ldap.SCOPE_SUBTREE
#         searchFilter = "uid=*" + username + "*"
#         resultID = l.search(LDAP_BASE, searchScope, searchFilter, None)
#         result_set = []
#         while 1:
#             result_type, result_data = l.result(resultID, 0)
#             if (result_data == []):
#                 break
#             else:
#                 if result_type == ldap.RES_SEARCH_ENTRY:
#                     result_set.append(result_data)
#         return result_set[0][0][1]['cn'][0]
#     except ldap.LDAPError, e:
#         print e
#
#
#
#
# def ldap_deactive(username):
#     try:
#         l = ldap.initialize(LDAP_HOST)
#         l.protocol_version = ldap.VERSION3
#         l.simple_bind(LDAP_BIND, LDAP_PASS)
#
#         deactiveDN = ("cn=%s," + LDAP_BASE) % ldap_getcn(username)
#         old = {'active':'TRUE'}
#         new = {'active':'FALSE'}
#         ldif = modlist.modifyModlist(old, new)
#         l.modify_s(deactiveDN, ldif)
#         l.unbind_s()
#     except ldap.LDAPError, e:
#         print e
#
#
# def ldap_delete(username):
#     try:
#         l = ldap.open(LDAP_HOST)
#         l.protocol_version = ldap.VERSION3
#         l.simple_bind(LDAP_BIND, LDAP_PASS)
#
#         deleteDN = ("cn=%s," + LDAP_BASE) % ldap_getcn(username)
#         l.delete_s(deleteDN)
#     except ldap.LDAPError, e:
#         print e