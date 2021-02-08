config=_config.yml
default:: localbuild

install:
	yes|sudo apt-get install ruby-full
	yes|sudo apt install ruby-bundler
	yes|sudo gem install bundler
	bundle install

localbuild:
	bundle exec jekyll serve -w

encode: $(config)
	@echo Creating the base64 encoded file
	@-rm $(config).base64
	@base64 $(config) > $(config).base64
	@sed -e :a -e '$!N;s/\n//;ta' $(config).base64 > $(config).base64.tmp
	@mv $(config).base64.tmp $(config).base64
