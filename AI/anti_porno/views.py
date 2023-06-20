from django.shortcuts import render
from google.cloud import videointelligence, storage
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
"""Detects explicit content from the GCS path to a video."""
from rest_framework.response import Response

@api_view(['POST'])
def check_porno(req):
    _data_file = req.FILES['movie']
    path = 'workspace/data.mp4'
    default_storage.save(path, _data_file)
    if default_storage.exists(path):
        print('save suc')
    bucket_name = "indiestraw-bucket"
    # The contents to upload to the file
    source_file_name = "C:\\Users\\dong\\PycharmProjects\\indistraw-AI\\AI\\anti_porno\\static\\workspace\\data.mp4"

    # The ID of your GCS object
    destination_blob_name = req.data['movie_name']

    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
    default_storage.delete(path)
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    print(features)
    operation = video_client.annotate_video(
        request={"features": features, f"input_uri": f"gs://indiestraw-bucket/{destination_blob_name}"}
    )
    print("\nProcessing video for explicit content annotations:")

    result = operation.result(timeout=90)
    print("\nFinished processing.")
    a = {'VERY_UNLIKELY': 0, 'UNLIKELY': 0, 'POSSIBLE': 0, 'LIKELY': 0, 'VERY_LIKELY': 0}
    # Retrieve first result because a single video was processed
    frame_time = 0
    for frame in result.annotation_results[0].explicit_annotation.frames:
        likelihood = videointelligence.Likelihood(frame.pornography_likelihood)
        frame_time = frame.time_offset.seconds + frame.time_offset.microseconds / 1e6
        # print("Time: {}s".format(frame_time))
        # print("\tpornography: {}".format(likelihood.name))
        a[likelihood.name] += 1
    blob.delete(if_generation_match=None)
    if frame_time / 3 < (a['VERY_LIKELY'] + a['LIKELY']):
        return Response("This is porno")
    else:
        return Response("This is not porno")


from django.shortcuts import render

# Create your views here.
