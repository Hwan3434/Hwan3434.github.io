# frozen_string_literal: true
#
# jekyll-seo-tag 템플릿에서 JSON-LD 블록만 뺀다.
# 구조화 데이터는 _includes/schema.html 이 Person 까지 묶은 @graph 하나로 낸다.

require "jekyll-seo-tag"

module Jekyll
  class SeoTag
    class << self
      private

      def template_contents
        @template_contents ||= File.read(template_path)
          .sub(%r!<script type="application/ld\+json">.*?</script>\s*!m, "")
          .gsub(MINIFY_REGEX, "")
      end
    end
  end
end
