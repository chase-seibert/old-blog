---
layout: post
title: React Native Multiple Release Variants
tags:
---

By default, React Native gives you a `debug` variant and a `release` variant.
In debug mode, the app connects to a running packager service, and enables various
`__DEV__` checks that could slow down performance. In release mode, the JavaScript,
CSS and JSX are bundled into the app itself, and optimizations are enabled.

You may have a use case for multiple `release` variants. For example, you want
a staging and production build of you app, and you want to deploy them both
to physical devices for testing.

In that case, you would add the following to the `buildTypes` section of your
`android/app/build.gradle` file:

```bash
buildTypes {
    debug {
        applicationIdSuffix ".debug"
    }
    release {
        minifyEnabled enableProguardInReleaseBuilds
        proguardFiles getDefaultProguardFile("proguard-android.txt"), "proguard-rules.pro"
        signingConfig signingConfigs.release
    }
    releaseStaging {
        initWith(buildTypes.release)
        applicationIdSuffix ".staging"
    }
}
```

Note that the naming convention for `releaseStaging` is actually significant. We
originally tried just `staging`, and ended up getting the following error when
deployed to a physical device:

```bash
java.lang.RuntimeException com.facebook.react.devsupport.JSException
Could not get BatchedBridge, make sure your bundle is packaged correctly
```

It turned out to be that the build had not bundled assets. You can actually correct
that by using the `project.ext.react` directive in `android/app/build.gradle`, as
noted in the in-line comments of that file. However, though that gave us a working build,
performance was suddenly horrible. We eventually figured out that the build was in
`__DEV__` mode.

Looking at the React Native source, we found this reference in
[eeact.gradle](https://github.com/facebook/react-native/blob/e083f9a139b3f8c5552528f8f8018529ef3193b9/react.gradle#L79):

```javascript
def devEnabled = !targetName.toLowerCase().contains("release")
if (Os.isFamily(Os.FAMILY_WINDOWS)) {
    commandLine("cmd", "/c", *nodeExecutableAndArgs, "node_modules/react-native/local-cli/cli.js", "bundle", "--platform", "android", "--dev", "${devEnabled}",
            "--reset-cache", "--entry-file", entryFile, "--bundle-output", jsBundleFile, "--assets-dest", resourcesDir, *extraPackagerArgs)
} else {
    commandLine(*nodeExecutableAndArgs, "node_modules/react-native/local-cli/cli.js", "bundle", "--platform", "android", "--dev", "${devEnabled}",
            "--reset-cache", "--entry-file", entryFile, "--bundle-output", jsBundleFile, "--assets-dest", resourcesDir, *extraPackagerArgs)
}
```

In other words, you must have the token "release" in the build variant name for regular
release build behavior to apply.
