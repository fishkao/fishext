from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import URLHook
from reviewboard.extensions.hooks import DashboardHook
from django.conf import settings
from django.conf.urls import patterns, include, url
from reviewboard.extensions.hooks import NavigationBarHook


class FishExtension(Extension):
    metadata = {
        'Name': 'Fish extension',
        'Summary': (
            'Get some customized datas. '
            'e.g. comments, bugs, bug details, bug distributions. '
            'By Yilan'
        ),
    }

    css_bundles = {
        'default': {
            'source_filenames': ["css/fish.less"],
        }
    }

    default_settings = {
        'enabled': True,
    }

    def __init__(self, *args, **kwargs):
        super(FishExtension, self).__init__(*args, **kwargs)
        pattern = patterns('', (r'^fishext/',
                                include('fishext.urls')))
        self.url_hook = URLHook(self, pattern)
        self.navigationbar_hook = NavigationBarHook(
            self,
            entries = [
                {
                    'label': 'Statistic',
                    'url': settings.SITE_ROOT + 'fishext/',
                },
            ]
        )

    def initialize(self):
        pass