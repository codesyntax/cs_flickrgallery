from cs_flickrgallery.utils import get_images
from plone.app.layout.viewlets.common import ViewletBase


class FlickrGalleryAdminViewlet(ViewletBase):
    def get_number_of_photos(self):
        return len(get_images(self.context))
