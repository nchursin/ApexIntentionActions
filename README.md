# Apex Intention Actions
#### A Sublime Text 3 plugin to speed up your Salesforce coding.

## Description
Snippets and commands to speed up you Salesfroce development

## Requirements
1. Sublime Text 3
2. [MavensMate](http://mavensmate.com/ "MavensMate") is highly recommended. But I guess you already have it.

Since MavensMate requires ST 3, there will be no ST 2 support.

## Installation
### Manual

1. Download [a release](https://github.com/nchursin/ApexIntentionActions/releases "Releases page"). Rename it to `Apex Intention Actions.sublime-package`
2. Copy the Sublime package file to your Sublime Text Packages folder. To find it use `Package Control -> List Packages` on any of the installed package.
3. Restart Sublime if needed.

## How to use it

### Intention Action
1. Find a line defining class property. E.g.
```public Boolean boolProperty;```
2. Press `Alt+Space` or use command `Apex Intention Actions: Show available actions`.
3. Choose action, press `Enter`

A little demo:

![Getter-setter demo](https://github.com/nchursin/resources/blob/master/ApexIntentionActions/getter-setter.gif?raw=true)

### Regular snippets
Just start typing something. If there is a snippet - autocomplete will show it to you. Full list of snippets is available [here](https://github.com/nchursin/ApexIntentionActions/wiki/Snippets "Snippets").

#### Working intention actions:

1. Add getter
2. Add setter
3. Add both getter and setter
4. Add constructor parameter
5. Add class constructor
6. Add init method and call in each constructor
7. Add 0-arg constructor and init method
8. Add method overload

All actions have short cut. `Ctrl+M` (`⌘+M` on Mac), then use following shortcuts:
1. `G` - Add getter
2. `S` - Add setter
3. `Ctrl+G(⌘+G)` or `Ctrl+S(⌘+S)` - Add both getter and setter
4. `Ctrl+P(⌘+P)` - Add constructor parameter
5. `C` - Add class constructor
6. `I` - Add init method and call in each constructor
7. `Ctrl+C(⌘+C)` or `Ctrl+I(⌘+I)` - Add 0-arg constructor and init method
8. `Ctrl+O(⌘+O)` - Add method overload

## Customizations
Action menu has two styles: quick panel and pop-up menu.
To switch between them use preferences command for the plugin and change the `intention_menu_mode` settings. Two options available: `quickpanel` and `popup`.

## License

Apache 2.0