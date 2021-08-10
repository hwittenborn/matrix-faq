<h1 align="center">matrix-faq</h1>
matrix-faq is a bot for Matrix homeservers that allows for predefined messages to be sent with shorter, command-like aliases.

For example, you could run the following command:

```sh
!faq projects
```

Which could then return the following text:

```
Projects I'm currently working on:

- Foo (github.com/user/foo)
- Bar (github.com/user/bar)
```

## Setup
To actually run the bot, you'll need to create an empty directory that contains a file named `config.yaml`. An example file containing the needed information can be found at `src/config.yaml` in this repository.

## Running
The preferred (and only supported) way for running the bot is with Docker.

A prebuilt image can be downloaded from here:

```
proget.hunterwittenborn.com/docker/hunter/matrix-faq:latest
```

The Docker image expects the configuration file to be located at `/data/config.yml` inside the container.

Likewise, you can use the following command to run the image:

```sh
docker run --volume="${PWD}:/data" --restart=unless-stopped proget.hunterwittenborn.com/docker/hunter/matrix-faq:latest
```

## Runtime data
If all prechecks pass (i.e. linting the config file, verifying the password, etc.), a new file named `sqlite3.db` will be created in same directory containing your config file. Do **NOT** delete this file, as it contains important information needed by the bot to run.
