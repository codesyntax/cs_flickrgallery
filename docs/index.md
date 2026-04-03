---
myst:
  html_meta:
    "description": "cs_flickrgallery Documentation"
    "property=og:description": "A Plone 6 add-on to synchronize and display Flickr photo sets and collections."
    "property=og:title": "cs_flickrgallery"
    "keywords": "cs_flickrgallery, documentation, Plone, Flickr"
---

# cs_flickrgallery

Welcome to the documentation for **cs_flickrgallery**!

`cs_flickrgallery` is a Plone 6 add-on designed to integrate Flickr galleries into a Plone CMS site. It allows content editors to synchronize photos from Flickr sets or collections directly into Plone content objects. 

This architecture prevents making slow API calls on every page load, avoids Flickr API rate limits, and cleanly decouples the presentation layer from the data fetching logic.

## Key Features

- **Classic UI Ready**: Provides an administrative viewlet to trigger synchronization and a default `flickr_gallery_view` to display the photos.
- **Volto / Headless Compatible**: Exposes a standard Plone REST API endpoint (`@update-flickr-photos`) to trigger synchronization, and saves the image data in a read-only JSON field (`flickr_images`) that frontend developers can consume to build custom React components.
- **Granular Control**: Configure global Flickr API keys in the Plone Control Panel, or override them on a per-item basis.

## Structure

This documentation is structured following the [Diátaxis](https://diataxis.fr/) framework:

```{toctree}
:caption: Tutorials
:maxdepth: 2
:hidden: true

tutorials/index
```

```{toctree}
:caption: How to guides
:maxdepth: 2
:hidden: true

how-to-guides/index
```

```{toctree}
:caption: Reference
:maxdepth: 2
:hidden: true

reference/index
```

```{toctree}
:caption: Concepts
:maxdepth: 2
:hidden: true

concepts/index
```

```{toctree}
:caption: Appendices
:maxdepth: 2
:hidden: true

glossary
genindex
```
