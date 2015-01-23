from tests.test_common import TestSlack


class TestApi(TestSlack):
    def test_api(self):
        assert self.slack.api

    def test_api_test(self):
        assert self.slack.api.test

    def test_api_test_response(self):
        assert self.slack.api.test.status_code == 200
