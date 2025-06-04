from Products.Five.browser import BrowserView
from cs_flickrgallery.utils import get_images

class FlickrGalleryView(BrowserView):
    def get_images(self):
        return get_images(self.context)