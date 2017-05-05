# Apex Smart Snippets
#### A Sublime Text 3 plugin to speed up your Salesforce coding.

## Description
Snippets and commands to speed up you Salesfroce development

#### ATTENTION! This plugin is currently under development and unstable.

## Requirements
1. Sublime Text 3
2. [MavensMate](http://mavensmate.com/ "MavensMate") is highly recommended. But I guess you already have it.

Since MavensMate requires ST 3, there will be no ST 2 support.

## Installation
### Manual

1. Download [a release](https://github.com/nchursin/ApexSmartSnippets/releases "Releases page") to your Sublime Text Packages folder. To find it go to `Preferences -> Browse Packages` (`Sublime Text -> Preferences -> Browse Packages` on Mac).
2. Restart Sublime if needed.

## How to use it

### "Smart" snippets exmaple
1. Find a line defining class property. E.g.
```public Boolean boolProperty;```
2. Press `Ctrl+M` (`⌘+M` on Mac) or use command `Apex Smart: Show available actions`.
3. Choose action, press `Enter`

### Regular snippets
Just start typing something. If there is a snippet - autocomplete will show it to you. Full list of snippets is yet to come.

#### Working actions:

1. Add getter
2. Add setter
3. Add both getter and setter
4. Add class constrctor

## License

MIT