from .utils import get_app
from .utils import get_site
from .utils import setup_logger_console
from cs_flickrgallery import logger
from cs_flickrgallery.behaviors.flickr_gallery import IFlickrGalleryMarker
from cs_flickrgallery.utils import get_images
from plone import api
from plone.i18n.interfaces import ILanguageSchema
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import hooks

import argparse
import sys
import transaction


def _parse_args(description: str, options: dict, args: list):
    parser = argparse.ArgumentParser(description=description)
    for key, help_text in options.items():
        if key.startswith("-"):
            parser.add_argument(key, action="store_true", help=help_text)
        else:
            parser.add_argument(key, help=help_text)
    namespace, _ = parser.parse_known_args(args[1:])
    return namespace


def main(args=sys.argv):
    namespace = _parse_args(
        "Import content into a Plone Site",
        {
            "zopeconf": "Path to zope.conf",
            "site": "Plone site ID to export the content from",
        },
        args,
    )
    app = get_app(namespace.zopeconf)

    setup_logger_console(logger)
    site = get_site(app, namespace.site, logger)
    with hooks.site(site), api.env.adopt_roles(["Manager"]):
        registry = getUtility(IRegistry)
        language_settings = registry.forInterface(
            ILanguageSchema, prefix="plone", check=False
        )
        default_language = language_settings.default_language
        brains = api.content.find(
            Language=default_language,
            object_provides=IFlickrGalleryMarker.__identifier__,
        )
        logger.info("Found %s items to process", len(brains))
        for brain in brains:
            logger.info("Processing gallery at %s", brain.getPath())
            obj = brain.getObject()
            if obj.flickr_set:
                if len(get_images(obj)):
                    logger.info("Gallery already has images")
                else:
                    update_photos_from_flickr = getMultiAdapter(
                        (obj, site.REQUEST), name="update_photos_from_flickr"
                    )
                    update_photos_from_flickr()
                    logger.info("Gallery processed")
            else:
                logger.info("Gallery not linked to Flickr")

        transaction.commit()
        logger.info("Done")
