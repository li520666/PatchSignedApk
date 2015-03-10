#!/usr/bin/python
import os
import sys

RELEASE_DIR = './release'
TEMP_DIR = './temp'
channelList = []
apkName = ''
easyName = ''
keystore =''
storepass = ''
alianame = ''

def configCmd():
    if os.path.isdir('/usr/local/') == False:
        os.system('sudo mkdir /usr/local/')
    if os.path.isdir('/usr/local/bin') == False:
        os.system('sudo mkdir /usr/local/bin')
    cp = r'sudo cp apktool apktool.jar /usr/local/bin/'
    chmodCmd = r'sudo chmod 777 /usr/local/bin/apktool'
    chmodJar = r'sudo chmod 777 /usr/local/bin/apktool.jar'
    os.system(cp)
    os.system(chmodCmd)
    os.system(chmodJar)

def readChannelfile(filename):
    f = file(filename)
    while True:
        line = f.readline().strip('\n')
        if len(line) == 0:
            break
        else:
            channelList.append(line);
    f.close()

def backUpManifest():
    if os.path.exists('./AndroidManifest.xml'):
        os.remove('./AndroidManifest.xml')
    manifestPath = TEMP_DIR + '/AndroidManifest.xml'
    os.system('cp %s %s' % (manifestPath, './AndroidManifest.xml'))

def modifyChannel(channel_name):
    from xml.dom.minidom import parse
    dom = parse(open(TEMP_DIR + '/AndroidManifest.xml'))
    for i in dom.getElementsByTagName('meta-data'):
        if i.getAttribute('android:name') == 'UMENG_CHANNEL':
            i.setAttribute('android:value', channel_name)
        if i.getAttribute('android:name') == 'TD_CHANNEL_ID':
            i.setAttribute('android:value', channel_name)
 
    open(TEMP_DIR+'/AndroidManifest.xml', 'w').write(dom.toxml().encode('utf-8'))

def buildChannelSignedApk(channel_name):
    unsignApk = r'%s/%s_%s_unsigned.apk'% (RELEASE_DIR, easyName, channel_name)
    cmdPack = r'java -jar apktool.jar b %s -o %s'% (TEMP_DIR, unsignApk)
    os.system(cmdPack)
    
    signedjar = r'%s/%s_%s.apk'% (RELEASE_DIR, easyName, channel_name)
    unsignedjar = r'%s/%s_%s_unsigned.apk'% (RELEASE_DIR, easyName, channel_name)
    #for jdk6.x
    #cmd_sign = r'jarsigner -verbose -keystore %s -storepass %s -signedjar %s %s %s'% (keystore, storepass, signedjar, unsignedjar, alianame)
    #for jdk7
    cmd_sign = r'jarsigner -digestalg SHA1 -sigalg MD5withRSA -verbose -keystore %s -storepass %s -signedjar %s %s %s'% (keystore, storepass, signedjar, unsignedjar, alianame)
    os.system(cmd_sign)
    os.remove(unsignedjar);

def cleanRemoveCache():
    if os.path.exists(TEMP_DIR):
        os.system('rm -rf %s' % TEMP_DIR)
    if os.path.exists('./AndroidManifest.xml'):
        os.remove('./AndroidManifest.xml')
    
if __name__ == '__main__':
    apkName = sys.argv[1]
    keystore = sys.argv[2]
    storepass = sys.argv[3]
    #alianame = apkName.split('.apk')[0]
    alianame = sys.argv[4]
    easyName = apkName.split('.apk')[0]

    configCmd()
    
    readChannelfile('./channel')
    print '-------------------- your channel values --------------------'
    print 'channel list: ', channelList

    cmdExtract = r'java -jar apktool.jar  d -f -s %s -o %s'% (apkName, TEMP_DIR)
    os.system(cmdExtract)

    backUpManifest()

    for channel in channelList:
        modifyChannel(channel)
        buildChannelSignedApk(channel)

    cleanRemoveCache()
    print '--------------------------- Done -----------------------------'

