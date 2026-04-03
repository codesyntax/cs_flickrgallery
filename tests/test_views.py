from cs_flickrgallery.behaviors.flickr_gallery import IFlickrGalleryMarker
from cs_flickrgallery.testing import FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.testing.zope import Browser
from unittest.mock import patch
from zope.interface import alsoProvides

import transaction
import unittest


class TestViews(unittest.TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc")
        self.doc = self.portal["doc"]
        alsoProvides(self.doc, IFlickrGalleryMarker)
        transaction.commit()

    @patch("cs_flickrgallery.views.update_photos_from_flickr.FlickrUpdater.update")
    def test_update_photos_from_flickr_view(self, mock_update):
        mock_update.return_value = 5

        b = Browser(self.layer["app"])
        b.addHeader("Authorization", f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}")

        # Test view performs redirect and update is called
        b.post(self.doc.absolute_url() + "/@@update_photos_from_flickr", data=b"")
        mock_update.assert_called_once()
        self.assertIn(self.doc.absolute_url(), b.url)

    def test_flickr_gallery_view(self):
        # Set some fake images using the utils
        from cs_flickrgallery.utils import set_images

        mock_images = [{"title": "Pic 1 Title", "srcset": "foo"}]
        set_images(self.doc, mock_images)
        transaction.commit()

        b = Browser(self.layer["app"])
        b.addHeader("Authorization", f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}")

        b.open(self.doc.absolute_url() + "/@@flickr_gallery_view")
        self.assertEqual(b.headers["status"], "200 OK")
        self.assertIn("Pic 1 Title", str(b.contents))
