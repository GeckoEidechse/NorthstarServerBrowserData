# NorthstarServerBrowserData
Data collected from polling `northstar.tf/client/servers` every 10 minutes

Note that the collected data is the raw response from the masterserver. Sanitising the response is not part of the data collection process. As such the `.json` files in the archives are not guaranteed to be actual JSON and can be HTTP/HTML error reponses instead, for example in cases when the masterserver was down.

## Folder structure

- `data/` contains folders per year which in turn contain an archive for each month of that year.
- `scripts/` contains folders for different programming languages which in turn contain helper scripts to extract archives and possibly run some form of analysis on the data. \
  If a language you use is missing, feel free to contribute it.


```
.
├── data/
│   └── <year>/
│           └── <year>-<month>.7z
└── scripts/
    └── <language>/
        └── <scripts>
```