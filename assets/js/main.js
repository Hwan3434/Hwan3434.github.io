document.addEventListener('DOMContentLoaded', () => {
  // Theme Toggle
  const themeBtn = document.getElementById('btn-theme-toggle');
  const iconSun = document.querySelector('.icon-sun');
  const iconMoon = document.querySelector('.icon-moon');
  
  function updateThemeIcons() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    if (isDark) {
      iconSun.style.display = 'block';
      iconMoon.style.display = 'none';
    } else {
      iconSun.style.display = 'none';
      iconMoon.style.display = 'block';
    }
  }

  if (themeBtn) {
    updateThemeIcons();
    themeBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      updateThemeIcons();
    });
  }

  // TOC Generation
  window.initTOC = function() {
    const prose = document.getElementById('prose');
    const tocList = document.getElementById('toc-list');
    if (!prose || !tocList) return;
    
    tocList.innerHTML = '';
    
    if (window.tocObserver) {
      window.tocObserver.disconnect();
    }

    const headings = prose.querySelectorAll('h2, h3');
    headings.forEach((heading, idx) => {
      if (!heading.id) {
        heading.id = 'heading-' + idx;
      }
      const isSub = heading.tagName.toLowerCase() === 'h3';
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '#' + heading.id;
      a.textContent = heading.textContent;
      if (isSub) a.className = 'sub';
      li.appendChild(a);
      tocList.appendChild(li);
    });

    // TOC Observer
    const tocLinks = tocList.querySelectorAll('a');
    if (tocLinks.length > 0 && typeof IntersectionObserver !== 'undefined') {
      window.tocObserver = new IntersectionObserver((entries) => {
        const visible = entries.filter(e => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        
        if (visible[0]) {
          tocLinks.forEach(link => link.classList.remove('active'));
          const activeLink = tocList.querySelector(`a[href="#${visible[0].target.id}"]`);
          if (activeLink) activeLink.classList.add('active');
        }
      }, { rootMargin: "-90px 0px -65% 0px", threshold: 0 });
      
      headings.forEach(h => window.tocObserver.observe(h));
    }
  };

  window.initTOC();

  // Search Logic
  const searchBtn = document.getElementById('btn-search-open');
  const searchScrim = document.getElementById('search-scrim');
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  let searchData = [];
  let searchIndex = -1;
  let currentResults = [];

  function openSearch() {
    searchScrim.classList.add('open');
    searchInput.value = '';
    searchResults.innerHTML = '';
    searchIndex = -1;
    setTimeout(() => searchInput.focus(), 60);
    
    if (searchData.length === 0) {
      fetch('/search.json').then(r => r.json()).then(data => {
        searchData = data;
      });
    }
  }

  function closeSearch() {
    searchScrim.classList.remove('open');
  }

  if (searchBtn && searchScrim) {
    searchBtn.addEventListener('click', openSearch);
    searchScrim.addEventListener('mousedown', (e) => {
      if (e.target === searchScrim) closeSearch();
    });
    
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (!q) {
        searchResults.innerHTML = '';
        currentResults = [];
        return;
      }
      currentResults = searchData.filter(item => 
        item.title.toLowerCase().includes(q) || 
        item.content.toLowerCase().includes(q) ||
        item.tags.toLowerCase().includes(q) ||
        item.categories.toLowerCase().includes(q)
      );
      
      searchIndex = -1;
      renderSearchResults();
    });

    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeSearch();
      else if (e.key === 'ArrowDown') {
        e.preventDefault();
        searchIndex = Math.min(searchIndex + 1, currentResults.length - 1);
        highlightResult();
      }
      else if (e.key === 'ArrowUp') {
        e.preventDefault();
        searchIndex = Math.max(searchIndex - 1, 0);
        highlightResult();
      }
      else if (e.key === 'Enter' && currentResults[searchIndex]) {
        window.location.href = currentResults[searchIndex].url;
      }
    });

    function renderSearchResults() {
      if (currentResults.length === 0) {
        searchResults.innerHTML = '<div class="search-empty">결과가 없습니다.</div>';
        return;
      }
      searchResults.innerHTML = currentResults.map((item, i) => `
        <a href="${item.url}" class="search-result ${i === searchIndex ? 'cur' : ''}" data-index="${i}">
          <div class="sr-title">${item.title}</div>
          <div class="sr-meta">${item.categories} — ${item.date}</div>
        </a>
      `).join('');
      
      searchResults.querySelectorAll('.search-result').forEach(el => {
        el.addEventListener('mouseenter', () => {
          searchIndex = parseInt(el.getAttribute('data-index'));
          highlightResult();
        });
      });
    }

    function highlightResult() {
      searchResults.querySelectorAll('.search-result').forEach((el, i) => {
        if (i === searchIndex) el.classList.add('cur');
        else el.classList.remove('cur');
      });
    }
  }

  // Pre-filter tag on load if in URL (e.g., /?tag=Flutter)
  const urlParams = new URLSearchParams(window.location.search);
  const preTag = urlParams.get('tag');
  if (preTag && typeof window.filterTag === 'function') {
    const btn = document.querySelector(`.filterbar button[data-tag="${preTag}"]`);
    if (btn) {
      window.filterTag(preTag, btn);
    }
  }
});
