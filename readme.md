# enkiWS


## Web Services for Games on Python Google App Engine

A permissively licensed Python web service for games developers. enkiWS is a library for setting up a website and ancillary services for games on [Google App Engine](https://github.com/juliettef/enkiWS#why-use-google-app-engine).

[Online demo](https://enkisoftware-webservices.appspot.com) *(may be out of sync with the source code)* 


## Status

This is a work in progress and not yet ready for production use.  
__[ NEW in v0.7 ] REST API app registration and user datastore viewer; reauthentication checks__


## Functionality

### Current

* User Accounts - email, display name
* [Login through OAuth & OpenID providers](https://github.com/juliettef/enkiWS#enabling-oauth-login-with-google-facebook-twitter) - Valve's Steam, Facebook, Google, Twitter
* Forums
* Localisation - English & French implemented
* Online store
    * Payment provider [FastSpring](http://www.fastspring.com/)  
    * Licence key generation and activation
    * Store emulator
* Friends
    * Search by display name and invite
    * Message alert for friend invite
* [REST API](https://github.com/juliettef/enkiWS#rest-api)
    * Authentication (account and game key)
    * Friends list
    * Data Store   

### Intended for release 1.0.0 
    
* Admin tools
* Installation and usage documentation
* REST API improvements:
    * datastore limits
    * online datastore explorer
    * authentication timeout control
    * datastore object modifcation time and lifetime controls

### Intended for  release 1.x.x

* User roles
* Issues reporting and tracking
* Static blogging tool integration
* Integration [presskit() for GAE](http://www.enkisoftware.com/devlogpost-20140123-1-Presskit_for_Google_App_Engine.html), 
[distribute()](https://dodistribute.com/), 
[Promoter](https://www.promoterapp.com/)


## Instructions

### Running the enkiWS website locally

You can run enkiWS on your machine using the Google App Engine Launcher:  

1. Download & extract [enkiWS](https://github.com/juliettef/enkiWS/archive/master.zip)  
1. Download & install [Google App Engine with python 2.7](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)  
1. Run GoogleAppEngineLauncher:  
    1. Choose File > Add Existing Application.  
    1. Set the Application Path to the directory enkiWS was extracted to (where the app.yaml file resides)  
    1. Select Add - enkiWS is added to the list of project.
1. In the GAE Launcher select enkiWS, press Run, then press Browse - the enkiWS site opens in your browser.  

### Debugging enkiWS locally using PyCharm CE

A *.idea* directory is included in the project. It is preconfigured to enable the use of the free Pycharm Community Edition as an IDE for debugging python GAE code, with one modification to make manually. 
Note: if you'd prefer to configure PyCharm CE yourself see the [detailed tutorial](http://www.enkisoftware.com/devlogpost-20141231-1-Python_Google_App_Engine_debugging_with_PyCharm_CE.html). Otherwise follow the simplified instructions below:

1. Ensure you have python 2.7 and Google app Engine installed. To check it works, try running the enkiWS website locally.  
1. Download and install [Pycharm CE](https://www.jetbrains.com/pycharm/download/)  
1. Start Pycharm and open the project - set the project location to the directory enkiWS was extracted to (the parent folder of the .idea directory).  
1. A *Load error: undefined path variables*, *GAE_PATH is undefined* warning is displayed. To fix it see the [PyCharm tutorial Method A step 3.c. onwards](http://www.enkisoftware.com/devlogpost-20141231-1-Python_Google_App_Engine_debugging_with_PyCharm_CE.html#pathvariable).
1. Note: if you get a message stating *No Python interpreter configured for the project*, go to File > Settings > Project:enkiWS > Project Interpreter and set the project interpreter to point to the location of *python.exe* on your computer (..\Python27\python.exe).
1. Restart PyCharm
1. You can now run / debug the project from PyCharm using one of the configurations provided (e.g. *GAE_config*).  

### Enabling OAuth login with Google, Facebook, Twitter

To set up Open Authentication, you need to configure secrets.py:  

1. Follow the instructions in [example_secrets.txt](https://github.com/juliettef/enkiWS/blob/master/example_secrets.txt)  
1. Go to the login page: you will see the login buttons for the providers you've set up. Clicking on those buttons creates and account &/or logs you into enkiWS using OAuth.  

Notes:  

 - Valve's Steam is always available since it doesn't require a client Id nor secret.  
 - When you navigate the enkiWS site you will no longer see the warning message stating that the setup is incomplete.  

### REST API

#### Overview

**_WARNING: The API is in flux until v1.0_**

The rest api provides a mechanism for developers to create games, apps and websites which interact with users data.

 - Protocol: HTTPS
 - Request method: POST  
 - Request and response format: JSON  
 - Request and result parameters format: String unless specified otherwise  

The REST API security mechanism is to use HTTPS for as the protocol combined with user authentication (detailed later). Currently we do not implement a client secret or other application verification mechanism since any global key available on a client machine can be stolen - thus the REST API is deliberatly limited in the scope of the changes it can make.

#### User Authentication via a Connect Code

EnkiWS encourages the use of OAUTH so users may not have a password, and having users type their password into an unknown application is potentially risky. So we've developed an approach which allows users to authenticate an app by getting a temporary short code which they use to login, and the app exchanges this for a long lasting authentication token. Users can remove authentication priviledges using their profile page.

1. User goes to their profile page and requests a 'Connect Code'
1. EnkiWS displays the code e.g. 'Q354D'
1. User types their full displayname and connect code into the app login screen
1. App uses the /api/v1/connect API to login
1. App receives an auth_token and user_id, which it can use for further API requests. This can be stored on disk and re-used if required
 
#### The datastore

The datastore provides a named JSON object store for users with private, friends, and public read access control. The Google App Engine backend limits the per-object size to around 1 megabyte, however we intend to add per user limits with product based increases (for example you could configure enkiWS to give all registered users a small amount of storage, but users with a given product several megabytes).

#### Example REST API uses

Once an app has authenticated the user, it can use the auth_token and user_id to perform further API queries, and use the datastore to store user data.

- Check if a user has purchased a game
    1. Use /api/v1/ownsproducts and request for your game
- Store and find out if friends are online
    1.  Get the list of friends with /api/v1/friends
    1. Use the datastore /api/v1/datastore/set to store a JSON structure containing the details you need for friend status (online, ingame, IP address and ports for chat or game connect etc.). Make sure to have "read_access" : "friends"
    1. Use /api/v1/datastore/getlist with "read_access" : "friends" to get a list of the status for each user_id
- Invite a friend to play a game
    1. We discover the friend status as above, ensuring that the datastore entry has an IP address and port for messages to be passed. The game can then connect via this address and send an invite
- Get a list of open servers
    1. Again using the datastore we store the details required (server name, IP address, port, game details) to connect to the game with "read_access" : "public"
    1. Clients can pull this list using /api/v1/datastore/getlist with "read_access" : "public", and ping the servers for online status

#### API Functionality table

<table valign="top">
    <tbody>
        <tr>
            <th><sup>URL</sup></th>
            <th><sup>Functionality</sup></th>
            <th><sup>Request Parameters</sup></th>
            <th><sup>Request example</sup></th>
            <th><sup>Response Parameters</sup></th>
            <th><sup>Response example (success)</sup></th>           
        </tr>
        <tr>
            <td><sup>/api/v1/<br>connect</sup></td>
            <td><sup>User connect</sup></td>
            <td><sup>displayname,<br>code,<br>app_id,<br>app_secret</sup></td>
            <td><sup>{"displayname":"Silvia#2702",<br>"code":"Q354D",<br>"app_id":"5141470990303232",<br>"app_secret":"0ZYWOl..Y9Xq"}</sup></td>
            <td><sup>user_id,<br>auth_token,<br>success, error</sup></td>
            <td><sup>{"user_id":"5066549580791808",<br>"auth_token":"kDfFg1..dw3S",<br>"success":true, "error":""}</sup></td>
        </tr>
        <tr>
            <td><sup>/api/v1/<br>logout</sup></td>
            <td><sup>User logout</sup></td>
            <td><sup>user_id,<br>auth_token,<br>app_secret</sup></td>
            <td><sup>{"user_id":"5066549580791808",<br>"auth_token":"kDfFg1..dw3S",<br>"app_secret":"0ZYWOl..Y9Xq"}</sup></td>
            <td><sup>success, error</sup></td>
            <td><sup>{"success":true, "error":""}</sup></td>
        </tr>
        <tr>
            <td><sup>/api/v1/<br>authvalidate</sup></td>
            <td><sup>Validate user</sup></td>
            <td><sup>user_id,<br>auth_token,<br>app_secret</sup></td>
            <td><sup>{"user_id":"5066549580791808",<br>"auth_token":"kDfFg1..dw3S",<br>"app_secret":"0ZYWOl..Y9Xq"}</sup></td>
            <td><sup>user_displayname,<br>success, error</sup></td>
            <td><sup>{"user_displayname":"Silvia#2702",<br>"success":true,"error":""}</sup></td>
        </tr>
        <tr>
            <td><sup>/api/v1/<br>ownsproducts</sup></td>
            <td><sup>List products activated by user</sup></td>
            <td><sup>user_id,<br>auth_token,<br>app_secret</sup></td>
            <td><sup>{"user_id":"5066549580791808",<br>"auth_token":"kDfFg1..dw3S",<br>"app_secret":"0ZYWOl..Y9Xq"}</sup></td>
            <td><sup>products_owned (list of strings),<br>success, error</sup></td>
            <td><sup>{"products_owned":["product_a","product_b"],<br>"success":true,"error":""}</sup></td>
        </tr>
        <tr>
            <td><sup>/api/v1/<br>ownsproducts</sup></td>
            <td><sup>List confirming products activated by user</sup></td>
            <td><sup>user_id,<br>auth_token,<br>app_secret,<br>products (list of strings)</sup></td>
            <td><sup>{"user_id":"5066549580791808",<br>"auth_token":"kDfFg1..dw3S",<br>"app_secret":"0ZYWOl..Y9Xq",<br>"products":["product_b","product_c"]}</sup></td>
            <td><sup>products_owned (list of strings),<br>success, error</sup></td>
            <td><sup>{"products_owned":["product_b"],<br>"success":true,"error":""}</sup></td>
        </tr>
        <tr>
            <td><sup>/api/v1/<br>friends</sup></td>
            <td><sup>List user's friends</sup></td>
            <td><sup>user_id,<br>auth_token,<br>app_secret</sup></td>
            <td><sup>{"user_id":"5066549580791808",<br>"auth_token":"kDfFg1..dw3S",<br>"app_secret":"0ZYWOl..Y9Xq"}</sup></td>
            <td><sup>friends user_id<br>and displayname<br>(list of dictionaries of strings),<br>success, error</sup></td>
            <td><sup>{"friends":[<br>{"user_id":"4677872220372992",<br>"displayname":"Toto#2929"},<br>{"user_id":"6454683010859008",<br>"displayname":"Ann#1234"}],<br>"success":true,"error":""}</sup></td>
        </tr>
        <tr>
            <td><sup>/api/v1/<br>datastore/<br>set</sup></td>
            <td><sup>Create / update user's data filtered by app id, data type and data id</sup></td>
            <td><sup>user_id,<br>auth_token,<br>app_secret,<br>data_type,<br>data_id,<br>data_payload (JSON,<br>inc. optional<br>calc_ip_addr),<br>time_expires (int)<br>read_access</sup></td>
            <td><sup>{"user_id":"5066549580791808",<br>"auth_token":"kDfFg1..dw3S",<br>"app_secret":"0ZYWOl..Y9Xq",<br>"data_type":"settings",<br>"data_id":"s42",<br>"data_payload":<br>"{"colour":"green","size":"0.5",<br>"calc_ip_addr":""}",<br>"time_expires":3600,<br>"read_access":"friends"}</sup></td>
            <td><sup>success, error</sup></td>
            <td><sup>{"success":true,"error":""}</sup></td>
        </tr>
        <tr>
            <td><sup>/api/v1/<br>datastore/<br>get</sup></td>
            <td><sup>Get user's data filtered by app id, data type and data id</sup></td>
            <td><sup>user_id,<br>auth_token,<br>app_secret,<br>data_type,<br>data_id</sup></td>
            <td><sup>{"user_id":"5066549580791808",<br>"auth_token":"kDfFg1..dw3S",<br>"app_secret":"0ZYWOl..Y9Xq",<br>"data_type":"settings",<br>"data_id":"s42"}</sup></td>
            <td><sup>data_payload (JSON),<br>time_expires (int),<br>read_access,<br>server_time (int),<br>success, error</sup></td>
            <td><sup>
            {"data_payload":[<br>
            {"colour":"green","size":"0.5","calc_ip_addr":"127.0.0.1"}],<br>
            "time_expires":1458074738000,<br>
            "read_access":"friends"<br>
            "server_time":1458071138,<br>
            "success":true,"error":""}
            </sup></td>
        </tr>
        <tr>
            <td><sup>/api/v1/<br>datastore/<br>getlist</sup></td>
            <td><sup>Get list of users' data filtered by app id, data type and read access. If read_access is<br>
             - "public": return all users public data.<br>
             - "friends": return user's friends' data that have read_access set to "friends".<br>
             - "private": return the user's private data.</sup></td>
            <td><sup>user_id,<br>auth_token,<br>app_secret,<br>data_type,<br>read_access ("public", "friends", "private")</sup></td>
            <td><sup>{"user_id":"5066549580791808",<br>"auth_token":"kDfFg1..dw3S",<br>"app_secret":"0ZYWOl..Y9Xq",<br>"data_type":"settings",<br>"read_access":"friends"}</sup></td>
            <td><sup>data_payloads<br>(list of dictionaries<br>(user_id, data_id,<br>data_payload (JSON),<br>time_expires (int))),<br>server_time (int),<br>success, error</sup></td>
            <td><sup>
            {"data_payloads":[<br>
            {"user_id":"4677872220372992","data_id":"s42",<br>
            "data_payload":{"colour":"blue","size":"0.8","calc_ip_addr":"127.0.0.4"},<br>
            "time_expires":1457777535},<br>
            {"user_id":"6454683010859008","data_id":"s15",<br>
            "data_payload":{"colour":"red","size":"0.4","calc_ip_addr":"127.0.0.3"},<br>
            "time_expires":1458223683}],<br>
            {"user_id":"6454683010859008","data_id":"s39",<br>
            "data_payload":{"colour":"white","size":"0.9","calc_ip_addr":"127.0.0.3"},<br>
            "time_expires":1458329792}],<br>
            "server_time":1458071139,<br>"success":true,"error":""}
            </sup></td>
        </tr>
        <tr>
            <td><sup>/api/v1/<br>datastore/<br>del</sup></td>
            <td><sup>Delete user's data filtered by app id, data type and data id</sup></td>
            <td><sup>user_id,<br>auth_token,<br>app_secret,<br>data_type,<br>data_id</sup></td>
            <td><sup>{"user_id":"5066549580791808",<br>"auth_token":"kDfFg1..dw3S",<br>"app_secret":"0ZYWOl..Y9Xq",<br>"data_type":"settings",<br>"data_id":"s42"}</sup></td>
            <td><sup>success, error</sup></td>
            <td><sup>{"success":true,"error":""}</sup></td>
        </tr>
    </tbody>
</table>

#### API Errors

<table valign="top">
    <tbody>
        <tr>
            <th><sup>Error messages</sup></th>
            <th><sup>Description</sup></th>
            <th><sup>Response example (failure)</sup></th>
        </tr>
        <tr>
            <td><sup>Invalid request</sup></td>
            <td><sup>Invalid or missing request parameters</sup></td>
            <td><sup>{"success":false,"error":"Invalid request"}</sup></td>
        </tr>
        <tr>
            <td><sup>Unauthorised app</sup></td>
            <td><sup>App not registered or invalid secret.<br> - Connect request: app_id/app_secret invalid.<br> - Other requests: app_secret invalid.</sup></td>
            <td><sup>{"success":false,"error":"Unauthorised app"}</sup></td>
        </tr>
        <tr>
            <td><sup>Unauthorised user</sup></td>
            <td><sup>User could not be authenticated.<br> - Connect request: user_displayname/code invalid.<br> - Other requests: user_id/auth_token invalid.</sup></td>
            <td><sup>{"success":false,"error":"Unauthorised user"}</sup></td>
        </tr>
        <tr>
            <td><sup>Not Found</sup></td>
            <td><sup>No data found or data expired</sup></td>
            <td><sup>{"success":false,"error":"Not found"}</sup></td>
        </tr>
    </tbody>
</table>


## FAQ

### Why use Google App Engine?

Small games developers like ourselves typically have very irregular backend requirements - website and service traffic are typically relatively low, but spike when there's a new release or if some content goes viral. Google App Engine (GAE) provides a low cost scalable solution for this scenario. For more information see our article on [Implementing a static website in Google App Engine](http://www.enkisoftware.com/devlogpost-20130823-1-Implementing_a_static_website_in_Google_App_Engine.html) or [Wolfire's article on GAE for indie developers](http://blog.wolfire.com/2009/03/google-app-engine-for-indie-developers/) as well as [Wolfire's article on hosting the Humble Indie Bundle](http://blog.wolfire.com/2010/06/Hosting-the-Humble-Indie-Bundle-on-App-Engine).

Note that if you don't want to use Google App Engine, you can use [the open source AppScale](http://www.appscale.com/) environment to run this code on other platforms.

### Why Python?

Python is sufficiently popular and easy to use that it made a convenient choice of language from those available on Google App Engine. We considered Google's Go language, but although it has many benefits we thought it would be less widely known in the game development community.

### EU Cookie law?
According to the [EU legislation on cookies](http://ec.europa.eu/ipg/basics/legal/cookies/index_en.htm#section_2), the cookies used in enkiWS are exempt from consent.


## Credits

Developed by [Juliette Foucaut](http://www.enkisoftware.com/about.html#juliette) - [@juliettef](https://github.com/juliettef)  
Architecture and OAuth implementation - [Doug Binks](http://www.enkisoftware.com/about.html#doug) - [@dougbinks](https://github.com/dougbinks)  
Testing - [Andy Binks](http://www.enkisoftware.com/about.html#andy)  
Testing - Sven Bentlage - [@sbe-dev](https://github.com/sbe-dev)  
Localisation - Charlotte Foucaut - [@charlf](https://github.com/charlf)


## Licence

zlib - see [licence.txt](https://github.com/juliettef/enkiWS/blob/master/licence.txt)
