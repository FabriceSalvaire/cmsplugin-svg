# -*- coding: utf-8 -*-

####################################################################################################

from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import SvgImage

####################################################################################################

class SvgImagePlugin(CMSPluginBase):

    model = SvgImage
    name = _("SVG Image")
    render_template = "cmsplugin_svg/plugin.html"

    # Editor fieldsets
    fieldsets = (
        (None, {
            'fields': ('svg_image',
                       'tag_type',
                       'height', 'width',
                       'alignment',
                       'caption_text',
                       'alt_text')
        }),
        (_('Advanced Settings'), {
            'classes': ('collapse',),
            'fields': (
                'additional_class_names',
                'label',
                'id_name',
            ),
        }),
    )

####################################################################################################

plugin_pool.register_plugin(SvgImagePlugin)
