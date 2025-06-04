from BTrees.IOBTree import IOBTree
from zope.annotation.interfaces import IAnnotations

from cs_flickrgallery import ANNOTATION_KEY


def set_images(context, images):
    annotated = IAnnotations(context)
    values = IOBTree()
    for i, image in enumerate(images):
        values[i] = image
    annotated[ANNOTATION_KEY] = values

def get_images(context):
    annotated = IAnnotations(context)
    return annotated.get(ANNOTATION_KEY, IOBTree()).values()
