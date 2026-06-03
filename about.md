---
layout: page
title: 소개
heading: "이정환<span style='color: var(--primary);'>.</span>"
lede: "\"팀원이 바뀌어도 코드는 읽혀야 하고, 오류는 구조가 막아야 합니다. 단기적인 타협이 남기는 기술 부채를 경계하는 10년 차 모바일 아키텍트입니다.\""
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
  .stitch-intro strong {
    color: var(--text-primary);
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
    margin-bottom: 10px;
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
  .stitch-tasks li strong {
    color: var(--text-primary);
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
    <p>10년간 백엔드, Android, iOS를 거쳐 현재 Flutter 개발에 이르기까지, 저는 <strong>'당장 작동만 하는 단기적인 해결책'이 미래에 얼마나 거대한 기술 부채와 재투자 비용을 요구하는지</strong> 뼈저리게 목격해 왔습니다.</p>
    <p>일정의 압박 속에서도 비즈니스 엣지 케이스(예: 광고 노출의 시작/종료일 등)를 누락한 채 화면 구현부터 서두르거나, 특정 Entity에 응집되어야 할 데이터를 여러 페이지에서 매번 새로 조회하도록 방치하는 형태의 타협을 엄격하게 경계합니다.</p>
    <p>하지만 <strong>당장의 목표를 벗어난 무리한 오버엔지니어링 역시 지양합니다.</strong> 목표한 바에 정확히 부합하는 유연한 아키텍처를 세우고, <strong>"팀원이 바뀌어도 코드가 쉽게 읽히며, 개발자의 주의력이 아닌 컴파일러(구조)가 오류를 사전에 막아주는 환경"</strong>을 구축하는 것이 저의 변하지 않는 개발 철학입니다.</p>
  </div>

  <div class="stitch-section-title">기술 역량 (Skills)</div>
  <div class="stitch-skills">
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">주력 분야</div>
      <div class="stitch-skill-value">Flutter, Android, iOS</div>
    </div>
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">언어</div>
      <div class="stitch-skill-value">Dart, Kotlin, Swift, Java</div>
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
        <li><strong>레거시 전면 클린아키텍처 재설계:</strong> 유지보수가 불가했던 거대 레거시를 9개 패키지의 멀티모듈 모노레포로 분리하여, 신규 기능 개발 시의 사이드 이펙트를 완벽히 차단</li>
        <li><strong>의존성 방향 강제 (Riverpod):</strong> 팀원들의 의도치 않은 의존성 주입을 방지하기 위해 패키지 레벨에서 아키텍처 규칙을 강제하여, 코드 리뷰 비용 절감 및 오류 발생률 최소화</li>
        <li><strong>높은 재사용성과 유연성:</strong> 분리된 코어 로직을 기반으로 두 번째 앱(플레이플래닛 AI) 론칭 시 개발 기간을 절반 이하로 단축</li>
        <li>소셜로그인 일반화 (Apple, Google, Kakao, Naver) 및 JWT 토큰 자동 갱신 아키텍처 구축</li>
        <li><strong>AI 도입 및 조직 문화 주도:</strong> 개발팀 맞춤형 AI 스킬(Harness), 룰, 에이전트를 직접 설계 및 배포하여 팀 생산성을 극대화하고, 사내 AI 계정 관리 및 전사적 활용 세미나를 주도</li>
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
        <li><strong>모바일 GPT Client (Flutter):</strong> 신규 사내 앱을 바닥부터 설계하며, Flutter의 조합(Composition) 철학을 극대화한 예측 가능한 UI 컴포넌트 시스템 구축 (오버엔지니어링을 배제하고 목표에 가장 적합한 클린 아키텍처 적용)</li>
        <li><strong>Contiple (Flutter 상담 솔루션):</strong> 프로젝트 초기 클린 아키텍처 기반 구조 설계 주도, Riverpod을 활용한 안정적인 페이징 구조 및 생체인증/딥링크 구현</li>
        <li><strong>공통 웹뷰 통신 구조 일반화:</strong> JS Interface 연동 시 발생하는 반복적인 코드 작성과 하드코딩을 제거하고 단일화된 구조로 개선하여 웹뷰 연동 버그 90% 차단</li>
        <li><strong>티켓링크 iOS:</strong> 예외 상황 처리가 부족했던 기존 오프라인 티켓 및 자동 로그인 프로세스 전면 리팩토링</li>
        <li><strong>운수도원 (Android/iOS):</strong> 구글 애드몹 전면 광고 적용 및 Jenkins CI/CD 자동화 파이프라인 구축</li>
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
        <li><strong>검색 조건 및 페이징 일반화:</strong> 각 페이지에서 파편화되어 처리되던 검색 로직을 걷어내고, 의존성이 분리된 단일 페이징 구조로 리팩토링하여 유지보수성 극대화</li>
        <li>복잡하게 꼬여있던 안드로이드 상태 관련 레거시 코드 전면 개선</li>
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
        <li>자체 Push 서버 개발 (Java Spring) 및 모바일 네이티브(Android/iOS) Push SDK 구축</li>
        <li><strong>미스리 메신저 및 주식인 앱 (Android/iOS):</strong> OAuth 연동, 주식 실시간 소켓 통신 앱 개발을 통해, 대용량 실시간 데이터를 병목 없이 처리하는 기반 설계 역량 확보</li>
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
      <div class="stitch-story-desc">AI가 범용적인 규칙은 알아서 고도화할 것을 믿고, 개발자는 도메인 지식에 집중해야 한다는 '하네스(Harness)' 전략을 회고합니다.</div>
    </div>
    
    <div class="stitch-story-item">
      <div class="stitch-story-title">💡 최신 테크 동향</div>
      <div class="stitch-story-desc">쏟아지는 최신 AI 및 IT 업계의 핵심 뉴스들을 꾸준히 정리하고 공유합니다.</div>
    </div>

  </div>

</div>
