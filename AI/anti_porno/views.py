from django.shortcuts import render
from google.cloud import videointelligence
from google.cloud import storage

"""Detects explicit content from the GCS path to a video."""


def dong(req):
    # The ID of your GCS bucket
    bucket_name = "indiestraw-bucket"
    print(req.data)
    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = req.data

    # storage_client = storage.Client()
    # bucket = storage_client.bucket(bucket_name)
    # blob = bucket.blob(destination_blob_name)
    #
    # blob.upload_from_string(contents)
    #
    # print(
    #     f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}."
    # )


def check_porno(req):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    print(features)
    operation = video_client.annotate_video(
        request={"features": features, "input_uri": "gs://indiestraw-bucket/ding.mp4"}
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
    if frame_time / 3 < (a['VERY_LIKELY'] + a['LIKELY']):
        return "This is porno"
    else:
        return "This is not porno"
from django.shortcuts import render

# Create your views here.