Slide 1
========

* This is the first item of the first slide
* This is the second item of the first slide
* This is the third item of the first slide

Slide 2
========

* This is the first item of the second slide
    * This is nested item 1
    * This is nested item 2
* This is the second item of the second slide
    * This is nested item 3

Slide Three
===============

* This is the first item of the second slide
    * This is nested level 1
        * This is nested level 2
        * This is nested level 3
            * This is nested level 4
* This is the second item of the second slide

Code
======

* We like writing code

.. code:: python
    :class: size50

    if foo:
        bar()
    else:
        baz()



Code
======

* What if we have larger code?

.. code:: python

    if foo and bar and baz and bam and boom and blarg and blurfle and boomtown and barglebargle:
        bar()
    else:
        baz()

* So there

Images
=======

* We have an svg file here

.. images:: alt=a red sphere,width=300, redsphere.svg


Images
=======

* We have three svg files here

.. images:: width=200, alt=red sphere,redsphere.svg, alt=green sphere,greensphere.svg, alt=blue sphere, bluesphere.svg

Images?
===========

* Perhaps a PNG file is nice

.. images:: width=400,alt=a torus,torus.jpg,height=300,alt=a cone,cone.png


Scripts
=========

* We must breathe O\ :sub:`2` or H\ :sub:`2`\ O
* x\ :sup:`2` + x + 1 = 0
* It is *important* that we **not** mess up __today__!!!
* Some :raw:`\textbf{raw}` inline content

.. raw::

    We have \textit{here} some raw block content
