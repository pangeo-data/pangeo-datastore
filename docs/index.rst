.. Sphinx Pangeo Test documentation master file, created by
   sphinx-quickstart on Tue Apr  2 16:50:05 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pangeo Cloud Data Catalog
=========================

Welcome to the Pangeo Cloud Data Catalog.
The Pangeo Cloud Data Catalog lives in the following GitHub repository:
`https://github.com/pangeo-data/pangeo-datastore <https://github.com/pangeo-data/pangeo-datastore>`_

Most of the data is stored in cloud-friendly formats like Zarr_
and meant to be opened with Xarray_.
Catalog formats for cloud-based data is an evolving area.

We are currently using two different approaches: Intake_ and ESMCol_.

Intake Catalogs
---------------

Intake_ is a python library for

The master intake catalog URL is::

    https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/master.yaml


To open the catalog and load a dataset from python, you can run the following code::

    import intake
    cat_url = 'https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/master.yaml'
    cat = intake.Catalog(cat_url)
    ds = cat.atmosphere.gmet_v1.to_dask()

To explore the whole catalog, you can try::

    cat.walk(depth=5)

You can also find a static, online browser for the intake catalogs following
the links below.

.. toctree::
   :maxdepth: 3
   :caption: Pangeo Intake Catalogs

   master

ESM Collection
--------------

ESMCol_ stands for Earth System Model Collection.
It is an experimental new format, inspired by STAC_, for cataloging large,
homogeneous archives of Earth System Model output like CMIP6.
The links below will take you to a javascript-based spreadsheet-style browser
for the ESMCol catalogs.
Data can be loaded in python with
`intake-esm <https://intake-esm.readthedocs.io/en/latest/>`_.

.. toctree::
   :maxdepth: 3
   :caption: Pangeo ESMCol Catalogs

   cmip6_pangeo
   cmip6_glade


.. _STAC: https://github.com/radiantearth/stac-spec
.. _Intake: https://intake.readthedocs.io
.. _ESMCol: https://github.com/NCAR/esm-collection-spec/
.. _Zarr: https://zarr.readthedocs.io
.. _Xarray: http://xarray.pydata.org
