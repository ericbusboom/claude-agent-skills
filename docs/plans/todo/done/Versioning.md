# Versioning. 

Unless specified elsewhere in Project Instructions, the version number model is this:

```
<major>.<isodate>.<build>
```

The major number is only ever implemented by hand by the software engineer or
through explicit request to update. 

The ISOF date is always maintained to be the current date. Whenever we're
changing the number, we will change the date to be the current date.  The build
number resets to 1 when the date is changed, and then after that, every time we
do a sprint, we're going to update the build number. 

I think the build number should be incremented after the sprint is completed in
the master branch. Otherwise, you can get conflicts of two sprints being done
simultaneously. The build number is related to when that sprint is merged, not
when it's created. 

And after you merge, your Git workflow is going to involve tagging the commit to
the master branch with the version preceded by a 'v'. 