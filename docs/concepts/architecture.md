---
myst:
  html_meta:
    "description": "cs_flickrgallery Architecture Concepts"
    "property=og:title": "Architecture"
    "keywords": "Plone, Flickr, Architecture, Annotation, Caching"
---

# Architecture

`cs_flickrgallery` relies heavily on a decoupled caching model instead of a live proxy model. 
This document explains the reasons behind the design.

## Why Synchronize?

When a visitor loads a page containing a Flickr gallery, they expect the page to load instantly.
If Plone were to fetch the photos on the fly from Flickr:
1. **Latency**: The TTFB (Time to First Byte) would increase drastically as Plone waits on an external API response.
2. **Rate Limiting**: High traffic pages would hammer the Flickr API, leading to potential HTTP `429 Too Many Requests` responses and broken galleries.

To fix this, `cs_flickrgallery` stores the response in **Zope Annotations**.

By using an explicit synchronization trigger (via the `@@update_photos_from_flickr` viewlet button or the `@update-flickr-photos` REST API endpoint), content editors pull the data down *once*. It is processed and saved inside the OOBTree of the content object's `IAnnotations`.

From then on, the data is served directly from the ZODB alongside the content item's fields, providing instantaneous load times and zero dependency on Flickr's uptime.

## Decoupled Presentation

Historically, Plone add-ons bundled the data fetching and the HTML rendering tightly together inside a Browser View.

With the shift to headless CMS environments, `cs_flickrgallery` fully decouples the two:
- **Fetching Logic**: Encapsulated entirely in the `FlickrUpdater` Python class. It writes data to the annotations and exits.
- **Presentation Logic**: A JSON field (`flickr_images`) merely reads the annotations and exposes it to the REST API payload.

Volto developers do not need to build API proxies in Node.js or worry about Flickr API keys. They can read the standardized `flickr_images` JSON payload from the Plone REST API out-of-the-box and implement their own presentation layer in React.

## Behavior-Driven Development

By providing this functionality as a Plone **Behavior** (`cs_flickrgallery.behaviors.flickr_gallery.IFlickrGalleryMarker`) rather than a hardcoded Content Type, the architecture is extremely flexible.

Developers are not forced to use a specific `FlickrAlbum` content type. Instead, they can build their own custom content types (e.g., a `Portfolio`, `Event`, or `News Item`) and simply attach the `IFlickrGalleryMarker` behavior to it.

Once attached, the content type instantly inherits:
1. The backend configuration fields (`flickr_set`, API overrides).
2. The administrative synchronization viewlet and REST API endpoint.
3. The `flickr_images` serialized JSON data.

This compositional approach allows for powerful, custom content models without duplicating code.
