from yapsy.PluginManager import PluginManager

def main():   
    # Load the plugins from the plugin directory.
    manager = PluginManager()
    manager.setPluginPlaces(["searchmodule"])
    manager.collectPlugins()

    for pluginInfo in sorted(manager.getAllPlugins(), key=lambda PluginInfo: PluginInfo.name):
        print "%s (%s): %s" % (pluginInfo.name, pluginInfo.version, pluginInfo.description)

    # Loop round the plugins and print their names.
    for plugin in manager.getAllPlugins():
        hashes = ("eed9c961d4bc5e0f7a59799950e1367ead2d2e312a87650c4613fb97d5ebe806", "be62f4a09574bbffd2808d449919a316473a3ce0", "0fe568b70a6e0044a1e315c11f8158d1")

        plugin.plugin_object.searchSample(hashes)
        
        if plugin.plugin_object.isDownloadable():
            plugin.plugin_object.downloadSample("downloadPfad")


if __name__ == "__main__":
    main()
    
    