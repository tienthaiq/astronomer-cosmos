"Maps Airflow Trino connections to OAuth client credential Trino dbt profiles."
from __future__ import annotations

from typing import Any

from .base import TrinoBaseProfileMapping


class TrinoOAuthClientProfileMapping(TrinoBaseProfileMapping):
    required_fields = TrinoBaseProfileMapping.required_fields + [
        "client_id",
        "client_secret",
        "token_endpoint",
    ]
    secret_fields = [
        "client_secret",
    ]
    airflow_param_mapping = {
        "client_id": "login",
        "client_secret": "password",
        "token_endpoint": "host",
        "scheme": "extra.scheme",
        **TrinoBaseProfileMapping.airflow_param_mapping,
    }

    @property
    def profile(self) -> dict[str, Any | None]:
        """
        Returns a dbt Trino profile based on the Airflow Trino connection.
        """
        common_profile_vars = super().profile
        profile_vars = {
            **self.mapped_params,
            **common_profile_vars,
            "method": "oauth_client_credential",
            **self.profile_args,
            # password should always get set as env var
            "password": self.get_env_var_format("password"),
        }

        # remove any null values
        return self.filter_null(profile_vars)
