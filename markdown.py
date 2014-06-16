#!/usr/bin/env python3

import sys, os

from gi.repository import Gtk, Gio, WebKit

import argparse
import markdown2
from string import Template

APP_MENU = """<interface>
  <menu id="appmenu">
    <section>
      <item>
        <attribute name="label" translatable="yes">_About</attribute>
        <attribute name="action">app.about</attribute>
      </item>
      <item>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="action">app.quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
      </item>
    </section>
  </menu>
</interface>"""

TEMPLATE = Template("""<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>DragnucsMD</title>
        <style>
            body {
				background-color: #002b36;
				color: #839496;
				font-family: "Droid sans", Droid, sans;
			}

			h1, h2, h3, h4, h5n h6 {
				color: #b58900;
				border-bottom: 1px solid #073642;
				font-family: Inconsolata, "Source pro";
			}

			a {
				text-decoration: underline;
				color: whitesmoke;
			}

			p {
				indent: 10px;
			}

			pre {
				border-radius: 3px;
				border: 1px solid #586e75;
				background-color: #073642;
				padding: 4px;
			}

			blockquote {
				font-family: "Droid serif", "Liberation serif", serif;
				background-color: #073642;
				padding: 1px 20px;
			}

			hr {
				border: none;
				border-bottom: 1px solid #2aa198;
			}

			table {
				width: 100%;
			}

			tr:nth-child(2n+1) {
				background-color: #002b36;
			}

			tr:nth-child(2n) {
				background-color: #073642;
			}

			tr:first-child {
				color: #b58900;
				font-weight: bold;
				text-transform: capitalize;
			}
        </style>
    </head>
    <body>
        $body
    </body>
</html>""")

class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="DragnucsMD", application=app)
        self.args = app.args

        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_icon_name("text-x-generic")

        # HeaderBar
        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = "DragnucsMD"
        self.set_titlebar(hb)

        # The webkit widget to view the document
        scrolled_view = Gtk.ScrolledWindow()
        scrolled_view.set_hexpand(True)
        scrolled_view.set_vexpand(True)
        self.view = WebKit.WebView()
        scrolled_view.add(self.view)
        self.add(scrolled_view)
        self.load("")

        if(self.args.file):
            file = open(self.args.file)
            content = file.read()
            self.load(content)
            file.close()
            hb.props.title=self.args.file
            hb.props.subtitle=os.path.abspath(self.args.file)

    def load(self, content):
        extras_list = ["code-friendly",
                       "cuddled-lists",
                       "fenced-code-blocks",
                       "footnotes",
                       "header-ids",
                       "metadata",
                       "pyshell",
                       "smarty-pants",
                       "wiki-tables",
                       "xml",
                       "tag-friendly"]
        html = TEMPLATE.safe_substitute(body=markdown2.markdown(content,
                                                            extras=extras_list))
        self.view.load_html_string(html, "file:///")


class DragnucsMD(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                                application_id="com.dragnucs.dragnucsmd")

    def do_activate(self):
        win = MainWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction(name="about")
        action.connect("activate", self.about_activated)
        self.add_action(action)

        action = Gio.SimpleAction(name="quit")
        action.connect("activate", lambda a,b: self.quit())
        self.add_action(action)

        builder = Gtk.Builder()
        builder.add_from_string(APP_MENU)
        self.set_app_menu(builder.get_object("appmenu"))

    def do_command_line(self, args):
        Gtk.Application.do_command_line(self, args)
        parser = argparse.ArgumentParser(prog='dragnucsmd',
                                         description='Render markdown files')
        parser.add_argument('-f', '--file', required=False)
        self.args = parser.parse_args(args.get_arguments()[1:])
        self.do_activate()

    def about_activated(self, action, data=None):
        dialog = Gtk.AboutDialog(program_name="DragnucsMD",
                   title="About DragnucsMD",
                   version="0.1",
                   license_type=Gtk.License.GPL_3_0,
                   icon_name=None,
                   comments="A little tool to preview Markdown documents",
                   authors=["Mohamed-Touhami MAHDI <dragnucs@gmail.com>"],
                   website="http://dragnucsmd.dragnucs.com/",
                   website_label="DragnucsMD homepage",
                   copyright="Copyright \xc2\xa9 2014 Mohamed-Touhami MAHDI")
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    app = DragnucsMD()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
