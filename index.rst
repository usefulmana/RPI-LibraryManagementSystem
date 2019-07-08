.. PIoT - Library Management System documentation master file, created by
   sphinx-quickstart on Mon Jul  8 14:36:15 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PIoT - Library Management System
******************************************

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
=========================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Introduction
=========================



Application Interface
=========================



Authentication
=========================

Classic Authentication
-------------------------



Face Recognition
-------------------------

The user can choose to use face recognition to log in instead of console-based 
authentication. At registration, the user is asked to take a picture of their face.
This image is stored in Reception Pi and encoded using ``face_recognition`` API.
The face encoding, in form of a numeric 1D array, is stored in database along with
other credentials such as email, name and password.

Upon logging in, an image of the person's face is captured and encoded. The resulted
encoding is compared with those stored in database to find a match. If no match found,
the person is recognised as Unknown and cannot be logged in to the system.

Library Features
=========================

Search a book
-------------------------



Borrow a book
-------------------------



Return a book
-------------------------


QR code scanning
+++++++++++++++++++++++++



Database
=========================

Members
-------------------------


Books
-------------------------




