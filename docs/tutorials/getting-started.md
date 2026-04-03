---
myst:
  html_meta:
    "description": "Getting Started with cs_flickrgallery"
    "property=og:title": "Getting Started"
    "keywords": "Plone, Flickr, tutorial, getting started"
---

# Getting Started

This tutorial provides a step-by-step guide to installing `cs_flickrgallery` and setting up your first Flickr photo gallery in Plone.

## Prerequisites

You need a Flickr API Key and Secret to interact with the Flickr API.
You can obtain one by registering your application on the [Flickr Developer Portal](https://www.flickr.com/services/apps/create/).

## Step 1: Installation

Add the package to your `pyproject.toml` (or `buildout.cfg`):

```toml
[project]
dependencies = [
    # ... other dependencies
    "cs_flickrgallery",
]
```

Restart your Plone instance and navigate to the **Site Setup > Add-ons** control panel to install `cs_flickrgallery`.

## Step 2: Global Configuration

Go to **Site Setup > Flickr Settings**.

Here, enter the global credentials:
- **Flickr User ID**: Your default Flickr NSID (e.g., `12345678@N00`).
- **Flickr API Key**: Your application API Key.
- **Flickr API Secret**: Your application API Secret.

These values act as fallbacks so editors don't have to enter them every time they create a new gallery.

## Step 3: Enable the Behavior

Go to **Site Setup > Dexterity Content Types**.
Select a content type (for example, **Page** or **Document**).
In the **Behaviors** tab, check the box for **Flickr Gallery** (`IFlickrGalleryMarker`) and save.

## Step 4: Create a Gallery

1. Navigate to the root of your site and add a new Page.
2. Fill in the Title and other standard fields.
3. Switch to the new **Flickr album configuration** tab.
4. Enter a **Flickr set id** or **Flickr collection id** that you want to display.
5. Save the page.

## Step 5: Synchronize the Photos

When viewing the saved page in Classic UI, an administrative viewlet will appear near the top of the page for users with editing permissions.

Click the **Update photos from Flickr** button. Plone will connect to Flickr, fetch the images, and store them securely inside the page.

## Step 6: Presentation

Now that the photos are cached:
- **Classic UI:** Click the *Display* menu and select **Flickr Gallery** (`flickr_gallery_view`) to render the built-in photo gallery.
- **Volto:** The photos are automatically available in the standard Plone REST API JSON response for this item under the `flickr_images` field, ready to be mapped into a custom React block by your frontend developers.
