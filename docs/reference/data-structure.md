---
myst:
  html_meta:
    "description": "Flickr JSON Data Structure"
    "property=og:title": "Data Structure"
    "keywords": "Plone, Flickr, JSON, schema, Volto"
---

# Data Structure

When synchronized, `cs_flickrgallery` translates raw Flickr API data into a predictable JSON payload. 

This array is saved to the `flickr_images` field on the content object.

## `flickr_images` Schema

The `flickr_images` field is an array of objects. Each object represents one photo.

| Key | Type | Description |
|---|---|---|
| `title` | `string` | The title of the photo on Flickr. |
| `description` | `string` | The description of the photo. |
| `image_url` | `string` | The URL for the `large` version of the photo (`_b` suffix). |
| `thumb_url` | `string` | The URL for the `small` version of the photo (`_s` suffix). |
| `original_image_url` | `string` | The URL for the `large` version of the photo. |
| `download_url` | `string` | The URL for the `large` version of the photo. |
| `link` | `string` | A permanent link to view the image on the Flickr website. |
| `sizes` | `array` | A list of available photo sizes/resolutions returned by Flickr. |
| `sizes_dict` | `object` | An object mapping size labels (e.g. "Medium", "Large") to size objects. |
| `srcset` | `string` | A comma-separated string suitable for an HTML `<img>` `srcset` attribute. |
| `portal_type` | `string` | Fixed to `_flickr`. |
| `copyright` | `string` | Always empty by default. |
| `keywords` | `string` | Always empty by default. |
| `bodytext` | `string` | Always empty by default. |
