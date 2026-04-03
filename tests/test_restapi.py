from cs_flickrgallery.behaviors.flickr_gallery import IFlickrGalleryMarker
from cs_flickrgallery.testing import FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.testing.zope import Browser
from unittest.mock import patch
from zope.interface import alsoProvides

import requests
import transaction
import unittest
import urllib.error


class TestRESTAPI(unittest.TestCase):
    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc")
        self.doc = self.portal["doc"]
        alsoProvides(self.doc, IFlickrGalleryMarker)
        transaction.commit()

    @patch(
        "cs_flickrgallery.services.update_flickr_photos.update_flickr_photos.FlickrUpdater.update"
    )
    def test_update_flickr_photos_endpoint(self, mock_update):
        # Setup mock
        mock_update.return_value = 5

        # Test endpoint as manager
        b = Browser(self.layer["app"])
        b.addHeader(
            "Authorization", "Basic %s:%s" % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        b.addHeader("Accept", "application/json")
        b.post(self.doc.absolute_url() + "/@update-flickr-photos", data=b"")

        self.assertEqual(b.headers["status"], "200 OK")
        self.assertIn("5 photos imported from Flickr", str(b.contents))
        mock_update.assert_called_once()

    def test_update_flickr_photos_unauthorized(self):
        # Anonymous users should get 401
        b = Browser(self.layer["app"])
        b.addHeader("Accept", "application/json")
        with self.assertRaises(urllib.error.HTTPError) as err:
            b.post(self.doc.absolute_url() + "/@update-flickr-photos", data=b"")

        self.assertEqual(err.exception.code, 401)
