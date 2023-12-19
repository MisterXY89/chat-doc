# Log extraction

How to extract logs from AWS CloudWatch in the correct format.

1. Go to [CloudWatch](https://eu-central-1.console.aws.amazon.com/cloudwatch/home)
2. Click on `Logs Insights` in the left menu
3. Select the correct log group and time range
4. Run the following query:
    ```sql
    fields @timestamp, @message
        | filter @message like /\Q{'loss': \E.*\Q, 'learning_rate': \E.*\Q, 'epoch': \E.*\Q}\E/
    ```
5. Click on `Export results` and select `CSV`
6. Save the file as `training-log-events-{MODEL-VARIANT}-DD-MM-YY.csv` in the `logs` folder.