# gzipped.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha6

# Code from <http://flask.pocoo.org/snippets/122/>
# Snippet by: taehyun kang
from flask import after_this_request, request
from cStringIO import StringIO as IO
import gzip
import functools

def gzipped(f):
  @functools.wraps(f)
  def view_func(*args, **kwargs):
    @after_this_request
    def zipper(response):
      accept_encoding = request.headers.get('Accept-Encoding', '')

      if 'gzip' not in accept_encoding.lower():
        return response

      response.direct_passthrough = False

      if (response.status_code < 200 or
          response.status_code >= 300 or
          'Content-Encoding' in response.headers):

        return response

      gzip_buffer = IO()
      gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
      gzip_file.write(response.data)
      gzip_file.close()

      response.data = gzip_buffer.getvalue()
      response.headers['Content-Encoding'] = 'gzip'
      response.headers['Vary'] = 'Accept-Encoding'
      response.headers['Content-Length'] = len(response.data)

      return response

    return f(*args, **kwargs)

  return view_func


