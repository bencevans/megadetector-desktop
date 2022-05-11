from distutils.core import setup
import py2app

setup(
    app=["app.py"],
    setup_requires=["py2app"]
)
