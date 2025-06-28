1. Install Azure Functions, Python as VSCODE Extensions
1. Press F5 to run locally.
1. Put in local.settings.json the following:

```
{
  "Values": {
    ...
    "SPOTIPY_CLIENT_ID": "ask-for-a-client-id",
    "SPOTIPY_CLIENT_SECRET": "ask-for-a-client-secret"
    ...
  },
  "Host": {
    "LocalHttpPort": 7071,
    "CORS": "http://localhost:4200"
  }
}
````