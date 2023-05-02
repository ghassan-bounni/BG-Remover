import os
import logging
import boto3
from rembg import remove
from PIL import Image
from botocore.exceptions import ClientError
import constants as c


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=c.ACCESS_KEY_ID,
        aws_secret_access_key=c.SECRET_ACCESS_KEY,
    )
    try:
        _ = s3_client.upload_file(file_name, bucket, object_name)
        s3_url = f"https://{c.BUCKET_NAME}.s3.amazonaws.com/{object_name}"
    except ClientError as error:
        logging.error(error)
        return False, None
    return (True, s3_url)


def remove_bg_local(input_path):
    output_path = (
        input_path.split(".")[0].replace("+", "%2B").replace(" ", "%20") + "-clean.png"
    )

    try:
        input_img = Image.open(input_path)
        output = remove(input_img)
        output.save(output_path)
    except IOError as error:
        print(str(error))

    res, url = upload_file(output_path, c.BUCKET_NAME)
    if not res:
        print("Upload failed")

    return url


def main():
    # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
    for f in os.listdir("images"):
        if f.endswith(".png"):
            input_path = os.path.join("images", f)
            print(remove_bg_local(input_path))

    # input_path = "images/075125.png"
    # print(remove_bg_local(input_path))


if __name__ == "__main__":
    main()
