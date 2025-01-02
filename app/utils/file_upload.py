from werkzeug.utils import secure_filename
import mimetypes
import io
from uuid import uuid4
import boto3
from app.config import config

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
def allowed_file(filename):
  """Verifica se a extensão do arquivo é permitida"""
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_upload(file):
  
  s3_client = boto3.client(
    's3',
    aws_access_key_id=config.AWS_IAM_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_IAM_SECRET_ACCESS_KEY,
    region_name=config.REGION_NAME
  )   
  try:
      filename = secure_filename(file.filename)
      key = f'uploads/{uuid4().hex}_{filename}'

      # Carregar o arquivo para o S3
      s3_client.upload_fileobj(
          file.stream,
          config.AWS_BUCKET_NAME,
          key,
      )

      # Retorna a URL pública do arquivo no S3
      file_url = f'https://{config.AWS_BUCKET_NAME}.s3.{config.REGION_NAME}.amazonaws.com/{key}'
      return file_url

  except Exception as e:
      print('[FILE_UPLOAD_FUNCTION_ERROR]', e)
      return False