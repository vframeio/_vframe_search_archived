"""
Export a zip file from a collection
"""

import click

@click.command('')
@click.option('-i', '--collection', 'opt_collection_id', required=True, 
  default=1,
  help='Collection ID')
@click.pass_context
def cli(ctx, opt_collection_id):
  """Export a zip file from a collection"""

  import logging
  from app.data.export import export_zip

  log = logging.getLogger('vframe')  # move to ctx
  zip_url = export_zip(opt_collection_id)

  print(f"Exported ZIP {zip_url}")
