from Products.Five.browser import BrowserView
from plone import api
from cs_flickrgallery import _

class UpdatePhotosFromFlickr(BrowserView):
    def __call__(self):
        api.portal.show_message(_('Photos imported from Flickr'), request=self.request, type="info")
        return self.request.response.redirect(self.context.absolute_url())