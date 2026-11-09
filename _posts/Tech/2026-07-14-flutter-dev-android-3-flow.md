---
title: "Flutter 개발자가 본 Android (3) Flow는 Stream이 아니다"
description: "Cold와 Hot, stateIn과 shareIn, collectAsStateWithLifecycle, StateFlow의 성질, 일회성 이벤트, flow와 channelFlow"
date: 2026-07-14 21:20:00 +0900
categories: [android, 코루틴]
tags: [Kotlin, Flow, StateFlow, Dart, Stream]
series: "Flutter 개발자가 본 Android"
series_order: 3
---

`Flow`를 처음 보면 Dart의 `Stream`이 떠오릅니다.
`flow { emit(x) }`는 `async* { yield x }`, `collect`는 `listen`.
대응표로 놓으면 그렇습니다.

하지만 쓰는 감각은 다릅니다.
`collect`는 콜백 등록이 아니라 **그 줄에서 멈추는 suspend 함수**이고, 구독 해제는 `cancel()`이 아니라 **코루틴 취소**입니다.
그리고 Cold와 Hot을 구분하지 않으면 같은 DB 쿼리가 구독자 수만큼 돕니다.

> 3편은 Cold와 Hot의 차이에서 출발해, Cold Flow를 `StateFlow`로 바꾸고 화면에서 읽기까지의 흐름을 따라갑니다.
> 그 위에서 일회성 이벤트를 어떻게 보낼지, Flow를 만들고 엮는 도구(`channelFlow`, `combine`, `flatMapLatest`)를 함께 정리합니다.

## Dart와 대응표

| Kotlin | Dart |
|---|---|
| `suspend fun` | `Future` + `async`/`await` |
| `flow { emit(x) }` | `async*` + `yield x` |
| `channelFlow { launch { send(x) } }` | 여러 작업이 `StreamController.add(x)`. 닫기와 취소는 알아서 |
| `StateFlow` | rxdart `BehaviorSubject` |
| `SharedFlow` | `StreamController.broadcast()` |
| `collect { }` | `listen()`. 다만 suspend라 그 줄에서 멈추고, 해제는 코루틴 취소로 |

`collect`가 suspend라는 점이 생각보다 큽니다.

```kotlin
viewModelScope.launch {
    repository.observeArticles().collect { render(it) }
    println("여기는 Flow가 끝나야 실행됩니다")
}
```

Dart에서 `listen` 다음 줄은 바로 실행됩니다.
Kotlin에서 `collect` 다음 줄은 Flow가 끝날 때까지 실행되지 않습니다.
끝나지 않는 Flow(DB 감시 등)라면 영원히 실행되지 않습니다.
두 Flow를 동시에 구독하려면 `launch`를 두 번 합니다.

## Cold와 Hot

- **Cold**: 누군가 `collect` 해야 그때 시작합니다. 구독자마다 처음부터 따로 돕니다. `flow { }`, Room의 Flow 반환 DAO가 이렇습니다.
- **Hot**: 구독자가 없어도 값이 있고 구독자들이 같은 흐름을 나눠 받습니다. `StateFlow`, `SharedFlow`가 이렇습니다.

Cold는 주문하면 그때 만드는 음식이고 Hot은 이미 틀어 놓은 라디오입니다.

Dart의 단일 구독 `Stream`은 Cold에 가깝고, broadcast `Stream`은 Hot에 가깝습니다.
다만 Dart에서는 단일 구독 Stream을 두 번 `listen`하면 예외가 납니다.
Kotlin의 Cold Flow는 두 번 `collect`하면 **조용히 두 번 실행**됩니다.

```kotlin
val articles = articleDao.observeAll()   // Cold

launch { articles.collect { renderList(it) } }    // 쿼리 1
launch { articles.collect { updateBadge(it) } }   // 쿼리 2
```

같은 데이터를 여러 곳에서 써야 하면 Hot으로 바꿔 하나를 나눕니다.
Cold Flow를 Hot으로 바꾸는 함수가 `stateIn`과 `shareIn`입니다.

## Hot으로 바꾸기: stateIn과 shareIn

| | `stateIn` → `StateFlow` | `shareIn` → `SharedFlow` |
|---|---|---|
| 초기값 | 필요 | 필요 없음 |
| 지금 값 | `.value` | `replayCache` (replay를 줬을 때) |
| 새 구독자 | 지금 값 1개 | replay 개수만큼. 0이면 없음 |
| 같은 값 연속 | 무시 | 그대로 내보냄 |

언제 시작하고 멈출지는 `SharingStarted`로 정합니다.

| `SharingStarted` | 동작 |
|---|---|
| `Eagerly` | 바로 시작, Scope가 끝날 때까지 |
| `Lazily` | 첫 구독자 때 시작, 그 뒤로 계속 |
| `WhileSubscribed(5_000)` | 구독자가 있을 때만. 다 떠나고 5초 뒤 멈춤 |

