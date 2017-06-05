# -*- coding: utf-8 -*-

import os
import random
import hashlib
import base64
import ldap
import ldap.modlist as modlist
import pinyin
import xlrd
from vsa.celery import app
from vsa.settings import server, base, admin, admin_pass
import sys
import simplejson
from celery.utils.log import get_task_logger
from celery.result import AsyncResult

from admanage.models import *

reload(sys)
sys.setdefaultencoding('utf8')


def randompasswd():
    '''
    随机生成密码模块
    '''
    str_passwd = "abcdefghigklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ`124567890-=[]\;',./~!@#$%^*()_+{}|:<>?"
    passwd = ''.join(random.choice(str_passwd) for x in range(8))
    return passwd


def hash(password):
    return "{SHA}" + base64.encodestring(hashlib.sha1(str(password)).digest())


class LdapUserManage(object):
    """
    """

    def __init__(self):
        """
        ssl connection LDAP initial
        """
        self.uri = server
        self.base = base
        self.user = admin
        self.passwd = admin_pass
        try:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            self.l = ldap.initialize(self.uri)
            self.l.set_option(ldap.OPT_REFERRALS, 0)
            self.l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            # self.l.protocol_version = ldap.VERSION3
            # self.l.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
            self.l.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
            self.l.set_option(ldap.OPT_X_TLS_DEMAND, True)
            self.l.set_option(ldap.OPT_DEBUG_LEVEL, 255)
            self.l.simple_bind_s(self.user, self.passwd)
        except ldap.LDAPError, e:
            print e

    def search(self, name, search_dn, fuzzy=True):
        """

        :param name: 需要查询的cn名称
        :param fuzzy: 是否模糊搜索
        :return: 查询结果列表
        """
        searchScope = ldap.SCOPE_SUBTREE
        if fuzzy:
            searchfiler = "cn=*%s*" % name
        else:
            searchfiler = "cn=%s" % name
        retrieve_attributes = None
        result1 = self.l.search(search_dn, searchScope, searchfiler, retrieve_attributes)
        result_set = []
        while 1:
            result_type, result_data = self.l.result(result1, 0)
            if not result_data:
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
        return result_set

    def search_unique(self, searchfilter):
        """

        :param name: 需要查询的cn名称
        :return: 查询结果列表
        """
        searchScope = ldap.SCOPE_SUBTREE

        retrieve_attributes = None
        result1 = self.l.search(self.base, searchScope, searchfilter, retrieve_attributes)
        result_set = []
        while 1:
            result_type, result_data = self.l.result(result1, 0)
            if not result_data:
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
        return result_set

    def add_group(self, groupname):
        '''

        '''
        dn = ("cn=%s,ou=group,%s" % (groupname, self.base))
        attrs = {
            'cn': groupname,
            'objectClass': ['posixGroup', 'top']
        }
        ldif = modlist.addModlist(attrs, self.base)
        result = self.l.add_s(dn, ldif)
        return result

    def add_user(self, username, department_tree, department, company, password, unique_number):
        """

        """
        firstname = username[0]
        lastname = username[1:]
        account = pinyin.get(lastname + '.' + firstname, format='strip')

        base_dn = self.base
        for i in department_tree.split('/'):
            ou = 'ou=%s,' % i
            base_dn = ou + base_dn
        user_result = self.search(name=username, search_dn=base_dn)
        if user_result:
            print '该部门已经存在用户：%s！' % username
            cn = username + '0' + str(len(user_result))
            lastname += '0' + str(len(user_result))
            print '用户名称变为：%s' % cn
        else:
            cn = username
        sAMAccountName = self.check_account(account=account,check_type='account')
        email = self.check_account(account=account,check_type='email')
        userPrincipalName = email + '@zhengjin99.com'
        # print account
        # searchfileter = "sAMAccountName=*%s*" % account
        # account_result = self.search_unique(searchfilter=searchfileter)
        # # print account_result
        # if account_result:
        #     account = account + '0' + str(len(account_result))
        # email = account + '@zhengjin99.com'
        # email_searchfileter = "userPrincipalName=*%s*" % account
        # email_result = self.search_unique(searchfileter)

        distinguishedName = "cn=%s,%s" % (cn, base_dn)
        print distinguishedName
        unicode_pass = unicode("\"" + password + "\"", "iso-8859-1")
        password_value = unicode_pass.encode('utf-16-le')
        attrs = {'cn': cn.encode('utf-8'),
                 'sn': firstname.encode('utf-8'),
                 'givenName': lastname.encode('utf-8'),
                 'objectclass': ['top', 'person', 'organizationalPerson', 'user'],
                 'department': department.encode('utf-8'),
                 'description': unique_number,
                 'displayName': str(cn),
                 'unicodePwd': password_value,
                 'sAMAccountName': sAMAccountName.encode('utf-8'),
                 'company': company.encode('utf-8'),
                 'userPrincipalName': userPrincipalName.encode('utf-8'),
                 'userAccountControl': '66080'
                 }
        lidf = modlist.addModlist(attrs)
        print lidf,type(lidf)
        # print type(lidf)
        # print type(distinguishedName)
        # print distinguishedName,type(distinguishedName)
        result = self.l.add_s(str(distinguishedName), lidf)
        return distinguishedName, sAMAccountName

    def group_add_user(self, groupname, user_cn):
        '''

        :param groupname:
        :param username:
        :return:
        '''
        ldap_base = "dc=zhengjin99,dc=com"
        # try:
        #     print self.search(groupname.encode('utf-8'), search_dn=ldap_base, fuzzy=False)[0][0]

        group_dn, group_entry = self.search(groupname.encode('utf-8'), search_dn=ldap_base, fuzzy=False)[0][0]
        # print self.search(username.encode('utf-8'), search_dn=ldap_base, fuzzy=False)[0][0]
        # user_cn, user_entry = self.search(username.encode('utf-8'), search_dn=ldap_base, fuzzy=False)[0][0]
        if user_cn not in group_entry.get('member', []):
            modlist = [(ldap.MOD_ADD, 'member', [user_cn.encode('utf-8')])]
            self.l.modify_s(group_dn, modlist)
            return True
        else:
            print 'user:%s is already in group:%s' % (user_cn, groupname)
            return False

        # except IndexError, a:
        #     print 'error:', a
        #     return False

    def change_user_passwd(self, user):
        """
        强制修改用户密码
        :param user: 用户名
        :return: 密码
        """
        PASSWORD_ATTR = "unicodePwd"
        password = randompasswd()
        # unicode_pass = unicode('"'+password+'"',"iso-8859-1")l
        unicode_pass = unicode("\"" + password + "\"", "iso-8859-1")
        password_value = unicode_pass.encode('utf-16-le')
        add_pass = [(ldap.MOD_REPLACE, PASSWORD_ATTR, [password_value])]
        user_dn = self.search(name=user, fuzzy=False)[0][0][0]
        try:
            self.l.modify_s(user_dn, add_pass)
            return password, True
        except ldap.LDAPError, e:
            sys.stderr.write('更改用户：%s密码失败' % user)
            sys.stderr.write('Message:' + str(e) + '\n')
            return password, False

    def check_account(self,account,check_type):
        '''
        账户查询账户，查询email是否已经存在，如果存在，尾后+1,直至查询到未存在的返回
        :param account:
        :param check_type:
        :return:
        '''
        if check_type =="account":
            ad_attr = 'sAMAccountName'
        elif check_type == 'email':
            ad_attr = 'userPrincipalName'
        else:
            print 'error'
            return
        start_num = 0
        str_num = ''
        while 1:
            accountseachfilter = "%s=*%s%s*" %(ad_attr,account,str_num)
            search_result = self.search_unique(accountseachfilter)
            if search_result:
                start_num +=1
                if start_num < 10:
                    str_num =  '0' + str(start_num)
                else:
                    str_num = str(start_num)
                continue
            else:
                break
        return account+str_num




