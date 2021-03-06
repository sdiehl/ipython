# -*- coding: utf-8 -*-
"""Top-level display functions for displaying object in different formats.

Authors:

* Brian Granger
"""

#-----------------------------------------------------------------------------
#       Copyright (C) 2008-2011 The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from xml.dom import minidom

from .displaypub import (
    publish_pretty, publish_html,
    publish_latex, publish_svg,
    publish_png, publish_json,
    publish_javascript, publish_jpeg
)

#-----------------------------------------------------------------------------
# Main functions
#-----------------------------------------------------------------------------

def display(*objs, **kwargs):
    """Display a Python object in all frontends.

    By default all representations will be computed and sent to the frontends.
    Frontends can decide which representation is used and how.

    Parameters
    ----------
    objs : tuple of objects
        The Python objects to display.
    include : list or tuple, optional
        A list of format type strings (MIME types) to include in the
        format data dict. If this is set *only* the format types included
        in this list will be computed.
    exclude : list or tuple, optional
        A list of format type string (MIME types) to exclue in the format
        data dict. If this is set all format types will be computed,
        except for those included in this argument.
    """
    include = kwargs.get('include')
    exclude = kwargs.get('exclude')

    from IPython.core.interactiveshell import InteractiveShell
    inst = InteractiveShell.instance()
    format = inst.display_formatter.format
    publish = inst.display_pub.publish

    for obj in objs:
        format_dict = format(obj, include=include, exclude=exclude)
        publish('IPython.core.display.display', format_dict)


def display_pretty(*objs, **kwargs):
    """Display the pretty (default) representation of an object.

    Parameters
    ----------
    objs : tuple of objects
        The Python objects to display, or if raw=True raw text data to
        display.
    raw : bool
        Are the data objects raw data or Python objects that need to be
        formatted before display? [default: False]
    """
    raw = kwargs.pop('raw',False)
    if raw:
        for obj in objs:
            publish_pretty(obj)
    else:
        display(*objs, include=['text/plain'])


def display_html(*objs, **kwargs):
    """Display the HTML representation of an object.

    Parameters
    ----------
    objs : tuple of objects
        The Python objects to display, or if raw=True raw HTML data to
        display.
    raw : bool
        Are the data objects raw data or Python objects that need to be
        formatted before display? [default: False]
    """
    raw = kwargs.pop('raw',False)
    if raw:
        for obj in objs:
            publish_html(obj)
    else:
        display(*objs, include=['text/plain','text/html'])


def display_svg(*objs, **kwargs):
    """Display the SVG representation of an object.

    Parameters
    ----------
    objs : tuple of objects
        The Python objects to display, or if raw=True raw svg data to
        display.
    raw : bool
        Are the data objects raw data or Python objects that need to be
        formatted before display? [default: False]
    """
    raw = kwargs.pop('raw',False)
    if raw:
        for obj in objs:
            publish_svg(obj)
    else:
        display(*objs, include=['text/plain','image/svg+xml'])


def display_png(*objs, **kwargs):
    """Display the PNG representation of an object.

    Parameters
    ----------
    objs : tuple of objects
        The Python objects to display, or if raw=True raw png data to
        display.
    raw : bool
        Are the data objects raw data or Python objects that need to be
        formatted before display? [default: False]
    """
    raw = kwargs.pop('raw',False)
    if raw:
        for obj in objs:
            publish_png(obj)
    else:
        display(*objs, include=['text/plain','image/png'])


def display_jpeg(*objs, **kwargs):
    """Display the JPEG representation of an object.

    Parameters
    ----------
    objs : tuple of objects
        The Python objects to display, or if raw=True raw JPEG data to
        display.
    raw : bool
        Are the data objects raw data or Python objects that need to be
        formatted before display? [default: False]
    """
    raw = kwargs.pop('raw',False)
    if raw:
        for obj in objs:
            publish_jpeg(obj)
    else:
        display(*objs, include=['text/plain','image/jpeg'])


def display_latex(*objs, **kwargs):
    """Display the LaTeX representation of an object.

    Parameters
    ----------
    objs : tuple of objects
        The Python objects to display, or if raw=True raw latex data to
        display.
    raw : bool
        Are the data objects raw data or Python objects that need to be
        formatted before display? [default: False]
    """
    raw = kwargs.pop('raw',False)
    if raw:
        for obj in objs:
            publish_latex(obj)
    else:
        display(*objs, include=['text/plain','text/latex'])


def display_json(*objs, **kwargs):
    """Display the JSON representation of an object.

    Parameters
    ----------
    objs : tuple of objects
        The Python objects to display, or if raw=True raw json data to
        display.
    raw : bool
        Are the data objects raw data or Python objects that need to be
        formatted before display? [default: False]
    """
    raw = kwargs.pop('raw',False)
    if raw:
        for obj in objs:
            publish_json(obj)
    else:
        display(*objs, include=['text/plain','application/json'])


def display_javascript(*objs, **kwargs):
    """Display the Javascript representation of an object.

    Parameters
    ----------
    objs : tuple of objects
        The Python objects to display, or if raw=True raw javascript data to
        display.
    raw : bool
        Are the data objects raw data or Python objects that need to be
        formatted before display? [default: False]
    """
    raw = kwargs.pop('raw',False)
    if raw:
        for obj in objs:
            publish_javascript(obj)
    else:
        display(*objs, include=['text/plain','application/javascript'])

