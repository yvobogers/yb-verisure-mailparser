# yb-verisure-mailparser
AWS Lambda for parsing Verisure email notifications. 

The Yale smart lock can be configured to send push notifications to the Verisure app and admin user's email addresses. This AWS lambda can be used to parse those emails, for instance after having stored the emails in S3 using an AWS SES email receiving pipeline. AWS Lambda can now trigger additional logic such as SNS or SQS notifications or, as I've done here, parse the emails and send out a simple JSON message with event name ("Locked", "Unlocked", etc.) and username to an external API endpoint.

Use at your own risk, the code is not secure and should probably include more advanced source signature checking etc. to prevent email spoofing and getting false notifications.

For more information on how to setup an SES email receiving pipeline see: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-getting-started.html
