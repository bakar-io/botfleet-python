import time
from typing import Dict, List

import pytest

import botfleet


def teardown():
    # When a Bot is deleted, the following cascade: BotBuilderJob, Build,
    # BotExecutorJob, BotExecutorCronJob, Execution. So we just have to delete
    # all the bots and the rest will be deleted automatically.
    _delete_all_bots()
    _delete_all_stores()
    _delete_all_bot_templates()


def prepare() -> Dict:
    """
    Since it takes time for the bot to get built and for an execution to be created,
    we want to do these things once and then use the same data for all tests.

    This function was initially called `setup` but pytest kept running it twice,
    instead of once as it should. So, it got renamed to `prepare`.
    """

    # This may seem weird here, but when tests are run for the very first time
    # against an user's account, we want to delete the default store. This is
    # so that we start with a clean slate and end with a clean slate every time
    # we run the tests.
    _delete_all_stores()

    store = botfleet.Store.create("teststore")

    bot = botfleet.Bot.create(
        name="testbot",
        script="def main():\n    print('hello world')\n",
        python_version="3.9",
        store_id=store.id,
    )

    bot_builder_job = botfleet.BotBuilderJob.list(bot_id=bot.id).results[0]
    build_id = None
    # Wait for the build to finish and get its id
    while True:
        time.sleep(3)
        builds = botfleet.Build.list(bot_builder_job_id=bot_builder_job.id).results
        if len(builds) == 1:
            build = builds[0]
            if build.status == "success":
                build_id = build.id
                break
            elif build.status == "failure":
                raise Exception("Build failed.")

    execution = bot.execute()

    return {
        "store_id": store.id,
        "bot_id": bot.id,
        "bot_builder_job_id": bot_builder_job.id,
        "build_id": build_id,
        "bot_executor_job_id": execution.bot_executor_job_id,  # type: ignore
        "execution_id": execution.id,
    }


@pytest.fixture(scope="session", autouse=True)
def prepare_and_teardown():
    """
    Run once at the beginning and once at the end of all tests.
    """

    data = prepare()
    yield data
    teardown()


def _get_every_page_paginated_resource(resource_class: type) -> List[object]:
    """
    Goes through all the pages of a paginated resource and returns a list of
    all the results.
    """
    ret = []
    resources = resource_class.list()  # type: ignore
    ret.extend(resources.results)
    while True:
        resources = resources.next()
        if resources is None:
            break
        ret.extend(resources.results)
    return ret


def _delete_all_bots():
    for bot in _get_every_page_paginated_resource(botfleet.Bot):
        botfleet.Bot.delete(bot.id)


def _delete_all_stores():
    for store in _get_every_page_paginated_resource(botfleet.Store):
        botfleet.Store.delete(store.id)


def _delete_all_bot_templates():
    for bot_template in _get_every_page_paginated_resource(botfleet.BotTemplate):
        botfleet.BotTemplate.delete(bot_template.id)
