from BTrees.IOBTree import IOBTree
from cs_flickrgallery import ANNOTATION_KEY
from plone import api
from plone.base.utils import get_installer
from zope.annotation.interfaces import IAnnotations


def set_images(context, images):
    annotated = IAnnotations(context)
    values = IOBTree()
    for i, image in enumerate(images):
        values[i] = image
    annotated[ANNOTATION_KEY] = values


def get_images(context):
    annotated = IAnnotations(context)
    return annotated.get(ANNOTATION_KEY, IOBTree()).values()


def is_multilingual_installed():
    portal = api.portal.get()
    installer = get_installer(portal)
    return installer.is_product_installed("plone.app.multilingual")
