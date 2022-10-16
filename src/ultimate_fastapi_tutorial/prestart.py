from utilities.git import get_repo_root

from alembic.command import upgrade
from alembic.config import Config


alembic_cfg = Config(file_=get_repo_root().joinpath("alembic.ini").as_posix())


from ultimate_fastapi_tutorial import (  # isort: skip # noqa: E402
    backend_pre_start,
)


backend_pre_start.main()


upgrade(alembic_cfg, "head")


from ultimate_fastapi_tutorial import initial_data  # isort: skip # noqa: E402

initial_data.main()
