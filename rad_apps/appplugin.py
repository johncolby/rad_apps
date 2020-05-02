from flask_wtf import FlaskForm


class AppPlugin(object):
    def __init__(self, long_name='', short_name='', description='', form_opts=FlaskForm,
                 wrapper_fun=None):

        self.long_name = long_name
        self.short_name = short_name
        self.description = description
        self.form_opts = form_opts
        self.wrapper_fun = wrapper_fun
