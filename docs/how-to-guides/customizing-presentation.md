---
myst:
  html_meta:
    "description": "How to customize the presentation of cs_flickrgallery"
    "property=og:title": "Customizing Presentation"
    "keywords": "Plone, Flickr, Volto, views, template"
---

# Customizing Presentation

The `cs_flickrgallery` package securely synchronizes photo data from the Flickr API directly into Plone annotations. By design, the add-on attempts to decouple the display from the data fetching logic.

## Classic UI Integration

Out-of-the-box, the package registers a default view called `flickr_gallery_view` for any content type that implements the `IFlickrGalleryMarker` behavior.

If the default template does not match your site's aesthetic, you can easily override it using `z3c.jbot`.

1. Create a `browser/overrides` directory inside your policy or theme package.
2. Create a file named `cs_flickrgallery.views.flickr_gallery_view.pt`.
3. Add your custom HTML/TAL structure.

You can access the synchronized images directly using the `flickr_images` attribute of the behavior adapter:

```html
<tal:block tal:define="gallery nocall:context/@@flickr_gallery_view">
    <div class="my-custom-gallery" tal:repeat="image gallery/flickr_images">
        <img tal:attributes="src image/image_url; alt image/title" />
    </div>
</tal:block>
```

## Volto Integration

For Volto, the presentation is entirely delegated to your frontend developers. The add-on deliberately avoids shipping a built-in Volto Block to give you total control over the design system (e.g., using masonry grids, lightboxes, carousels, etc.).

When you request a content object from the Plone REST API that has the `IFlickrGallery` behavior enabled, the API automatically serializes the `flickr_images` JSON field:

```json
{
  "@id": "http://localhost:8080/Plone/my-gallery",
  "@type": "Document",
  "title": "My Gallery",
  "flickr_set": "123456789",
  "flickr_images": [
    {
      "title": "My Photo Title",
      "image_url": "https://farm1.static.flickr.com/456/123_abc_b.jpg",
      "thumb_url": "https://farm1.static.flickr.com/456/123_abc_s.jpg",
      "link": "https://www.flickr.com/photos/user/123/sizes/o/",
      "sizes": ["..."],
      "srcset": "..."
    }
  ]
}
```

In your custom Volto View or Block component, simply access `content.flickr_images` from the Redux state or props, and map over the array to render your preferred React image components.
