#!/usr/bin/env python
__author__ = 'David Moser - david.moser@bitmovin.net'

import bitcodin

bitcodin.api_key = 'YOUR API KEY'

input_obj = bitcodin.Input(url='http://url.to.video.with.closed.captions')
input_result = bitcodin.create_input(input_obj)

video_configs = list()

video_configs.append(bitcodin.VideoStreamConfig(
    default_stream_id=0,
    bitrate=4800000,
    profile='Main',
    preset='premium',
    height=1080,
    width=1920
))
video_configs.append(bitcodin.VideoStreamConfig(
    default_stream_id=0,
    bitrate=2400000,
    profile='Main',
    preset='premium',
    height=768,
    width=1024
))
video_configs.append(bitcodin.VideoStreamConfig(
    default_stream_id=0,
    bitrate=1200000,
    profile='Main',
    preset='premium',
    height=480,
    width=854
))

audio_configs = [
    bitcodin.AudioStreamConfig(default_stream_id=0, bitrate=192000),
    bitcodin.AudioStreamConfig(default_stream_id=1, bitrate=192000)
]

encoding_profile_obj = bitcodin.EncodingProfile('API Test Profile Closed Captions', video_configs, audio_configs)
encoding_profile_result = bitcodin.create_encoding_profile(encoding_profile_obj)

manifests = ['mpd', 'm3u8']

audio_meta_data = [
    bitcodin.AudioMetaData(0, 'Spanish', 'es'),
    bitcodin.AudioMetaData(1, 'English', 'en')
]

video_meta_data = [
    bitcodin.VideoMetaData(0, 'Spanish', 'es')
]

job = bitcodin.Job(
    input_id=input_result.input_id,
    encoding_profile_id=encoding_profile_result.encoding_profile_id,
    manifest_types=manifests,
    speed='standard',
    extract_closed_captions=True,
    audio_meta_data=audio_meta_data,
    video_meta_data=video_meta_data
)

job_result = bitcodin.create_job(job)
