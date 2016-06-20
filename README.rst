.. blog_klein documentation master file, created by
   sphinx-quickstart on Sun May 22 08:53:05 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to blog_klein's documentation!
======================================

Contents
========

.. toctree::
   :maxdepth: 2

   basic_routes_vars
   nonblocking
   branching


Introduction
============

With Python finally getting async functionality out of the box and a plethora of web frameworks exposing those capabilities, I thought I'd create a basic how-to using another asynchronous framework.  There’s a great asynchronous Python web framework out there called Klein.  It hasn’t gotten the same love that other web frameworks has received, such as Tornado, Werkzeug/Flask, Django, or Falcon/Hug.  One reason for the lackluster popularity may be due to the sparse documentation and "cryptic" nature of the underlying Twisted framework.  Hopefully, the following posts will shed some light on Klein and bring the documentation up to the standards of the other more prominent frameworks.  The hope is to extend Klein’s documentation as well as provide detailed examples.

As stated previously, Klein is an asynchronous web framework, like Tornado, and is syntactically similar to Flask and Hug.  If you’re familiar with either Flask or Hug, than you should be in good shape can browse to more advanced topics of this blog.  In fact, Klein is actually built on top of Werkzueg just like Flask.  Klein also leverages the Twisted framework to provide asynchronous request handling without the need for threads.  Even with the Twisted under the hood (which many consider to be “complex”), Klein is very lean and minimalistic so that developers have more control their web app.  The examples used in this blog post are Python 3.5+ compatible unless otherwise noted.

