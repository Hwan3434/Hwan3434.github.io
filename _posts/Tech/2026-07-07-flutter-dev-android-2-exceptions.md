---
title: "Flutter 개발자가 본 Android (2) 코루틴의 예외와 취소"
description: "실패와 취소가 흐르는 방향, SupervisorJob, CoroutineExceptionHandler, 취소를 삼키지 않는 법, 협조적 취소. 그리고 ViewModel에 try/catch를 두지 않는 규칙"
date: 2026-07-07 21:00:00 +0900
categories: [android, 코루틴]
tags: [Kotlin, Coroutine, 예외 처리, 취소, SupervisorJob]
series: "Flutter 개발자가 본 Android"
series_order: 2
---

Dart에서 `Future`의 예외는 단순합니다.
`await`한 자리에서 터지고 `try/catch`로 잡습니다.
잡지 않으면 Zone까지 올라가 로그에 남고 앱은 대부분 그대로 돕니다.

Kotlin 코루틴은 다릅니다.
1편에서 본 부모와 자식 관계를 따라 **예외가 위로 올라가고, 취소는 아래로 내려갑니다.**
그리고 Android에서는 아무도 잡지 않은 예외가 앱을 종료시킵니다.

2편은 예외와 취소가 이 구조 위에서 어떻게 흐르는지, 그리고 그 흐름을 전제로 예외 처리를 어디에 둘지 정리합니다.

## 실패는 위로, 취소는 아래로

일반 `Job` 아래에서 자식 하나가 예외로 실패하면, 자식은 부모에게 실패를 알립니다.
부모는 나머지 자식을 모두 취소하고 자신도 같은 예외로 실패하며 다시 그 위로 알립니다.
이렇게 맨 위까지 올라간 예외를 아무도 처리하지 않으면 앱이 종료됩니다.

이 동작은 "같이 해야 의미 있는 일"을 묶을 때 맞습니다.
기사 본문과 댓글을 함께 불러 한 화면을 만든다면, 본문이 실패했을 때 댓글을 계속 받는 것은 낭비이기 때문입니다.

취소는 반대 방향으로 흐릅니다.
부모가 취소되면 자식이 모두 취소되지만 자식이 취소됐다고 부모에게 알리지는 않습니다.
방향이 반대인 이유는 `loadMoreJob?.cancel()` 같은 코드를 떠올리면 분명해집니다.
취소까지 위로 올라간다면 다음 페이지 요청 하나를 끄는 순간 형제와 부모가 모두 멈춥니다.
일부만 골라 끌 수 없게 됩니다.

`Job`이 실패와 취소를 구분하는 기준은 예외의 타입 하나입니다.
코루틴이 `CancellationException`으로 끝나면 "취소됨", 다른 예외로 끝나면 "실패"로 봅니다.
`withTimeout`이 던지는 `TimeoutCancellationException`도 하위 클래스라 취소로 처리됩니다.

## SupervisorJob과 viewModelScope

`SupervisorJob`은 자식의 실패를 부모에게 올리지 않습니다.
자식 하나가 실패해도 형제는 계속 돕니다.

`viewModelScope`는 `SupervisorJob + Dispatchers.Main.immediate`로 만들어져 있습니다.
기사 북마크 저장이 실패해도 목록 불러오기는 계속돼야 하기 때문입니다.

다만 `SupervisorJob`이 하는 일은 형제를 살리는 데까지입니다.
실패한 `launch`의 예외는 여전히 처리되지 않은 채 남고 Android에서는 그대로 앱이 종료됩니다.

`SupervisorJob`을 직접 넘기는 코드는 의도와 다르게 동작합니다.

```kotlin
viewModelScope.launch(SupervisorJob()) { ... }
```

새로 만든 `SupervisorJob`이 이 코루틴의 부모가 되면서 `viewModelScope`와의 연결이 끊깁니다.
그래서 화면을 나가도 이 코루틴은 취소되지 않습니다.
묶음 안에서 서로 독립적으로 실패하게 하려면 `supervisorScope { }`를 씁니다.

## 예외는 코루틴 안에서 잡는다

`launch`를 `try/catch`로 감싸도 그 안의 예외는 잡히지 않습니다.
`launch`는 코루틴을 시작하자마자 반환하고 예외는 나중에 그 코루틴 안에서 터지기 때문입니다.
예외를 잡으려면 `try/catch`가 코루틴 안에 있어야 합니다.

```kotlin
// launch 바깥의 try/catch는 코루틴 안의 예외를 잡지 못합니다
try {
    viewModelScope.launch { throw IOException() }
} catch (e: Exception) { }

// 코루틴 안에서 잡습니다
viewModelScope.launch {
    try { load() } catch (e: IOException) { showError() }
}
```

