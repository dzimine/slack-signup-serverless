# StackStorm Community Signup Serverless Service

[![Build Status](https://circleci.com/gh/dzimine/slack-signup-serverless/tree/master.svg?style=shield)](https://circleci.com/gh/dzimine/slack-signup-serverless)

> This time, with [Serverless framework](https://serverless.com)

This is a 'take two' on [Slack Signup with AWS Lambda](https://github.com/dzimine/slack-signup-lambda).
It was simple and functional, but working with AWS raw is such a pain in the butt...

Here, I use 1) [serverless.com](https://serverless.com) to make working with lambda enjoyable and 2) AWS step-functions
for multi-step sign-up workflow that touches multiple services.


### Install, configure, deploy, test
1. Clone this repository.
2. Install [serverless framework](https://serverless.com/framework/docs), and the required plugins:

    ```
    npm install -g serverless
    npm install
    ```

3. Configure credentials

    1. For AWS credentials, follow [setup docs](https://serverless.com/framework/docs/providers/aws/guide/credentials/).
        I prefer using [AWS CLI with named profiles](http://docs.aws.amazon.com/cli/latest/userguide/
        cli-multiple-profiles.html). Test AWS CLI settings: `aws lambda list-functions`.

        To use an AWS profile in Serverless, `export AWS_PROFILE="profileName"`,
        or use `--aws-profile profileName` when invoking `sls` CLI. Unfortunately there's no way
        to test it before you try to deploy.

        Create `./private.yml` file and set up the accountID and region there,
        see [`private.yml.example`](./private.yml.example)
    2. Slack and ActiveCampaign: place your credentials and config in `./env.yml`, use [env.yml.example](./env.yml.example)

4. Deploy

    1. Install Python dependencies:

        ```
        ./build.sh
        ```
    2. Deploy serverless stack

        ```
        sls deploy -v
        ```
    3. Enable the CORS via AWS console (for calling from web UI). Select resource, click "Actions"
        menu button, "Enable CORS", click the blue "Enable CORS" button.
        It will add "OPTIONS" method and set up the proper response headers.

        >TODO: Create CloudFormation API Resource in serverless file (instead of [serverless-step-function
        plugin](https://github.com/horike37/serverless-step-functions) shortcut which doesn't support CORS,
        or [fix the issue](https://github.com/horike37/serverless-step-functions/issues/37))

5. Run, with `curl`:

    ```
    curl -X PUT -H "Content-Type: application/json" -d '{"email":"your@email.com", "first_name":"Donald", "last_name":"Trump"}'  https://wqftmz3m97.execute-api.us-east-1.amazonaws.com/dev/signup
    ```
    
    Or, with `serverless`, for convenience: 
    
    ```
    sls invoke stepf --name signup --data '{"email":"your@email.com", "first_name":"Donald", "last_name":"Trump"}' 
    ```

### Unit testing
1. Set up python unit tests(TODO: script and CI this).

    ```
    virtualenv .venv
    source .venv/bin/activate
    pip install -r tests/test_requirements.txt
    ```

2. Run unit tests (hint: use `-s` to see output.

    ```
    python -m pytest
    ```


### Tips and tricks

* Call individual lambda functions with serverless

    ```
    sls invoke -f RecordAC --data '{"email":"your@email.com", "first_name":"Donald", "last_name":"Trump"}' 
    ```
* Watch the logs:

    ```
    sls logs -f RecordAC
    ```

