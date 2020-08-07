from sitri import Sitri
from sitri.contrib.system import SystemConfigProvider

from tyazhko import __project__

configurator = Sitri(
    config_provider=SystemConfigProvider(prefix=__project__.upper()),
    credential_provider=None,
)
