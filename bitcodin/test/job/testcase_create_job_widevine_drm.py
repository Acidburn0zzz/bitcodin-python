__author__ = 'Dominic Miglar <dominic.miglar@bitmovin.net>'

import unittest
from bitcodin import create_job
from bitcodin import create_input
from bitcodin import create_encoding_profile
from bitcodin import delete_input
from bitcodin import delete_encoding_profile
from bitcodin import Job
from bitcodin import Input
from bitcodin import AudioStreamConfig
from bitcodin import VideoStreamConfig
from bitcodin import EncodingProfile
from bitcodin import DrmConfig
from bitcodin import WidevineDrmConfig
from bitcodin import PlayreadyDrmConfig
from bitcodin.exceptions import BitcodinBadRequestError
from bitcodin.test.config import test_video_url
from bitcodin.test.bitcodin_test_case import BitcodinTestCase


class CreateJobWidevineDrmTestCase(BitcodinTestCase):
    def setUp(self):
        super(CreateJobWidevineDrmTestCase, self).setUp()
        input_url = test_video_url
        input = Input(input_url)
        self.input = create_input(input)
        audio_stream_config = AudioStreamConfig(default_stream_id=0, bitrate=192000)
        video_stream_config = VideoStreamConfig(default_stream_id=0, bitrate=512000,
                                                profile='Main', preset='premium', height=480, width=640)
        encoding_profile = EncodingProfile('API Test Profile', [video_stream_config], [audio_stream_config])
        self.encoding_profile = create_encoding_profile(encoding_profile)
        self.manifests = ['m3u8', 'mpd']
        self.drm_config = WidevineDrmConfig(
            provider='widevine_test',
            signing_key='1ae8ccd0e7985cc0b6203a55855a1034afc252980e970ca90e5202689f947ab9',
            signing_iv='d58ce954203b7c9a9a9d467f59839249',
            request_url='http://license.uat.widevine.com/cenc/getcontentkey',
            content_id='746573745f69645f4639465043304e4f',
            method='mpeg_cenc'
        )

    def runTest(self):
        job = Job(
            input_id=self.input.input_id,
            encoding_profile_id=self.encoding_profile.encoding_profile_id,
            manifest_types=self.manifests,
            speed='standard',
            drm_config=self.drm_config
        )
        self.job = create_job(job)
        self.assertEquals(self.job.input.input_id, job.inputId)
        self.assertEquals(self.job.input.url, self.input.url)
        self.assertEquals(self.job.encoding_profiles[0].encoding_profile_id, job.encodingProfileId)
        self.wait_until_job_finished(self.job.job_id)

    def tearDown(self):
        delete_input(self.input.input_id)
        delete_encoding_profile(self.encoding_profile.encoding_profile_id)
        super(CreateJobWidevineDrmTestCase, self).tearDown()


if __name__ == '__main__':
    unittest.main()
