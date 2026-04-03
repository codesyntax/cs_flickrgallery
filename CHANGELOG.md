# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 1.5 (2026-04-03)


### New features:

- - Create `update-flickr-photos` REST API endpoint to trigger photo synchronization from Flickr @erral
  - Refactor the photo synchronization logic into a reusable `FlickrUpdater` class located in `cs_flickrgallery.flickr` @erral 
- Replace the default documentation placeholders with a custom Flickr-inspired logo and favicon @erral 


### Bug fixes:

- Do not expose Flickr details in REST API @erral 


### Internal:

- Add GitHub Actions workflow to automatically publish Sphinx documentation to GitHub Pages @erral 
- Add documentation URL to README and pyproject.toml @erral 
- Add test coverage for FlickrClient, IFlickrGallery behavior, Classic UI views, and the @update-flickr-photos REST API endpoint @erral 
- Update Development Status classifier to 5 - Production/Stable @erral 


### Documentation:

- Add Sphinx documentation structure using the cookieplone `documentation_starter` subtemplate @erral 
- Add explanation of behavior-driven architecture design choices in documentation @erral 
- Add how-to guide for creating custom content types using the Flickr Gallery behavior @erral 
- Write complete documentation covering tutorials, how-to guides, reference, and concepts @erral 

## 1.3.1 (2026-03-30)


### Bug fixes:

- Flicrk Api key is not required in behavior field @erral 

## 1.3 (2026-03-30)


### New features:

- Allow configuring local Flickr API settings to override site-wide settings @erral 


### Bug fixes:

- Allow entering usernames and delegate converting it user-id @erral 


### Internal:

- Refactor Flickr connection to be reusable @erral 

## 1.2 (2025-12-07)


### New features:

- Add restapi support through @inherit endpoint @erral 

## 1.1.0 (2025-10-02)


### New features:

- Make it work without requiring plone.app.multilingual @erral [#1](https://github.com/codesyntax/cs_flickrgallery/issues/1)

## 1.0.0 (2025-10-02)


### New features:

- Initial release @erral
