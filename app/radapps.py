from .apps import gbm, mets

class RadApps(object):
    def __init__(self):
        self.apps = {
            'gbm': gbm.app,
            'mets': mets.app
        }

    def get_app_list(self):
        return [(x, y.long_name) for x, y in zip(self.apps.keys(), self.apps.values())]

    def get_app_info(self, short_name):
        # import pdb; pdb.set_trace()
        return self.apps[short_name]

