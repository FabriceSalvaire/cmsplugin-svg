# -*- coding: utf-8 -*-

####################################################################################################

import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from filer.fields.image import FilerFileField

####################################################################################################

CLASS_NAME_FORMAT = re.compile(r'^\w[\w_-]*$')

class SvgImage(CMSPlugin):

    """
    A django CMS Plugin to use SVG image
    """

    TAG_TYPE_CHOICES = (
        ('figure', 'figure'),
        # ('div', 'div'),
    )

    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'
    FLOAT_CHOICES = ((LEFT, _('left')),
                     (RIGHT, _('right')),
                     (CENTER, _('center')),
                     )

    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='+',
        parent_link=True,
    )

    label = models.CharField(
        _('label'),
        max_length=128,
        blank=True,
        help_text=_('Optional label for this plugin.'),
    )

    id_name = models.CharField(
        _('id name'),
        max_length=50,
        blank=True,)

    tag_type = models.CharField(
        verbose_name=_('tag Type'),
        max_length=50,
        choices=TAG_TYPE_CHOICES,
        default=TAG_TYPE_CHOICES[0][0],
    )

    svg_image = FilerFileField(
        verbose_name=_('file'),
        null=True,
        on_delete=models.SET_NULL,
    )

    additional_class_names = models.TextField(
        verbose_name=_('additional classes'),
        blank=True,
        help_text=_('Comma separated list of additional classes to apply to tag_type'),
    )

    alignment = models.CharField(_("image alignment"), max_length=10, blank=True, null=True, choices=FLOAT_CHOICES)

    width = models.PositiveIntegerField(_("width"), null=True, blank=True)
    height = models.PositiveIntegerField(_("height"), null=True, blank=True)

    caption_text = models.CharField(_("caption text"), null=True, blank=True, max_length=255)
    alt_text = models.CharField(_("alt text"), null=True, blank=True, max_length=255)

    ##############################################

    def __str__(self):

        """ Instance's name shown in structure page """

        display = self.tag_type or ''
        if self.additional_class_names:
            display = '{0} ({1})'.format(display, self.additional_class_names)
        if self.label:
            display = '“{0}”: {1}'.format(self.label, display)
        return display

    ##############################################

    def clean(self):

        if self.additional_class_names:
            additional_class_names = list(html_class.strip()
                                          for html_class in self.additional_class_names.split(','))
            for class_name in additional_class_names:
                class_name = class_name.strip()
                if not CLASS_NAME_FORMAT.match(class_name):
                    raise ValidationError(
                        _('"{0}" is not a proper css class name.').format(class_name))
            self.additional_class_names = ', '.join(set(additional_class_names))

    ##############################################

    @property
    def get_additional_class_names(self):

        if self.additional_class_names:
            # Removes any extra spaces
            return ' '.join((html_class.strip()
                             for html_class in self.additional_class_names.split(',')))
        else:
            return ''
