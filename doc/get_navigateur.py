import psutil

def get_navigateur_pid():
    """python3 -m webbrowser -t 'http://www.python.org'
        'mozilla' Mozilla('mozilla')
        'firefox' Mozilla('mozilla')
        'netscape' Mozilla('netscape')
        'galeon' Galeon('galeon')
        'epiphany' Galeon('epiphany')
        'skipstone' BackgroundBrowser('skipstone')
        'kfmclient' Konqueror()
        'konqueror' Konqueror()
        'kfm' Konqueror()
        'mosaic' BackgroundBrowser('mosaic')
        'opera' Opera()
        'grail' Grail()
        'links' GenericBrowser('links')
        'elinks' Elinks('elinks')
        'lynx' GenericBrowser('lynx')
        'w3m' GenericBrowser('w3m')
        'windows-default' WindowsDefault
        'macosx' MacOSX('default')
        'safari' MacOSX('safari')
        'google-chrome' Chrome('google-chrome')
        'chrome' Chrome('chrome')
        'chromium' Chromium('chromium')
        'chromium-browser' Chromium('chromium-browser')
    """

    a = webbrowser.get()
    # #print(dir(a))
    # #print(a)
    # #print(a.background, a.basename, a.name)
    procs = {p.pid: p.info for p in psutil.process_iter(['name', 'username'])}
    for key, val in procs.items():
        if a.name in val["name"]:
            print("bingo:", key)
