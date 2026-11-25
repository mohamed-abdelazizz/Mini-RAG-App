from .BaseDataModel import BaseDataModel
from .db_schemas import DataChunk
from .enums.DataBaseEnums import DataBaseEnums
from typing import Union
from bson.objectid import ObjectId
from pymongo import InsertOne


class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object):

        super().__init__(db_client=db_client)
        self.collection = db_client[DataBaseEnums.COLLECTION_CHUNK_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):

        instance = cls(db_client=db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):

        existing_indexes = await self.collection.index_information()
        indexes = DataChunk.get_indexes()

        for index in indexes:
            if index["name"] not in existing_indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_chunk(self, chunk: DataChunk):

        result = await self.collection.insert_one(chunk.model_dump(by_alias=True, exclude_unset=True))
        chunk.id = result.inserted_id
        return chunk

    async def get_chunk(self, chunk_id: Union[str, ObjectId]):

        if isinstance(chunk_id, str):
            chunk_id = ObjectId(chunk_id)

        record = await self.collection.find_one({
            "_id": chunk_id
        })

        if record is None:
            return None

        return DataChunk(**record)

    async def insert_many_chunks(self, chunks: list, batch_size: int=100):

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]

            operations = [
                InsertOne(chunk.model_dump(by_alias=True, exclude_unset=True))
                for chunk in batch
            ]

            await self.collection.bulk_write(operations)

        return len(chunks)

    async def delete_chunks_by_project_id(self, project_id: Union[str, ObjectId]):

        if isinstance(project_id, str):
            project_id = ObjectId(project_id)

        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })

        return result.deleted_count
