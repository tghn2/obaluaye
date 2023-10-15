from fastapi import UploadFile
import sys
from uuid import UUID
from pathlib import Path
from io import BufferedReader
from collections.abc import Iterator
from botocore.response import StreamingBody

from app.core.config import settings
from app.crud.crud_spaces import spaces


class CRUDFiles:
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD) working data on the local drive.
        """
        self.directory = self.check_path(directory=settings.WORKING_PATH)
        self.use_spaces = settings.USE_SPACES

    ###################################################################################################
    # PATH MANAGEMENT
    ###################################################################################################
    def check_path(self, *, directory: Path | str) -> Path:
        if isinstance(directory, str):
            directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def check_source(self, *, source: Path | str) -> bool:
        if isinstance(source, str):
            source = Path(source)
        return source.exists()

    ###################################################################################################
    # SOURCE MANAGEMENT
    ###################################################################################################
    def exists(
        self,
        *,
        folder_id: UUID | str | None = None,
        source_id: UUID | str,
    ) -> StreamingBody | Iterator[BufferedReader]:
        if self.use_spaces:
            return spaces.exists(folder_id=folder_id, filename=source_id)
        source_path = self.directory
        if folder_id:
            source_path = self.check_path(directory=self.directory / folder_id)
        return self.check_source(source=source_path / source_id)

    def create(
        self,
        *,
        source: UploadFile,
        folder_id: UUID | str | None = None,
        source_id: UUID | str
    ):
        # https://stackoverflow.com/questions/63048825/how-to-upload-file-using-fastapi/70657621#70657621
        source_path = self.directory
        if folder_id:
            source_path = self.check_path(directory=self.directory / folder_id)
        try:
            with open(source_path / source_id, "wb") as f:
                while contents := source.file.read():
                    f.write(contents)
        except Exception as e:
            raise ValueError(e)
        finally:
            source.file.close()
        if self.use_spaces:
            spaces.upload_file(folder_id=folder_id, filename=source_id, source_path=source_path / source_id)

    def get(
        self,
        *,
        folder_id: UUID | str | None = None,
        source_id: UUID | str,
    ) -> StreamingBody | Iterator[BufferedReader]:
        if self.use_spaces:
            if spaces.exists(folder_id=folder_id, filename=source_id):
                return spaces.get_stream(folder_id=folder_id, filename=source_id)
        source_path = self.directory
        if folder_id:
            source_path = self.check_path(directory=self.directory / folder_id)
        if self.check_source(source=source_path / source_id):
            with open(source_path / source_id, mode="rb") as stream:
                while chunk := stream.read(settings.CHUNK_SIZE):
                    yield chunk

    def remove(self, *, folder_id: UUID | str | None = None, source_id: UUID | str):
        source_path = self.directory
        if folder_id:
            source_path = self.directory / folder_id
        source_path = source_path / source_id
        if self.check_source(source=source_path):
            try:
                assert sys.version_info >= (3, 8)
            except AssertionError:
                source_path.unlink()
            else:
                source_path.unlink(missing_ok=True)
        if self.use_spaces:
            if spaces.exists(folder_id=folder_id, filename=source_id):
                spaces.remove(folder_id=folder_id, filename=source_id, source_path=source_path)
        return source_path

files = CRUDFiles()
