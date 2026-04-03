from cs_flickrgallery import _
from cs_flickrgallery import logger
from cs_flickrgallery.utils import get_images
from plone import schema
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.schema import JSONField
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


class IFlickrGalleryMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IFlickrGallery(model.Schema):
    """ """

    model.fieldset(
        "flickr",
        label=_("Flickr album configuration"),
        fields=("flickr_set", "flickr_collection", "flickr_images"),
    )

    directives.read_permission(flickr_set="cmf.ModifyPortalContent")
    flickr_set = schema.TextLine(
        title=_(
            "Flickr set id",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )

    directives.read_permission(flickr_collection="cmf.ModifyPortalContent")
    flickr_collection = schema.TextLine(
        title=_(
            "Flickr collection id",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )

    flickr_images = JSONField(
        title=_("Flickr images"),
        description=_(
            "This is a read-only field, only used to return the list of images."
        ),
        default={},
        required=False,
        readonly=True,
    )

    model.fieldset(
        "flickr_settings",
        label=_("Flickr API settings"),
        fields=("flickr_api_key", "flickr_api_secret", "flickr_user_id"),
    )

    directives.read_permission(flickr_api_key="cmf.ModifyPortalContent")
    flickr_api_key = schema.TextLine(
        title=_(
            "Flickr API key",
        ),
        description=_(
            "Use this setting to override site-wide one, in case this "
            "specific album is from a different user.",
        ),
        default="",
        required=False,
        readonly=False,
    )

    directives.read_permission(flickr_api_secret="cmf.ModifyPortalContent")
    flickr_api_secret = schema.TextLine(
        title=_(
            "Flickr API secret",
        ),
        description=_(
            "Use this setting to override site-wide one, in case this "
            "specific album is from a different user.",
        ),
        default="",
        required=False,
        readonly=False,
    )

    directives.read_permission(flickr_user_id="cmf.ModifyPortalContent")
    flickr_user_id = schema.TextLine(
        title=_(
            "Flickr User ID",
        ),
        description=_(
            "Use this setting to override site-wide one, in case this "
            "specific album is from a different user.",
        ),
        default="",
        required=False,
        readonly=False,
    )


@implementer(IFlickrGallery)
@adapter(IFlickrGalleryMarker)
class FlickrGallery:
    def __init__(self, context):
        self.context = context

    @property
    def flickr_set(self):
        if safe_hasattr(self.context, "flickr_set"):
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

    @property
    def flickr_images(self):
        return list(get_images(self.context))

    @flickr_images.setter
    def flickr_images(self, value):
        logger.info("Nothing should be done here")

    @property
    def flickr_api_key(self):
        if safe_hasattr(self.context, "flickr_api_key"):
            return self.context.flickr_api_key
        return None

    @flickr_api_key.setter
    def flickr_api_key(self, value):
        self.context.flickr_api_key = value

    @property
    def flickr_api_secret(self):
        if safe_hasattr(self.context, "flickr_api_secret"):
            return self.context.flickr_api_secret
        return None

    @flickr_api_secret.setter
    def flickr_api_secret(self, value):
        self.context.flickr_api_secret = value

    @property
    def flickr_user_id(self):
        if safe_hasattr(self.context, "flickr_user_id"):
            return self.context.flickr_user_id
        return None

    @flickr_user_id.setter
    def flickr_user_id(self, value):
        self.context.flickr_user_id = value