```kotlin
val uiState: StateFlow<ArticleListUiState> = observeArticles()
    .map { it.toUiState() }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ArticleListUiState())
```

5초는 화면 회전처럼 잠깐 구독이 끊기는 순간에 업스트림을 다시 시작하지 않으려는 여유입니다.

여기서 구독자는 화면입니다.
화면이 언제 구독을 시작하고 끊는지는 화면 쪽에서 쓰는 함수가 정합니다.

## 화면에서 읽기: collectAsStateWithLifecycle

Compose에서 Flow를 `State`로 바꿔 읽는 함수입니다.

- `collectAsState()`는 화면이 백그라운드에 가도 계속 구독합니다.
- `collectAsStateWithLifecycle()`은 기본으로 `STARTED` 이상일 때만 구독합니다. 화면이 안 보이면(`onStop`) 멈추고 다시 보이면 이어서 받습니다.

```kotlin
@Composable
fun ArticleListRoute(viewModel: ArticleListViewModel = hiltViewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    ArticleListScreen(state = state, onRefresh = viewModel::onRefresh)
}
```

앞의 `WhileSubscribed(5_000)`과 짝을 이룹니다.
화면이 안 보이면 구독하던 코루틴이 취소되고 5초 뒤 업스트림(DB 감시, 위치 업데이트)까지 멈춥니다.
도입에서 말한 "해제는 코루틴 취소"가 이 모습입니다.
Flutter에서 `StreamBuilder`가 위젯 트리에서 빠질 때 구독을 끊는 것과 비슷하지만 여기서는 **화면이 트리에 있어도 안 보이면** 끊습니다.

Compose 밖(Activity)에서는 `repeatOnLifecycle(Lifecycle.State.STARTED) { flow.collect { } }`가 같은 역할입니다.

## stateIn은 어디에 두는가

기본은 ViewModel입니다.
Hot Flow는 언제까지 살지 정할 Scope가 필요한데, 그게 `viewModelScope`입니다.
Repository와 UseCase는 Cold Flow를 돌려주는 것이 기본입니다.

여러 화면이 같은 데이터를 나눠야 할 때만 Repository에서 앱 수명 Scope(1편의 `@ApplicationScope`)로 `shareIn`합니다.

`stateIn`은 초기값이 필수라, DB에서 첫 값을 읽기 전에도 화면에 줄 값이 있어야 합니다.
이때 빈 목록을 초기값으로 주면 데이터가 있는데도 "목록이 비어 있습니다" 화면이 잠깐 그려졌다가 바뀝니다.
그럴 때는 `stateIn` 대신 `shareIn(replay = 1)`을 쓰거나, 초기값을 `Loading` 상태로 둡니다.

## StateFlow의 성질

`stateIn`으로 만든 것도, ViewModel이 직접 쥐는 `MutableStateFlow`도 `StateFlow`입니다.
`StateFlow`는 화면 상태를 담는 기본 그릇입니다.
성질 네 가지를 알아 두면 대부분의 문제를 미리 피합니다.

1. **값이 항상 하나 있습니다.** 초기값이 필수이고, 새로 구독하면 지금 값을 바로 받습니다.
2. **같은 값은 다시 내보내지 않습니다.** `equals`로 비교합니다. 그래서 상태는 `data class`로 둡니다.
3. **빠르게 여러 번 바뀌면 중간 값을 건너뜁니다(conflation).** 최신 값만 중요한 상태에는 맞고 이벤트를 값 하나씩 보내는 데는 맞지 않습니다.
4. **읽고 쓰는 사이에 다른 코루틴이 끼면 덮어씁니다.** 그래서 `update { }`를 씁니다.

```kotlin
private val _uiState = MutableStateFlow(ArticleListUiState())
val uiState: StateFlow<ArticleListUiState> = _uiState.asStateFlow()

fun onRefreshDone() {
    // ❌ _uiState.value = _uiState.value.copy(refreshing = false)
    _uiState.update { it.copy(refreshing = false) }
}
```

주석 처리한 줄은 "읽기, 고치기, 쓰기" 세 단계입니다.
두 코루틴이 이 세 단계를 동시에 밟으면 경쟁 상태(race condition)가 생깁니다.

1. A가 `refreshing = true`인 상태를 읽습니다.
2. B도 같은 상태를 읽습니다.
3. A가 `refreshing = false`로 고쳐 씁니다.
4. B가 자기가 읽은 옛 상태에서 다른 필드만 고쳐 씁니다. A가 바꾼 `refreshing = false`는 덮여 사라집니다.

`update`는 읽은 뒤 그사이 다른 코루틴이 값을 바꿨으면 최신 값으로 다시 계산합니다.
그래서 두 코루틴이 동시에 고쳐도 한쪽의 수정이 덮여 사라지지 않습니다.
블록이 여러 번 돌 수 있으므로 안에서는 새 값을 계산하는 일만 합니다.

