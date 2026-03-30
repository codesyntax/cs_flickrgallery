"""
The code in this module has been adapted from the code on the
collective.ptg.flickr project published at https://github.com/collective/collective.ptg.flickr

The license of that code (GPL) is retained in this project.

"""

from cs_flickrgallery import _
from cs_flickrgallery.flickr import FlickrClient
from cs_flickrgallery.utils import is_multilingual_installed
from cs_flickrgallery.utils import set_images
from logging import getLogger
from plone import api
from plone.memoize import ram
from Products.Five.browser import BrowserView

import time


try:
    from plone.app.multilingual.api import get_translation_manager
except ImportError:
    get_translation_manager = None

logger = getLogger(__name__)


def cache_key(fun, self):
    return (fun.__name__, self.context.absolute_url(), time.time() // 60 * 60 * 15)


class UpdatePhotosFromFlickr(BrowserView):
    def __call__(self):
        images = self.retrieve_images()
        set_images(self.context, images)
        if is_multilingual_installed():
            manager = get_translation_manager(self.context)
            for translation in manager.get_restricted_translations().values():
                set_images(translation, images)
                logger.info("Images set in translation: %s", translation.getId())

        api.portal.show_message(
            _("Photos imported from Flickr"), request=self.request, type="info"
        )
        return self.request.response.redirect(self.context.absolute_url())

    def assemble_image_information(self, client: FlickrClient, image: dict) -> dict:
        photo = client.get_photo_sizes(photo_id=image.get("id"))
        sizes = photo.get("sizes", {}).get("size", [])
        srcset = []
        for size in sizes:
            srcset.append(f"{size.get('source')} {size.get('width')}w")

        img_url = client.get_large_photo_url(image)

        return {
            "srcset": ", ".join(srcset),
            "sizes": sorted(sizes, key=lambda x: int(x.get("width", 0))),
            "sizes_dict": {item.get("label"): item for item in sizes},
            "image_url": img_url,
            "thumb_url": client.get_mini_photo_url(image),
            "link": client.get_photo_link(image, self.flickr_username),
            "title": image.get("title"),
            "description": "",
            "original_image_url": img_url,
            "download_url": img_url,
            "copyright": "",
            "portal_type": "_flickr",
            "keywords": "",
            "bodytext": "",
        }

    @property
    def flickr_username(self):
        return self.context.flickr_user_id or api.portal.get_registry_record(
            "cs_flickrgallery.flickr_settings.flickr_user_id"
        )

    @property
    def flickr_set(self):
        return self.context.flickr_set

    @property
    def flickr_collection(self):
        return self.context.flickr_collection

    @property
    def flickr_api_key(self):
        return self.context.flickr_api_key or api.portal.get_registry_record(
            "cs_flickrgallery.flickr_settings.flickr_api_key"
        )

    @property
    def flickr_api_secret(self):
        return self.context.flickr_api_secret or api.portal.get_registry_record(
            "cs_flickrgallery.flickr_settings.flickr_api_secret"
        )

    @ram.cache(cache_key)
    def retrieve_images(self):
        client = FlickrClient(self.flickr_api_key, self.flickr_api_secret)

        # These values are expected to be valid. We trust the user.
        user_id = client.get_user_id(self.flickr_username)
        photoset_id = client.get_photoset_id(user_id=user_id, theset=self.flickr_set)
        collection_id = self.flickr_collection

        if photoset_id:
            try:
                photos = client.get_photoset_photos(user_id, photoset_id)
            except Exception:
                log = getLogger(__name__)
                log.info(
                    "Error getting images from Flickr photoset %s",
                    photoset_id,
                )
                return []

        elif collection_id:
            try:
                photos = client.get_collection_photos(user_id, collection_id)
            except Exception:
                log = getLogger(__name__)
                log.info(
                    "Error getting images from Flickr collection %s",
                    collection_id,
                )
                return []
        else:
            log = getLogger(__name__)
            log.info(
                "No Flickr photoset or collection provided, "
                "or not owned by user (%s). No images to show.",
                user_id,
            )
            photos = []

        return [self.assemble_image_information(client, image) for image in photos]
