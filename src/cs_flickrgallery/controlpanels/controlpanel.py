from cs_flickrgallery import _
from cs_flickrgallery.interfaces import IBrowserLayer
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IFlickrSettingsControlPanel(Interface):
    flickr_api_key = schema.TextLine(
        title=_(
            "Flickr API key",
        ),
        description=_(
            "",
        ),
        default="",
        required=True,
        readonly=False,
    )

    flickr_api_secret = schema.TextLine(
        title=_(
            "Flickr API secret",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )

    flickr_user_id = schema.TextLine(
        title=_(
            "Flickr User ID",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )


class FlickrSettingsControlPanel(RegistryEditForm):
    schema = IFlickrSettingsControlPanel
    schema_prefix = "cs_flickrgallery.flickr_settings"
    label = _("Flickr Settings")


FlickrSettingsControlPanelView = layout.wrap_form(
    FlickrSettingsControlPanel, ControlPanelFormWrapper
)


@adapter(Interface, IBrowserLayer)
class FlickrSettingsControlPanelConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IFlickrSettingsControlPanel
    configlet_id = "flickr_settings-controlpanel"
    configlet_category_id = "Products"
    title = _("Flickr Settings")
    group = ""
    schema_prefix = "cs_flickrgallery.flickr_settings"
