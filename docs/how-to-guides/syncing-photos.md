---
myst:
  html_meta:
    "description": "How to sync photos in cs_flickrgallery"
    "property=og:title": "Syncing Photos"
    "keywords": "Plone, Flickr, sync, REST API, Volto"
---

# Syncing Photos

Because `cs_flickrgallery` fetches and caches image metadata directly into Plone content objects to prevent performance degradation and rate limiting, you must actively synchronize the content object with Flickr whenever you want to pull in the latest changes from the external set or collection.

## Classic UI

When you view a piece of content that has the `IFlickrGalleryMarker` behavior applied and has a Flickr Set or Collection ID configured, an administrative viewlet will automatically appear at the top of the page.

1. Ensure you have the `cmf.ModifyPortalContent` permission (typically Editor, Site Administrator, or Manager).
2. Click the **Update photos from Flickr** button displayed in the viewlet.
3. Plone will redirect you back to the current page with an informational message indicating that the photos were successfully imported.

Under the hood, this simply makes a `POST` request to the `@@update_photos_from_flickr` view.

## Volto / Headless Environment

If you are building a custom frontend in Volto, you do not have access to the Classic UI viewlets. Instead, you can trigger the exact same synchronization process using the standard Plone REST API.

Send an authenticated `POST` request to the `@update-flickr-photos` endpoint on the content object.

**Example using `curl`**:

```bash
curl -X POST -H "Accept: application/json" \
     -u admin:admin \
     http://localhost:8080/Plone/my-gallery/@update-flickr-photos
```

**Example using JavaScript (`fetch`)**:

```javascript
fetch("http://localhost:8080/Plone/my-gallery/@update-flickr-photos", {
  method: "POST",
  headers: {
    "Accept": "application/json",
    "Authorization": "Basic YWRtaW46YWRtaW4=" // Replace with a valid Bearer token
  }
})
.then(response => response.json())
.then(data => console.log(data.message)); // Expected: "X photos imported from Flickr"
```

Once this request succeeds, the `flickr_images` field on the content object will be fully populated and up-to-date with the latest photos from Flickr.
