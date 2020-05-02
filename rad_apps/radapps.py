import importlib


class RadApps(object):
    def __init__(self, app):
        app_names = eval(app.config['APPS'])
        apps = [importlib.import_module(app_name).app for app_name in app_names]
        self.apps = {app.short_name: app for app in apps}

    def get_app_list(self):
        return [(x, y.long_name) for x, y in zip(self.apps.keys(), self.apps.values())]

    def get_app_info(self, short_name):
        return self.apps[short_name]
