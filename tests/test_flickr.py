from cs_flickrgallery.flickr import empty
from cs_flickrgallery.flickr import FlickrClient
from cs_flickrgallery.flickr import FlickrUpdater
from unittest.mock import MagicMock
from unittest.mock import patch

import unittest


class DummyContext:
    def __init__(self):
        self.flickr_user_id = "123@N01"
        self.flickr_set = "123456"
        self.flickr_collection = None
        self.flickr_api_key = "dummy_key"
        self.flickr_api_secret = "dummy_secret"
        self.absolute_url = lambda: "http://dummy"


class TestFlickrFunctions(unittest.TestCase):
    def test_empty(self):
        self.assertTrue(empty(None))
        self.assertTrue(empty(""))
        self.assertTrue(empty("   "))
        self.assertFalse(empty("abc"))


class TestFlickrClient(unittest.TestCase):
    @patch("cs_flickrgallery.flickr.flickrapi.FlickrAPI")
    def test_client_init(self, mock_flickrapi):
        client = FlickrClient("key", "secret")
        self.assertEqual(client.api_key, "key")
        self.assertEqual(client.api_secret, "secret")
        mock_flickrapi.assert_called_once_with("key", "secret", format="parsed-json")

    @patch("cs_flickrgallery.flickr.flickrapi.FlickrAPI")
    def test_get_user_id_by_username(self, mock_flickrapi):
        client = FlickrClient("key", "secret")
        # Setup mock response
        mock_client = mock_flickrapi.return_value
        mock_client.people_findByUsername.return_value = {"user": {"nsid": " 456@N01 "}}

        user_id = client.get_user_id("dummyuser")
        self.assertEqual(user_id, "456@N01")
        mock_client.people_findByUsername.assert_called_once_with(username="dummyuser")

    def test_static_urls(self):
        photo = {"id": "123", "secret": "abc", "server": "456", "farm": "1"}
        self.assertEqual(
            FlickrClient.get_mini_photo_url(photo),
            "https://farm1.static.flickr.com/456/123_abc_s.jpg",
        )
        self.assertEqual(
            FlickrClient.get_large_photo_url(photo),
            "https://farm1.static.flickr.com/456/123_abc_b.jpg",
        )
        self.assertEqual(
            FlickrClient.get_photo_link(photo, "myuser"),
            "https://www.flickr.com/photos/myuser/123/sizes/o/",
        )


class TestFlickrUpdater(unittest.TestCase):
    @patch("cs_flickrgallery.flickr.is_multilingual_installed")
    @patch("cs_flickrgallery.flickr.FlickrUpdater.retrieve_images")
    @patch("cs_flickrgallery.flickr.set_images")
    def test_update_saves_images(self, mock_set_images, mock_retrieve_images, mock_ml):
        mock_ml.return_value = False
        context = DummyContext()
        updater = FlickrUpdater(context)

        mock_images = [{"title": "Pic 1"}, {"title": "Pic 2"}]
        mock_retrieve_images.return_value = mock_images

        count = updater.update()

        self.assertEqual(count, 2)
        mock_set_images.assert_called_once_with(context, mock_images)
