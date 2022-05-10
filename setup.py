from distutils.core import setup
import py2app

setup(
    app=["myscript.py"],
    setup_requires=["py2app"]
)
