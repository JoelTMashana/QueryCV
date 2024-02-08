import os

TESTING = os.environ.get("TESTING")

if TESTING:
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
else:
    SQLALCHEMY_DATABASE_URL = "postgres://nwkymrfrsziztn:c37e75d8ec360648907dc8b018fec36b1e788ce78f0d73e4c3a2871ecbc0ba19@ec2-54-195-120-0.eu-west-1.compute.amazonaws.com:5432/d7haada96kmjl"
