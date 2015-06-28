convenient tool
    print.red.bgblue

    check and set color
         [ ] add argument `--show-names`

    stream color

deploy
    information
        document (include PyDoc)
            [ ] add docstring to `AttributeMapping` so that `colormap` has docinfo
            [ ] :mod:`__init__`
            [✓] :mod:`color_mapping`
            [ ] :mod:`methods`
            [ ] :mod:`command`

        command help
            [ ] write help info to CLI tool

        `README.rst` FAQ
            [ ] :cmd:`echo ccc--ooo-----tt | python3.4 -m colorprint  -P "(--)" reverse`

    Python2 support
        [ ] python2 support with setuptools

    generate some information from `README.rst`
        [ ] `author`, `version`
        [ ] :mod:`colorprint.__init__`
        [ ] :mod:`colorprint.methods`

    unittest / doctest (use `py.text` or `nosetest`)
        [ ] :mod:`methods`
        [ ] :mod:`color_mapping`
        [ ] :mod:`commad`

    exception
        [ ] review error handler; 自訂顏色的檢查足夠嗎?
        [ ] use "During handling of the above exception, another exception occurred" or not??
            consider :mod:`methods` line 48

    naming and architecture
        [✓] `commands.run_cmd` → `command.run`
        [✓] `attributes.color_attr_mapping` → `color_mapping.colormap`
        [ ] refactor