`launch`와 `async`는 예외가 드러나는 때도 다릅니다.
`launch`는 실패하는 즉시 부모에게 알립니다.
`async`는 예외를 `Deferred`에 담아 두었다가 `await()`를 부를 때 던집니다.
Dart의 `Future`가 `await`한 자리에서 예외를 던지는 것과 같은 모양입니다.

여기에 한 가지 조건이 붙습니다.
일반 `Job` 아래의 `async`는 `await()`를 부르기 전이라도 실패하는 즉시 부모를 취소시킵니다.
부모 입장에서는 자식 하나가 실패한 것이기 때문입니다.
`await()`의 `try/catch`가 예외를 받는 것과 별개로, 형제는 이미 취소되어 있습니다.

## 마지막 안전망: CoroutineExceptionHandler

맨 위까지 올라간 예외가 앱을 종료시키기 전에 가로챌 수 있는 곳이 `CoroutineExceptionHandler`입니다.

```kotlin
private val handler = CoroutineExceptionHandler { _, throwable ->
    logger.report(throwable)
    _uiState.update { it.copy(error = true) }
}

fun bookmark(id: Long) {
    viewModelScope.launch(handler) {
        repository.bookmark(id)
    }
}
```

이 Handler는 아무도 처리하지 않은 예외가 마지막에 도착하는 곳입니다.
여기서 로그를 남기거나 오류 상태를 보여 줄 수는 있지만 코루틴을 되살리지는 못합니다.
Handler가 불린 시점에 그 코루틴은 이미 실패로 끝나 있습니다.

Handler가 동작하는 자리는 정해져 있습니다.

- **루트 `launch`에서만 동작합니다.** Scope 바로 아래에서 시작한 `launch`, 또는 Scope 자체의 Context에 둔 Handler가 불립니다. 자식 코루틴에 붙인 Handler는 무시됩니다. 자식의 예외는 Handler를 보지 않고 부모에게 올라가기 때문입니다.
- **`async`에는 효과가 없습니다.** `async`는 예외를 `Deferred`에 담아 `await()`를 부른 쪽에 넘기므로, 처리하지 않은 예외로 취급되지 않습니다.
- **`SupervisorJob` 바로 아래의 자식은 루트처럼 취급됩니다.** `viewModelScope.launch(handler)`가 동작하는 이유가 이것입니다.

Dart에서 `runZonedGuarded`나 `PlatformDispatcher.instance.onError`로 처리되지 않은 오류를 모으는 것과 역할이 비슷합니다.
다만 범위가 앱 전체가 아니라, Handler를 붙인 루트 코루틴 하나입니다.

## 취소를 삼키지 않기

취소가 `CancellationException`이라는 예외로 전달된다는 점이 문제를 만듭니다.
`Exception`을 넓게 잡으면 취소도 같이 잡히기 때문입니다.

```kotlin
viewModelScope.launch {
    try {
        repository.load()
    } catch (e: Exception) {
        showError()     // 화면을 나가며 생긴 취소도 여기서 잡힘
    }
    doNext()            // 취소된 코루틴이 다음 일을 계속함
}
```

화면을 나가서 취소된 코루틴이 오류 상태를 만들고, 다음 일까지 이어서 합니다.
그래서 `Exception`을 넓게 잡는 곳에서는 취소만 먼저 다시 던집니다.

```kotlin
try {
    Result.Success(api.fetchArticles())
} catch (e: CancellationException) {
    throw e
} catch (e: Exception) {
    Result.Failure(e)
}
```

Kotlin 표준 라이브러리의 `runCatching`도 같은 문제를 가지고 있습니다.
Dart의 `try/catch`를 한 줄로 쓰고 싶을 때 먼저 떠오르는 함수인데, 내부에서 `Throwable`을 전부 잡습니다.
suspend 함수에 쓰면 `CancellationException`이 `Result.failure`로 바뀌어 위의 예와 같은 일이 생깁니다.
`OutOfMemoryError` 같은 `Error`도 함께 잡힙니다.
그래서 suspend 함수에서는 `runCatching` 대신 위처럼 `try/catch`로 취소를 통과시키거나, 같은 일을 하는 함수를 따로 만들어 씁니다.

```kotlin
suspend inline fun <R> suspendRunCatching(block: () -> R): Result<R> =
    try { Result.success(block()) }
    catch (e: CancellationException) { throw e }
    catch (e: Exception) { Result.failure(e) }
```

## 취소는 협조적이다

`job.cancel()`은 코루틴에 "취소됨" 표시를 남길 뿐, 실행 중인 스레드를 강제로 멈추지 못합니다.
코루틴은 다음 중단 지점(`delay`, `emit`, Room이나 Retrofit의 suspend 호출)에서 이 표시를 확인하고 `CancellationException`을 던지며 멈춥니다.

