import flickrapi
import logging


logger = logging.getLogger(__name__)

SIZES = {
    "small": {"width": 500, "height": 375},
    "medium": {"width": 640, "height": 480},
    "large": {"width": 1024, "height": 768},
    "thumb": {"width": 72, "height": 72},
    "flickr": {"small": "_m", "medium": "", "large": "_b"},
}


def empty(v):
    return v is None or len(v.strip()) == 0


class FlickrClient:
    """A reusable wrapper around flickrapi to interact with Flickr."""

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = flickrapi.FlickrAPI(
            api_key or "",
            api_secret or "",
            format="parsed-json",
        )

    def get_user_id(self, username: str) -> str | None:
        """Retrieves a Flickr NSID for a given username or ID."""
        if empty(username):
            logger.info("No Flickr username or ID provided")
            return None

        username = username.strip()

        # Must be an username.
        try:
            return (
                self.client
                .people_findByUsername(username=username)
                .get("user", {})
                .get("nsid", "")
                .strip()
            )

        # No ? Must be an ID then.
        except Exception:
            try:
                return (
                    self.client
                    .people_getInfo(user_id=username)
                    .get("person", {})
                    .get("nsid", "")
                    .strip()
                )
            except Exception:
                logger.info("Can't find Flickr username or ID")

        return None

    def get_photoset_id(self, user_id: str | None, theset: str | None) -> str | None:
        """Retrieves a photoset ID for a user matching the title or ID."""
        if user_id is None:
            return None

        if empty(theset):
            return None

        theset = theset.strip()
        photosets = (
            self.client.photosets
            .getList(user_id=user_id)
            .get("photosets", {})
            .get("photoset", [])
        )

        for photoset in photosets:
            photoset_title = photoset.get("title", {}).get("_content", "")
            photoset_id = photoset.get("id")

            # Matching title or ID means we found it.
            if theset in (photoset_title, photoset_id):
                return photoset_id

        logger.info("Can't find Flickr photoset, or not owned by user (%s).", user_id)

        return None

    def get_collection_sets(self, user_id: str, collection_id: str):
        """Yields all photosets inside a collection."""
        # Exception handling is expected to be made by calling context.
        yield from (
            self.client.collections
            .getTree(user_id=user_id, collection_id=collection_id)
            .get("collections", {})
            .get("collection", [])
        )

    def get_photoset_photos(self, user_id: str, photoset_id: str):
        """Yields all photos inside a photoset."""
        # Exception handling is expected to be made by calling context.
        yield from (
            self.client.photosets
            .getPhotos(
                user_id=user_id,
                photoset_id=photoset_id,
                extras="date_upload",
                media="photos",
            )
            .get("photoset", {})
            .get("photo", [])
        )

    def get_collection_photos(self, user_id: str, collection_id: str):
        """Yields all photos inside all photosets of a collection, most recent first."""
        photos = []
        for photoset in self.get_collection_sets(user_id, collection_id):
            photoset_id = photoset.get("id")
            for photo in self.get_photoset_photos(user_id, photoset_id):
                photos.append(photo)

        # Most recent first.
        photos.sort(key=lambda p: p.get("dateupload", ""), reverse=True)

        return iter(photos)

    def get_photo_sizes(self, photo_id: str):
        """Retrieves sizes for a given photo."""
        return self.client.photos.getSizes(photo_id=photo_id)

    @staticmethod
    def get_mini_photo_url(photo: dict) -> str:
        return f"https://farm{photo.get('farm')}.static.flickr.com/{photo.get('server')}/{photo.get('id')}_{photo.get('secret')}_s.jpg"

    @staticmethod
    def get_photo_link(photo: dict, username: str) -> str:
        return f"https://www.flickr.com/photos/{username}/{photo.get('id')}/sizes/o/"

    @staticmethod
    def get_large_photo_url(photo: dict) -> str:
        return f"https://farm{photo.get('farm')}.static.flickr.com/{photo.get('server')}/{photo.get('id')}_{photo.get('secret')}{SIZES['flickr']['large']}.jpg"
