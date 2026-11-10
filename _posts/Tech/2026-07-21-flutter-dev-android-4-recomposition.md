---
title: "Flutter 개발자가 본 Android (4) 리컴포지션과 rebuild"
description: "Compose의 세 단계, stable과 Strong Skipping, 상태를 늦게 읽기, derivedStateOf와 snapshotFlow, Lazy key, Effect를 Flutter의 rebuild와 비교"
date: 2026-07-21 21:20:00 +0900
categories: [android, compose]
tags: [Jetpack Compose, 리컴포지션, Flutter, 성능, 상태 관리]
series: "Flutter 개발자가 본 Android"
series_order: 4
---

Compose를 처음 보면 Flutter와 너무 닮아서 오히려 방심합니다.
`@Composable` 함수는 `build()`, `mutableStateOf`는 `setState`, `remember`는 `State` 객체의 필드.
상태가 바뀌면 함수가 다시 실행된다는 그림도 같습니다.

차이는 **무엇을 건너뛰느냐**에서 납니다.
Flutter는 `setState`를 부른 위젯부터 아래로 `build()`를 다시 돌리고 같은 인스턴스의 위젯을 만나면 멈춥니다.
Compose는 State를 **읽은 범위만** 다시 실행하고 파라미터가 이전과 같은 자식은 건너뜁니다.
그리고 "같다"의 기준이 타입마다 다릅니다.

> 4편은 한 프레임을 만드는 세 단계에서 출발해, 다시 실행할 함수를 줄이는 방법(stable과 Strong Skipping)과 State를 늦은 단계에서 읽는 방법을 따라갑니다.
> 그 위에서 `derivedStateOf`와 `snapshotFlow`, Lazy 목록의 key, Effect를 함께 정리합니다.

## 한 프레임은 세 단계로 만들어진다

| 단계 | 하는 일 | Flutter로 치면 |
|---|---|---|
| Composition | Composable 함수를 실행해 UI 트리를 만듦 | build |
| Layout | 크기를 재고 자리를 정함 | layout |
| Drawing | 화면에 그림 | paint |

리컴포지션은 첫 단계를 다시 하는 것입니다.
"다시 그린다"와 같은 말이 아닙니다.

Compose는 **어느 단계에서 어떤 State를 읽었는지** 기록합니다.
그 State가 바뀌면 그 단계부터만 다시 합니다.

- Composition에서 읽었으면 세 단계를 다 다시 합니다.
- Layout에서 읽었으면 Layout과 Drawing만 다시 합니다.
- Drawing에서 읽었으면 Drawing만 다시 합니다.

그래서 최적화의 방향은 두 가지입니다.
다시 실행할 함수를 줄이는 것과 State를 늦은 단계에서 읽는 것입니다.

## 건너뛰기와 stable

부모가 다시 실행돼도, 자식의 파라미터가 이전과 같으면 자식은 다시 실행하지 않습니다.
이것이 리컴포지션을 줄이는 가장 큰 장치입니다.

"이전과 같다"고 믿으려면 그 값이 몰래 바뀌지 않아야 합니다.
Compose가 그렇게 믿을 수 있는 타입을 **stable**이라고 합니다.

| stable | unstable |
|---|---|
| `Int`, `String`, `Boolean` 같은 기본 타입 | `var` 프로퍼티가 하나라도 있는 클래스 |
| 모든 프로퍼티가 `val`이고 그 타입도 stable인 data class | `List`, `Map`, `Set` |
| `State<T>`, `@Immutable`·`@Stable`을 붙인 클래스 | Compose 컴파일러가 돌지 않은 다른 모듈의 클래스 |

`List`가 unstable인 이유는 인터페이스이기 때문입니다.
실제로는 `ArrayList`처럼 바뀔 수 있는 리스트일 수도 있는데, Compose는 확인할 방법이 없습니다.

### Strong Skipping

Kotlin 2.0.20부터 Strong Skipping이 기본으로 켜져 있습니다.

| 파라미터 | 비교 방법 |
|---|---|
| stable | `equals`. 내용이 같으면 건너뜀 |
| unstable | 같은 인스턴스(`===`)인지. 같은 객체면 건너뜀 |

예전에는 unstable 파라미터가 하나만 있어도 절대 건너뛰지 않았습니다.
지금은 같은 인스턴스면 건너뜁니다.
람다도 자동으로 `remember`되어, 캡처한 값이 같으면 같은 인스턴스가 유지됩니다.

Flutter 개발자에게 unstable 쪽 규칙은 익숙합니다.
`const` 위젯이나 미리 만들어 둔 `child`를 넘기면, 같은 인스턴스라 Flutter가 그 아래 `build()`를 건너뛰는 것과 같습니다.
Compose는 여기에 stable 타입의 **내용 비교**를 더했습니다.

