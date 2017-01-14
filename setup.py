from distutils.core import setup

author_info = {"Josh Manning": "jcmanning@email.arizona.edu",
               "Calvin McLean": "calvinmclean@email.arizona.edu",
               "Shawtaroh Nakajima": "shawtarohg@email.arizona.edu",
               "Eric Evans": "ericmichaelevans@email.arizona.edu"}

authors, author_emails = map(', '.join, zip(*author_info.items()))
setup(
    name="Hackerz",
    version="0.1.0",
    author=authors,
    author_email=author_emails,

    packages=["hackerz"],
    include_package_data=True,
    url="None",

    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "flask-wtf",
        "flask-nav",
        "flask-bootstrap"
    ],
)
