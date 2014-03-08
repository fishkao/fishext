from django.conf.urls import patterns

from fishext.extension import FishExtension
from fishext.forms import FishSettingsForm


urlpatterns = patterns(
    '',

    (r'^$', 'reviewboard.extensions.views.configure_extension',
     {
         'ext_class': FishExtension,
         'form_class': FishSettingsForm,
     }),
)