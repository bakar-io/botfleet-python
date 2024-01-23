# BotFleet Python SDK

[![PyPI version](https://img.shields.io/pypi/v/botfleet.svg)](https://pypi.org/project/botfleet/)

The BotFleet Python SDK provides convenient access to the BotFleet REST API from any Python 3.8+
application. The SDK includes rich type definitions and enables receiving real-time executions
via WebSockets.

## Documentation

Full documentation of the SDK is available at [https://botfleet.ai/docs/sdk/introduction](https://botfleet.ai/docs/sdk/introduction). You may also want to check out the [REST API Reference](https://botfleet.ai/docs/api/v1/introduction).

## Installation

You can install the SDK via `pip`:

```bash
pip install botfleet
```

## Usage

Once installed, you can use it to make requests.

### Create a Bot

```python
import botfleet

botfleet.api_key = "YOUR_API_KEY"

bot = botfleet.Bot.create(
    name="My Bot",
    script="def main(request, store):\n    return request.payload",
    requirements="requests==2.31.0\npandas==2.1.4",
    env_vars="FOO=bar\nBAZ=qux",
    python_version="3.11",
    store_id="b553e996-6556-42dd-8990-ddb7ef2142f6",
)
```

### Execute a Bot

```python
import botfleet

botfleet.api_key = "YOUR_API_KEY"

bot = botfleet.Bot.retrieve(id="15d19ca3-26f1-4adb-9cea-3955b73d9b4e")

execution = bot.execute(payload={"key": "value"})
```

### Create a Cron Job

```python
import botfleet

botfleet.api_key = "YOUR_API_KEY"

cron_job = botfleet.BotExecutorCronJob.create(
    bot_id="15d19ca3-26f1-4adb-9cea-3955b73d9b4e",
    name="My cron job",
    expression="* * * * *",
)
```

### Stream Executions from a Cron Job

```python
import botfleet

botfleet.api_key = "YOUR_API_KEY"

cron_job = botfleet.BotExecutorCronJob.retrieve(id="f3384d13-7a32-4abe-9c10-964ca17413b7")

for execution in cron_job.stream():
    # Every time a new execution is created, it will be printed.
    print(execution)
```

These are only a few examples of what you can do with the SDK. Refer to the [full documentation](https://botfleet.ai/docs/sdk/introduction) to learn more about the SDK.