SPHINXBUILD   = sphinx-build
BUILDDIR      = _build
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees .

.PHONY: help clean html text man

help:
	@echo "  html       to make standalone HTML files"
	@echo "  text       to make text files"
	@echo "  man        to make manual pages"
	@echo "  info       to make Texinfo files and run them through makeinfo"

clean:
	-rm -rf $(BUILDDIR)
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
text:
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
	mv $(BUILDDIR)/man/pycommand.3 ..

info:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	make -C $(BUILDDIR)/texinfo info
	mv $(BUILDDIR)/texinfo/pycommand.info ..
