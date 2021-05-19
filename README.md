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
cat = intake.open_catalog(cat_url)
ds = cat.atmosphere.gmet_v1.to_dask()
```

To explore the whole catalog, you can try
```python
cat.walk(depth=5)
```

### Accessing requester pays data

Several of the datasets within the cloud data catalog are contained in [requester pays](https://cloud.google.com/storage/docs/requester-pays) storage buckets.
This means that a user requesting data must provide their own billing project (created and authenticated through Google Cloud Platform) to be billed for the charges associated with accessing a dataset.
To set up an GCP billing project and use it for authentication in applications:

- [Create a project on GCP](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project); if this is the first time using GCP, a prompt will appear to choose a Google account to link to all GCP-related activities.
- [Create a Cloud Billing account](https://cloud.google.com/billing/docs/how-to/manage-billing-account#create_a_new_billing_account) associated with the project and [enable billing for the project](https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project) through this account.
- Using [Google Cloud IAM](https://cloud.google.com/iam/docs/granting-changing-revoking-access#granting-console), add the **Service Usage Consumer** role to your account, which enables it to make billed requests on the behalf of the project.
- Through command line, install the [Google Cloud SDK](https://cloud.google.com/sdk); this can be done using conda:
```
 conda install -c conda-forge google-cloud-sdk 
```
- Initialize the `gcloud` command line interface, logging into the account used to create the aforementioned project and selecting it as the default project; this will allow the project to be used for requester pays access through the command line:
```
gcloud auth login
gcloud init
```
- Finally, use `gcloud` to establish application default credentials; this will allow the project to be used for requester pays access through applications:
```
gcloud auth application-default login
```

### Adding Datasets

To suggest adding a new dataset, please [open an issue](https://github.com/pangeo-data/pangeo-datastore/issues).
