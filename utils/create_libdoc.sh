#!/usr/bin/env bash
echo "### creating Keyword Documentation in folder docs ###"
libdoc ../libs/BITBUCKETKeywords.py ../docs/BITBUCKET_Keywords.html
libdoc ../libs/JIRAKeywords.py ../docs/JIRA_Keywords.html
libdoc ../libs/CONFLUENCEKeywords.py ../docs/CONFLUENCE_Keywords.html
libdoc ../libs/SERVICEDESKKeywords.py ../docs/SERVICE_DESK_Keywords.html
echo "### Documentation created ###"