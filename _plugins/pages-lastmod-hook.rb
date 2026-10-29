# frozen_string_literal: true
#
# 사이트맵 <lastmod> 를 페이지에도 단다.
# 목록 페이지(front matter `list:`)는 그 목록에 나오는 최신 글 날짜, 나머지는 파일의 마지막 커밋 날짜.
# 목록 규칙은 _layouts/home.html, news.html, philosophy.html 과 같다.

Jekyll::Hooks.register :site, :pre_render do |site|
  site.pages.each do |page|
    next unless page.html?

    list = page.data["list"]
    if list
      lang = page.data["lang"] || "ko"
      posts = site.posts.docs.select { |post| (post.data["lang"] || "ko") == lang }
      posts = if list == "home"
                posts.reject { |post| (post.data["categories"] & %w(news philosophy)).any? }
              else
                posts.select { |post| post.data["categories"].include?(list) }
              end
      page.data["last_modified_at"] = posts.map(&:date).max
    else
      lastmod_date = `git log -1 --pretty="%ad" --date=iso -- "#{page.path}"`.strip
      page.data["last_modified_at"] = lastmod_date unless lastmod_date.empty?
    end
  end
end
