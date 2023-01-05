# Linkedin profile parser (Selenium)


Mini linkedin profile parser on selenium.

### Instruction to start
>1. Add file .env with keys **ACCOUNT_LOGIN** **ACCOUNT_PASSWORD**
>2. Run main.py 
>3. Enter full path do file with urls (Example D:/Files/urls.txt) <br>

For step 2 you can add time (TimeToParseEveryProfile) Default is 5sec<br>

If you will get temporary ban try increasing the time | You can get temporary ban if you have many urls (many requests or long session) <br>

python main.py 10 - 1 page will parse in 10 sec

### Parsed data:
- Username
- Date of Registration
- Followers
- Description
- Location
- ProfileImageURL


### File with urls ↓
**Urls in file should look like that**
> url1 <br>
> url2 <br>
> url3


### Result file ↓
File title: **result.csv** <br>
File will be **saved in path where you clone repository**<br>
And in *****.csv*** extension** with *****utf-8*** encoding**

If html element not found instead of information will be None <br>

Example: <br>
| Username | Join In | Followers | Description | Location | ProfileImageURL <br>
| TestUsername | Joined in info | **None** | User Description | User location | ProfileImgURL