계산만 하는 반복문에는 중단 지점이 없습니다.
그래서 취소해도 반복문이 끝날 때까지 돕니다.
이런 곳에는 직접 확인하는 지점을 넣습니다.

```kotlin
withContext(Dispatchers.Default) {
    for (image in images) {
        ensureActive()          // 취소됐으면 여기서 CancellationException
        makeThumbnail(image)
    }
}
```

가장 흔히 쓰는 것이 `ensureActive()`입니다.
멈추기 전에 정리할 것이 있으면 `isActive`로 상태만 확인하고, 다른 코루틴에게 잠깐 차례를 넘겨야 하면 `yield()`를 씁니다.
일반 suspend 함수 안에서는 `currentCoroutineContext().ensureActive()`로 부릅니다.
취소된 뒤 `finally`에서 suspend 함수로 정리해야 한다면 `withContext(NonCancellable) { }`로 감쌉니다.

## ViewModel에는 예외 처리를 두지 않는다

여기까지의 규칙을 매번 기억하며 화면마다 `try/catch`를 쓰면, 한 곳만 빠뜨려도 취소를 삼키거나 앱이 종료됩니다.
그래서 저는 예외가 값으로 바뀌는 곳을 data 레이어에 모으고, ViewModel에는 `try/catch`를 두지 않습니다.

> 하위 레이어는 운영 중에 생길 수 있는 실패를 모두 `Result.Failure`로 바꿔 올린다.
> 지키지 못하면 ViewModel이 아니라 하위 레이어를 고친다.

예외가 값으로 바뀌는 곳은 네트워크 응답(연결 실패, HTTP 오류, 파싱 실패), DB 쓰기, 그리고 DB를 구독하는 Flow의 `catch` 연산자 정도로 정해집니다.
이 모든 곳에서 `CancellationException`은 다시 던집니다.
ViewModel은 돌아온 값을 `when`으로 나눠 상태만 바꿉니다.

```kotlin
sealed interface Result<out T> {
    data class Success<T>(val value: T) : Result<T>
    data class Failure(val error: Exception) : Result<Nothing>
}

fun refresh() {
    viewModelScope.launch {
        when (val result = repository.getArticles(page = 1)) {
            is Result.Success -> _uiState.update { it.copy(articles = result.value) }
            is Result.Failure -> _uiState.update { it.copy(error = true) }
        }
    }
}
```

실패를 예외로 던지지 않고 값으로 돌려주는 Result 패턴입니다.
Flutter에서도 같은 패턴을 그대로 쓸 수 있습니다.
다른 점은 하나입니다.
Kotlin에서는 예외를 값으로 바꾸는 그 자리에서, 취소만은 값으로 바꾸지 않고 다시 던져야 합니다.

### 이 규칙의 대상이 아닌 것

`OutOfMemoryError`는 `Exception`이 아니라 `Error`이므로 잡지 않습니다.
프로그래머의 실수를 잡는 검사도 값으로 바꾸지 않습니다.
`require(조건)`은 인자가 잘못됐을 때 `IllegalArgumentException`을, `check(조건)`과 `error("메시지")`는 상태가 잘못됐거나 있을 수 없는 분기에 들어왔을 때 `IllegalStateException`을 던집니다.
이런 버그는 값으로 감추지 않고 빨리 종료되어 드러나야 고칠 수 있습니다.
Dart의 `assert`와 달리 이 함수들은 release 빌드에서도 동작합니다.

## 정리

- 실패는 위로, 취소는 아래로 흐른다. 둘을 가르는 기준은 `CancellationException`인지 아닌지 하나다.
- `SupervisorJob`은 형제를 살릴 뿐, 예외를 처리해 주지 않는다.
- 예외는 코루틴 안에서 잡는다. `async`의 예외는 `await()`에서 드러나지만, 일반 `Job` 아래에서는 그 전에 형제를 취소시킨다.
- `CoroutineExceptionHandler`는 루트 `launch`의 마지막 안전망이다. 자식과 `async`에는 효과가 없다.
- `Exception`을 넓게 잡거나 `runCatching`을 쓰면 취소까지 삼킨다. 취소는 다시 던진다.
- 취소는 중단 지점에서만 확인된다. 계산 반복문에는 `ensureActive()`를 둔다.
- 예외를 값으로 바꾸는 곳을 data 레이어에 모으면, ViewModel에는 `try/catch`가 필요 없다. 실패를 값으로 돌려주는 Result 패턴이다.

다음 편에서는 Dart의 `Stream` 자리에 있는 `Flow`를 다룹니다.
이름은 비슷하지만 Cold와 Hot을 구분하지 않으면 같은 쿼리가 두 번 돕니다.
