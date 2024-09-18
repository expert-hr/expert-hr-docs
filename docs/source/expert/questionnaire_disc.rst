DISC Module Features
====================

Module for calculating the assessment of dominants according to DISC.

`Details <https://docs.google.com/document/d/1xE7JOn06IfeOiZuOK5U2vd4aMPDTEAgMU0AJWdC0hFA/edit#heading=h.76hgv3b0hgd9>`_

questions
~~~~~~~~~

Returns questions for the DISC questionnaire.

::

   /disc/questions

Params
^^^^^^

No params

Return example
^^^^^^^^^^^^^^

::

   {
   "disc": [
       ["Надежный, увлеченный", "Терпимый, уважительный", "Смелый, предприимчивый", "Приятный, сговорчивый"],
       ["Инновационный, дальновидный", "Сдержанный, немногословный", "Общительный, близкий по духу", "Миротворец, посредник в переговорах"],
       // ...
   ],
   }

score
~~~~~

Receives a user-sorted list of phrase lists from the DISC test and returns coordinates for natural and adaptive behavior.

::

   /disc/score

.. _params-1:

Params
^^^^^^

User-sorted list of phrases.

::

   {
   "disc": [
       ["Надежный, увлеченный", "Терпимый, уважительный", "Смелый, предприимчивый", "Приятный, сговорчивый"],
       ["Инновационный, дальновидный", "Сдержанный, немногословный", "Общительный, близкий по духу", "Миротворец, посредник в переговорах"],
       // ...
   ],
   }

.. _return-example-1:

Return example
^^^^^^^^^^^^^^

::

   {
   "score": {
       "natural": [0.25, 0.5, 0.37, 0.1],
       "adaptive": [0.2, 0.6, 0.4, 0.2]
   }
   }


Requirements
============

- Python >=3.9
- pip >=22.0 or PDM >=2.4.8


Installation
============

1. Clone the repository locally.

.. code-block:: bash

    $ git clone https://github.com/expert-hr/expert-hr.git
    $ cd expert-hr/libs/questionnaire_disc/

2. Install basic requirements.

.. code-block:: bash

    $ python -m pip install -r requirements.txt


Usage
=====

Basic usage.

.. code-block:: bash

    $ # With pdm (recommended)
    $ pdm run python -m app.run

    $ # Without pdm
    $ python -m app.run

