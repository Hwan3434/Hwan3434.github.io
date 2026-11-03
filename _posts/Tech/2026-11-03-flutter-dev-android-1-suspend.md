---
title: "Flutter 개발자가 본 Android (1) suspend는 스레드를 막지 않는다"
description: "Dart의 async/await에 익숙한 개발자가 Kotlin 코루틴을 이해하는 기준점: suspend, launch와 async, 구조화된 동시성, Dispatcher"
date: 2026-11-03 22:00:00 +0900
categories: [android, 코루틴]
tags: [Kotlin, Coroutine, Dart, Flutter, 구조화된 동시성]
series: "Flutter 개발자가 본 Android"
series_order: 1
toc: true
---

Flutter를 3년 하고 다시 Android 코드를 열었을 때, 코루틴은 낯설지 않았습니다.
`suspend`는 `async`, 함수 호출은 `await`, `Deferred`는 `Future`.
대응표만 외우면 끝날 것 같았습니다.

막상 써 보니 그렇지 않았습니다.
문법은 닮았지만 **실행 모델이 달랐습니다.**
Dart의 Future는 Isolate 하나의 이벤트 루프, 즉 스레드 하나에서만 돕니다.
Kotlin의 코루틴은 Dispatcher에 따라 여러 스레드를 오갑니다.
같은 층위끼리 놓으면 Future는 코루틴과, Isolate는 스레드와 대응합니다. 다만 Isolate끼리는 메모리를 공유하지 않고 스레드끼리는 공유합니다.
이 차이를 모르고 대응표로만 읽으면, 메인 스레드를 막는 코드를 "비동기"라고 믿고 쓰게 됩니다.

이 시리즈는 Flutter 개발자의 눈으로 Android를 다시 보는 기록입니다.
1편은 코루틴의 출발점인 `suspend`입니다.

## suspend는 스레드를 막는가

결론부터 쓰면, **`suspend`는 코루틴을 멈추고 스레드는 풀어 줍니다.**

```kotlin
Thread.sleep(1000)  // 스레드를 막음 (blocking). 메인이면 화면이 멈춤
delay(1000)         // 코루틴만 멈춤 (suspend). 스레드는 다른 일을 함
```

`delay`가 호출되면 컴파일러가 만든 Continuation에 "여기서 멈췄다가 이어서 할 정보"가 담기고 스레드는 풀려납니다.
1초 뒤 코루틴은 그 지점부터 다시 실행됩니다.
멈출 수 있는 지점(중단 지점)은 `delay`, `await`, `withContext`, 그리고 다른 suspend 함수 호출입니다.

여기서 짚어 둘 점이 하나 있습니다.
**`suspend`를 붙인다고 스레드가 바뀌지 않습니다.**
첫 중단 지점까지는 부른 스레드에서 그대로 돕니다.
Dart의 `async` 함수가 첫 `await` 전까지 동기로 도는 것과 같습니다.

```kotlin
suspend fun parseAll(raw: List<String>): List<Article> {
    // 중단 지점이 없음 → 메인에서 부르면 메인이 그대로 막힘
    return raw.map { heavyParse(it) }
}
```

| 코드 | 스레드 | 메인에서 쓰면 |
|---|---|---|
| `Thread.sleep` | 막힘 | 화면 멈춤 |
| `delay` | 풀려남 | 안 멈춤 |
| suspend 함수 안의 무거운 반복문 | 막힘 | 화면 멈춤 |

Dart라면 무거운 계산은 `Isolate.run`(또는 `compute`)으로 보냅니다.
Kotlin에서는 `withContext`로 다른 Dispatcher에 보냅니다.

```kotlin
suspend fun parseAll(raw: List<String>): List<Article> =
    withContext(Dispatchers.Default) {
        raw.map { heavyParse(it) }
    }
```

### Dart와 대응표

| Dart | Kotlin |
|---|---|
| `async` 키워드 | `suspend` |
| `await` | suspend 함수를 그냥 부르기 |
| `Future<T>` | `Deferred<T>` |
| `await` 없이 부르기 | `async { }` |
| Isolate (메모리 공유 안 함) | 스레드 (메모리 공유함) |