#-----------------------------------------------------------------------------
# Smart classes
#-----------------------------------------------------------------------------


class DisplayObject(object):
    """An object that wraps data to be displayed."""

    _read_flags = 'r'

    def __init__(self, data=None, url=None, filename=None):
        """Create a display object given raw data.

        When this object is returned by an expression or passed to the
        display function, it will result in the data being displayed
        in the frontend. The MIME type of the data should match the
        subclasses used, so the Png subclass should be used for 'image/png'
        data. If the data is a URL, the data will first be downloaded
        and then displayed. If

        Parameters
        ----------
        data : unicode, str or bytes
            The raw data or a URL to download the data from.
        url : unicode
            A URL to download the data from.
        filename : unicode
            Path to a local file to load the data from.
        """
        if data is not None and data.startswith('http'):
            self.url = data
            self.filename = None
            self.data = None
        else:
            self.data = data
            self.url = url
            self.filename = None if filename is None else unicode(filename)
        self.reload()

    def reload(self):
        """Reload the raw data from file or URL."""
        if self.filename is not None:
            with open(self.filename, self._read_flags) as f:
                self.data = f.read()
        elif self.url is not None:
            try:
                import urllib2
                response = urllib2.urlopen(self.url)
                self.data = response.read()
                # extract encoding from header, if there is one:
                encoding = None
                for sub in response.headers['content-type'].split(';'):
                    sub = sub.strip()
                    if sub.startswith('charset'):
                        encoding = sub.split('=')[-1].strip()
                        break
                # decode data, if an encoding was specified
                if encoding:
                    self.data = self.data.decode(encoding, 'replace')
            except:
                self.data = None

class Pretty(DisplayObject):

    def _repr_pretty_(self):
        return self.data


class HTML(DisplayObject):

    def _repr_html_(self):
        return self.data


class Math(DisplayObject):

    def _repr_latex_(self):
        return self.data


class SVG(DisplayObject):
    
    # wrap data in a property, which extracts the <svg> tag, discarding
    # document headers
    _data = None
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, svg):
        if svg is None:
            self._data = None
            return
        # parse into dom object
        x = minidom.parseString(svg)
        # get svg tag (should be 1)
        found_svg = x.getElementsByTagName('svg')
        if found_svg:
            svg = found_svg[0].toxml()
        else:
            # fallback on the input, trust the user
            # but this is probably an error.
            pass
        self._data = svg
    
    def _repr_svg_(self):
        return self.data


class JSON(DisplayObject):

    def _repr_json_(self):
        return self.data


class Javascript(DisplayObject):

    def _repr_javascript_(self):
        return self.data


class Image(DisplayObject):

    _read_flags = 'rb'

    def __init__(self, data=None, url=None, filename=None, format=u'png', embed=False):
        """Create a display an PNG/JPEG image given raw data.

        When this object is returned by an expression or passed to the
        display function, it will result in the image being displayed
        in the frontend.

        Parameters
        ----------
        data : unicode, str or bytes
            The raw data or a URL to download the data from.
        url : unicode
            A URL to download the data from.
        filename : unicode
            Path to a local file to load the data from.
        format : unicode
            The format of the image data (png/jpeg/jpg). If a filename or URL is given
            for format will be inferred from the filename extension.
        embed : bool
            Should the image data be embedded in the notebook using a data URI (True)
            or be loaded using an <img> tag. Set this to True if you want the image
            to be viewable later with no internet connection. If a filename is given
            embed is always set to True.
        """
        if filename is not None:
            ext = self._find_ext(filename)
        elif url is not None:
            ext = self._find_ext(url)
        elif data.startswith('http'):
            ext = self._find_ext(data)
        else:
            ext = None
        if ext is not None:
            if ext == u'jpg' or ext == u'jpeg':
                format = u'jpeg'
            if ext == u'png':
                format = u'png'
        self.format = unicode(format).lower()
        self.embed = True if filename is not None else embed
        super(Image, self).__init__(data=data, url=url, filename=filename)

    def reload(self):
        """Reload the raw data from file or URL."""
        if self.embed:
            super(Image,self).reload()

    def _repr_html_(self):
        if not self.embed:
            return u'<img src="%s" />' % self.url

    def _repr_png_(self):
        if self.embed and self.format == u'png':
            return self.data

    def _repr_jpeg_(self):
        if self.embed and (self.format == u'jpeg' or self.format == u'jpg'):
            return self.data

    def _find_ext(self, s):
        return unicode(s.split('.')[-1].lower())


def clear_output(stdout=True, stderr=True, other=True):
    """Clear the output of the current cell receiving output.
    
    Optionally, each of stdout/stderr or other non-stream data (e.g. anything
    produced by display()) can be excluded from the clear event.
    
    By default, everything is cleared.
    
    Parameters
    ----------
    stdout : bool [default: True]
        Whether to clear stdout.
    stderr : bool [default: True]
        Whether to clear stderr.
    other : bool [default: True]
        Whether to clear everything else that is not stdout/stderr
        (e.g. figures,images,HTML, any result of display()).
    """
    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.instance().display_pub.clear_output(
        stdout=stdout, stderr=stderr, other=other,
    )
