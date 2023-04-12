#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the function do_deploy
"""
from os import path
from fabric.api import env, put, run

env.hosts = ["52.91.132.17", "34.224.63.71"]


def do_deploy(archive_path):
    """
    Distributes archives to web servers
    """
    if not path.exists(archive_path):
        return False
    compressedFile = archive_path.split("/")[-1]
    fileName = compressedFile.split(".")[0]
    upload_path = "/tmp/{}".format(compressedFile)
    if put(archive_path, upload_path).failed:
        return False
    current_release = '/data/web_static/releases/{}'.format(fileName)
    if run("sudo rm -rf {}".format(current_release)).failed:
        return False
    if run("sudo mkdir -p {}".format(current_release)).failed:
        return False
    uncompress = "sudo tar -xzf /tmp/{} -C {}".format(
        compressedFile, current_release
    )
    if run(uncompress).failed:
        return False
    delete_archive = "sudo rm -f /tmp/{}".format(compressedFile)
    if run(delete_archive).failed:
        return False
    if run("sudo rm -rf /data/web_static/current").failed:
        return False
    relink = "sudo ln -s {} /data/web_static/current".format(current_release)
    if run(relink).failed:
        return False
    return True