화면이 모든 중간 값을 받는다는 뜻은 아닙니다.
내보내기는 여전히 3번 성질대로 최신 값만 남깁니다.
`update`는 쓰는 쪽의 안전장치이고 화면이 받는 값과는 따로 움직입니다.

이 문제는 1편에서 본 "스레드는 메모리를 공유한다"의 결과입니다.

Flutter의 `ValueNotifier`도 같은 값이면 알리지 않습니다.
2번은 익숙하고 3번과 4번이 새로운 부분입니다.

## 일회성 이벤트도 상태로

스낵바나 화면 이동 같은 일회성 이벤트를 어떻게 보낼지는 늘 논쟁입니다.

| 방식 | 문제 |
|---|---|
| `Channel` | 화면이 그 순간 받지 않으면 쌓였다가 엉뚱한 때 뜨거나, 처리 전에 화면이 사라지면 잃음 |
| `SharedFlow(replay = 0)` | 구독자가 없을 때 보내면 사라짐 |
| UiState에 넣고 처리 후 지움 | 지우는 함수를 따로 불러야 해서 코드가 조금 늘어남 |

구글 공식 가이드는 마지막 방식을 권합니다.
"ViewModel에서 시작한 UI 동작은 상태 갱신으로 표현하라"는 것이 요지입니다.

```kotlin
data class ArticleListUiState(
    val articles: ImmutableList<ArticleUiModel> = persistentListOf(),
    val messages: ImmutableList<UiMessage> = persistentListOf(),
)

fun onMessageShown(id: Long) {
    _uiState.update { s -> s.copy(messages = s.messages.filterNot { it.id == id }.toPersistentList()) }
}
```

앞에서 StateFlow는 이벤트를 값 하나씩 보내는 데는 맞지 않는다고 했습니다(3번 성질).
여기서는 메시지를 하나씩 보내지 않고 목록에 쌓습니다.
중간 값을 건너뛰어도 최신 목록에는 아직 처리하지 않은 메시지가 남아 있으므로, 화면은 하나도 놓치지 않습니다.

메시지마다 `id`를 붙이는 이유는 StateFlow의 2번 성질 때문입니다.
같은 문구의 메시지 두 개가 하나로 합쳐지지 않게 합니다.

## flow와 channelFlow

| | `flow { }` | `channelFlow { }` |
|---|---|---|
| 내보내기 | `emit` | `send` |
| 안에서 `launch` | 다른 코루틴에서 `emit`하면 예외 | 여러 `launch`에서 동시에 `send` 가능 |
| 끝나는 때 | 블록이 끝나면 | 블록과 안의 코루틴이 모두 끝나면 |

둘 다 Cold입니다.
`flow { }` 안에서 `launch { emit(x) }`를 하면 `IllegalStateException: Flow invariant is violated`가 납니다.
`flow`는 한 코루틴 안에서 순서대로 내보낸다는 약속이기 때문입니다.

DB 감시, 새로고침 신호, 항목별 추가 요청처럼 여러 일을 동시에 돌려 하나의 흐름으로 내보내야 하면 `channelFlow`를 씁니다.

## combine과 flatMapLatest

- **`combine(a, b)`**: 둘 중 하나라도 새 값을 내면, 각자의 최신 값으로 합쳐 내보냅니다. 화면 상태는 보통 이것입니다.
- **`zip(a, b)`**: 1번째와 1번째, 2번째와 2번째처럼 짝을 맞춥니다. 한쪽이 느리면 기다립니다.
- **`flatMapLatest`**: 바깥 값이 바뀔 때마다 새 안쪽 Flow로 갈아타고 이전 것은 취소합니다.

```kotlin
query
    .debounce(300)
    .flatMapLatest { text -> repository.search(text) }  // 새 검색어가 오면 이전 검색 취소
```

1편에서 `Job`을 쥐고 이전 요청을 취소하던 일을 연산자 하나가 대신합니다.

## 정리

- `collect`는 그 줄에서 멈추는 suspend 함수다. 해제는 코루틴 취소로 한다.
- Cold Flow는 구독자마다 따로 돈다. 나눠 써야 하면 `stateIn`·`shareIn`으로 Hot으로 바꾼다.
- 화면에서는 `collectAsStateWithLifecycle()`로 읽는다. `WhileSubscribed`와 함께 쓰면 안 보이는 화면의 업스트림까지 멈춘다.
- `StateFlow`는 같은 값을 무시하고 중간 값을 건너뛴다. 값 변경은 `update { }`로 한다.
- 일회성 이벤트는 상태의 목록에 쌓고 처리한 뒤 지운다.
- 여러 코루틴에서 내보내려면 `channelFlow`를 쓴다.

다음 편에서는 이 상태를 받아 그리는 Compose로 넘어갑니다.
Flutter의 rebuild와 Compose의 리컴포지션은 비슷해 보이지만 무엇을 건너뛰는지가 다릅니다.
