# from scripts.database_creation import database_creation
from scripts.ingest import database_creation
from scripts.extract_graph import extract_graph
from scripts.ingest import ingesting


def main():
    indexing=True
    extract_graph()
    indexing = database_creation(indexing)
    ingesting(indexing=indexing)


if __name__ == "__main__":
    main()


