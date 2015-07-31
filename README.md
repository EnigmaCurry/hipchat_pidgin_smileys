Hipchat Emoticon Theme Builder for Pidgin
-----------------------------------------

This is a tool that will download all the emoticons associated with
your hipchat account, both the standard set provided by hipchat, as
well as the ones your organization has customized. It will create a
theme in your pidgin directory (~/.purple/smileys/hipchat)

First time users, run this:

    hipchat_pidgin_smilies.py --setup

This will create a config file and it will ask you for your
Organization name within hipchat, your email address to login with,
and your password. The config file is stored in the theme directory
and is only readable by your account (and root, of course.)

Once setup, just run without any arguments. The images will be
downloaded and the theme file created. Inside Pidgin, make sure to
select the Hipchat theme in Tools -> Preferences -> Themes -> Smiley Theme

License
=======

Standard MIT License:

    Copyright (c) 2015 Ryan McGuire

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
