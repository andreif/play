import os, os.path
import shutil
import platform

from play.utils import *

COMMANDS = ['idealize', 'idea', 'ideaproj']

HELP = {
    'idealize': 'Create all IntelliJ Idea configuration files'
}

def execute(**kargs):
    command = kargs.get("command")
    app = kargs.get("app")
    args = kargs.get("args")
    play_env = kargs.get("env")

    app.check()
    modules = app.modules()
    classpath = app.getClasspath()

    application_name = app.readConf('application.name')
    imlFile = os.path.join(app.path, application_name + '.iml')
    
    if command == 'ideaproj':
        iprFile = os.path.join(app.path, application_name + '.ipr') # project file
        iwsFile = os.path.join(app.path, application_name + '.iws') # workspace file
    
        shutil.copyfile(os.path.join(play_env["basedir"], 'resources/idea/iwsTemplate.xml'), iwsFile)
        replaceAll(iwsFile, r'%APP_NAME%', application_name)
        
        shutil.copyfile(os.path.join(play_env["basedir"], 'resources/idea/iprTemplate.xml'), iprFile)
        replaceAll(iprFile, r'%MODULE_NAME%', application_name)
    
    shutil.copyfile(os.path.join(play_env["basedir"], 'resources/idea/imlTemplate.xml'), imlFile)
    cpXML = ""

    replaceAll(imlFile, r'%PLAYHOME%', play_env["basedir"].replace('\\', '/'))
    replaceAll(imlFile, r'%PLAYVERSION%', play_env["version"].replace('\\', '/'))

    if len(modules):
        lXML = ""
        classXML = ""
        jarXML = ""
        for i, module in enumerate(modules):
            lXML += '    <content url="file://%s">\n            <sourceFolder url="file://%s" isTestSource="false" />\n        </content>\n' % (module, os.path.join(module, 'app').replace('\\', '/'))
            classXML += '    <root url="file://%s" />\n' % (os.path.join(module, 'lib').replace('\\', '/'))
            jarXML += '    <jarDirectory url="file://%s" recursive="false" />\n' % (os.path.join(module, 'lib').replace('\\', '/'))
            if i == (len(modules) -1):
                replaceAll(imlFile, r'%LINKS%', lXML)
                replaceAll(imlFile, r'%MODULE_LINKS%', '')
                replaceAll(imlFile, r'%MODULE_LIB_CLASSES%', classXML)
                replaceAll(imlFile, r'%MODULE_LIBRARIES%', jarXML)
    else:
        replaceAll(imlFile, r'%LINKS%', '')
        replaceAll(imlFile, r'%MODULE_LINKS%', '')
        replaceAll(imlFile, r'%MODULE_LIB_CLASSES%', '')
        replaceAll(imlFile, r'%MODULE_LIBRARIES%', '')


    print "~ OK, the application is ready for Intellij Idea"
    if command == 'ideaproj':
        if platform.system() == 'Darwin':
            os.system("open -a /Applications/IntelliJ\\ IDEA*.app %s" % iprFile)
    else:
        print "~ Use File/New Module/Import Existing module"
    print "~"
