---
myst:
  html_meta:
    "description": "IFlickrGallery Schema Reference"
    "property=og:title": "Behavior Schema"
    "keywords": "Plone, Flickr, behavior, schema"
---

# Behavior Schema

The `IFlickrGalleryMarker` interface marks content to which the `IFlickrGallery` behavior has been applied.
Below is the reference for all fields defined by this behavior and exposed to editors or over the REST API.

## Configuration Fields

| Field Name | Type | Permission | Description |
|---|---|---|---|
| `flickr_set` | `TextLine` | `cmf.ModifyPortalContent` | The ID of the Flickr photoset to display (mutually exclusive with `flickr_collection`). |
| `flickr_collection` | `TextLine` | `cmf.ModifyPortalContent` | The ID of the Flickr collection to display. |

## Override Fields

These fields are used to override the global registry settings on a per-item basis. If they are left blank, the `cs_flickrgallery.flickr_settings` registry configuration is used instead.

| Field Name | Type | Permission | Description |
|---|---|---|---|
| `flickr_user_id` | `TextLine` | `cmf.ModifyPortalContent` | Use this setting to override site-wide ID, in case this specific album is from a different user. |
| `flickr_api_key` | `TextLine` | `cmf.ModifyPortalContent` | Override the site-wide API key. |
| `flickr_api_secret` | `TextLine` | `cmf.ModifyPortalContent` | Override the site-wide API secret. |

## Data Fields

| Field Name | Type | Permission | Description |
|---|---|---|---|
| `flickr_images` | `JSONField` | Public (Read) | This is a read-only field, only used to return the list of synchronized images. Volto developers consume this data directly. |

