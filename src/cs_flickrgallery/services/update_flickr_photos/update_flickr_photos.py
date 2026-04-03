from cs_flickrgallery.flickr import FlickrUpdater
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class UpdateFlickrPhotos(Service):
    def reply(self):
        updater = FlickrUpdater(self.context)
        count = updater.update()
        return {"message": f"{count} photos imported from Flickr"}
