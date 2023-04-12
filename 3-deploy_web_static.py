#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the function do_deploy
"""
from os import path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["52.91.132.17", "34.224.63.71"]


def do_pack():
    """
    A function that generates an archive
    """
    date = datetime.now()
    archive = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        date.year, date.month, date.day,
        date.hour, date.minute, date.second
    )
    if not path.isdir("versions"):
        if local("mkdir versions").failed:
            return None
    cmd = "cd web_static && tar -cvzf ../{} . && cd -".format(archive)
    if local(cmd).succeeded:
        return archive
    return None


def do_deploy(archive_path):
    """
    Distributes archives to web servers
    Args:
        archive_path: path to local archive to be uploaded
    """
    if not path.exists(archive_path):
        return False
    compressedFile = archive_path.split("/")[-1]
    fileName = compressedFile.split(".")[0]
    upload_path = "/tmp/{}".format(compressedFile)
    if put(archive_path, upload_path).failed:
        return False
    current_release = '/data/web_static/releases/{}'.format(fileName)
    if run("rm -rf {}".format(current_release)).failed:
        return False
    if run("mkdir {}".format(current_release)).failed:
        return False
    uncompress = "tar -xzf /tmp/{} -C {}".format(
        compressedFile, current_release
    )
    if run(uncompress).failed:
        return False
    delete_archive = "rm -f /tmp/{}".format(compressedFile)
    if run(delete_archive).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    relink = "ln -s {} /data/web_static/current".format(current_release)
    if run(relink).failed:
        return False
    return True


def deploy():
    """
    Creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
