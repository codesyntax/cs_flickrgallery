from plone.app.layout.viewlets.common import ViewletBase
from zope.annotation.interfaces import IAnnotations
from cs_flickrgallery import ANNOTATION_KEY
from BTrees.OOBTree import OOBTree
from cs_flickrgallery.utils import get_images


class FlickrGalleryAdminViewlet(ViewletBase):
    def get_number_of_photos(self):
        return len(get_images(self.context))