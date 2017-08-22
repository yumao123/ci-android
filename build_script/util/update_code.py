#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, shutil, re
from build_script import config
from build_script.util import helpers
from build_script.globals import ci_globals
import fnmatch

class ExecuteCmdCtx(object):

    def __init__(self, dest_path):
        self.current_path = os.getcwd()
        self.dest_path = dest_path

    def __enter__(self):
        try:
            os.chdir(self.dest_path)
        except:
            os.mkdir(self.dest_path)
            os.chdir(self.dest_path)

    def __exit__(self, e_t, e_v, t_b):
        os.chdir(self.current_path)



class UpdateCode(object):

    @classmethod
    def char_escape(cls, contents):
        escapes = {"(":"\(", ")":"\)"}

        for k,v in escapes.items():
            contents = contents.replace(k, v)
        return contents

    @classmethod
    def iterfindfiles(cls, path, fnexp):
        for root, dirs, files in os.walk(path):
            for filename in fnmatch.filter(files, fnexp):
                yield os.path.join(root, filename)


    '''
    usage:    
    params:
    code_url:        
    code_version:    
    eg:         update_code_by_svn()
    modify:
        2017-01-11:
    '''
    @classmethod
    def update_code_by_svn(cls, code_info, callback= None):
        err             = None
        old_file_name   = None
        usage           = code_info.get('usage')
        code_url        = code_info.get('code_url')

        code_version    = str(code_info.get('code_version'))
        #eg:/Users/xw/CiApp/code/
        local_reperotry     = code_info['local_reperotry']
        #eg:/Users/xw/CiApp/repository/
        cache_reperotry     = code_info['cache_reperotry']
        #eg:xtion6.2
        folder_name         = code_url.split('/')[-1]
        #eg:/Users/xw/CiApp/code/xtion6.2
        local_code          = '{local_reperotry}{folder_name}'.format(
            local_reperotry= local_reperotry, folder_name= folder_name)
        #eg:/Users/xw/CiApp/repository/code/xtion6.2_2013
        cache_file = '{cache_reperotry}code/{folder_name}_{code_version}'.format(
                cache_reperotry= cache_reperotry, folder_name= folder_name, code_version= code_version
            )

        #Try to remove local_code
        try:
            shutil.rmtree(local_code)
        except OSError:
            pass

        #a.If cache_file exist, copy to the local_code
        #
        try:
            shutil.copytree(cache_file, local_code)
            return None
        except OSError:
            #Means cache_file is not exist
            pass


        if isinstance(code_url, unicode):
            code_url = code_url.encode('utf-8')
        local_path      = code_info.get('local_reperotry') if usage == 'update' else '{0}code/'.format(code_info.get('cache_reperotry'))
        log_name        = ci_globals.update_code_log
        print 'update in svn'
        with ExecuteCmdCtx(local_path) as ecc:
            if usage == 'update':
                cmd = 'svn co {url} -r {version} --username {username} --password {password} --no-auth-cache'.format(
                        url= code_url, version= code_version, username= config.SVN_USER_NAME, password= config.SVN_PASSWORD
                    )
                ret = helpers.timeout_command(cmd, fileName= log_name, timeout= 4*60)
            else:
                old_file_name = code_url.split('/')[-1]
                cmd = 'svn co {url} -r {version} --username {username} --password {password} --no-auth-cache'.format(
                        url= code_url, version= code_version, username= config.SVN_USER_NAME, password= config.SVN_PASSWORD
                    )
                ret = helpers.timeout_command(cmd, timeout= 4*60)
           
            if ret is None:
                err = 'Svn checkout timeout...'
            if old_file_name:
                new_file_name = '{0}_{1}'.format(old_file_name, code_version)
                try:
                    os.rename(old_file_name, new_file_name)
                except Exception, e:
                    err = 'Svn checkout error:{0}'.format(e)
        if ret:
            err = 'Svn checkout error'
        if callback:
            return callback(err)
        else:
            return err

    @classmethod
    def update_code_by_git(cls, code_info, callback= None):
        log_name        = ci_globals.update_code_log
        app_path        = None
        code_version    = code_info.get('code_version')
        if isinstance(code_version, unicode):
            code_version = code_version.encode('utf-8')
        code_url        = code_info.get('code_url')
        remote_url      = code_info.get('code_url').replace('http://', '')
        #eg:/Users/xw/CiApp/code/
        local_reperotry     = code_info['local_reperotry']
        #eg:android.git
        folder_name         = code_url.split('/')[-1]
        #eg:android
        cache_folder_name   = folder_name.split('.')[0]
        #eg:/Users/xw/CiApp/repository/code/
        cache_reperotry     = code_info['cache_reperotry'] + 'code/'
        #eg:/Users/xw/CiApp/code/android.git
        local_code          = '{local_reperotry}{folder_name}'.format(
            local_reperotry= local_reperotry, folder_name= folder_name)
        #eg:/Users/xw/CiApp/repository/code/android
        cache_folder = cache_reperotry + cache_folder_name
        try:
            shutil.rmtree(local_code)
        except OSError:
            pass
        try:
            shutil.rmtree(cache_folder)
        except OSError:
            pass
        # 2.clone -> cache:
        with ExecuteCmdCtx(cache_reperotry) as ecc:
            clone_cmd   = config.GIT_CLONE.format(config.GIT_USER_NAME, config.GIT_PASSWORD, remote_url)
            ret = helpers.timeout_command(clone_cmd, fileName= log_name, timeout= 4*60)
            if ret is None:
                err = 'git clone timeout...'
                return err
        # 3.checkout -> 
        with ExecuteCmdCtx(cache_folder) as ecc:
            code_version = cls.char_escape(code_version)
            checkout_cmd = config.GIT_CHECKOUT.format(code_version)
            ret = helpers.timeout_command(checkout_cmd, fileName= log_name, timeout= 4*60)
            if ret is None:
                err = 'git checkout timeout...'
                return err
            # 4.cp cache -> 
            for flag in config.APP_FLAG:
                for filename in cls.iterfindfiles(cache_folder, flag):
                    if filename is not None:
                        app_path = filename.replace(flag, "")
                        shutil.copytree(app_path, local_code)
                        return None
            return "App file is not exits!"


def update_code(code_info):
    """

    """

    def callback(err):
        return err

    #eg:http://172.16.0.245:9000/xtionkx/trunk/web/New_Web/SFA
    #eg:http://172.16.0.141/kx100-mobile/android.git
    tools = 'svn'

    if code_info.get('usage') == 'update':
        #eg:svn / git
        tools = code_info['code_type']

    #b.f cache_file not exist, check it out
    update_function = getattr(UpdateCode, "update_code_by_%s" % tools)
    return update_function(code_info, callback)