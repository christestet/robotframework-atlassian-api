# robotframework-atlassian-api
A Robotframework wrapper for python atlassian api 

This Project bases on  [robotframework-jira](https://github.com/IlfirinPL/robotframework-jira) - thank you for the great idea Marcin!

## Getting started
- Install the requrements.txt with `pip install -r requirements.txt`
- Use the Librarys in your `*** Settings ***` Definition Block 

## Create Libdoc
- Use the [create_libdoc](./utils/create_libdoc.sh) bash script in the *utils* folder

## Known Issues
### Keyword definded Multiple Times Error, when generating libdoc for Bitbucket Keywords
- Go to Bitbucket Library Definition into __init__.py and delete the depricated function `get_pullrequest`
    ```
    @deprecated(version="1.15.1", reason="Use get_pull_request()")
    def get_pullrequest(self, *args, **kwargs):
        """
        Deprecated name since 1.15.1. Let's use the get_pull_request()
        """
        return self.get_pull_request(*args, **kwargs)
    ``` 