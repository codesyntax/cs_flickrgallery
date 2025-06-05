# cs_flickrgallery

An addon for Plone to show photos from Flickr

## Installation

Install cs_flickrgallery adding it to your project's dependencies.

Then go to the Plone's add-on controlpanel and install it from there.

## Configuration and usage

A new control panel will be added in the Plone's Site Setup, where you should configure the Flickr API Key and the username
from which your images will be fetched.

This add-on createse a new behavior that you should apply to your content-types of choice (for example to pages).

When doing so, a new fieldset will be added to that content-type's edit page where you can set the Flickr set or collection that will be imported into Plone.

After setting all, a viewlet will show the status of the import process with the number of imported photos, and will allow refreshing the values.

This package provides a simple view called `flickr_gallery_view` that can be applied to all content-types implementing the behavior so the images are shown in the Plone template.

If you are applying the behavior in your project add-on, you can also apply the view using generic setup profile, as follows, in a {file}`Document.xml` (for example):

```xml
...
<property name="behaviors"
            purge="false"
  >
    ...
    <element value="cs_flickrgallery.flickr_gallery" />
  </property>
...
  <property name="view_methods" purge="false">
    ...
    <element value="flickr_gallery_view" />
    <element value="view" />
  </property>
...
```

It will be common that you want to show the images using a gallery script of your choice, to do so, you can call the utility method `cs_flickrgallery.utils.get_images` passing the context object where you have saved the collection id, and it will return a list with items representing the image.

Each of the images has the following structure:

```python

    {
        'srcset': "https://  75w, https:// 100w, https:// 200w", # perfect to render a img tag with srcset
        'sizes': [{'label': 'Square', 'width': 75}, ...],        # all image sizes with their attributes, sorted from smallest to largest
        'sizes_dict': {'Large': {'width': 75, ...}, ...}         # dict with all sizes, using size label as key
        'image_url': "https://",                                 # large photo url
        'thumb_url': "https://",                                 # mini photo url
        'link': "https://",                                      # photo's url in flickr
        'title': "Some Title",
        'description': "",
        'original_image_url': "https://",                        # original photo url
        'download_url': "https://",                              # download url
        'copyright': '',
        'portal_type': '_flickr',
        'keywords': '',
        'bodytext': ''
    }

```

## Contribute

- [Issue tracker](https://github.com/codesyntax/cs_flickrgallery/issues)
- [Source code](https://github.com/codesyntax/cs_flickrgallery/)

### Prerequisites ✅

- An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
- [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
- [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
- [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
- [Docker](https://docs.docker.com/get-started/get-docker/) (optional)

### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone git@github.com:codesyntax/cs_flickrgallery.git
    cd cs_flickrgallery
    ```

2.  Install this code base.

    ```shell
    make install
    ```

## License

The project is licensed under GPLv2.

Parts of this project have been adapted from [collective.ptg.flickr](https://github.com/collective/collective.ptg.flickr)

## Credits and acknowledgements 🙏

Generated using [Cookieplone (0.9.7)](https://github.com/plone/cookieplone) and [cookieplone-templates (ed4fa08)](https://github.com/plone/cookieplone-templates/commit/ed4fa08f29fbca564b8871163f66a67ed5f4acf4) on 2025-06-04 13:23:09.646096. A special thanks to all contributors and supporters!