마지막 줄이 가장 중요합니다.
Dart는 Isolate끼리 메모리를 공유하지 않으니 동시 수정 문제가 구조적으로 막혀 있습니다.
Kotlin은 스레드가 메모리를 공유하므로, 여러 코루틴이 같은 상태를 바꿀 때 직접 신경 써야 합니다.
그래서 `MutableStateFlow.update { }`를 씁니다. 비교 후 바꾸기를 반복하므로 동시에 바뀌어도 변경 하나가 사라지지 않습니다. StateFlow는 3편에서 자세히 다룹니다.

## launch와 async

- **`launch`**: 결과 없이 일을 시작하고 `Job`을 돌려줍니다. `Job`으로 취소하거나 끝나길 기다립니다(`join`).
- **`async`**: 결과가 있는 일을 시작하고 `Deferred<T>`를 돌려줍니다. `.await()`로 꺼냅니다. `Deferred`는 `Job`의 일종이고 Dart의 `Future`와 같습니다.

1초 걸리는 요청 두 개를 차례로 부르면 2초, `async` 두 개로 동시에 시작하고 기다리면 1초 남짓입니다.

```kotlin
coroutineScope {
    val article = async { repository.getArticle(id) }
    val comments = async { repository.getComments(id) }
    show(article.await(), comments.await())
}
```

Dart의 `Future.wait([...])`와 같은 그림입니다.

`withContext`는 새 코루틴이 아닙니다.
지금 코루틴이 다른 스레드로 옮겨 가서 일하고 결과를 들고 돌아옵니다.
그래서 순서대로 실행됩니다.

### Job을 쥐고 있으면 늦은 응답을 버릴 수 있다

`launch`가 돌려주는 `Job`은 생각보다 쓸모가 많습니다.
목록 새로고침이 대표적입니다.

```kotlin
private var loadJob: Job? = null

fun refresh() {
    loadJob?.cancel()   // 진행 중인 이전 요청을 먼저 취소
    loadJob = viewModelScope.launch {
        val articles = repository.getArticles(page = 1)
        _uiState.update { it.copy(articles = articles) }
    }
}
```

이전 `Job`을 취소하지 않으면, 늦게 도착한 옛 응답이 새 결과를 덮어쓸 수 있습니다.
Dart에서는 요청 번호를 들고 다니며 "내가 마지막 요청인가"를 비교하던 코드가, 여기서는 `cancel()` 한 줄입니다.

## 구조화된 동시성: mounted 확인이 필요 없는 이유

Flutter에서 가장 많이 쓰는 방어 코드 중 하나는 이것입니다.

```dart
final articles = await repository.getArticles();
if (!mounted) return;   // 화면이 사라졌으면 setState 하지 않음
setState(() => _articles = articles);
```

Kotlin에는 이 확인이 없습니다.
코루틴이 **화면 수명에 묶인 Scope 안에서** 돌기 때문입니다.

Scope는 두 가지를 가집니다.
수명을 정하는 `Job`, 그리고 기본으로 쓸 Dispatcher입니다.
Scope 안에서 띄운 코루틴은 그 Scope의 자식이고 부모와 자식 사이에는 세 가지 규칙이 있습니다.

- 부모가 취소되면 자식도 모두 취소됩니다.
- 부모는 자식이 모두 끝날 때까지 끝나지 않습니다.
- 자식이 실패하면 부모에게 전달됩니다(2편에서 다룹니다).

이것이 **구조화된 동시성**입니다.
코루틴이 아무 데도 묶이지 않은 채 떠다니지 않게 하는 규칙입니다.

화면을 닫으면 ViewModel이 정리되면서 `viewModelScope`가 취소되고 그 아래 띄운 요청도 모두 취소됩니다.
진행 중이던 코루틴은 다음 중단 지점에서 `CancellationException`으로 멈추고 그 아래 `_uiState.update`는 실행되지 않습니다.
`mounted`를 확인할 대상 자체가 없어지는 셈입니다.

| Scope | 수명 | 기본 Dispatcher |
|---|---|---|
| `viewModelScope` | ViewModel이 정리될 때까지. 화면 회전에도 살아남음 | `Main.immediate` |
| `lifecycleScope` | Activity·Fragment가 `onDestroy` 될 때까지. 회전하면 취소 | `Main.immediate` |
| `rememberCoroutineScope()` | Composable이 화면에서 빠질 때까지 | 메인 |
| `coroutineScope { }` | 블록 안의 자식이 다 끝날 때까지 | 부른 곳 그대로 |
| `GlobalScope` | 앱 전체. 부모 없음 | `Default` |

