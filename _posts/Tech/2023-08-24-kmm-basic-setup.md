---
title: "KMM 기본 세팅"
description: "Android Studio에서 KMM 샘플 프로젝트를 만들고 Android, iOS로 실행한 뒤 GitHub에 올리기까지"
date: 2023-08-24 21:35:07 +0900
categories: [kotlin, kmm]
tags: [KMM, Kotlin Multiplatform Mobile, Android Studio]
series: "KMM(Kotlin Multiplatform Mobile)"
series_order: 2
toc: true
---

> 2023년 velog에 올렸던 글을 옮겨 왔습니다.

이번에는 Kotlin Multiplatform Mobile(이하 KMM)로 샘플 프로젝트를 만들어 보겠습니다.

## Create Github repository

먼저 우린 모두 Github을 쓰고 있을 테니 git repository부터 만들어 보겠습니다.
이름은 kmm_sample로 만들었어요!

![GitHub에 kmm_sample 저장소 만들기](/assets/img/posts/kmm/setup-01.png)

Android Studio를 실행하고 툴바 메뉴에서
Android Studio > Settings > Plugins로 가서 'Kotlin Multiplatform'을 검색해 주세요!
이 플러그인이 설치되어 있어야 새 프로젝트를 만들 수 있어요.

![Kotlin Multiplatform 플러그인 설치](/assets/img/posts/kmm/setup-02.png)

## Create KMM Project

이제 Android Studio를 켜고 우측 상단의
New Project로 새 프로젝트를 만들어 봅시다!

![New Project](/assets/img/posts/kmm/setup-03.png)

오, 제일 아래에 Kotlin Multiplatform App이 있군요!

![Kotlin Multiplatform App 템플릿](/assets/img/posts/kmm/setup-04.png)

이제 프로젝트 이름을 정해서 앱을 만듭니다.

![프로젝트 이름 입력](/assets/img/posts/kmm/setup-05.png)

흐음.. 이건 뭘까요..
Android project 이름,
iOS project 이름,
그리고 KMM Module 이름인 것 같군요.

우린 샘플 앱을 만들 테니 기본 세팅대로 두고 Finish!

![모듈 이름 설정](/assets/img/posts/kmm/setup-06.png)

새 프로젝트를 만드는 데 3분이 넘게 걸렸어요..
아마 android, ios project를 같이 만들어서 그런 것 같네요..

어쨌든 잘 만들어졌습니다.
좌측 상단 보기가 Project인지 Android인지 꼭 확인하세요!

![프로젝트 구조](/assets/img/posts/kmm/setup-07.png)

오, Android 프로젝트는 기본적으로 Compose로 작성되어 있군요.

![Android 쪽 Compose 코드](/assets/img/posts/kmm/setup-08.png)

그럼 iOS 쪽도 SwiftUI로 되어 있으려나..?
정답! iOS는 SwiftUI로 작성되어 있습니다.

이걸 보면 KMM은 선언형 UI를 권장하는 것 같네요.
물론 android, ios 둘 다 명령형 UI로도 구현할 수 있을 듯합니다.

KMM의 역할은 UI 지원이 아니라 비즈니스 로직, 도메인 데이터 지원이니까요.

![iOS 쪽 SwiftUI 코드](/assets/img/posts/kmm/setup-09.png)

## Run KMM 프로젝트!

자, 이제 OS별로 한번 실행해 보죠!
먼저 Android로 실행합니다!
불편하네요. 가운데 정렬은 좀 해 주지..

![Android 실행 화면](/assets/img/posts/kmm/setup-10.png)

이번에는 iOS입니다.
KMM을 잘 쓰려면 Android Studio에서 iOS도 run할 수 있어야 할 것 같아요.
네, 있습니다! 과연 이게 될 것인가..? 한번 해 보죠.

![Android Studio에서 iOS 실행 설정](/assets/img/posts/kmm/setup-11.png)

오, 잘 실행됩니다.
근데... 역시 Android Studio에서는 iOS UI를 개발하지 못할 듯하네요..
당연한 건가..? 폐쇄적인 애플...

![iOS 실행 화면](/assets/img/posts/kmm/setup-12.png)

## Greeting Class?

Greeting().greet()를 호출하니
Android는 "Hello, Android 33!"이라고 뜨고
iOS는 "Hello, iOS 16.4!"라고 뜨네요??
아! Greeting은 공통 모듈이군요!
그럼 shared 모듈에 Greeting이 있어야 합니다!

![shared 모듈의 Greeting](/assets/img/posts/kmm/setup-13.png)

## Greeting 파헤치기

좋은 실마리를 찾았네요.
이제 Greeting 클래스의 패턴을 익히면 custom class를 마구 만들어 낼 수 있겠습니다!
살펴보니 OS별로 다른 값을 주려면 인터페이스를 작성해야 하는군요.

![shared 모듈의 폴더 구조](/assets/img/posts/kmm/setup-14.png)

### Greeting interface

OS별로 처리하려면 매우 번거롭네요.
불가피한 경우가 아니라면 데이터는 OS 영향을 타지 않도록 작업해야겠습니다.

![Greeting과 OS별 Platform 구현의 관계](/assets/img/posts/kmm/setup-15.png)

## Connect Github Repository by Android Studio

앗, 그러고 보니 샘플 코드를 github에 연동하는 걸 잊었네요.
깃을 연결하려고 보니 오잉?
KMM이 미리 .gitignore 파일을 만들어 줬네요?
작성법을 찾아볼까 했는데 이러면 바로 붙여도 되겠습니다!

![자동으로 만들어진 .gitignore](/assets/img/posts/kmm/setup-16.png)

맥에서는 많은 분들이 GitKraken, Fork, 소스트리 같은 툴이나
terminal을 쓰는 것 같은데, 저는 Android Studio의 git을 씁니다.

알탭할 필요가 없어서 편리해요. GOOD.

![Android Studio에서 커밋](/assets/img/posts/kmm/setup-17.png)

자, 커밋했으니 이제 Push를 해야겠죠?
시작할 때 kmm_sample repository를 만들어 뒀으니 Push만 하면 되는데,
이런... Push하기 전 스크린샷을 못 찍었네요 ;;;
아래 첫 번째 스크린샷에서 Push All up to Here를 클릭하시면 돼요.

![Push All up to Here](/assets/img/posts/kmm/setup-18.png)

이 화면에서 Define remote를 클릭해서 아까 만들어 둔 repository 주소를 적어 주시면 됩니다!

![Define remote](/assets/img/posts/kmm/setup-19.png)

이제 커밋한 내용이 나오고, Push를 하면?!

![Push](/assets/img/posts/kmm/setup-20.png)

## Github Connection Success 😎

역시 잘 올라가는군요.

![GitHub에 올라간 결과](/assets/img/posts/kmm/setup-21.png)

## End

오늘은 여기까지 하고, 다음에는 데이터를 가져와서 Android, iOS의 List에 뿌려 볼게요.
KMM에 최대한 집중하려고 Compose, SwiftUI에 대한 내용은 따로 정리하지 않을 거예요!
참고해 주세요!
