.. Sphinx Pangeo Test documentation master file, created by
   sphinx-quickstart on Tue Apr  2 16:50:05 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pangeo Cloud Data Catalog
=========================

Welcome to the Pangeo Cloud Data Catalog.
The Pangeo Cloud Data Catalog lives in the following GitHub repository:
`https://github.com/pangeo-data/pangeo-datastore <https://github.com/pangeo-data/pangeo-datastore>`_

It consists of a nested set of Intake_ catalogs
Most of the data is stored in cloud-friendly formats like Zarr_
and meant to be opened with Xarray_.

The master intake catalog URL is::

    https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/master.yaml

Examples
--------

To open the catalog and load a dataset from python, you can run the following code::

    import intake
    cat_url = 'https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/master.yaml'
    cat = intake.Catalog(cat_url)
    ds = cat.atmosphere.gmet_v1.to_dask()

To explore the whole catalog, you can try::

    cat.walk(depth=5)

Catalog Contents
----------------

This website is a statically generated Sphinx site from which you can browse the catalog contents.

.. toctree::
   :maxdepth: 3

   cmip6_catalog
   master


.. _Intake: https://intake.readthedocs.io
.. _Zarr: https://zarr.readthedocs.io
.. _Xarray: http://xarray.pydata.org
