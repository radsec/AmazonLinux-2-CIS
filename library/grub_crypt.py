#!/usr/bin/python
## COPYRIGHT NOTICE - LICENSED UNDER GNU GPLV3 ##
## START COPYRIGHT NOTICE ##
# AmazonLinux-CIS Ansible Script - Under Join Copyright
# Copyright (C) 2018  RADSec
# Copyright (C) 2018  Glownew Group
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
## END COPYRIGHT NOTICE ##
import random, string, crypt

def gen_pass(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def gen_salt(salt):
    '''Generate a random salt.'''
    ret = ''
    if not salt:
        with open('/dev/urandom', 'rb') as urandom:
            while True:
                byte = urandom.read(1)
                if byte in ('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                            './0123456789'):
                    ret += byte
                    if len(ret) == 16:
                        break
        return '$6$%s' % ret
    else:
        return '$6$%s' % salt

def main():
    module = AnsibleModule(
            argument_spec = dict(
                salt = dict(required=False, default=None),
                password = dict(no_log=True, required=False, default='random', type='str'),
                )

            )
    salt = module.params['salt']
    password = module.params['password']
    if password == 'random':
        password = gen_pass()
    sha512_salt = gen_salt(salt)
    salted_pass = crypt.crypt(password, sha512_salt)
    module.exit_json(changed=False, passhash=salted_pass)

from ansible.module_utils.basic import *
if __name__ == '__main__':
        main()
