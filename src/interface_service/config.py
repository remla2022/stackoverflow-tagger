"""
Provides a configuration management object.
"""

from dynaconf import Dynaconf, Validator
from interface_service.var_names import VarNames

settings = Dynaconf(
    # variables exported in .env as `REMLA_FOO=bar` becomes `settings.FOO == "bar"`
    envvar_prefix="REMLA",
    load_dotenv=False,
    settings_files=['interface_service/configs/settings.yaml'],
    # Enable layered environments
    environments=True,
    # To switch environments `export REMLA_ENV=deployment`
    env_switcher="REMLA_ENV",
)

settings.validators.register(
    # Check that either the development or the deployment envs is active.
    Validator("env", is_in=["development", "deployment"]),

    Validator(VarNames.OBJECT_STORAGE_ENDPOINT.value, must_exist=True),
    Validator(VarNames.OBJECT_STORAGE_ACCESS_KEY.value, must_exist=True),
    Validator(VarNames.OBJECT_STORAGE_SECRET_KEY.value, must_exist=True),
    Validator(VarNames.OBJECT_STORAGE_TLS.value, default=False),
    Validator(VarNames.BUCKET_NAME.value, must_exist=True),
    Validator(VarNames.MODEL_OBJECT_KEY.value, must_exist=True),
    Validator(VarNames.MODEL_LOCAL_PATH.value, must_exist=True),

    Validator(VarNames.PUBSUB_EMULATOR_HOST.value, default=None),
    Validator(VarNames.PUBSUB_PROJECT_ID.value, must_exist=True),
    Validator(VarNames.PUBSUB_DATA_TOPIC_ID.value, must_exist=True),
    Validator(VarNames.PUBSUB_MODEL_TOPIC_ID.value, must_exist=True),
    Validator(VarNames.PUBSUB_SUBSCRIPTION_ID.value, must_exist=True),
)

settings.validators.validate()
