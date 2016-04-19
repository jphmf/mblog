#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Post(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        self.render("front.html")


class CreatePostHandler(Handler):
    def render_form(self, title="", content="", error=""):
        posts = db.GqlQuery("Select * from Post")
        self.render("form.html", title=title, content=content, error=error,
                    posts=posts)

    def get(self):
        self.render_form()

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        if title and content:
            post = Post(title=title, content=content)
            post.put()
            self.redirect("/createPost")
        else:
            error = "We need both a title and some artwork"
            self.render_form(title, content, error)
app = webapp2.WSGIApplication([('/', MainPage),
                              ('/createPost', CreatePostHandler)], debug=True)
