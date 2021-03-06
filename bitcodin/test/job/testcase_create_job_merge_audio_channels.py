#!/usr/bin/env python
from time import sleep

import bitcodin
from bitcodin.test.bitcodin_test_case import BitcodinTestCase


class CreateJobTestCase(BitcodinTestCase):
    def setUp(self):
        super(CreateJobTestCase, self).setUp()
        input_url = 'http://bitbucketireland.s3.amazonaws.com/at_test/mono_streams.mkv'
        input = bitcodin.Input(input_url)
        self.input = bitcodin.create_input(input)

        audio_configs = [
            bitcodin.AudioStreamConfig(
                default_stream_id=0,
                bitrate=192000
            )
        ]

        video_stream_config = [
            bitcodin.VideoStreamConfig(
                default_stream_id=0,
                bitrate=512000,
                profile='Main',
                preset='premium',
                height=480,
                width=640
            )
        ]

        encoding_profile = bitcodin.EncodingProfile('API Merge Audio Multi Profile',
                                                    video_stream_config,
                                                    audio_configs)

        self.encoding_profile = bitcodin.create_encoding_profile(encoding_profile)
        self.manifests = ['m3u8', 'mpd']

        merge_audio_channel_config = bitcodin.MergeAudioChannelConfig([1, 2, 3, 4, 5, 6])

        self.merge_audio_channel_configs = [merge_audio_channel_config]

        audio_meta_data = bitcodin.AudioMetaData(0, 'en', 'All audio channels merged')

        self.audio_meta_data = [audio_meta_data]

    def runTest(self):
        job = bitcodin.Job(
            input_id=self.input.input_id,
            encoding_profile_id=self.encoding_profile.encoding_profile_id,
            manifest_types=self.manifests,
            speed='standard',
            merge_audio_channel_configs=self.merge_audio_channel_configs,
            audio_meta_data=self.audio_meta_data
        )
        self.job = bitcodin.create_job(job)
        self.assertEquals(self.job.input.input_id, job.inputId)
        self.assertEquals(self.job.input.url, self.input.url)
        self.assertEquals(self.job.encoding_profiles[0].encoding_profile_id, job.encodingProfileId)
        self.wait_until_job_finished(self.job.job_id)

    def tearDown(self):
        bitcodin.delete_input(self.input.input_id)
        bitcodin.delete_encoding_profile(self.encoding_profile.encoding_profile_id)
        super(CreateJobTestCase, self).tearDown()
