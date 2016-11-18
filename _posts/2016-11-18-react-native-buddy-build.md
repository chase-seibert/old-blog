---
layout: post
title: Deploying React Native apps with Buddy Build
tags: app react-native
---

[Buddy Build](https://buddybuild.com/) is a great tool for getting your app out
to physical devices, whether that is during development, or in production. Their
tool is fairly agnostic to frameworks. For example, their documentation is nearly
devoid of mentions of React Native, but it's actually quite simple to get a
React Native app building.

In fact, nearly all the challenges we faced involved specific requirements, for
example having multiple builds with different configurations. In the end, most
of our learnings were about React Native itself. But maybe this guide will be
useful to other people who are trying to not only figure out how Buddy Build
works, but how React Native builds work.


# Private NPM Repositories

If you have a private NPM repository, you can upload the `.npmrc` file
using the "Secure Files" feature in Buddy Build. We ended up doing the same
for gradle.properties. For the later, you need a [custom post-clone script](http://docs.buddybuild.com/docs/custom-prebuild-and-postbuild-steps)
to copy the file into the correct location.

```bash
#!/usr/bin/env bash

cp ${BUDDYBUILD_SECURE_FILES}/.npmrc ${BUDDYBUILD_WORKSPACE}
mkdir -p ~/.gradle
cp ${BUDDYBUILD_SECURE_FILES}/gradle.properties ~/.gradle
```

# Multiple configurations

Maybe you have a use case where you want to have multiple builds that you actually
distribute to phones for testing. In our case, we wanted a staging build and a
production build. Both needed to be fully self-contained, with the Javascript
packaged into the app. But the URLs for the APIs they were hitting, as well as
some of the API keys, needed to be different.

We ended up using [react-native-config](https://github.com/luggit/react-native-config)
to create `.env.staging` and `.env.production` config files. In order to be able
to re-use some exiting Node code, we also mapped these into the
`process.env` space.

```javascript
import Config from 'react-native-config';

const env = Config;

// this is for backwards compatibility with existing Node pattern
export default function injectEnv() {
  Object.assign(process.env, env);
}
```

# Debug Builds

For iOS, React Native has two "variants", `debug` and `release`. For Android,
React Native will have gradle builds with the same names. In both cases, the
primary difference is whether the Javascript code is packaged and bundled with
the build, or loaded from a live packager running outside the app. Initially, we
tried to separate configuration by debug/release, and were confused when debug
builds deployed via Buddy Build crashed immediately. It turns out they were
trying and failing to connect to a packager.

The solution is to have *multiple release builds*.

# Multiple iOS Builds

On iOS, making a second release build is just duplicating your Release scheme in XCode.
**Note: the new schemes must be marked as "shared" in XCode.** You also want to
make sure that in the scheme definition, all the targets for Build/Run/Archive etc
are set to "Release", not "Debug". This is what React Native uses to determine
whether to package the Javascript code, or not.

You can follow the [react-native-config iOS setup](https://github.com/luggit/react-native-config#ios-1)
to get it to pick up a different `.env` file per scheme. We ended up using the
recommended `Build -> Pre-action` step, which worked fine. You could probably
also get our Android branch solution to work.

# Multiple Android Builds

On Android, creating a second release build was more problematic. It should be
possible to create additional gradle variants, but after a lot of experimentation,
we could not stop those builds from crashing on physical devices. At a low level,
we were never sure how React Native was choosing to bundle the package, or not.
We assumed it was based on the name of the build, but we're not sure.

What we ended up doing is changing our build script to push multiple release
branches up to GitHub, one for `staging` and one for `production`. We then
configured the Buddy Build project for Android to run a custom pre-build script to
copy in the correct `.env` file based on git branch.

```bash
#!/usr/bin/env bash

echo "BUDDYBUILD_BRANCH: $BUDDYBUILD_BRANCH"
if [ "$BUDDYBUILD_BRANCH" = "production" ]
then
   echo "Using .env.production"
   cp ${BUDDYBUILD_WORKSPACE}/.env.production ${BUDDYBUILD_WORKSPACE}/.env
else
   echo "Using .env.staging"
   cp ${BUDDYBUILD_WORKSPACE}/.env.staging ${BUDDYBUILD_WORKSPACE}/.env
fi

cat ${BUDDYBUILD_WORKSPACE}/.env
```

# Buddy Build SDKs

The SDKs, which enables user feedback in the app, was fantastically useful.
Highly recommended!
