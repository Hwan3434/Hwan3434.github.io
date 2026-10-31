---
title: "KMM Basic Setup"
description: "Creating a KMM sample project in Android Studio, running it on Android and iOS, and pushing it to GitHub"
date: 2023-08-24 21:35:07 +0900
categories: [kotlin, kmm]
tags: [KMM, Kotlin Multiplatform Mobile, Android Studio]
series: "KMM (Kotlin Multiplatform Mobile)"
series_order: 2
toc: true
---

This time, let's build a sample project with Kotlin Multiplatform Mobile (KMM).

## Create Github repository

We're all using GitHub anyway, so let's start with a git repository.
I named it kmm_sample!

![Creating the kmm_sample repository on GitHub](/assets/img/posts/kmm/setup-01.png)

Launch Android Studio, and from the toolbar menu go to
Android Studio > Settings > Plugins and search for 'Kotlin Multiplatform'!
You need this plugin installed to create the new project.

![Installing the Kotlin Multiplatform plugin](/assets/img/posts/kmm/setup-02.png)

## Create KMM Project

Now open Android Studio and create a new project
with New Project at the top right!

![New Project](/assets/img/posts/kmm/setup-03.png)

Oh, there's Kotlin Multiplatform App at the very bottom!

![Kotlin Multiplatform App template](/assets/img/posts/kmm/setup-04.png)

Give the project a name and create the app.

![Entering the project name](/assets/img/posts/kmm/setup-05.png)

Hmm.. what's this..
The Android project name,
the iOS project name,
and the KMM module name, it seems.

We're only making a sample app, so keep the defaults and hit Finish!

![Module names](/assets/img/posts/kmm/setup-06.png)

Creating the project took more than three minutes..
Probably because it creates both the Android and iOS projects..

Anyway, it was created fine.
Make sure the view at the top left is set to Project or Android!

![Project structure](/assets/img/posts/kmm/setup-07.png)

Oh, the Android project is written in Compose by default.

![Compose code on the Android side](/assets/img/posts/kmm/setup-08.png)

Then is the iOS side in SwiftUI too..?
Correct! iOS is written in SwiftUI.

So it looks like KMM recommends declarative UI.
Of course, you could probably build both Android and iOS with imperative UI as well.

After all, KMM's job isn't UI; it's business logic and domain data.

![SwiftUI code on the iOS side](/assets/img/posts/kmm/setup-09.png)

## Run the KMM Project!

Now let's run it on each OS!
Android first!
Kind of awkward. Couldn't they at least center it..

![Running on Android](/assets/img/posts/kmm/setup-10.png)

Now iOS.
To use KMM well, I think you should be able to run iOS from Android Studio too.
And yes, you can! Will it actually work..? Let's try.

![iOS run configuration in Android Studio](/assets/img/posts/kmm/setup-11.png)

Oh, it runs fine.
But... as expected, you can't really develop iOS UI in Android Studio..
I guess that's natural..? Closed-off Apple...

![Running on iOS](/assets/img/posts/kmm/setup-12.png)

## Greeting Class?

Calling Greeting().greet()
shows "Hello, Android 33!" on Android
and "Hello, iOS 16.4!" on iOS??
Ah! Greeting is a shared module!
Then Greeting must live in the shared module!

![Greeting in the shared module](/assets/img/posts/kmm/setup-13.png)

## Digging into Greeting

Found a good clue.
Once we learn the pattern of the Greeting class, we can crank out custom classes!
Looking closer, giving a different value per OS requires writing an interface.

![Folder structure of the shared module](/assets/img/posts/kmm/setup-14.png)

### Greeting interface

Handling things per OS is a real hassle.
Unless it's unavoidable, I should keep data free from OS dependencies.

![How Greeting relates to the per-OS Platform implementations](/assets/img/posts/kmm/setup-15.png)

## Connect Github Repository by Android Studio

Oops, I forgot to hook the sample code up to GitHub.
About to connect git and, huh?
KMM already created a .gitignore file?
I was going to look up how to write one, but this means I can use it right away!

![The generated .gitignore](/assets/img/posts/kmm/setup-16.png)

On the Mac, many people seem to use tools like GitKraken, Fork or Sourcetree,
or the terminal, but I use the git built into Android Studio.

No need to Alt-Tab. GOOD.

![Committing in Android Studio](/assets/img/posts/kmm/setup-17.png)

Committed, so now it's time to push, right?
We created the kmm_sample repository at the start, so we just need to push,
but... I forgot to take a screenshot before pushing ;;;
In the first screenshot below, click Push All up to Here.

![Push All up to Here](/assets/img/posts/kmm/setup-18.png)

On this screen, click Define remote and enter the address of the repository we created earlier!

![Define remote](/assets/img/posts/kmm/setup-19.png)

Now the commits show up, and if you push?!

![Push](/assets/img/posts/kmm/setup-20.png)

## Github Connection Success 😎

Uploaded just fine.

![The result on GitHub](/assets/img/posts/kmm/setup-21.png)

## End

That's it for today. Next time I'll fetch some data and show it in a list on Android and iOS.
To stay focused on KMM, I won't cover Compose or SwiftUI separately!
Just so you know!
