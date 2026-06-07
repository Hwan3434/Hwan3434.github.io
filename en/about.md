---
layout: page
title: About
heading: "Predictable Code<br>Controllable <span style='color: var(--primary);'>Architecture</span>."
lede: "Code must be readable even as team members change, and errors must be prevented by structure. I am Jeonghwan Lee, a 10-year mobile architect who strictly guards against the technical debt left by short-term compromises."
permalink: /en/about/
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
    font-family: var(--font-display);
    font-weight: 400;
    font-size: 28px;
    letter-spacing: -0.5px;
    color: var(--ink);
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
    font-family: var(--font-body);
    font-size: 19px;
    font-weight: 600;
    color: var(--ink);
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
    font-family: var(--font-body);
    font-size: 19px;
    font-weight: 600;
    color: var(--ink);
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
      <strong>Notice:</strong> All posts, page designs, and code authoring for this blog were comprehensively planned, developed, and written in collaboration with an <strong>AI Agent</strong>.
    </div>
  </div>

  <div class="stitch-intro">
    <p>Throughout my 10 years spanning Backend, Android, iOS, and currently Flutter development, I have established one firm principle across numerous projects: <strong>If you compromise principles just to be satisfied with 'something that works right now', you will eventually pay a massive reinvestment cost later.</strong></p>
    <p>That is why I obsess over <strong>predictable code</strong>. Software is ultimately built by people, and code is read overwhelmingly more times than it is written. Rather than taking temporary shortcuts under the excuse of immediate deadlines, I aim for code where the intent is clearly read by anyone, by designing the flow to meet its fundamental purpose from the beginning.</p>
    <p>Moreover, I consider building a <strong>controllable architecture</strong> to be paramount. Human attention can waver at any time, so mistakes must be prevented in advance by systems and structures, not individual caution. I strictly guard against unreasonable over-engineering that strays from immediate goals, while establishing a 'solid yet flexible foundation' where the structure blocks incorrect approaches and guides toward the right direction.</p>
  </div>

  <div class="stitch-section-title">Skills</div>
  <div class="stitch-skills">
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">Main Domains</div>
      <div class="stitch-skill-value">Flutter, Android, iOS</div>
    </div>
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">Languages</div>
      <div class="stitch-skill-value">Dart, Kotlin, Swift, Java</div>
    </div>
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">Architecture</div>
      <div class="stitch-skill-value">Clean Arch, MVVM</div>
    </div>
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">State Management</div>
      <div class="stitch-skill-value">Riverpod, Provider</div>
    </div>
    <div class="stitch-skill-card">
      <div class="stitch-skill-label">Tools & Infra</div>
      <div class="stitch-skill-value">Git, CI/CD, Firebase</div>
    </div>
  </div>

  <div class="stitch-section-title">Experience</div>
  <div class="stitch-timeline">
    
    <div class="stitch-timeline-item">
      <div class="stitch-timeline-dot"></div>
      <div class="stitch-timeline-header">
        <div class="stitch-company">BankX Inc.</div>
        <div class="stitch-period">2025.09 - Present</div>
      </div>
      <div class="stitch-role">PlayPlanet & PlayPlanet AI (Flutter)</div>
      <ul class="stitch-tasks">
        <li><strong>Complete Legacy Clean Architecture Redesign:</strong> Separated massive legacy code reaching maintenance limits into a 9-package multi-module monorepo to minimize code coupling.</li>
        <li><strong>Enforcing Dependency Direction (Riverpod):</strong> Designed architecture rules to be enforced at the package level to prevent unintended dependency injection by team members.</li>
        <li><strong>High Reusability & Flexibility:</strong> Achieved fast development speed and high code reusability by applying the separated core logic identically to the new app (PlayPlanet AI).</li>
        <li>Generalized social login (Apple, Google, Kakao, Naver) and built automated JWT token renewal architecture.</li>
        <li><strong>Leading AI Adoption & Organizational Culture:</strong> Conducted internal seminars on AI account management and usage, and directly designed and deployed AI skills (Harness), rules, and agents tailored for the development team.</li>
      </ul>
    </div>

    <div class="stitch-timeline-item">
      <div class="stitch-timeline-dot"></div>
      <div class="stitch-timeline-header">
        <div class="stitch-company">NHN Injeinc</div>
        <div class="stitch-period">2023.03 - 2025.07</div>
      </div>
      <div class="stitch-role">Mobile Development Part</div>
      <ul class="stitch-tasks">
        <li><strong>Mobile GPT Client (Flutter):</strong> Designed internal Chat GPT app from scratch, applying the most suitable Clean Architecture and MVVM pattern for the goals.</li>
        <li><strong>Contiple (Flutter Consulting Solution):</strong> Designed initial project Clean Architecture structure, Riverpod pagination, biometric authentication, and deep links.</li>
        <li><strong>Generalizing Common WebView Communication:</strong> Generalized JavaScript-based object data transmission/reception to eliminate boilerplate code during WebView integration.</li>
        <li><strong>Ticketlink iOS:</strong> Refactored and improved existing offline ticket inquiry and auto-login processes.</li>
        <li><strong>Unsudowon (Android/iOS):</strong> Applied Google AdMob interstitial ads and configured Jenkins CI/CD.</li>
      </ul>
    </div>

    <div class="stitch-timeline-item">
      <div class="stitch-timeline-dot"></div>
      <div class="stitch-timeline-header">
        <div class="stitch-company">Paymint Inc.</div>
        <div class="stitch-period">2022.12 - 2023.03</div>
      </div>
      <div class="stitch-role">Gyeolje-Seonsaeng App Refactoring (Android)</div>
      <ul class="stitch-tasks">
        <li><strong>Generalizing Search Conditions & Paging:</strong> Separated dependencies and proceeded with refactoring by generalizing paging and search conditions during search.</li>
        <li>Improved complex, tangled Android state-related legacy code.</li>
      </ul>
    </div>

    <div class="stitch-timeline-item">
      <div class="stitch-timeline-dot"></div>
      <div class="stitch-timeline-header">
        <div class="stitch-company">Miso & Cloud</div>
        <div class="stitch-period">2015.10 - 2022.09</div>
      </div>
      <div class="stitch-role">Mobile & Backend Development</div>
      <ul class="stitch-tasks">
        <li>Developed proprietary Push server (Java Spring) and mobile native (Android/iOS) Push SDK.</li>
        <li><strong>Real-time Stock Trading Program (Windows):</strong> Integrated real-time stock data and implemented buy/sell and trigger (automated) trading systems.</li>
        <li><strong>Misslee Messenger (Android/iOS):</strong> Developed mobile messenger app based on OAuth integration and socket communication.</li>
        <li><strong>Jusikin (Android/iOS):</strong> Developed a mobile app for sharing stock information utilizing REST APIs.</li>
      </ul>
    </div>

  </div>

  <div class="stitch-section-title">Stories in this Blog</div>
  <div class="stitch-story-box">
    
    <div class="stitch-story-item">
      <div class="stitch-story-title">📱 Flutter & Mobile Architecture</div>
      <div class="stitch-story-desc">Recording structural contemplations and practical troubleshooting that do not go against the framework's philosophy.</div>
    </div>
    
    <div class="stitch-story-item">
      <div class="stitch-story-title">🤖 AI Agents & Productivity</div>
      <div class="stitch-story-desc">Reflecting on the 'Harness' strategy: believing AI will independently refine general rules, allowing developers to focus on domain knowledge.</div>
    </div>
    
    <div class="stitch-story-item">
      <div class="stitch-story-title">💡 Latest Tech Trends</div>
      <div class="stitch-story-desc">Consistently organizing and sharing key news from the rapidly pouring AI and IT industries.</div>
    </div>

  </div>

</div>
