# --------------------------------------------------------
# This is just Alembic's CLI script, provided here so we
# can access application state.
# --------------------------------------------------------

import re
import sys

from alembic.config import main

if __name__ == '__main__':
  sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
  sys.exit(main())
