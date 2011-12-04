# Copyright (c) 2007, Columbia Center For New Media Teaching And Learning (CCNMTL)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the CCNMTL nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY CCNMTL ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


#!/usr/bin/python

"""
REST client convenience library

This module contains everything that's needed for a nice, simple REST client.

the main function it provides is rest_invoke(), which will make an HTTP
request to a REST server. it allows for all kinds of nice things like:

    * alternative verbs: POST, PUT, DELETE, etc.
    * parameters
    * file uploads (multipart/form-data)
    * proper unicode handling
    * Accept: headers
    * ability to specify other headers

this library is mostly a wrapper around the standard urllib and
httplib2 functionality, but also includes file upload support via a
python cookbook recipe
(http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306) and
has had additional work to make sure high unicode characters in the
parameters or headers don't cause any UnicodeEncodeError problems. 

Joe Gregario's httplib2 library is required. It can be easy_installed, or downloaded
nose is required to run the unit tests.

CHANGESET:
  * 2011-09-22 - @macat - Cleanup for Minus.com
  * 2010-07-25 - Anders - merged Greg Baker's <gregb@ifost.org.au> patch for https urls
  * 2007-06-13 - Anders - added experimental, partial support for HTTPCallback
  * 2007-03-28 - Anders - merged Christopher Hesse's patches for fix_params and to eliminate
                          mutable default args
  * 2007-03-14 - Anders - quieted BaseHTTPServer in the test suite
  * 2007-03-06 - Anders - merged Christopher Hesse's bugfix and self-contained test suite
  * 2006-12-01 - Anders - switched to httplib2. Improved handling of parameters and made it
                          stricter about unicode in headers (only ASCII is allowed). Added
                          resp option. More docstrings.
  * 2006-03-23 - Anders - working around cherrypy bug properly now by being more
                          careful about sending the right 
  * 2006-03-17 - Anders - fixed my broken refactoring :) also added async support
n                          and we now use post_multipart for everything since it works
                          around a cherrypy bug.
  * 2006-03-10 - Anders - refactored and added GET, POST, PUT, and DELETE
                          convenience functions
  * 2006-02-22 - Anders - handles ints in params + headers correctly now

"""


import urllib2,urllib, types, httplib

__version__ = "0.10.1"

def rest_invoke(url, method=u"GET", params=None, accept=None, headers=None):
    """ make an HTTP request with all the trimmings.

    rest_invoke() will make an HTTP request and can handle all the
    advanced things that are necessary for a proper REST client to handle:

    * alternative verbs: POST, PUT, DELETE, etc.
    * parameters
    * file uploads (multipart/form-data)
    * proper unicode handling
    * Accept: headers
    * ability to specify other headers

    rest_invoke() returns the body of the response that it gets from
    the server.

    rest_invoke() does not try to do any fancy error handling. if the
    server is down or gives an error, it will propagate up to the
    caller.

    this function expects to receive unicode strings. passing in byte
    strings risks double encoding.

    parameters:

    url: the full url you are making the request to
    method: HTTP verb to use. defaults to GET
    params: dictionary of params to include in the request
    accept: list of mimetypes to accept in order of preference. defaults to '*/*'
    headers: dictionary of additional headers to send to the server
    """
    if params  is None: params  = {}
    if accept  is None: accept  = []
    if headers is None: headers = {}
    
    headers = add_accepts(accept,headers)

    has_file = False
    for value in params.values():
        if type(value) == file:
            has_file = True

    if method == u"POST" and has_file:
        return post_multipart(url, params, fix_headers(headers))
    else:
        return non_multipart(fix_params(params), extract_host(url),
                             method, extract_path(url), fix_headers(headers),
                             scheme=extract_scheme(url))

def non_multipart(params, host, method, path, headers, scheme="http"):
    params = urllib.urlencode(params)
    if method == "GET":
        headers['Content-Length'] = '0'
        if params:
            # put the params into the url instead of the body
            if "?" not in path:
                path += "?" + params
            else:
                if path.endswith('?'):
                    path += params
                else:
                    path += "&" + params
            params = ""
    else:
        headers['Content-Length'] = str(len(params))
    if method in ['POST', 'PUT'] and not headers.has_key('Content-Type'):
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

    if scheme == 'https':
        connection = httplib.HTTPSConnection(host)
    else:
        connection = httplib.HTTPConnection(host)

    connection.request(method, path, params.encode('utf-8'), headers)
    response = connection.getresponse()
    content = response.read()
    return response.status, content

def post_multipart(url, fields, headers=None):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    from poster.streaminghttp import register_openers
    from poster.encode import multipart_encode
    register_openers()
    datagen, multi_headers = multipart_encode(fields)
    headers.update(multi_headers)
    request = urllib2.Request(url, datagen, headers)
    status = 200
    
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        # Reponse doesn't exist if we land here!
        #status = response.code
        print e

    return status, response.read()


def extract_host(url):
    return my_urlparse(url)[1]

def extract_scheme(url):
    return my_urlparse(url)[0]

def extract_path(url):
    return my_urlparse(url)[2]

def my_urlparse(url):
    (scheme,host,path,ps,query,fragment) = urllib2.urlparse.urlparse(url)
    if ps:
        path += ";" + ps
    if query:
        path += "?" + query

    return (scheme,host,path)
        
def unpack_params(params):
    return [(k,params[k]) for k in params.keys()]

def unpack_files(files):
    return [(k,files[k]['filename'],files[k]['file']) for k in files.keys()]

def add_accepts(accept=None,headers=None):
    if accept  is None: accept  = []
    if headers is None: headers = {}
    
    if accept:
        headers['Accept'] = ','.join(accept)
    else:
        headers['Accept'] = '*/*'
    return headers

def fix_params(params=None):
    if params is None: params = {}
    for k in params.keys():
        if type(k) not in types.StringTypes:
            new_k = str(k)
            params[new_k] = params[k]
            del params[k]
        else:
            try:
                k = k.encode('ascii')
            except UnicodeEncodeError:
                new_k = k.encode('utf8')
                params[new_k] = params[k]
                del params[k]
            except UnicodeDecodeError:
                pass

    for k in params.keys():
        if type(params[k]) not in types.StringTypes:
            params[k] = str(params[k])
        try:
            v = params[k].encode('ascii')                
        except UnicodeEncodeError:
            new_v = params[k].encode('utf8')
            params[k] = new_v
        except UnicodeDecodeError:
            pass

    return params

def fix_headers(headers=None):
    if headers is None: headers = {}
    for k in headers.keys():
        if type(k) not in types.StringTypes:
            new_k = str(k)
            headers[new_k] = headers[k]
            del headers[k]
        if type(headers[k]) not in types.StringTypes:
            headers[k] = str(headers[k])        
        try:
            v = headers[k].encode('ascii')                
            k = k.encode('ascii')
        except UnicodeEncodeError:
            new_k = k.encode('ascii','ignore')
            new_v = headers[k].encode('ascii','ignore')
            headers[new_k] = new_v
            del headers[k]
    return headers

