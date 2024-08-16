import os
import json
import boto3
import pathlib
from botocore.exceptions import ClientError
from tempfile import mkdtemp
from pdfminer.high_level import extract_text

# LanceDB and Langchain imports (assuming these libraries have equivalent Python support)
from vectordb import connect  # LanceDB equivalent in Python
from langchain.embeddings import BedrockEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PDFLoader
from langchain.vectorstores import LanceDB

# Environment variables
LANCE_DB_SRC = os.getenv('s3BucketName')
LANCE_DB_TABLE = os.getenv('lanceDbTable')
AWS_REGION = os.getenv('region')

# S3 client
s3_client = boto3.client('s3', region_name=AWS_REGION)

# Initialize the text splitter and embeddings
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
embeddings = BedrockEmbeddings(region=AWS_REGION, model='amazon.titan-embed-text-v1')

def return_error(error):
    return {
        'statusCode': 500,
        'body': json.dumps({'message': str(error)})
    }

def download_object(bucket_name, object_key, download_path):
    try:
        # Get the object from the S3 bucket
        s3_client.download_file(bucket_name, object_key, download_path)
        print(f"File downloaded to {download_path}")
    except ClientError as e:
        print(f"Error downloading object {object_key} from bucket {bucket_name}: {str(e)}")
        raise e

def create_directory():
    try:
        tmp_path = mkdtemp()
        print(f"Directory created at: {tmp_path}")
        return tmp_path
    except Exception as e:
        print(f"Error creating directory: {str(e)}")
        raise e

def lambda_handler(event, context):
    try:
        # Get bucket and object key from the S3 event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        file_path = f"/tmp/{pathlib.PurePath(object_key).name}"

        # Create temporary directory and download the file
        create_directory()
        download_object(bucket_name, object_key, file_path)

        # Load and split the PDF
        try:
            loader = PDFLoader(file_path, split_pages=False)
            docs = loader.load_and_split(splitter)
        except Exception as error:
            print(f"Error loading documents: {error}")
            return return_error(error)

        # Connect to LanceDB
        dir = f"s3://{LANCE_DB_SRC}/embeddings"
        try:
            db = connect(dir)
        except Exception as error:
            print(f"Error connecting to LanceDB: {error}")
            return return_error(error)

        # Open or create the LanceDB table
        create_table = False
        try:
            table = db.open_table(LANCE_DB_TABLE)
        except Exception as error:
            create_table = True
            print(f"Table not found with error: {error}")

        if create_table:
            try:
                table = db.create_table(LANCE_DB_TABLE, [
                    {'vector': [0] * 1536, 'text': 'sample'},
                ])
            except Exception as error:
                print(f"Error creating LanceDB table {LANCE_DB_TABLE}: {error}")
                return return_error(error)

        # Prepare documents and upload to LanceDB
        docs = [{'pageContent': doc.page_content, 'metadata': {}} for doc in docs]
        LanceDB.from_documents(docs, embeddings, table=table)

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'OK'})
        }

    except Exception as e:
        return return_error(e)