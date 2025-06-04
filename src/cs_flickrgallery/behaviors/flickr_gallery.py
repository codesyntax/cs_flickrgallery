# -*- coding: utf-8 -*-

from cs_flickrgallery import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider


class IFlickrGalleryMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IFlickrGallery(model.Schema):
    """
    """

    flickr_set = schema.TextLine(
        title=_(
            u'Flickr set id',
        ),
        description=_(
            u'',
        ),
        default=u'',
        required=False,
        readonly=False,
    )

    flickr_collection = schema.TextLine(
        title=_(
            u'Flickr collection id',
        ),
        description=_(
            u'',
        ),
        default=u'',
        required=False,
        readonly=False,
    )

@implementer(IFlickrGallery)
@adapter(IFlickrGalleryMarker)
class FlickrGallery(object):
    def __init__(self, context):
        self.context = context

    @property
    def flickr_set(self):
        if safe_hasattr(self.context, 'flickr_set'):
            return self.context.flickr_set
        return None

    @flickr_set.setter
    def flickr_set(self, value):
        self.context.flickr_set = value

    @property
    def flickr_collection(self):
        if safe_hasattr(self.context, "flickr_collection"):
            return self.context.flickr_collection
        return None

    @flickr_collection.setter
    def flickr_collection(self, value):
        self.context.flickr_collection = value
