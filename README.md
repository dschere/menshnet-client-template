# README #

This is a template for you to use to provide hardware acceleration for your 
computer vision algorithms.


### Directory Structure ###

* config
    A collection of *.yml files which you define to setup your pipelines. See
    the existing samples as a guide. The name attribute in the yml file is what
    is used to identifiy the pipline and makes it callable using the menshnet 
    client api.
    ```
# config:
config/myprocessor.yml:

name: 'my-processor'   

# using menshnet client in your application:
import menshnet

p = menshnet.launch(apikey, "my-processor", { ... config ... })

    ```
* sensors
    A collection of demo python files for creating computer vision pipelines
    that process video.
   
### How do I get set up? ###

* Login to menshnet.online and create an account
* You will then be assigned an apiKey that you can use
* Fork this git repo 
* Reguster it with menshnet
* Your off and running! Use the menshnet client to launch and interact 
  with you code.

### Contribution guidelines ###

* Any suggestions for improvements can be posted to lighinlogic@gmail.com

### Consulting Opportunities? ###

* Please visit menshnet.online under contact information. 

