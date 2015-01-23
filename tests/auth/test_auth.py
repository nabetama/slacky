from tests.test_common import TestSlack


class TestAuth(TestSlack):
    def test_auth(self):
        assert self.slack.auth

    def test_auth_test(self):
        assert self.slack.auth.test

    def test_auth_test_response(self):
        assert self.slack.auth.test.status_code == 200
