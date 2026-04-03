from cs_flickrgallery import _
from cs_flickrgallery.flickr import FlickrUpdater
from logging import getLogger
from plone import api
from Products.Five.browser import BrowserView


logger = getLogger(__name__)


class UpdatePhotosFromFlickr(BrowserView):
    def __call__(self):
        updater = FlickrUpdater(self.context)
        updater.update()

        api.portal.show_message(
            _("Photos imported from Flickr"), request=self.request, type="info"
        )
        return self.request.response.redirect(self.context.absolute_url())