문제가 하나 남습니다.
상태를 `copy`할 때마다 목록을 새로 만들면, 내용이 같아도 다른 인스턴스라 다시 실행됩니다.
`ImmutableList`는 stable 타입이라 인스턴스가 아니라 `equals`로 비교합니다.
목록을 새로 만들어도 내용이 같으면 건너뜁니다.

### 목록은 ImmutableList로, UI 모델은 @Immutable로

```kotlin
data class ArticleListUiState(
    val articles: ImmutableList<ArticleUiModel> = persistentListOf(),
)

@Immutable
data class ArticleUiModel(
    val id: Long,
    val title: String,
    val publishedAt: Instant,   // 다른 모듈 타입이 섞여도 @Immutable로 약속
)
```

- 목록은 `kotlinx.collections.immutable`의 `ImmutableList`를 씁니다. 만들 때 `toPersistentList()`를 씁니다.
- domain 모델을 그대로 넘기지 않고 화면용 UI 모델로 바꿉니다. 모두 `val`로 두고 `@Immutable`을 붙입니다.

`@Immutable`과 `@Stable`은 컴파일러에게 하는 약속이고 검사는 하지 않습니다.
실제로 바뀌는 클래스에 `@Immutable`을 붙이면, 값이 바뀌어도 건너뛰어 화면이 갱신되지 않습니다.

## 상태를 늦게, 아래에서 읽기

스크롤이나 드래그처럼 매 프레임 바뀌는 값을 Composition에서 읽으면, 매 프레임 함수가 다시 실행됩니다.
같은 값을 Layout이나 Drawing에서 읽으면 Composition은 건너뜁니다.

| 값을 넘기는 방식 (Composition에서 읽음) | 람다 방식 (늦은 단계에서 읽음) |
|---|---|
| `Modifier.offset(x = 10.dp)` | `Modifier.offset { IntOffset(x, 0) }` Layout 단계 |
| `Modifier.background(color)` | `Modifier.drawBehind { drawRect(color) }` Drawing 단계 |
| `Modifier.alpha(a)` | `Modifier.graphicsLayer { alpha = a }` Drawing 단계 |

```kotlin
val offsetY = remember { Animatable(0f) }

Box(
    Modifier
        .offset { IntOffset(0, offsetY.value.roundToInt()) }   // 람다 안에서 읽음 → Layout
        .graphicsLayer { alpha = 1f - offsetY.value / 1000f }  // 람다 안에서 읽음 → Drawing
)
```

끌어서 닫는 이미지 뷰어를 이렇게 만들면, 끄는 동안 Composition이 한 번도 다시 돌지 않습니다.

Flutter에서 `AnimatedBuilder`의 `child`를 따로 빼거나, `CustomPainter`에 `Listenable`을 넘겨 paint만 다시 하던 것과 같은 생각입니다.
Compose는 그 선택을 Modifier의 **값 버전과 람다 버전**으로 드러냅니다.

"아래에서 읽기"도 같은 원리입니다.
State를 부모에서 읽고 값을 자식에게 넘기면 부모까지 다시 실행됩니다.
필요한 자식 안에서 읽거나, 값 대신 `() -> T` 람다를 넘기면 범위가 좁아집니다.

```kotlin
// 부모에서 scrollState.value를 읽으면 스크롤할 때마다 부모가 다시 실행됨
Header(scrollProvider = { scrollState.value })

@Composable
fun Header(scrollProvider: () -> Int) {
    Box(Modifier.offset { IntOffset(0, -scrollProvider()) })  // 실제로 읽는 곳은 Layout 단계
}
```

부모는 람다만 넘기고 값을 읽지 않으므로, 스크롤해도 부모와 `Header` 함수 모두 다시 실행되지 않습니다.

## remember, derivedStateOf, snapshotFlow

다시 실행할 함수를 줄이는 방법이 하나 더 있습니다.
자주 바뀌는 State를 그대로 읽지 않고 화면에 필요한 결과만 읽는 것입니다.

| 상황 | 쓰는 것 |
|---|---|
| 입력이 바뀔 때마다 다시 계산하면 되는 값 | `remember(key) { }` |
| 입력은 자주 바뀌는데 결과는 드물게 바뀌는 State | `derivedStateOf` |
| State 변화를 보고 일을 해야 할 때(요청, 로그) | `snapshotFlow` + `LaunchedEffect` |

```kotlin
val listState = rememberLazyListState()
val showTopButton by remember {
    derivedStateOf { listState.firstVisibleItemIndex > 0 }
}
```

`firstVisibleItemIndex`는 스크롤할 때마다 바뀌지만 버튼에 필요한 것은 "0보다 크냐" 하나입니다.
`derivedStateOf`는 결과가 바뀔 때만 알리므로, 버튼은 맨 위를 벗어나는 순간과 돌아오는 순간에만 다시 실행됩니다.

두 값을 단순히 합칠 때는 `derivedStateOf`가 이득이 없습니다.
입력이 바뀔 때마다 결과도 바뀌므로, 그때는 `remember(a, b)`를 씁니다.

