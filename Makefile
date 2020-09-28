default:: localbuild
# Helpful Liquid: https://shopify.github.io/liquid/filters/replace/

install:
	bundle install

localbuild:
	bundle exec jekyll serve -w
