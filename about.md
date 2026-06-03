---
layout: page
title: 소개
heading: "이정환<span style='color: var(--primary);'>.</span>"
lede: "\"팀원이 바뀌어도 코드는 읽혀야 하고, 구조가 오류를 막아야 한다고 믿는 10년 차 모바일 개발자입니다.\""
permalink: /about/
---

<style>
  :root {
    --brand-primary: #4f46e5;
    --brand-gradient: linear-gradient(135deg, #4f46e5 0%, #ec4899 100%);
    --card-bg: #ffffff;
    --card-border: #f3f4f6;
    --text-primary: #111827;
    --text-secondary: #4b5563;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }

  /* Dark mode support if the blog uses it */
  @media (prefers-color-scheme: dark) {
    :root {
      --card-bg: #1f2937;
      --card-border: #374151;
      --text-primary: #f9fafb;
      --text-secondary: #9ca3af;
    }
  }

  .stitch-container {
    max-width: 800px;
    margin: 0 auto;
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    color: var(--text-primary);
  }

  /* AI Notice Card */
  .stitch-notice {
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.08) 0%, rgba(236, 72, 153, 0.08) 100%);
    border: 1px solid rgba(79, 70, 229, 0.2);
    border-left: 4px solid var(--brand-primary);
    padding: 18px 24px;
    border-radius: 12px;
    margin-bottom: 48px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: var(--shadow-sm);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .stitch-notice:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  .stitch-notice-icon {
    font-size: 28px;
    line-height: 1;
    flex-shrink: 0;
  }
  .stitch-notice-text {
    font-size: 14.5px;
    line-height: 1.6;
    color: var(--text-secondary);
  }
  .stitch-notice-text strong {
    color: var(--brand-primary);
    font-weight: 700;
  }

  /* Intro Section */
  .stitch-intro {
    font-size: 1.125rem;
    line-height: 1.8;
    color: var(--text-secondary);
    margin-bottom: 32px;
  }
  .stitch-intro p {
    margin-bottom: 16px;
  }

  /* Section Titles */
  .stitch-section-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 64px 0 24px;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .stitch-section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--card-border);
  }

  /* Skills Grid */
  .stitch-skills {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
  }
  .stitch-skill-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 20px;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .stitch-skill-card:hover {
    border-color: var(--brand-primary);
    box-shadow: var(--shadow-lg);
    transform: translateY(-4px);
  }
  .stitch-skill-label {
    font-size: 0.875rem;
    color: var(--brand-primary);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
  }
  .stitch-skill-value {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  /* Experience Timeline */
  .stitch-timeline {
    position: relative;
    padding-left: 24px;
  }
  .stitch-timeline::before {
    content: '';
    position: absolute;
    left: 0;
    top: 8px;
    bottom: 0;
    width: 2px;
    background: var(--card-border);
    border-radius: 2px;
  }
  .stitch-timeline-item {
    position: relative;
    margin-bottom: 48px;
  }
  .stitch-timeline-item:last-child {
    margin-bottom: 0;
  }
  .stitch-timeline-dot {
    position: absolute;
    left: -29px;
    top: 6px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--brand-primary);
    border: 3px solid var(--card-bg);
    box-shadow: 0 0 0 2px var(--brand-primary);
  }
  .stitch-timeline-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 8px;
  }
  .stitch-company {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
  }
  .stitch-period {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--brand-primary);
    background: rgba(79, 70, 229, 0.1);
    padding: 4px 12px;
    border-radius: 20px;
  }
  .stitch-role {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 12px;
  }
  .stitch-tasks {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .stitch-tasks li {
    position: relative;
    padding-left: 20px;
    margin-bottom: 8px;
    color: var(--text-secondary);
    line-height: 1.6;
    font-size: 0.95rem;
  }
  .stitch-tasks li::before {
    content: '→';
    position: absolute;
    left: 0;
    color: var(--brand-primary);
    font-weight: bold;
  }

  /* Blog Stories */
  .stitch-story-box {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 32px;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
  }
  .stitch-story-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--brand-gradient);
  }
  .stitch-story-item {
    margin-bottom: 24px;
  }
  .stitch-story-item:last-child {
    margin-bottom: 0;
  }
  .stitch-story-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .stitch-story-desc {
    color: var(--text-secondary);
    line-height: 1.6;
    font-size: 0.95rem;
  }
</style>

