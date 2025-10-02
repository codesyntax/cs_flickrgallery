"""
The code in this module has been adapted from the code on the
collective.ptg.flickr project published at https://github.com/collective/collective.ptg.flickr

The license of that code (GPL) is retained in this project.

"""

import time
from logging import getLogger

import flickrapi
from cs_flickrgallery import _
from cs_flickrgallery.utils import is_multilingual_installed, set_images
from plone import api
from plone.memoize import ram
from Products.Five.browser import BrowserView

try:
    from plone.app.multilingual.api import get_translation_manager
except ImportError:
    get_translation_manager = None

logger = getLogger(__name__)


def empty(v):
    return v is None or len(v.strip()) == 0


def cache_key(fun, self):
    return (fun.__name__, self.context.absolute_url(), time.time() // 60 * 60 * 15)


SIZES = {
    "small": {"width": 500, "height": 375},
    "medium": {"width": 640, "height": 480},
    "large": {"width": 1024, "height": 768},
    "thumb": {"width": 72, "height": 72},
    "flickr": {"small": "_m", "medium": "", "large": "_b"},
}


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

    def assemble_image_information(self, image):
        photo = self.flickr.photos.getSizes(photo_id=image.get("id"))
        sizes = photo.get("sizes", {}).get("size", [])
        srcset = []
        for size in sizes:
            srcset.append(f"{size.get('source')} {size.get('width')}w")

        img_url = self.get_large_photo_url(image)

        return {
            "srcset": ", ".join(srcset),
            "sizes": sorted(sizes, key=lambda x: x["width"]),
            "sizes_dict": {item.get("label"): item for item in sizes},
            "image_url": img_url,
            "thumb_url": self.get_mini_photo_url(image),
            "link": self.get_photo_link(image),
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
        return api.portal.get_registry_record(
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
        return api.portal.get_registry_record(
            "cs_flickrgallery.flickr_settings.flickr_api_key"
        )

    @property
    def flickr_api_secret(self):
        return api.portal.get_registry_record(
            "cs_flickrgallery.flickr_settings.flickr_api_secret"
        )

    def get_flickr_user_id(self):
        flickr = self.flickr

        if empty(self.flickr_username):
            log = getLogger(__name__)
            log.info("No Flickr username or ID provided")

            return None

        username = self.flickr_username.strip()

        # Must be an username.
        try:
            return (
                flickr.people_findByUsername(username=username)
                .find("user")
                .get("nsid")
                .strip()
            )

        # No ? Must be an ID then.
        except Exception:
            try:
                return (
                    flickr.people_getInfo(user_id=username)
                    .find("person")
                    .get("nsid")
                    .strip()
                )

            except Exception:
                log = getLogger(__name__)
                log.info("Can't find Flickr username or ID")

        return None

    def get_flickr_photoset_id(self, user_id):
        flickr = self.flickr

        if user_id is None:
            return None

        # This could mean we're using a collection instead of a set.
        if empty(self.flickr_set):
            return None

        theset = self.flickr_set.strip()
        # photosets = flickr.photosets_getList(
        #     user_id=user_id).find('photosets').getchildren()
        photosets = (
            flickr.photosets.getList(user_id=user_id)
            .get("photosets", {})
            .get("photoset", [])
        )

        for photoset in photosets:
            photoset_title = photoset.get("title", {}).get("_content", "")
            photoset_id = photoset.get("id")

            # Matching title or ID means we found it.
            if theset in (photoset_title, photoset_id):
                return photoset_id

        log = getLogger(__name__)
        log.info("Can't find Flickr photoset, or not owned by user (%s).", user_id)

        return None

    def gen_collection_sets(self, user_id, collection_id):
        flickr = self.flickr

        # Yield all photosets.
        # Exception handling is expected to be made by calling context.
        yield from (
            flickr.collections.getTree(user_id=user_id, collection_id=collection_id)
            .get("collections", {})
            .get("collection", [])
        )

    def gen_photoset_photos(self, user_id, photoset_id):
        flickr = self.flickr

        # Yield all photos.
        # Exception handling is expected to be made by calling context.

        yield from (
            flickr.photosets.getPhotos(
                user_id=user_id,
                photoset_id=photoset_id,
                extras="date_upload",
                media="photos",
            )
            .get("photoset", {})
            .get("photo", [])
        )

    def gen_collection_photos(self, user_id, collection_id):
        # Collect every single photo from that collection.
        photos = []
        for photoset in self.gen_collection_sets(user_id, collection_id):
            photoset_id = photoset.attrib["id"]
            for photo in self.gen_photoset_photos(user_id, photoset_id):
                photos.append(photo)

        # Most recent first.
        photos.sort(key=lambda p: p.attrib["dateupload"], reverse=True)

        # This could be a large list,
        # but the retrieve_images method will slice it.
        return iter(photos)

    def get_mini_photo_url(self, photo):
        return f"https://farm{photo.get('farm')}.static.flickr.com/{photo.get('server')}/{photo.get('id')}_{photo.get('secret')}_s.jpg"

    def get_photo_link(self, photo):
        return f"https://www.flickr.com/photos/{self.flickr_username}/{photo.get('id')}/sizes/o/"

    def get_large_photo_url(self, photo):
        return f"https://farm{photo.get('farm')}.static.flickr.com/{photo.get('server')}/{photo.get('id')}_{photo.get('secret')}{SIZES['flickr']['large']}.jpg"

    @property
    def flickr(self):
        """
        Returns a FlickrAPI instance.
        API key and secret both come from settings interface.
        - self.settings.flickr_api_key
        - self.settings.flickr_api_secret


        """
        return flickrapi.FlickrAPI(
            self.flickr_api_key or "",
            self.flickr_api_secret or "",
            format="parsed-json",
        )

    @ram.cache(cache_key)
    def retrieve_images(self):
        # These values are expected to be valid. We trust the user.
        user_id = self.flickr_username
        photoset_id = self.get_flickr_photoset_id(user_id=user_id)
        collection_id = self.flickr_collection

        if photoset_id:
            try:
                photos = self.gen_photoset_photos(user_id, photoset_id)
            except Exception:
                log = getLogger(__name__)
                log.info(
                    "Error getting images from Flickr photoset %s",
                    photoset_id,
                )

                return []

        elif collection_id:
            try:
                photos = self.gen_collection_photos(user_id, collection_id)
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

        return [self.assemble_image_information(image) for image in photos]
