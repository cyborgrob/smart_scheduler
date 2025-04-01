Here you can find the code for the AWS Lambda functions I use in my intelligent AI appointment setter.

You will have to adjust these based on your setup, but basically you pass an "event" to your lambda function as an argument from Make.com - this argument is in the form of a JSON object.

You can then use code to extract the data you need from the JSON.

There are two sets of files above - one for the Specific branch, and one for the Vague. I've included both the code as well as an image from Make.com to show what is being passed to the function.
