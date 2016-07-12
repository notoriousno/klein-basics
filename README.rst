.. blog_klein documentation master file, created by
   sphinx-quickstart on Sun May 22 08:53:05 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to blog_klein's documentation!
======================================


Introduction
------------

There's a fantastic Python web framework out there called Klein.  It leverages the power of industry giants Werkzeug and Twisted.  It's asynchronous and very easy to pick up.  I've been using it now for about 2+ years and I'm amazed at what I'm able to achieve.  Fortunate for me, I learned Flask (which uses Werkzeug) and Twisted very early on in my career, so I as able to pick up on Klein rather easily.  Klein requires and expects a good understanding of Twisted as well as Werkzeug, but not all may posses this knowledge and the online resources are scarce (but growing).  My hope is to "demystify" some concepts and provide recipes which are provided in other frameworks.  I hope to effectively demonstrate how easily one can write scalable, asynchronous applications (like Tornado) and do so with minimal effort (like Flask or Hug).


Installation
------------

.. code-block:: bash

   pip install klein

Klein works with both Python 2.7+ and 3.4+.  However, Twisted hasn't been fully ported over to Python 3 yet.  Most of the code here will be Python 3 compatible unless stated otherwise.


Contents
--------

.. toctree::
   :maxdepth: 2

   basic_routes_vars
   requestobject
   templates
   branching
   nonblocking
   sessions
   databases


The majority of this blog will pay homage to Jean-Paul Calderone's `Twisted Web in 60 Seconds <http://twistedmatrix.com/documents/current/web/howto/web-in-60/index.html>`_.  These are a very good set of tutorials and I only wish I can make as big an impact on the next generation of Twisted developers as the ``Twisted Web in 60 Seconds`` series had on me.
