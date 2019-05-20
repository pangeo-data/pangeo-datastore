import os
import pathlib
import intake
import re

import jinja2
from rstcloth.rstcloth import RstCloth


template_html = """    <div class="panel-group" id="accordion-{{ id }}">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h4 class="panel-title">
            <a data-toggle="collapse" data-parent="#accordion-{{ id }}" href="#collapse1-{{ id }}">
            load in python
            </a>
          </h4>
        </div>
        <div id="collapse1-{{ id }}" class="panel-collapse collapse">
          <div class="panel-body">
          <pre>{{ open_code | indent(4) | e }}</pre>
          </div>
        </div>
      </div>
      <div class="panel panel-default">
        <div class="panel-heading">
          <h4 class="panel-title">
            <a data-toggle="collapse" data-parent="#accordion-{{ id }}" href="#collapse2-{{ id }}">
             metadata</a>
          </h4>
        </div>
        <div id="collapse2-{{ id }}" class="panel-collapse collapse">
          <div class="panel-body">
           <table class="table table-condensed table-hover">
            <tbody>
           {% for key, value in metadata.items() %}
             <tr><td>{{ key | e }}</td><td>{{ value | e }}</td></tr>
           {% endfor %}
            </tbody>
           </table>
          </div>
        </div>
      </div>
      <div class="panel panel-default">
        <div class="panel-heading">
          <h4 class="panel-title">
            <a data-toggle="collapse" data-parent="#accordion-{{ id }}" href="#collapse3-{{ id }}">
            xarray preview</a>
          </h4>
        </div>
        <div id="collapse3-{{ id }}" class="panel-collapse collapse">
          <div class="panel-body">
          <pre>{{ repr | indent(4) | e }}</pre>
          </div>
        </div>
      </div>
    </div>
"""
template = jinja2.Template(template_html)


# https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
def to_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s).lower()

def normalize_document_path(prefix_and_name, extension=''):
    if len(prefix_and_name)==0:
        return
    path = os.path.join(*[to_valid_filename(p) for p in prefix_and_name])
    return path + extension

def ensure_dir_exists(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


class CatalogRSTBuilder:


    def __init__(self, master_catalog_path, output_dir, remote_url_base,
                 actually_load=False):
        self.master_catalog_path = master_catalog_path
        self.output_dir = output_dir
        self.remote_url_base = remote_url_base
        self.actually_load = actually_load
        self.cat = intake.Catalog(master_catalog_path)


    def remote_catalog_url(self, path):
        # translate local path name to url
        local_base_path = os.path.abspath(os.path.dirname(self.master_catalog_path))
        abs_path = os.path.abspath(path)
        url_path = abs_path.replace(local_base_path, self.remote_url_base)
        return url_path


    def dataset_open_code(self, intake_ds):
        path = self.remote_catalog_url(intake_ds.cat.path)
        code = ['import intake',
                f'cat = intake.Catalog("{path}")',
                f'ds = cat["{intake_ds.name}"].to_dask()']
        return '\n'.join(code)


    def dataset_repr(self, intake_ds):
        if self.actually_load:
            return repr(intake_ds.to_dask())
        else:
            return ""


    def walk_and_write_rst(self, cat, prefix=None, depth=2):
        prefix = [] if prefix is None else prefix
        parent_dir = normalize_document_path([self.output_dir] + prefix)
        document_path = normalize_document_path([self.output_dir] + prefix + [cat.name],
                                                extension='.rst')
        print(document_path)
        d = RstCloth()

        assert cat.description, 'Catalog needs a description for title'
        #title = cat.description

        title = cat.name + ': ' + cat.description
        d.title(title)
        d.newline()
        d.content('Catalog URL:')
        d.newline()
        d.codeblock(self.remote_catalog_url(cat.path), language='html')
        d.newline()

        if len(prefix) > 0:
            d.h2('Parent Catalogs')
            d.newline()

            parent_links = []
            for n in range(len(prefix)):
                levels_up = len(prefix) - n
                extra_prefixes = ['..'] * levels_up
                full_path = extra_prefixes + [to_valid_filename(prefix[n])]
                parent_cat_path = os.path.join(*full_path)
                parent_link = ':doc:' + d.inline_link(prefix[n], parent_cat_path)[:-1]
                parent_links.append(parent_link)
            d.content(' / '.join(parent_links))
            d.newline()

        sub_catalogs = []
        entries = []
        for name, item in cat.items():
            if item._container == 'catalog':
                if depth > 1:
                    self.walk_and_write_rst(item(), prefix + [cat.name], depth-1)
                sub_catalogs.append(name)
            else:
                entries.append(name)
            n = '.'.join(prefix + [name])

        path_path = '/'.join(prefix) + '.rst'

        if len(sub_catalogs) > 0:
            d.h2('Child Catalogs')
            d.newline()
            sub_catalog_path = os.path.join(to_valid_filename(cat.name), '*')
            d.directive('toctree',
                        fields=[#('caption', 'Child Datasets'),
                                ('glob', ''), ('maxdepth', '1')],
                        content=sub_catalog_path)

        if len(entries) > 0:
            d.h2('Datasets')
            d.newline()

        for name in entries:
            d.h3(name)
            d.newline()
            ds_item = cat[name]
            description = ds_item.description
            if description:
                d.content(description)
                d.newline()

            ds_repr = self.dataset_repr(ds_item)
            open_code = self.dataset_open_code(ds_item)
            name_jsfriendly = to_valid_filename(name).replace('.', '_')
            html = template.render(id=name_jsfriendly, open_code=open_code,
                                   repr=ds_repr, metadata=ds_item.metadata)
            d.directive('raw', arg='html', content=html)
            d.newline()

        ensure_dir_exists(parent_dir)
        d.write(document_path)


    def build(self, depth=5):
        self.walk_and_write_rst(self.cat, depth=depth)


def main():
    master_catalog = './intake-catalogs/master.yaml'
    output_rst_dir = 'catalog-docs'
    remote_url_base = 'https://raw.githubusercontent.com/pangeo-data/pangeo-datastore/master/intake-catalogs'
    builder = CatalogRSTBuilder(master_catalog, output_rst_dir, remote_url_base,
                                actually_load=True)
    builder.build()


if __name__ == "__main__":
    # execute only if run as a script
    main()
