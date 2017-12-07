# EagleEye

### Eagle Eye, a subsidiary of Eagle Eye LLC 

By Qi Liang, Christian Rodrigues, and Matthew Yuen 
 
 
**Goal Statement:** "To see the world through a different eye."

We want to make a product that is based on open-source software which people can easily duplicate and use at home. This product is built from off the shelf to keep costs low and to empower laziness at home. 
 
**Function and technical requirements:**

Eagle Eye is the perfect product for people who "work smarter, not harder."  As hardworking US citizens, people do not have enough time to do perform menial tasks such as checking doors or greeting visitors.  Eagle Eye provides both of these tasks for the user, automatically. 

Eagle Eye consists of two separate devices, a Raspberry Pi with a camera which looks through the peephole of the person's door and a Raspberry Pi with a speaker which greets the person at the door.  By separating the speaker from the camera, the user can position each device in its optimal place, removing the physical restrictions. If the scope of a second raspberry pi with a speaker is a stretch, then a minimum viable product would be sending an email to the user.   

A small camera looks through the peephole or is mounted near a door, and when a visitor comes to the door, it will use its facial recognition software to see who is there.  Eagle Eye will response: 

- If the person is known and welcomed to the user, Eagle Eye will greet him or her with a customizable, personalized response. 
- If the person is known and not welcome to the user, Eagle Eye will politely tell him or her to go way and not come back 
- If the person is unknown, Eagle Eye will respond with one of a set of typical responses and the user will receive an SMS message/email that a stranger came to the door 
 
**Specific pieces of AWS or any other cloud provider used**

Eagle Eye depends on AWS for publishing SMS messages and sending emails to the owner of the device. Using the AWS IoT, AWS Lambda, and AWS SMS. AWS IoT is used to connect the Raspberry Pi's to AWS. AWS Lambda handles the code. AWS SMS sends out the SMS messages and emails to the owner.   