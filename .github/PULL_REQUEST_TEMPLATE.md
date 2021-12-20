## Overview

Brief description of what this PR does, and why it is needed.

Closes #XXX

### Demo

Optional. Screenshots, `curl` examples, etc.

### Notes

Optional. Ancillary topics, caveats, alternative strategies that didn't work out, anything else.

## Testing Instructions

If you are opening a PR for functionality that requires access to the remote GIS
datbase from your review app, don't forget to attach the QuotaGuard static add-on
to your review app after initializes, like so:

```bash
# From your local command line
heroku addons:attach -a ${REVIEW_APP} quotaguardstatic
```

* How to test this PR
* Prefer bulleted description
* Start after checking out this branch
* Include any setup required, such as bundling scripts, restarting services, etc.
* Include test case, and expected output
