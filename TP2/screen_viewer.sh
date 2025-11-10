#!/bin/bash
page=$1
if [ -n "$page" ]; then
    mkdir $page
    grep screenshot $page.json | awk '{print $2}' | sed 's/\"//g' | sed 's/,//' | base64 -d > $page/screenshot.png
fi