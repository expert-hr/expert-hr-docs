CV-Vacancy Comparison
---------------------


CV-Vacancy Comparator Features
==============================

Assessing the correspondence between the fields of the vacancy and the CV to generate recommendations for filling out the fields, questions for the candidate and an overall assessment of the correspondence between the CV and the vacancy to rank candidates.

.. image:: docs/UML_comparator.png
    :width: 700px
    :align: center
    :alt: Comparator Diagram


Requirements
============

- Python >=3.9
- pip >=22.0 or PDM >=2.4.8


Installation
============

1. Clone the repository locally.

.. code-block:: bash

    $ git clone https://github.com/expert-hr/expert-hr.git
    $ cd expert-hr/libs/hr_comparator/

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


Citation
========

.. code-block:: bash

    @software{expert-hr,
        title = {expert-hr},
        author = {Laushkina, Anastasiya and Smirnov, Ivan and Medvedev, Anatolii et al.},
        year = {2024},
        url = {https://github.com/expert-hr/expert-hr},
        version = {1.0.0}
    }

