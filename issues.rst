convenient tool
    print.red.bgblue

    check and set color
        - [ ] add argument `--show-names`

    stream color

deploy
    testing
        unittest
            - [ ] add testing for CLI tool by inject input data (including command) and assert the output string

        doctest

    information 
        document

        command help
            - [ ] write help info to CLI tool

        pydoc
            - [ ] add docstring to `AttributeMapping` so that `colormap` has docinfo

        FAQ
            - [ ] ``echo ccc--ooo-----tt | python3.4 -m colorprint  -P "(--)" reverse``

    support
        no Win

        py2
            - [ ] python2 support with setuptools

        py3

        edit information only at one place

        unittest / doctest

        exception
            - [ ] review error handler; 自訂顏色的檢查足夠嗎?
            - [ ] use "During handling of the above exception, another exception occurred" or not??
                  consider `methods.py` line 48

        naming and architecture
            - [ ] use `from colorprint.attributes import colormap`
            - [ ] `color_attr_mapping` -> `colormap`
            - [ ] redesign
