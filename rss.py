#!/usr/bin/python
import os
import jinja2


def get_rss(language, timespan, projects):
	JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

	values = {"language": language, "timespan": timespan, "projects": projects}
	return JINJA_ENVIRONMENT.get_template("rss.xml").render(values)

