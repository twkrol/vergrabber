# vergrabber
Vergrabber is the tool written to grab & publish version information of selected software packages.
It produces the json file that can be further processed programmaticaly (eg. by automation tools).

It includes only supported and stable editions - not necessarily the latest or experimental versions.

It is always available at the following link: http://vergrabber.kingu.pl/vergrabber.json

# Example output
JSON formatted file

```json
{
"client": {
	"Google Chrome": {
		"57.0": {
		"latest": true,
		"product": "Google Chrome",
		"stable": true,
		"version": "57.0.2987.110",
		"released": "2017-03-16",
		"edition": "57.0"
		}
	},
	"Mozilla Firefox": {...}
},
"server": {
	"Apache2": {
		"2.4": {
		"latest": true,
		"product": "Apache2",
		"stable": true,
		"version": "2.4.25",
		"released": "2016-12-20",
		"edition": "2.4"
		},
		"2.2": {
		"latest": false,
		"product": "Apache2",
		"stable": true,
		"version": "2.2.32",
		"released": "2017-01-13",
		"edition": "2.2"
		}
	},
	"PHP": {...},
	"MySQL": {...},
	"Linux Kernel": {...},
	"Nginx": {...},
	"OpenSSL": {...}
}
}
```

# Current modules

Every software product needs a custom python module to be included in vergrabber processing.

## Server modules

    Apache2
    Linux kernel
    MySQL Community Server
    Nginx
    OpenSSL
    PHP
    Symfony (PHP framework)

## Client modules

    Adobe Flash
    Google Chrome
    Microsoft Windows 10
    Mozilla Firefox
    Mozilla Thunderbird
    OpenVPN
    Oracle Java
    TeamViewer
    VeraCrypt

Contact me if you want to help creating modules for other software products. 


# FAQ
## How it works?
Vergrabber runs every midnight (GMT+1) to grab and process current version of software packages defined in modules. Then it compiles results to one, simple json file. It is intended to use with automated systems, that's why it generates json content that can be programmaticaly processed.

## What it can be used for?
I use it daily with my other systems to verify and report how actual the software on servers and workstations is at the organization I work for as CISO. You may use it for similar task, or whatever you like until it's not used for illegal activities.

## What is the source of version information??
All software information is scrapped from the websites of their software vendors or publishers. Not all of them (well, most of them not) provide machine understandable format like json or xml, so the vergrabber need to pick information by scrapping and parsing html content. For this reason, the modules need to be updated from time to time to respect new layout or design changes.

## Is the vergrabber service free?
Yes, it's free for your personal or corporate use. Just be nice and don't overload the server - a single daily request is fine. I do appreciate any donations if you find this service useful, and you want to support it's further development.
