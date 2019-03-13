import intake
import pytest

def crawl_nested_catalog(cat_or_entry, parent_name=()):
    for name in cat_or_entry:
        entry = cat_or_entry[name].get()
        full_name = parent_name + (name,)
        if isinstance(entry, intake.catalog.local.YAMLFileCatalog):
            yield from crawl_nested_catalog(entry, parent_name=full_name)
        else:
            yield full_name, entry

def get_nested_item(cat, keys):
    item = cat[keys[0]].get()
    if len(keys) > 1:
        return get_nested_item(item, keys[1:])
    else:
        return item

def get_master_catalog():
    # TODO: replace with environment variable
    return intake.Catalog('/home/jovyan/intake-catalogs/master.yaml')

@pytest.fixture(scope="module")
def catalog(request):
    return get_master_catalog()

def test_open_master_catalog(catalog):
    pass

ALL_ENTRIES = [res[0] for res in crawl_nested_catalog(get_master_catalog())]

@pytest.fixture(scope="module", params=ALL_ENTRIES,
                ids=['.'.join(name) for name in ALL_ENTRIES])
def dataset_name(request):
    return request.param

#@pytest.mark.parametrize("dataset_name", ALL_ENTRIES, ids=['.'.join(name) for name in ALL_ENTRIES])
def test_get_intake_source(catalog, dataset_name):
    item = get_nested_item(catalog, dataset_name)

#@pytest.mark.parametrize("dataset_name", ALL_ENTRIES, ids=['.'.join(name) for name in ALL_ENTRIES])
def test_intake_dataset_to_dask(catalog, dataset_name):
    item = get_nested_item(catalog, dataset_name)
    ds = item.to_dask()
