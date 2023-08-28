# Copyright 2023 Curtin University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Author: Alex Massen-Hane

import os
import pathlib
from typing import Dict, Union, List, Optional
from openaire.files import schema_folder as default_schema_folder


class Table:
    def __init__(
        self,
        name: str,
        num_parts: int,
        zenodo_url_path: str,
        full_table_id: str,
        download_folder: str,
        decompress_folder: str,
        gcs_uri_pattern: str,
        alt_name: Optional[str] = None,
        remove_nulls: Optional[Union[str, List[str]]] = None,
        local_part_list_gz: Optional[List[str]] = None,
        uri_part_list: Optional[List[str]] = None,
    ):
        self.name = name
        self.num_parts = num_parts
        self.zenodo_url_path = zenodo_url_path
        self.full_table_id = full_table_id
        self.remove_nulls = remove_nulls
        self.alt_name = alt_name
        self.local_part_list_gz = local_part_list_gz
        self.uri_part_list = uri_part_list

        self.gcs_uri_pattern = gcs_uri_pattern

        self.download_folder = os.path.join(download_folder, name)
        self.decompress_folder = os.path.join(decompress_folder)
        self.part_location = os.path.join(decompress_folder, name)

        self.zenodo_name = alt_name if alt_name else name

    @property
    def schema_path(self):
        return os.path.join(default_schema_folder(), "schemas", f"{self.name}.json")

    @property
    def download_paths(self) -> Dict[str, str]:
        """Dictionary of downloads[download_url] = download_local_file_location ."""

        # Create the download folder for this table's data.
        pathlib.Path(self.download_folder).mkdir(parents=True, exist_ok=True)

        downloads = {}
        if self.num_parts > 1:
            for i in range(self.num_parts):
                downloads[f"{self.zenodo_url_path}/files/{self.zenodo_name}_{i+1}.tar"] = os.path.join(
                    self.download_folder, f"{self.name}_{i+1}.tar"
                )
        else:
            downloads[f"{self.zenodo_url_path}/files/{self.zenodo_name}.tar"] = os.path.join(
                self.download_folder, f"{self.name}.tar"
            )

        return downloads
