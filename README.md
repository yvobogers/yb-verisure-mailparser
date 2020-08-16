# yb-verisure-mailparser
AWS Lambda for parsing Verisure email notifications. 

![Yale Doorman](https://www.yale.se/presets/product-slideshow/Yale/YaleSE/produkter/entredorr/Yale%20Doorman%20V2N%20förpackning%20silver%20front%20kant.jpg)

The Yale Doorman smart lock can be configured to send push notifications to the Verisure app and admin user's email addresses. This AWS lambda can be used to parse those emails, for instance after having stored the emails in S3 using an AWS SES email receiving pipeline. AWS Lambda can now trigger additional logic such as SNS or SQS notifications or, as I've done here, parse the emails and send out a simple JSON message with event name ("Locked", "Unlocked", etc.) and username to an external API endpoint.

Use at your own risk, the code is not secure and should probably include more advanced source signature checking etc. to prevent email spoofing and getting false notifications.

This example assumes hardcoded strings (in Swedish) in the email notifications, otherwise it just uses the Subject: field. It also expects these Lambda Environment variables to be set:
. URL: external URL endpoint, should support POST requests (e.g. using AWS API Gateway or some NodeJS server) 
. DELETE_SRC_MAIL: whether or not emails should be deleted from S3 after processing
. SRC_BUCKET: S3 bucket where the Verisure emails are dumped (e.g. by AWS SES)

For more information on how to setup an SES email receiving pipeline see: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-getting-started.html
