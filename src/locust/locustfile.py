from random import randint, choice
from locust import HttpLocust, TaskSet, task

class AsyncTest(TaskSet):
    @task(10)
    def threaded(self):
        self.client.get('/async/sleep/{0}'.format(randint(0,20)))

    @task(1)
    def hashSite(self):
        domains = ['google', 'facebook', 'twitter']
        self.client.get('/async/phish/%s' % (choice(domains)))

    @task(20)
    def coroutine(self):
        self.client.get('/async/coro')

    @task(15)
    def error(self):
        with self.client.get('/async/error', catch_response=True) as response:
            if response.status_code == 400:
                response.success()

class WebsiteUser(HttpLocust):
    task_set = AsyncTest
    min_wait=9000
    max_wait=10000

