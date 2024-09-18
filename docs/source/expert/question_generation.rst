Questions Generator Features
============================

Generating interview questions based on matches and mismatches between the vacancy and resume fields.


Requirements
============

- Python >=3.9
- pip >=22.0 or PDM >=2.4.8


Installation
============

1. Clone the repository locally.

.. code-block:: bash

    $ git clone https://github.com/expert-hr/expert-hr.git
    $ cd expert-hr/libs/question_generation/

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
