import os
import heroku3
import asyncio

from sys import executable as execute

from git import Repo as Repository
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from ..events import register as CgbanBang
from .. import HEROKU_API_KEY, HEROKU_APP_NAME


# rqrmnt = os.path.join(
#    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
# )

# rqr = str(rqrmnt)

build_packages = "https://github.com/unknownkz/BuildPackages"


# async def actuate():
#    try:
#        process = await asyncio.create_subprocess_shell(
#            " ".join([execute, "-m", "pip", "install", "-r", rqr]),
#            stdout=asyncio.subprocess.PIPE,
#            stderr=asyncio.subprocess.PIPE,
#        )
#        await process.communicate()
#        return process.returncode
#    except Exception as e:
#        return __repr__(e)


# async def booster(Quick, repository, upstream_remote, active_branch):
#    try:
#        upstream_remote.pull(active_branch)
#    except GitCommandError:
#        repository.git.reset("--hard", "FETCH_HEAD")
#    await actuate()
#    xx = await Quick.edit(
#        "Successfully Boost!\n-Restarting..."
#    )
#    await event.client.reload(xx) 


async def bootloader(Quick, repository, upstream_remote, active_branch, txt):
    herogay = heroku3.from_key(HEROKU_API_KEY)
    herogay_applications = herogay.apps()
    upstream_remote.fetch(active_branch)
    repository.git.reset("--hard", "FETCH_HEAD")
    herogay_app = next(
        (app for app in herogay_applications if app.name == HEROKU_APP_NAME),
        None,
    )

    if herogay_app is None:
        await Quick.edit(
            f"Failling!!"
        )
        return repo.__del__()
    await Quick.edit(
        "Rebooting..."
    )
    herogay_git_url = herogay_app.git_url.replace(
        "https://", f"https://api:{HEROKU_API_KEY}@"
    )
    if "herogay" in repository.remotes:
        remote = repository.remote("herogay")
        remote.set_url(herogay_git_url)
    else:
        remote = repository.create_remote("herogay", herogay_git_url)
    try:
        remote.push(refspec="HEAD:refs/heads/main", force=True)
    except Exception as error:
        await Quick.edit(f"{txt}\n**Error :**\n`{error}`")
        return repository.__del__()
    build_status = herogay_app.builds(order_by="created_at", sort="desc")[0]
    if build_status.status == "failed":
        return await Quick.get_reply_message(
            "Build failed."
        )
    try:
        await event.client.disconnect()
        if HEROKU_ is not None:
            HEROKU_.restart()
    except CancelledError:
        pass        


@CgbanBang(pattern=r"^[.$!/;@]gitpush$")
async def upstream(event):
    await event.get_reply_message("is building a packages..")

    try:
        txt = (
            "Sorry, an error has occured."
            + "LOGTRACE:\n"
        )

        repository = Repository()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\nDirectory {error} isn't found.")
        return repository.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\nFailling {error}")
        return repository.__del__()
    except InvalidGitRepositoryError:
        repository = Repository.init()
        original = repository.create_remote("upstream", build_packages)
        original.fetch()
        repository.create_head("main", original.refs.main)
        repository.heads.main.set_tracking_branch(origin.refs.main)
        repository.heads.main.checkout(True)
    try:
        repository.create_remote("upstream", build_packages)
    except BaseException:
        pass
    active_branch = repository.active_branch.name
    upstream_remote = repository.remote("upstream")
    upstream_remote.fetch(active_branch)
    await event.edit("Bootloader...")
    await bootloader(Quick, repository, upstream_remote, active_branch, txt)
