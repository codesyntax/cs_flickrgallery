---
myst:
  html_meta:
    "description": "Flickr Update REST API Endpoint Reference"
    "property=og:title": "REST API Endpoint"
    "keywords": "Plone, Flickr, REST API, Volto"
---

# REST API Endpoint

`cs_flickrgallery` exposes a custom REST API endpoint to trigger a synchronization from the Flickr API without needing to use the Plone Classic UI administration viewlet.

## `@update-flickr-photos`

Forces the Plone context to connect to the configured Flickr API and download/cache the latest images.

**URL**: `/@update-flickr-photos`  
**Method**: `POST`  
**Permission**: `cmf.ModifyPortalContent`  
**Condition**: The context must implement the `IFlickrGalleryMarker` interface.

### Success Response

**Code**: `200 OK`  
**Content-Type**: `application/json`  

**Example**:
```json
{
  "message": "25 photos imported from Flickr"
}
```

### Error Responses

**Code**: `401 Unauthorized`  
**Content-Type**: `application/json`  
**Condition**: If the user does not have `cmf.ModifyPortalContent` permission.

**Example**:
```json
{
  "error": {
    "type": "Unauthorized",
    "message": "You are not authorized to access this resource."
  }
}
```
