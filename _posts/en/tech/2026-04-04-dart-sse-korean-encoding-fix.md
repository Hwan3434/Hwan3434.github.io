---
title: "Korean Character Encoding Issues in Dart SSE Communication"
description: "Causes of corrupted multibyte characters in SSE streams and a solution using Dart stream pipelines"
date: 2026-04-04 19:00:00 +0900
categories: [flutter, troubleshooting]
tags: [Dart, SSE, UTF-8, Encoding]
toc: true
---

## The Problem

When receiving stream data, decoding each chunk immediately as it arrives causes Korean characters to break.

```dart
// ❌ Incorrect approach: decoding each chunk independently
response.stream.listen((chunk) {
  final decodedString = utf8.decode(chunk);
  final lines = decodedString.split('\n');
  for (final line in lines) {
    // ... data: line processing and JSON parsing logic ...
  }
});
```

### Why does it break?

Network chunks are split into arbitrary sizes **without considering character boundaries**.

- `'한'` = UTF-8 3 bytes `[0xED, 0x95, 0x9C]`
- **Chunk 1** ends with only `[0xED, 0x95]` arriving → `utf8.decode()` fails → corrupted character
- **Chunk 2** starts with `[0x9C]` → again, not a complete character → corrupted character
- The corrupted string is not valid JSON, which leads to parsing errors in `jsonDecode`

---

## Core Cause

This happens because each chunk is **treated as an unrelated, independent unit** and decoded in a **Stateless** manner.

Since the decoder doesn't remember the last bytes of the previous chunk, it cannot restore characters that were cut off at the chunk boundaries.

---

## Solution: Stateful Stream Pipeline

Build a pipeline using Dart's **stateful stream converters**.

```dart
// ✅ Correct approach: Stateful decoding
final ResponseBody responseBody = response.data;

// 1. Prepare byte stream
final Stream<List<int>> byteStream = responseBody.stream;

// 2. Stateful UTF-8 decoding (remembers incomplete bytes and combines them with the next chunk)
final stringStream = utf8.decoder.bind(byteStream);

// 3. Split by lines
final lineStream = stringStream.transform(const LineSplitter());

// 4. Use safely
await for (final line in lineStream) {
  if (line.startsWith('data:')) {
    final jsonData = line.substring(5).trim();
    if (jsonData.isNotEmpty) {
      final dataMap = jsonDecode(jsonData);
      // ... successful logic processing ...
    }
  }
}
```

---

## How it works

> `Bytes Stream` → `Stateful UTF-8 Decoder` → `String Stream` → `Line Splitter` → `Line Stream`

- **`utf8.decoder.bind(byteStream)`** — If a chunk ends with an incomplete character, it does not emit the result and **waits for the next chunk**. When the remaining bytes arrive, they are combined to restore the complete character.
- **`transform(const LineSplitter())`** — Safely separates the decoded string by `\n` and delivers it perfectly line by line.

---

## Conclusion

If there's a possibility of multibyte characters being included, do not decode individual chunks directly. **Building a declarative pipeline with `bind` and `transform`** is a more stable method that aligns well with Dart's stream philosophy.
