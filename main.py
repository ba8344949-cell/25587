from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from pymilvus import DataType, MilvusClient

load_dotenv()

VECTOR_DIM = int(os.getenv("VECTOR_DIM", "4"))
DB_NAME = os.getenv("MILVUS_DB_NAME", "demo_db")
COLLECTION = os.getenv("MILVUS_COLLECTION", "products")


def get_client() -> MilvusClient:
    uri = os.environ["MILVUS_URI"]
    token = os.environ["MILVUS_TOKEN"]
    return MilvusClient(uri=uri, token=token, db_name=DB_NAME)


def ensure_database(client: MilvusClient) -> None:
    databases = client.list_databases()
    if DB_NAME not in databases:
        client.create_database(DB_NAME)


def ensure_collection(client: MilvusClient) -> None:
    if client.has_collection(collection_name=COLLECTION):
        return

    schema = client.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="title", datatype=DataType.VARCHAR, max_length=256)
    schema.add_field(field_name="price", datatype=DataType.FLOAT)
    schema.add_field(
        field_name="vector",
        datatype=DataType.FLOAT_VECTOR,
        dim=VECTOR_DIM,
    )

    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="vector",
        index_type="AUTOINDEX",
        metric_type="COSINE",
    )

    client.create_collection(
        collection_name=COLLECTION,
        schema=schema,
        index_params=index_params,
    )


def seed(client: MilvusClient) -> None:
    rows = [
        {"id": 1, "title": "Keyboard", "price": 149.0, "vector": [0.10, 0.20, 0.30, 0.40]},
        {"id": 2, "title": "Mouse", "price": 79.0, "vector": [0.20, 0.10, 0.40, 0.30]},
        {"id": 3, "title": "Monitor", "price": 899.0, "vector": [0.40, 0.30, 0.20, 0.10]},
    ]
    client.insert(collection_name=COLLECTION, data=rows)


def search(client: MilvusClient, vector: list[float], limit: int = 3) -> list[dict[str, Any]]:
    return client.search(
        collection_name=COLLECTION,
        data=[vector],
        anns_field="vector",
        limit=limit,
        output_fields=["id", "title", "price"],
    )


def main() -> None:
    client = get_client()
    ensure_database(client)
    ensure_collection(client)
    seed(client)
    print(search(client, [0.10, 0.20, 0.30, 0.40]))


if __name__ == "__main__":
    main()
