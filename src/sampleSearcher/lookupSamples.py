import os
import sys

PLUGIN_DIR = 'searchmodule'

def AddPlugin(cClass):
    plugins.append(cClass)

def LoadPlugins():
    pluginPath = os.path.join(os.path.dirname(sys.argv[0]), PLUGIN_DIR)
    dirList = os.listdir(pluginPath)
    
    for plugin in dirList:
        try:
            if plugin.lower().endswith('.py'):
                exec open(os.path.join(pluginPath, plugin), 'r') in globals(), globals()
                print "Load Plugin: %s" % plugin.replace('.py', '')
        except Exception as e:
            print('Error %s loading plugin: %s' % (e, plugin.replace('.py', '')))
            
def process(hashes):   
    # Loop round the plugins and print their names.
    for cPlugin in plugins:
        oPlugin = cPlugin()
        oPlugin.searchSample(hashes)
        
        if oPlugin.isDownloadable():
            oPlugin.downloadSample("downloadPfad")

if __name__ == "__main__":
    global plugins
    plugins = []
    # Load the plugins from the plugin directory.
    LoadPlugins()
        
    hashes = ("eed9c961d4bc5e0f7a59799950e1367ead2d2e312a87650c4613fb97d5ebe806", "be62f4a09574bbffd2808d449919a316473a3ce0", "0fe568b70a6e0044a1e315c11f8158d1")
    process(hashes)
    
    