def read_group_releation():
    '''
    读取部门与组之间关系
    返回关系字典
    '''
    f_group_releation = xlrd.open_workbook('/root/groups.xls')
    group_table = f_group_releation.sheet_by_name('Sheet1')
    group_releation_dict = {}
    for i in range(1, group_table.nrows):
        t = group_table.row_values(i)
        group_releation_dict[t[1]] = {'group': [x for x in t[2].split(',')], 'department': t[3], 'company': t[4]}
    return group_releation_dict


@app.task(name='addaduser')
def adadduser(xls_file):
    # userlist = raw_input('please input userlist sheet path:')
    f = xlrd.open_workbook(xls_file)
    table = f.sheet_by_name('Sheet1')
    for i in range(1, table.nrows):
        password = '34er#$ER'
        t = table.row_values(i)
        l = LdapUserManage()
        if t[3]:
            unique_number = str(int(t[3]))
        else:
            unique_number = ""
        if GroupReleation.objects.filter(adtree=t[1]):
            grouprelation = GroupReleation.objects.get(adtree=t[1])
            company = grouprelation.company
            department = grouprelation.department
            attchto = grouprelation.attachto
            user, account = l.add_user(username=t[0], department_tree=t[1], department=department, company=company,
                                       password=password, unique_number=unique_number)
            if account:
                l_group = LdapUserManage()
                vlan_group = []
                for group in attchto.split(','):
                    add_user_to_group = l_group.group_add_user(group, user)
                    print '增加用户:%s 至组：%s ----------%s' % (account, group, add_user_to_group)
                    if add_user_to_group:
                        vlan_group.append({group: add_user_to_group})
                xlsusers = {'aduserfile': xls_file, 'aduser': t[0], 'department': t[1], 'addaduserstatus': True, 'vlangroup': simplejson.dumps(vlan_group),
                            'adaccount': account,'detail':'增加用户成功'}
            else:
                xlsusers = {'aduserfile': xls_file, 'aduser': t[0], 'department': t[1], 'addaduserstatus': False, 'detail': '增加用户出现异常',
                            'adaccount': account}
        else:
            print '添加用户：%s 失败,组关系缺未找到:%s' % (t[0], t[1])
            xlsusers = {'aduserfile': xls_file, 'aduser': t[0], 'department': t[1], 'addaduserstatus': False, 'detail': '结构关系不存在'}

        AdAddUserLog.objects.create(**xlsusers)