무한 스크롤의 "목록 끝 감지"는 결과로 해야 할 일이 "다음 페이지 요청"이라 `snapshotFlow`를 씁니다.

```kotlin
val currentOnLoadMore by rememberUpdatedState(onLoadMore)

LaunchedEffect(listState) {
    snapshotFlow {
        val info = listState.layoutInfo
        (info.visibleItemsInfo.lastOrNull()?.index ?: 0) to info.totalItemsCount
    }
        .distinctUntilChanged()
        .collect { (lastVisible, total) ->
            if (total > 0 && lastVisible >= total - 5) currentOnLoadMore()
        }
}
```

스크롤 상태를 Composition에서 읽지 않으므로, 스크롤해도 목록 화면 함수가 다시 실행되지 않습니다.
`rememberUpdatedState`는 Effect를 다시 시작하지 않고 `onLoadMore`의 최신 값을 쓰게 해 줍니다. 아래 Effect 구간에서 다시 다룹니다.

## Lazy 목록의 key

```kotlin
items(state.articles, key = { it.id }) { article ->
    ArticleRow(article, onClick = { onArticleClick(article.id) })
}
```

key가 없으면 Compose는 위치(index)로 항목을 구분합니다.
맨 앞에 하나가 끼면 모든 항목의 위치가 밀리고 항목 안의 `remember` 상태도 위치를 따라 엉뚱한 항목에 붙습니다.

Flutter의 `ListView`에 `ValueKey`를 주는 이유와 정확히 같습니다.
다른 점이 두 가지 있습니다.

- **같은 key가 두 번 나오면 앱이 종료됩니다.** 다음 페이지를 붙일 때 `distinctBy { it.id }`로 중복을 거릅니다.
- **key는 Bundle에 저장될 수 있어야 합니다.** 화면 회전 같은 구성 변경 뒤에 스크롤 위치와 항목 상태를 key로 되찾기 때문입니다. `Int`, `Long`, `String` 같은 값을 씁니다.

항목 모양이 여러 종류라면 `contentType`도 줍니다. 같은 종류끼리만 화면 밖 항목을 재사용합니다.

## Effect: 한 번만 해야 하는 일

Composable 함수는 언제든, 몇 번이든 다시 실행될 수 있습니다.
`build()` 안에서 네트워크를 부르지 않는 것과 같은 이유로, 화면 밖에 영향을 주는 일은 Effect 안에서 합니다.

| API | 언제 | Flutter로 치면 |
|---|---|---|
| `LaunchedEffect(key)` | 화면에 있는 동안 코루틴. key가 바뀌면 취소 후 다시 | `initState` + `didUpdateWidget` |
| `rememberCoroutineScope()` | 클릭이나 드래그에서 코루틴 시작 | 이벤트 핸들러의 `async` |
| `DisposableEffect(key)` | 등록하고 해제하는 짝. `onDispose` 필수 | `initState` + `dispose` |
| `rememberUpdatedState(x)` | Effect를 다시 시작하지 않고 최신 값 쓰기 | `widget.onX`를 매번 읽기 |

`LaunchedEffect`의 key는 "언제 다시 시작할지"입니다.
`Unit`이면 화면에 있는 동안 한 번만 돌고 자주 바뀌는 값을 넣으면 계속 취소되고 다시 시작합니다.

## 확인하는 순서

1. **Layout Inspector**로 리컴포지션 횟수와 건너뛴 횟수를 봅니다. 스크롤하면서 숫자가 계속 오르는 곳을 찾습니다.
2. **Compose 컴파일러 리포트**로 그 파라미터가 stable인지, 함수가 skippable인지 확인합니다.
3. State를 어느 단계에서 읽는지 확인합니다.
4. 고친 뒤 다시 횟수를 봅니다. 프레임 자체가 늦다면 Perfetto와 Macrobenchmark로 넘어갑니다.

## 정리

- 리컴포지션은 읽은 State의 범위만 다시 실행한다. 다시 그리는 것과 다르다.
- stable 파라미터는 `equals`로, unstable 파라미터는 인스턴스로 비교한다(Strong Skipping).
- 목록은 `ImmutableList`, UI 모델은 `val`만 가진 `@Immutable` data class로 둔다.
- 매 프레임 바뀌는 값은 Modifier의 람다 버전으로 Layout·Drawing 단계에서 읽는다.
- 결과가 드물게 바뀌면 `derivedStateOf`, 변화에 일을 해야 하면 `snapshotFlow`.
- Lazy 목록에는 key를 준다. 중복 key는 앱을 종료시킨다.

Flutter에서 "rebuild를 줄이려면 `const`를 붙이고 위젯을 쪼개라"고 배웠다면, Compose에서도 같은 생각이 통합니다.
다만 Compose는 그 판단의 근거를 **타입의 안정성**과 **읽는 단계**로 더 세밀하게 나눕니다.

다음 편에서는 화면이 ViewModel을 받아 오는 방법, Hilt를 Flutter의 Context 기반 DI와 비교합니다.
