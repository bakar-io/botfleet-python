import botfleet

from .fixtures import prepare_and_teardown  # noqa: F401


def test_bot_builder_job(prepare_and_teardown):
    data = prepare_and_teardown

    jobs = botfleet.BotBuilderJob.list(bot_id=data["bot_id"])
    assert jobs.total_count == 1
    assert jobs.results[0].id == data["bot_builder_job_id"]

    job = botfleet.BotBuilderJob.retrieve(data["bot_builder_job_id"])
    assert job.id == data["bot_builder_job_id"]


def test_build(prepare_and_teardown):
    data = prepare_and_teardown

    builds = botfleet.Build.list(bot_builder_job_id=data["bot_builder_job_id"])
    assert builds.total_count == 1
    assert builds.results[0].id == data["build_id"]

    build = botfleet.Build.retrieve(data["build_id"])
    assert build.id == data["build_id"]


def test_execution(prepare_and_teardown):
    data = prepare_and_teardown

    executions = botfleet.Execution.list(bot_id=data["bot_id"])
    assert len(executions.results) == 1
    assert executions.results[0].id == data["execution_id"]

    execution = botfleet.Execution.retrieve(data["execution_id"])
    assert execution.id == data["execution_id"]


def test_bot_executor_job(prepare_and_teardown):
    data = prepare_and_teardown

    botfleet.BotExecutorJob.create(bot_id=data["bot_id"], payload={"foo": "bar"})

    jobs = botfleet.BotExecutorJob.list(bot_id=data["bot_id"])
    assert len(jobs.results) == 2

    job = botfleet.BotExecutorJob.retrieve(data["bot_executor_job_id"])
    assert job.id == data["bot_executor_job_id"]


def test_bot(prepare_and_teardown):
    data = prepare_and_teardown

    bot = botfleet.Bot.create(
        name="testbot2",
        script="def main():\n    print('hello world')\n",
        requirements="requests",
        env_vars="FOO=BAR",
        python_version="3.9",
        store_id=data["store_id"],
    )
    assert botfleet.Bot.update(bot.id, name="updated").name == "updated"
    assert botfleet.Bot.list().total_count == 2
    assert botfleet.Bot.retrieve(bot.id).id == bot.id
    botfleet.Bot.delete(bot.id)
    assert botfleet.Bot.list().total_count == 1


def test_execute_bot(prepare_and_teardown):
    data = prepare_and_teardown

    bot = botfleet.Bot.retrieve(data["bot_id"])

    execution = bot.execute()
    assert type(execution) is botfleet.Execution

    bot_executor_job = bot.execute(wait=False)
    assert type(bot_executor_job) is botfleet.BotExecutorJob


def test_bot_executor_cron_job(prepare_and_teardown):
    data = prepare_and_teardown

    cron_job = botfleet.BotExecutorCronJob.create(
        bot_id=data["bot_id"], name="test", expression="* * * * *"
    )
    assert cron_job.status == "running"
    assert (
        botfleet.BotExecutorCronJob.update(cron_job.id, status="suspended").status
        == "suspended"
    )
    assert botfleet.BotExecutorCronJob.list(bot_id=data["bot_id"]).total_count == 1
    assert botfleet.BotExecutorCronJob.retrieve(cron_job.id).id == cron_job.id
    botfleet.BotExecutorCronJob.delete(cron_job.id)
    assert botfleet.BotExecutorCronJob.list(bot_id=data["bot_id"]).total_count == 0


def test_store():
    store = botfleet.Store.create("test")
    assert botfleet.Store.update(store.id, name="updated").name == "updated"
    assert botfleet.Store.list().total_count == 2
    assert botfleet.Store.retrieve(store.id).id == store.id
    botfleet.Store.delete(store.id)
    assert botfleet.Store.list().total_count == 1


def test_bot_template():
    bot_template = botfleet.BotTemplate.create(
        name="test",
        description="test",
        script="def main():\n    print('hello world')\n",
        requirements="requests",
        env_vars="FOO=BAR",
        python_version="3.9",
        public=True,
    )
    assert (
        botfleet.BotTemplate.update(bot_template.id, name="updated").name == "updated"
    )
    assert botfleet.BotTemplate.list().total_count == 1
    assert botfleet.BotTemplate.retrieve(bot_template.id).id == bot_template.id
    botfleet.BotTemplate.delete(bot_template.id)
    assert botfleet.BotTemplate.list().total_count == 0
