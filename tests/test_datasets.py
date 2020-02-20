import os
import intake
import pytest

def get_master_catalog():
    # TODO: replace with environment variable
    fname = os.path.join(os.path.dirname(__file__),
                         '../intake-catalogs/master.yaml')
    return intake.Catalog(fname)

ALL_ENTRIES = list(get_master_catalog().walk(depth=10))

@pytest.fixture(scope="module")
def catalog(request):
    return get_master_catalog()

@pytest.fixture(scope="module", params=ALL_ENTRIES, ids=ALL_ENTRIES)
def dataset_name(request):
    return request.param

def test_get_intake_source(catalog, dataset_name):
    item = catalog[dataset_name]
    if item.container == "catalog":
        item.reload()   
    elif item.container == "xarray:
        if item._driver == "zarr":
            pytest.skip("need to resolve credentials issue for requester-pays data")
            # ds = item.to_dask()
        elif item._driver == "intake_esm.esm_datastore":
            pytest.skip("need to resolve credentials issue for requester-pays data")
            # col = item.get()
