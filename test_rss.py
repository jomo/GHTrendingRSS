#!/usr/bin/python
import rss
import github

print rss.get_rss('c', 'C', 'weekly', github.get_projects('csharp', 'weekly'))
