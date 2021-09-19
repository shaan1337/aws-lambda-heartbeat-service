# Simple, free-tier heartbeat service for server uptime monitoring with AWS Lambda, DynamoDB, API Gateway, Cloudwatch and a Telegram bot

## What's this all about?
This script is useful when:
- you don't want to monitor any metrics on your server but just want to be notified when there's a power cut or internet interruption
- you don't have a public IP on the internet and cannot, for example, use uptimerobot.com. This is common on mobile networks
- you don't want to spend any $$$
- you want something lightweight and do not want to install any custom agent or bloat-ware on your server

## How does it work?
The principle is simple: your server sends HTTP requests to a fixed URL at regular intervals. AWS Cloudwatch triggers a check at 1 minute intervals and if the last heartbeat didn't happen within a configured time window, a notification is sent to the configured Telegram chat.

## Pre-requisites for setup
```
aws-cli
python3-pip
```

## Setup steps
1. [Create a Telegram bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot) and note down the bot token
2. Create a Telegram group chat and [fetch the group chat ID](https://stackoverflow.com/a/32572159)
3. Rename `config.py.example` to `config.py` and adjust the values. In particular, make sure you set the `notification_recipient_id` to your Telegram group chat ID and `notification_authorization_info` to your Telegram bot token
4. Run `setup.sh` to download required dependencies into the `libs` folder:
```
$ ./scripts/setup.sh
```
5. Run `aws configure` and set your `AWS Access Key ID`, `AWS Secret Access Key` and your region.
6. Create an AWS Lambda function named `my-heartbeat-service`
7. Run: `deploy.sh` to deploy the Lambda function code:
```
$ ./scripts/deploy.sh my-heartbeat-service
```
8. Add an API Gateway trigger for the Lambda function.
<details>
<summary>Click to expand</summary>

 - Create a `REST API` called `my-heartbeat-service-API`
 - Note down the API URL and API Key
 - Click on `Actions` -> `Create Resource`, check `Configure as proxy resource`. The tree should look like this: `/my-heartbeat-service/{proxy+}/ANY`
 - Enable the API key for added security
 - Deploy the API: `Actions` -> `Deploy API`.
</details>

9. Create an AWS DynamoDB table named `heartbeats` with an `int` PRIMARY KEY named `id`

10. On AWS IAM, give your lambda function `my-heartbeat-service` read-write access to the DynamoDB table `heartbeats`. Below is a sample policy you can attach to your Lambda function role:
<details>
<summary>Click to expand</summary>

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ReadWriteTable",
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGetItem",
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/heartbeats"
        },
        {
            "Sid": "GetStreamRecords",
            "Effect": "Allow",
            "Action": "dynamodb:GetRecords",
            "Resource": "arn:aws:dynamodb:*:*:table/heartbeats/stream/* "
        },
        {
            "Sid": "WriteLogStreamsAndGroups",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Sid": "CreateLogGroup",
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "*"
        }
    ]
}
```
</details>

11. On the server to be monitored, create a script called `heartbeat.sh` (replace your API gateway URL/API key below):
```
while true; do
curl -v -X POST "https://<id>.execute-api.<region>.amazonaws.com/default/my-heartbeat-service/set" -H "X-API-Key: <API key>"
sleep 30
done
```
12. Test the script by running it and verifying if you're getting a `200` status code. You can also open the `heartbeats` table on AWS DynamoDB and verify if the heartbeats are being updated.
13. If everything is working fine, you can launch it in a screen/tmux session and also add it on startup:
```
screen -dmS heartbeat bash /path/to/heartbeat.sh
```
14. On AWS Cloudwatch, go to `Events` -> `Rules` -> `Create Rule`. Select `Schedule` and a fixed rate of `1 minute`. Select your Lambda function as `Target` and configure its input with the following `Constant(JSON Text)`:
```
{"httpMethod": "GET","pathParameters": {"proxy": "check"}}
```
15. That's it you're finally done!