# PatchSignedApk
A python shell for patching apks of many channels

本脚本主要用于正式发布Apk文件时，快速打包签名不同渠道平台的apk

所需环境：
	Python 建议版本2.5.4以上

ps: /Users/lipei/Program/Python/signApk/为脚本所在路径

需要复制到上面路径的文件夹下的文件：
1. .keystore或.key密钥文件
2. 待发布的apk包

如何运行：
	命令行cd /Users/lipei/Program/Python/signApk/
	python signShell.py Test.Apk test.keystore thispwd testAlias

参数说明：
	1. 待发布apk(Test.Apk)；
	2. 密钥文件(test.keystore)；
	3. 密钥密码(thispwd)；
	4. alias别名(testAlias)；

1. channel文件里存储需打包签名的平台，可根据需要自行添加、修改、删除
2. 生成的apk在release文件夹下

如有疑问或建议请联系我: li5206666@gmail.com

