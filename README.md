# Pangeo Cloud Datastore

**Catalog Status**: [![Build Status](https://travis-ci.org/pangeo-data/pangeo-datastore.svg?branch=master)](https://travis-ci.org/pangeo-data/pangeo-datastore) 

**Browseable Online Website**: <https://pangeo-data.github.io/pangeo-datastore/>

This repository is where Pangeo's official cloud data catalog lives.
This catalog is an [Intake](https://github.com/ContinuumIO/intake) catalog.
Most of the data is stored in [Zarr](https://github.com/zarr-developers/zarr) format
and meant to be opened with [Xarray](http://xarray.pydata.org/en/latest/).

The master intake catalog URL is
```
https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/master.yaml
```

### Requirements

Using this catalog requires package versions that are quite recent as of April, 2019.

- [Intake](https://github.com/ContinuumIO/intake) >= 0.4.4
- [Xarray](http://xarray.pydata.org/en/latest/) >= 0.12.0
- [Zarr](https://github.com/zarr-developers/zarr) >= 2.3.1
- [Dask](https://docs.dask.org/en/latest/) >= 1.0

### Examples

To open the catalog and load a dataset from python, you can run the following code

```python
import intake
cat_url = 'https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs/master.yaml'
cat = intake.Catalog(cat_url)
ds = cat.atmosphere.gmet_v1.to_dask()
```

To explore the whole catalog, you can try
```python
cat.walk(depth=5)
```

### Adding Datasets

To suggest adding a new dataset, please [open an issue](https://github.com/pangeo-data/pangeo-datastore/issues).
