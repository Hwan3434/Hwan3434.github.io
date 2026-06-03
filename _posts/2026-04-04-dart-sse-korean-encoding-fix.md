---
title: "Dart SSE 통신 시 한글 깨짐 문제"
description: "SSE 스트림에서 멀티바이트 문자가 깨지는 원인과 Dart 스트림 파이프라인을 활용한 해결책"
date: 2026-03-09 19:00:00 +0900
categories: [Flutter, 트러블슈팅]
tags: [Dart, SSE, UTF-8, 인코딩]
toc: true
---

## 문제 상황

스트림 데이터를 받을 때, 각 청크가 도착할 때마다 즉시 디코딩하는 방식은 한글에서 깨짐을 유발한다.

```dart
// ❌ 잘못된 접근: 각 청크를 독립적으로 디코딩
response.stream.listen((chunk) {
  final decodedString = utf8.decode(chunk);
  final lines = decodedString.split('\n');
  for (final line in lines) {
    // ... data: 라인 처리 및 JSON 파싱 로직 ...
  }
});
```

### 왜 깨지는가

네트워크 청크는 **문자 경계를 고려하지 않고** 임의의 크기로 잘린다.

- `'한'` = UTF-8 3바이트 `[0xED, 0x95, 0x9C]`
- **청크 1** 끝에 `[0xED, 0x95]`만 도착 → `utf8.decode()` 실패 → 깨진 문자
- **청크 2** 시작이 `[0x9C]` → 역시 완전한 글자가 아님 → 깨진 문자
- 손상된 문자열은 유효한 JSON이 아니므로 `jsonDecode`에서 파싱 오류 발생

---

## 핵심 원인

각 청크를 **서로 관계 없는 독립 단위로 취급**하여 **상태 없이(Stateless)** 디코딩했기 때문이다.

디코더가 이전 청크의 마지막 바이트를 기억하지 못하므로 청크 경계에서 잘린 문자를 복원할 수 없다.

---

## 해결: 상태 유지 스트림 파이프라인

Dart의 **상태를 유지하는 스트림 변환기**로 파이프라인을 구축한다.

```dart
// ✅ 올바른 접근: 상태 유지 디코딩
final ResponseBody responseBody = response.data;

// 1. 바이트 스트림 준비
final Stream<List<int>> byteStream = responseBody.stream;

// 2. 상태 유지 UTF-8 디코딩 (불완전한 바이트를 기억하고 다음 청크와 조합)
final stringStream = utf8.decoder.bind(byteStream);

// 3. 줄 단위로 분리
final lineStream = stringStream.transform(const LineSplitter());

// 4. 안전하게 사용
await for (final line in lineStream) {
  if (line.startsWith('data:')) {
    final jsonData = line.substring(5).trim();
    if (jsonData.isNotEmpty) {
      final dataMap = jsonDecode(jsonData);
      // ... 성공적인 로직 처리 ...
    }
  }
}
```

---

## 동작 원리

> `Bytes Stream` → `Stateful UTF-8 Decoder` → `String Stream` → `Line Splitter` → `Line Stream`

- **`utf8.decoder.bind(byteStream)`** — 청크 끝이 불완전한 문자로 끝나면 결과를 내보내지 않고 **다음 청크를 기다린다**. 나머지 바이트가 도착하면 조합하여 완전한 글자로 복원한다.
- **`transform(const LineSplitter())`** — 안전하게 디코딩된 문자열을 `\n` 기준으로 분리하여 완벽한 한 줄씩 전달한다.

---

## 마치며

멀티바이트 문자가 포함될 가능성이 있다면 개별 청크를 직접 디코딩하지 말고, **`bind`와 `transform`으로 선언적 파이프라인을 구축**하는 것이 안정적이고 Dart의 스트림 철학에 부합하는 방법이다.
