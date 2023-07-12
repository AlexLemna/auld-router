
## Overall structure

*See: [Command Line Interface Guidelines](https://clig.dev)*

#### Help text

Display help text when passed no options, passed the `-h` flag, or passed the `--help` flag. 

By default (i.e.: when passed no options), display a concise help text containing a short description of the program and a note that the `-h` or `--help` flags will display more information. 

```
# SHORT HELP TEXT
$ auld-router
<...program name, purpose, how to get additional help...>
```

When passed the `-h` or `--help` flags, display a full help text.

```
# FULL HELP TEXT
$ auld-router --help
$ auld-router -h
<..program usage...>

<...program description...>

<list of all valid next arguments>
    <command 1>     <...command description...>
    <command 2>     <...command description...>
    <command 3>     <...command description...>
    <command 4>     <...command description...>
    <command 5>     <...command description...>
    <...>           <...>

<...program epilogue...>
```


## Commands

```
config commit
config confirm
config save
config show


commit configuration

confirm configuration

disable configuration
disable service <service>

enable configuration
enable service <service>

reboot

save configuration
save "<command>" --output-file <output file>

set <config_key> = <config_value>

show configuration
show dns
show interfaces
show nat
show nat translations
show networks
show ntp
show router services
show router version
show routes
show version

shutdown
```
