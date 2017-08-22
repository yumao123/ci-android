# -*- coding: utf-8 -*-

import platform

#Android:代码图片存放相对路径
LOGO_INSIDE_CODE = "/app/src/main/res/"

#SVN配置信息
SVN_USER_NAME = 'dabao'
SVN_PASSWORD = '12345678'

#GIT配置信息
GIT_USER_NAME = 'dabao'
GIT_PASSWORD = '12345678'

#打包服务器地址端口
BUILD_SERVER = 'http://127.0.0.1:8003/'

#打包服务api
BUILD_API = {
	'GET_PROCESS' : 	'api/get_process',
	'ASK_FOR_BUILD' : 	'api/ask_for_build',
	'CACHE_CODE': 		'api/cache_code',
	'GET_LOG': 			'api/get_log',
	'UPLOAD_PACKAGE': 	'api/upload_package',
	'STOP_PACKAGE':		'api/stop_package',
}

GRADLE_SETTING = {
	'GRADLE_VERSION' : {
		'com.android.tools.build:gradle:2.1.0': 'gradle-2.10',
		'com.android.tools.build:gradle:1.2.3': 'gradle-2.7',
		'com.android.tools.build:gradle:2.2.2': 'gradle-2.14.1',
	}
}

#gitapi
GIT_CLONE 		= "git clone http://{0}:{1}@{2}"
GIT_CHECKOUT 	= "git checkout {0}"

#APP_FLAG
APP_FLAG		= ["ideaAndroidStyle.xml", "settings.gradle"]
# APP_FLAG = "ideaAndroidStyle.xml"


#远程路径
HTML_SERVER = {
	'hostname': '211.155.27.212',
	'port': 22,
	'username': 'easyinfo',
	'password': r'FDG9#$%WRgd2',
	'dir':	r'/home/easyinfo/web/soft/',	
}
#安装包存放地址
PACKAGE_SERVER = {
	'hostname': '42.159.86.120',
	'port': 54770,
	'username': 'xuanxunuser',
	'password': r"R0`\H{E)f'C1X9L",
	'dir':	r'/home/easyinfo/web/soft/',	
}

#windos系统,就是我的调试环境啦
if platform.system() == 'Windows':
	#android keystore 信息
	#若有新的keystore,需要另外新建
	KEY_STORE = 'D:/trunk/keystore/android.keystore'
	KEY_ALIAS = 'android'
	STORE_PWD = 'xw123456'
	ALIAS_PWD = 'xw123456'

	#package本地存放地址(用于远程下载)
	PACKAGE_REPROSITORY = 'E:/configmanage/repository/'

	#package本地存放地址(用于上传远程服务器)
	UPLOAD_REPROSITORY = 'E:/configmanage/upload/'

	#Android:服务器sdk地址
	LOCAL_SDK= 'D:/Program Files/adt-bundle-windows-x86_64-20140702/sdk'

	#本地代码存储地址
	LOCAL_CODE_REPERTORY = 'D:/trunk/'

	#Gradle:存放路径
	GRADLE_PATH = 'D:/Program Files/android-studio/gradle'

	#本地图片存放地址
	LOCAL_LOGO_REPERTORY = 'E:/configmanage/enterprise_logo/'

	#本地下载ip port
	DOWNLOAD_URL = 'http://183.63.72.242:8061/'

	#LOG路径
	LOG_DIR = 'E:/configmanage/buildLog/'

	DB_PATH = 'E:/'

#linux环境
elif platform.system() == 'Linux':
	#android keystore 信息
	#若有新的keystore,需要另外新建
	KEY_STORE = '/Users/xw/android_tools/keystore/android.keystore'
	KEY_ALIAS = 'android'
	STORE_PWD = 'xw123456'
	ALIAS_PWD = 'xw123456'

	#package本地存放地址(用于远程下载)
	PACKAGE_REPROSITORY = '/Users/xw/CiApp/repository/'

	#package本地存放地址(用于上传远程服务器)
	UPLOAD_REPROSITORY = '/Users/xw/CiApp/repository/upload/'

	#Android:服务器sdk地址
	LOCAL_SDK= '/Users/xw/android_tools/adt-bundle-mac/sdk/'

	#Gradle:存放路径
	GRADLE_PATH = '/Users/xw/CiApp/android_tools/'

	#本地代码存储地址
	LOCAL_CODE_REPERTORY = '/Users/xw/CiApp/code/'

	#本地图片存放地址
	LOCAL_LOGO_REPERTORY = '/Users/xw/repository/logo/'

	#本地下载ip port
	DOWNLOAD_URL = 'http://172.16.0.75:8082/'

	#LOG路径
	LOG_DIR = '/Users/xw/CiApp/buildLog/'

	DB_PATH = '/Users/xw/CiApp/application/db/'
	
#正式环境,默认是mac环境咯
else:
	#android keystore 信息
	#若有新的keystore,需要另外新建
	KEY_STORE = '/Users/xw/CiApp/android_tools/keystore/android.keystore'
	KEY_ALIAS = 'android'
	STORE_PWD = 'xw123456'
	ALIAS_PWD = 'xw123456'

	#package本地存放地址(用于远程下载)
	PACKAGE_REPROSITORY = '/Users/xw/CiApp/repository/'

	#package本地存放地址(用于上传远程服务器)
	UPLOAD_REPROSITORY = '/Users/xw/CiApp/repository/upload/'

	#Android:服务器sdk地址
	LOCAL_SDK= '/Users/xw/CiApp/android_tools/adt-bundle-mac/sdk/'

	#Gradle:存放路径
	GRADLE_PATH = '/Users/xw/CiApp/android_tools/'

	#本地代码存储地址
	LOCAL_CODE_REPERTORY = '/Users/xw/CiApp/code/'

	#本地图片存放地址
	LOCAL_LOGO_REPERTORY = '/Users/xw/Documents/jenkins/source/'

	#本地下载ip port
	DOWNLOAD_URL = 'http://183.63.72.242:8087/'

	#LOG路径
	LOG_DIR = '/Users/xw/CiApp/buildLog/'

	DB_PATH = '/Users/xw/CiApp/application/db/'
