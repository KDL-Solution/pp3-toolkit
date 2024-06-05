from pp3.toolkit.resource import download_public_resource
from pp3.toolkit.auth import login
session = login("admin", "admin1234")
download_public_resource(session,1)