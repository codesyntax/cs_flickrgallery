from plone.app.layout.viewlets.common import ViewletBase
from zope.annotation.interfaces import IAnnotations
from cs_flickrgallery import ANNOTATION_KEY
from BTrees.OOBTree import OOBTree


class FlickrGalleryAdminViewlet(ViewletBase):
    def get_number_of_photos(self):
        context = self.context
        annotated = IAnnotations(context)
        annotations = annotated.get(ANNOTATION_KEY, OOBTree())
        return len(annotations.keys())