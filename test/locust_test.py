"""
Locust Load Testing Tool

An open source load testing tool.

Define user behaviour with Python code, 
and swarm your system with millions of simultaneous users. 

dependencies:
    - locust

pip install locust

Run Locust with command:
    locust -f locust_test.py --host=http://
"""

from locust import HttpUser, task, between

class AppUser(HttpUser):
    wait_time = between(2, 5)

    # Endpoint to test
    @task
    def index_page(self):
        self.client.get("/")