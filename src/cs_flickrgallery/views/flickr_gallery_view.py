from cs_flickrgallery.utils import get_images
from Products.Five.browser import BrowserView


class FlickrGalleryView(BrowserView):
    def get_images(self):
        return get_images(self.context)
