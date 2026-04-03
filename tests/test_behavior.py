from cs_flickrgallery.behaviors.flickr_gallery import IFlickrGallery
from cs_flickrgallery.behaviors.flickr_gallery import IFlickrGalleryMarker
from cs_flickrgallery.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.interface import alsoProvides

import unittest


class TestBehavior(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "doc")
        self.doc = self.portal["doc"]
        from cs_flickrgallery.behaviors.flickr_gallery import FlickrGallery
        from zope.component import getGlobalSiteManager

        getGlobalSiteManager().registerAdapter(FlickrGallery)
        alsoProvides(self.doc, IFlickrGalleryMarker)
        self.adapted = IFlickrGallery(self.doc)

    def test_behavior_properties(self):
        # Set values
        self.adapted.flickr_set = "12345"
        self.adapted.flickr_user_id = "user1"
        self.adapted.flickr_api_key = "mykey"

        # Check they are saved on the context
        self.assertEqual(self.doc.flickr_set, "12345")
        self.assertEqual(self.doc.flickr_user_id, "user1")
        self.assertEqual(self.doc.flickr_api_key, "mykey")

        # Read via adapted interface
        self.assertEqual(self.adapted.flickr_set, "12345")
        self.assertEqual(self.adapted.flickr_user_id, "user1")
        self.assertEqual(self.adapted.flickr_api_key, "mykey")

    def test_flickr_images_property(self):
        from cs_flickrgallery.utils import set_images

        # Verify initial state is empty
        self.assertEqual(len(list(self.adapted.flickr_images)), 0)

        # Set some fake images
        mock_images = [{"title": "Test 1"}, {"title": "Test 2"}]
        set_images(self.doc, mock_images)

        images = list(self.adapted.flickr_images)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0]["title"], "Test 1")
