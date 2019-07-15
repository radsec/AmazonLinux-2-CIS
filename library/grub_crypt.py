#!/usr/bin/python
## START COPYRIGHT NOTICE ##
# AmazonLinux2-CIS Ansible Script
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
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
