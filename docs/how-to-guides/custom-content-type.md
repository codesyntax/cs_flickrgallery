---
myst:
  html_meta:
    "description": "How to create a custom content type with cs_flickrgallery"
    "property=og:title": "Custom Content Type"
    "keywords": "Plone, Flickr, behavior, dexterity, content type"
---

# Creating a Custom Content Type

Because `cs_flickrgallery` exposes its functionality via a Plone Behavior rather than a fixed content type, you can easily attach Flickr synchronization capabilities to any custom content type you create in your own add-on policy package.

This guide shows you how to define a custom `Portfolio` content type that inherits the Flickr gallery features.

## Step 1: Create your Content Type XML

In your own Plone package, define the new Dexterity content type by creating an XML file in your GenericSetup profile (e.g., `profiles/default/types/Portfolio.xml`).

The key is to add `cs_flickrgallery.behaviors.flickr_gallery.IFlickrGalleryMarker` to the `<property name="behaviors">` list.

```xml
<?xml version="1.0"?>
<object name="Portfolio" meta_type="Dexterity FTI" i18n:domain="plone"
        xmlns:i18n="http://xml.zope.org/namespaces/i18n">
  
  <property name="title" i18n:translate="">Portfolio Item</property>
  <property name="description" i18n:translate=""></property>
  <property name="icon_expr">string:${portal_url}/document_icon.png</property>
  <property name="factory">Portfolio</property>
  
  <property name="add_view_expr">string:${folder_url}/++add++Portfolio</property>
  <property name="link_target"></property>
  <property name="immediate_view">view</property>
  <property name="global_allow">True</property>
  <property name="filter_content_types">True</property>
  <property name="allowed_content_types" />
  <property name="allow_discussion">False</property>
  <property name="default_aliases">
    <alias from="(Default)" to="(dynamic view)"/>
    <alias from="view" to="(selected layout)"/>
    <alias from="edit" to="@@edit"/>
    <alias from="sharing" to="@@sharing"/>
  </property>
  <property name="default_view">view</property>
  <property name="view_methods">
    <element value="view"/>
    <element value="flickr_gallery_view"/>
  </property>
  <property name="klass">plone.dexterity.content.Container</property>

  <!-- Enable the Flickr Gallery behavior -->
  <property name="behaviors">
    <element value="plone.dublincore"/>
    <element value="plone.namefromtitle"/>
    <element value="cs_flickrgallery.behaviors.flickr_gallery.IFlickrGalleryMarker"/>
  </property>
  
</object>
```

## Step 2: Register the Type in types.xml

Ensure your `Portfolio.xml` is registered in `profiles/default/types.xml`:

```xml
<?xml version="1.0" ?>
<object name="portal_types" meta_type="Plone Types Tool">
    <property name="title">Controls the available content types in your portal</property>
    <object name="Portfolio" meta_type="Dexterity FTI" />
</object>
```

## Step 3: Install your Package

When you install or reinstall your policy package:
1. Plone will create the new `Portfolio` content type.
2. Because it has the `IFlickrGalleryMarker` behavior, the "Flickr album configuration" and "Flickr API settings" tabs will automatically appear on the edit form.
3. The administrative synchronization viewlet will appear when viewing the item.
4. The standard REST API endpoint (`@update-flickr-photos`) will become available for the item.
5. The `flickr_images` field will automatically be serialized in REST API responses.

This pattern allows you to compose complex, domain-specific content types (like Portfolios, Events, or News Items) that effortlessly integrate with Flickr.