<div class="stitch-container">
  
  <div class="stitch-notice">
    <div class="stitch-notice-icon">🤖</div>
    <div class="stitch-notice-text">
      <strong>안내:</strong> 이 블로그의 모든 글, 페이지 디자인, 그리고 코드 작성은 전면적으로 <strong>AI 에이전트와의 협업</strong>을 통해 기획, 개발 및 작성되었습니다.
    </div>
  </div>

  <div class="stitch-intro">
    <p>10년간 Android, iOS, Flutter를 거치며 다양한 아키텍처와 상태관리를 경험했고, 프레임워크의 기본 철학을 거스르지 않는 설계가 장기적으로 가장 효과적임을 확신하게 되었습니다.</p>
    <p>최근에는 레거시 코드를 9개의 패키지 멀티모듈 클린아키텍처로 전면 재설계하고, 동일한 구조를 신규 앱에 적용하여 빠른 개발 속도와 높은 코드 재사용성을 달성했습니다. 오류를 개발자의 주의력이 아닌 구조로 차단하고, 누구나 이해 가능한 간결한 구조를 지향합니다.</p>
  </div>

  <div class="stitch-section-title">기술 역량 (Skills)</div>
  <div class="stitch-skills">
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">주력 분야</div>
      <div class="stitch-skill-value">Flutter, Android, iOS</div>
    </div>
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">언어</div>
      <div class="stitch-skill-value">Dart, Kotlin, Swift</div>
    </div>
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">아키텍처</div>
      <div class="stitch-skill-value">Clean Arch, MVVM</div>
    </div>
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">상태 관리</div>
      <div class="stitch-skill-value">Riverpod, Provider</div>
    </div>
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">도구 & 인프라</div>
      <div class="stitch-skill-value">Git, CI/CD, Firebase</div>
    </div>
  </div>

  <div class="stitch-section-title">주요 경력 (Experience)</div>
  <div class="stitch-timeline">
    
    <div class="stitch-timeline-item">
      <div class="stitch-timeline-dot"></div>
      <div class="stitch-timeline-header">
        <div class="stitch-company">주식회사 뱅크엑스</div>
        <div class="stitch-period">2025.09 - 현재</div>
      </div>
      <div class="stitch-role">플레이플래닛 & 플레이플래닛 AI (Flutter)</div>
      <ul class="stitch-tasks">
        <li>레거시 코드 전면 클린아키텍처 재설계 (9개 패키지 멀티모듈 모노레포)</li>
        <li>MVVM + 커스텀 상태관리 라이브러리 패턴 설계 및 적용</li>
        <li>Riverpod 기반 의존성 주입, 패키지 레벨 의존성 방향 강제</li>
        <li>소셜로그인 일반화 (Apple, Google, Kakao, Naver) 및 JWT 토큰 자동 갱신</li>
      </ul>
    </div>

    <div class="stitch-timeline-item">
      <div class="stitch-timeline-dot"></div>
      <div class="stitch-timeline-header">
        <div class="stitch-company">엔에이치엔인재아이엔씨(NHN)</div>
        <div class="stitch-period">2023.03 - 2025.07</div>
      </div>
      <div class="stitch-role">모바일 개발 파트</div>
      <ul class="stitch-tasks">
        <li><strong>모바일 GPT Client (Flutter):</strong> 사내용 Chat GPT 앱 개발 및 MVVM 패턴 적용</li>
        <li><strong>티켓링크 iOS:</strong> 오프라인 티켓 조회, 자동 로그인 프로세스 개선</li>
        <li><strong>운수도원 (Android/iOS):</strong> 구글 애드몹 전면 광고 적용 및 Jenkins CI/CD 설정</li>
      </ul>
    </div>

    <div class="stitch-timeline-item">
      <div class="stitch-timeline-dot"></div>
      <div class="stitch-timeline-header">
        <div class="stitch-company">페이민트 주식회사</div>
        <div class="stitch-period">2022.12 - 2023.03</div>
      </div>
      <div class="stitch-role">결제선생 앱 리팩토링 (Android)</div>
      <ul class="stitch-tasks">
        <li>검색 시 페이징과 검색 조건 일반화 및 의존성 분리</li>
      </ul>
    </div>

    <div class="stitch-timeline-item">
      <div class="stitch-timeline-dot"></div>
      <div class="stitch-timeline-header">
        <div class="stitch-company">미소앤클라우드</div>
        <div class="stitch-period">2015.10 - 2022.09</div>
      </div>
      <div class="stitch-role">모바일 및 백엔드 개발</div>
      <ul class="stitch-tasks">
        <li>자체 Push 서버 개발 (Java Spring) 및 Android/iOS Push SDK 개발</li>
        <li>주식 매매 및 실시간 데이터 연동 앱 개발 (OAuth, 소켓 통신)</li>
      </ul>
    </div>

  </div>

  <div class="stitch-section-title">이 블로그의 이야기들</div>
  <div class="stitch-story-box">
    
    <div class="stitch-story-item">
      <div class="stitch-story-title">📱 Flutter & 모바일 아키텍처</div>
      <div class="stitch-story-desc">프레임워크의 철학을 거스르지 않는 구조적 고민과 실무 트러블슈팅을 기록합니다.</div>
    </div>
    
    <div class="stitch-story-item">
      <div class="stitch-story-title">🤖 AI 에이전트와 생산성</div>
      <div class="stitch-story-desc">AI 코딩 에이전트를 실무 환경에 맞게 커스텀하며 겪은 시행착오와 효율적인 협업 전략을 회고합니다.</div>
    </div>
    
    <div class="stitch-story-item">
      <div class="stitch-story-title">💡 최신 테크 동향</div>
      <div class="stitch-story-desc">쏟아지는 최신 AI 및 IT 업계의 핵심 뉴스들을 꾸준히 정리하고 공유합니다.</div>
    </div>

  </div>

</div>
