from .BaseDataModel import BaseDataModel
from .db_schemas import Asset
from .enums.DataBaseEnums import DataBaseEnums
from typing import Union
from bson.objectid import ObjectId


class AssetModel(BaseDataModel):

    def __init__(self, db_client: object):

        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnums.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):

        instance = cls(db_client=db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):

        existing_indexes = await self.collection.index_information()
        indexes = Asset.get_indexes()

        for index in indexes:
            if index["name"] not in existing_indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_asset(self, asset: Asset):

        result = await self.collection.insert_one(asset.model_dump(by_alias=True, exclude_none=True))
        asset.id = result.inserted_id
        return asset

    async def get_all_project_assets(self, asset_project_id: Union[str, ObjectId]):

        if isinstance(asset_project_id, str):
            asset_project_id = ObjectId(asset_project_id)

        return await self.collection.find({
            "asset_project_id": asset_project_id
        }).to_list(length=None)