`lifecycleScope`는 `onStop`에서 취소되지 않습니다.
화면이 안 보일 때 멈추려면 `repeatOnLifecycle(STARTED)`를 씁니다.

### GlobalScope를 쓰지 않는 이유

`GlobalScope`는 부모가 없어서 위 규칙 밖으로 나갑니다.

- 화면이 사라져도 자동으로 취소되지 않습니다. 화면을 붙잡고 있으면 메모리 누수입니다.
- 실패를 알릴 부모가 없습니다. 처리기가 없으면 앱이 종료됩니다.
- 코드에 박혀 있어 테스트에서 바꿔 끼울 수 없습니다.

화면보다 오래 살아야 하는 일(로그 전송 등)은 앱 수명의 Scope를 만들어 **주입**합니다.

```kotlin
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class ApplicationScope

@Module
@InstallIn(SingletonComponent::class)
object ScopeModule {
    @Provides @Singleton @ApplicationScope
    fun provideAppScope(): CoroutineScope =
        CoroutineScope(SupervisorJob() + Dispatchers.Default)
}
```

앱 프로세스가 죽어도 반드시 끝내야 하는 일은 WorkManager로 보냅니다.
코루틴은 프로세스와 함께 사라집니다.

Flutter에서 `context`를 통해 의존성을 위에서 내려받듯, Kotlin에서도 Scope를 전역에서 꺼내 쓰지 않고 위에서 받습니다.
수명을 누가 쥐고 있는지가 코드에 드러나야 한다는 점에서 두 생태계의 철학은 같습니다.

## Dispatcher와 main-safe

| Dispatcher | 스레드 | 쓰는 곳 |
|---|---|---|
| `Main` | 메인 스레드 1개 | 화면 갱신 |
| `Main.immediate` | 메인. 이미 메인이면 줄 서지 않고 바로 실행 | `viewModelScope`·`lifecycleScope` 기본값 |
| `Default` | CPU 코어 수만큼 | 정렬, 파싱 같은 계산 |
| `IO` | 최대 64개(또는 코어 수 중 큰 값) | 막는 입출력(파일, 블로킹 API) |

`Default`는 이름과 달리 메인이 아니라 **계산용 스레드 묶음**입니다.

**main-safe**는 메인 스레드에서 불러도 안전한 함수를 말합니다.
무거운 일은 함수가 스스로 다른 Dispatcher로 옮깁니다.

- Room의 suspend DAO 함수와 Flow를 반환하는 함수는 Room이 자기 스레드에서 쿼리를 돌립니다.
- Retrofit의 suspend 함수, Apollo의 `execute()`도 네트워크를 내부에서 다른 스레드로 보냅니다.

그래서 이런 라이브러리를 감싸는 Repository에 `withContext(Dispatchers.IO)`를 습관처럼 두를 필요는 없습니다.
`withContext`가 필요한 곳은 **직접 만든** 무거운 계산(`Default`)과 막는 API 호출(`IO`)입니다.
그리고 그 옮기는 책임은 부르는 쪽이 아니라 **그 함수 안**에 둡니다.

## 정리

- `suspend`는 코루틴을 멈추고 스레드를 풀어 준다. 하지만 스레드를 바꾸지는 않는다.
- 무거운 계산은 Dart의 `Isolate.run` 자리에 `withContext(Dispatchers.Default)`를 둔다.
- `launch`는 `Job`, `async`는 `Deferred`. `Job`을 쥐고 있으면 늦은 응답을 취소로 버릴 수 있다.
- 구조화된 동시성 덕분에 `mounted` 확인이 필요 없다. `GlobalScope` 대신 Scope를 주입한다.
- `Dispatchers.Default`는 메인이 아니다.

문법은 대응표로 넘어오지만 실행 모델은 대응표로 넘어오지 않습니다.
다음 편에서는 이 구조 위에서 예외와 취소가 어떻게 흐르는지, 그리고 `runCatching`이 왜 코루틴 안에서 위험한지 다룹니다.
